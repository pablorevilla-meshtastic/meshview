import asyncio
import datetime
import gzip
import json
import logging
import shutil
from pathlib import Path

from sqlalchemy import delete

from meshview import migrations, models, mqtt_database, mqtt_reader, mqtt_store
from meshview.config import CONFIG

# -------------------------
# Basic logging configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s:%(lineno)d [pid:%(process)d] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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
# Database backup function
# -------------------------
async def backup_database(database_url: str, backup_dir: str = ".") -> None:
    """
    Create a compressed backup of the database file.

    Args:
        database_url: SQLAlchemy connection string
        backup_dir: Directory to store backups (default: current directory)
    """
    try:
        # Extract database file path from connection string
        # Format: sqlite+aiosqlite:///path/to/db.db
        if not database_url.startswith("sqlite"):
            cleanup_logger.warning("Backup only supported for SQLite databases")
            return

        db_path = database_url.split("///", 1)[1] if "///" in database_url else None
        if not db_path:
            cleanup_logger.error("Could not extract database path from connection string")
            return

        db_file = Path(db_path)
        if not db_file.exists():
            cleanup_logger.error(f"Database file not found: {db_file}")
            return

        # Create backup directory if it doesn't exist
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{db_file.stem}_backup_{timestamp}.db.gz"
        backup_file = backup_path / backup_filename

        cleanup_logger.info(f"Creating backup: {backup_file}")

        # Copy and compress the database file
        with open(db_file, 'rb') as f_in:
            with gzip.open(backup_file, 'wb', compresslevel=9) as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Get file sizes for logging
        original_size = db_file.stat().st_size / (1024 * 1024)  # MB
        compressed_size = backup_file.stat().st_size / (1024 * 1024)  # MB
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0

        cleanup_logger.info(
            f"Backup created successfully: {backup_file.name} "
            f"({original_size:.2f} MB -> {compressed_size:.2f} MB, "
            f"{compression_ratio:.1f}% compression)"
        )

    except Exception as e:
        cleanup_logger.error(f"Error creating database backup: {e}")


# -------------------------
# Database backup scheduler
# -------------------------
async def daily_backup_at(hour: int = 2, minute: int = 0, backup_dir: str = "."):
    while True:
        now = datetime.datetime.now()
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_run <= now:
            next_run += datetime.timedelta(days=1)
        delay = (next_run - now).total_seconds()
        cleanup_logger.info(f"Next backup scheduled at {next_run}")
        await asyncio.sleep(delay)

        database_url = CONFIG["database"]["connection_string"]
        await backup_database(database_url, backup_dir)


# -------------------------
# Database cleanup using ORM
# -------------------------
async def daily_cleanup_at(
    hour: int = 2,
    minute: int = 0,
    days_to_keep: int = 14,
    vacuum_db: bool = True,
    wait_for_backup: bool = False,
):
    while True:
        now = datetime.datetime.now()
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_run <= now:
            next_run += datetime.timedelta(days=1)
        delay = (next_run - now).total_seconds()
        cleanup_logger.info(f"Next cleanup scheduled at {next_run}")
        await asyncio.sleep(delay)

        # If backup is enabled, wait a bit to let backup complete first
        if wait_for_backup:
            cleanup_logger.info("Waiting 60 seconds for backup to complete...")
            await asyncio.sleep(60)

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
        # Check if migrations are needed before running them
        logger.info("Checking for pending database migrations...")
        if await migrations.is_database_up_to_date(mqtt_database.engine, database_url):
            logger.info("Database schema is already up to date, skipping migrations")
        else:
            logger.info("Database schema needs updating, running migrations...")
            migrations.run_migrations(database_url)
            logger.info("Database migrations completed")

        # Create tables if needed (for backwards compatibility)
        logger.info("Creating database tables...")
        await mqtt_database.create_tables()
        logger.info("Database tables created")

    finally:
        # Clear migration in progress flag
        logger.info("Clearing migration status...")
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

    backup_enabled = get_bool(CONFIG, "cleanup", "backup_enabled", False)
    backup_dir = CONFIG.get("cleanup", {}).get("backup_dir", "./backups")
    backup_hour = get_int(CONFIG, "cleanup", "backup_hour", cleanup_hour)
    backup_minute = get_int(CONFIG, "cleanup", "backup_minute", cleanup_minute)

    logger.info(f"Starting MQTT ingestion from {CONFIG['mqtt']['server']}:{CONFIG['mqtt']['port']}")
    if cleanup_enabled:
        logger.info(
            f"Daily cleanup enabled: keeping {cleanup_days} days of data at {cleanup_hour:02d}:{cleanup_minute:02d}"
        )
    if backup_enabled:
        logger.info(
            f"Daily backups enabled: storing in {backup_dir} at {backup_hour:02d}:{backup_minute:02d}"
        )

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

        # Start backup task if enabled
        if backup_enabled:
            tg.create_task(daily_backup_at(backup_hour, backup_minute, backup_dir))

        # Start cleanup task if enabled (waits for backup if both run at same time)
        if cleanup_enabled:
            wait_for_backup = (
                backup_enabled
                and (backup_hour == cleanup_hour)
                and (backup_minute == cleanup_minute)
            )
            tg.create_task(
                daily_cleanup_at(
                    cleanup_hour, cleanup_minute, cleanup_days, vacuum_db, wait_for_backup
                )
            )

        if not cleanup_enabled and not backup_enabled:
            cleanup_logger.info("Daily cleanup and backups are both disabled by configuration.")


# -------------------------
# Entry point
# -------------------------
if __name__ == '__main__':
    asyncio.run(main())
