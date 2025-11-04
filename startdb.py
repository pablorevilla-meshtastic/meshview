import asyncio
import datetime
import json
import logging

from sqlalchemy import delete

from meshview import migrations, models, mqtt_database, mqtt_reader, mqtt_store
from meshview.config import CONFIG

# -------------------------
# Logging for cleanup
# -------------------------
cleanup_logger = logging.getLogger("dbcleanup")
cleanup_logger.setLevel(logging.INFO)
cleanup_logfile = CONFIG.get("logging", {}).get("db_cleanup_logfile", "dbcleanup.log")
file_handler = logging.FileHandler(cleanup_logfile)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
cleanup_logger.addHandler(file_handler)


# -------------------------
# Helper functions
# -------------------------
def get_bool(config, section, key, default=False):
    return str(config.get(section, {}).get(key, default)).lower() in ("1", "true", "yes", "on")


def get_int(config, section, key, default=0):
    try:
        return int(config.get(section, {}).get(key, default))
    except ValueError:
        return default


# -------------------------
# Shared DB lock
# -------------------------
db_lock = asyncio.Lock()


# -------------------------
# Database cleanup using ORM
# -------------------------
async def daily_cleanup_at(
    hour: int = 2, minute: int = 0, days_to_keep: int = 14, vacuum_db: bool = True
):
    while True:
        now = datetime.datetime.now()
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_run <= now:
            next_run += datetime.timedelta(days=1)
        delay = (next_run - now).total_seconds()
        cleanup_logger.info(f"Next cleanup scheduled at {next_run}")
        await asyncio.sleep(delay)

        # Local-time cutoff as string for SQLite DATETIME comparison
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days_to_keep)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        cleanup_logger.info(f"Running cleanup for records older than {cutoff}...")

        try:
            async with db_lock:  # Pause ingestion
                cleanup_logger.info("Ingestion paused for cleanup.")

                async with mqtt_database.async_session() as session:
                    # -------------------------
                    # Packet
                    # -------------------------
                    result = await session.execute(
                        delete(models.Packet).where(models.Packet.import_time < cutoff)
                    )
                    cleanup_logger.info(f"Deleted {result.rowcount} rows from Packet")

                    # -------------------------
                    # PacketSeen
                    # -------------------------
                    result = await session.execute(
                        delete(models.PacketSeen).where(models.PacketSeen.import_time < cutoff)
                    )
                    cleanup_logger.info(f"Deleted {result.rowcount} rows from PacketSeen")

                    # -------------------------
                    # Traceroute
                    # -------------------------
                    result = await session.execute(
                        delete(models.Traceroute).where(models.Traceroute.import_time < cutoff)
                    )
                    cleanup_logger.info(f"Deleted {result.rowcount} rows from Traceroute")

                    # -------------------------
                    # Node
                    # -------------------------
                    result = await session.execute(
                        delete(models.Node).where(models.Node.last_update < cutoff)
                    )
                    cleanup_logger.info(f"Deleted {result.rowcount} rows from Node")

                    await session.commit()

                if vacuum_db:
                    cleanup_logger.info("Running VACUUM...")
                    async with mqtt_database.engine.begin() as conn:
                        await conn.exec_driver_sql("VACUUM;")
                    cleanup_logger.info("VACUUM completed.")

                cleanup_logger.info("Cleanup completed successfully.")
                cleanup_logger.info("Ingestion resumed after cleanup.")

        except Exception as e:
            cleanup_logger.error(f"Error during cleanup: {e}")


# -------------------------
# MQTT loading
# -------------------------
async def load_database_from_mqtt(
    mqtt_server: str,
    mqtt_port: int,
    topics: list,
    mqtt_user: str | None = None,
    mqtt_passwd: str | None = None,
):
    async for topic, env in mqtt_reader.get_topic_envelopes(
        mqtt_server, mqtt_port, topics, mqtt_user, mqtt_passwd
    ):
        async with db_lock:  # Block if cleanup is running
            await mqtt_store.process_envelope(topic, env)


# -------------------------
# Main function
# -------------------------
async def main():
    logger = logging.getLogger(__name__)

    # Initialize database
    database_url = CONFIG["database"]["connection_string"]
    mqtt_database.init_database(database_url)

    # Create migration status table
    await migrations.create_migration_status_table(mqtt_database.engine)

    # Set migration in progress flag
    await migrations.set_migration_in_progress(mqtt_database.engine, True)
    logger.info("Migration status set to 'in progress'")

    try:
        # Run any pending migrations (synchronous operation)
        logger.info("Checking for pending database migrations...")
        migrations.run_migrations(database_url)
        logger.info("Database migrations check complete")

        # Create tables if needed (for backwards compatibility)
        await mqtt_database.create_tables()

    finally:
        # Clear migration in progress flag
        await migrations.set_migration_in_progress(mqtt_database.engine, False)
        logger.info("Migration status cleared - database ready")

    mqtt_user = CONFIG["mqtt"].get("username") or None
    mqtt_passwd = CONFIG["mqtt"].get("password") or None
    mqtt_topics = json.loads(CONFIG["mqtt"]["topics"])

    cleanup_enabled = get_bool(CONFIG, "cleanup", "enabled", False)
    cleanup_days = get_int(CONFIG, "cleanup", "days_to_keep", 14)
    vacuum_db = get_bool(CONFIG, "cleanup", "vacuum", False)
    cleanup_hour = get_int(CONFIG, "cleanup", "hour", 2)
    cleanup_minute = get_int(CONFIG, "cleanup", "minute", 0)

    logger.info("Starting MQTT ingestion and cleanup tasks...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            load_database_from_mqtt(
                CONFIG["mqtt"]["server"],
                int(CONFIG["mqtt"]["port"]),
                mqtt_topics,
                mqtt_user,
                mqtt_passwd,
            )
        )

        if cleanup_enabled:
            tg.create_task(daily_cleanup_at(cleanup_hour, cleanup_minute, cleanup_days, vacuum_db))
        else:
            cleanup_logger.info("Daily cleanup is disabled by configuration.")


# -------------------------
# Entry point
# -------------------------
if __name__ == '__main__':
    asyncio.run(main())
