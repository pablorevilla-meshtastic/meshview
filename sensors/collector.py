#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_DB_PATH = "readings.db"
DEFAULT_READINGS_LIMIT = 100
BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                temperature_c REAL NOT NULL,
                humidity REAL NOT NULL,
                received_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_readings_device_received_at
            ON readings (device_id, received_at DESC)
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_reading(db_path, reading):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute(
            """
            INSERT INTO readings (
                device_id,
                sensor_type,
                temperature_c,
                humidity,
                received_at
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                reading["device_id"],
                reading["sensor_type"],
                reading["temperature_c"],
                reading["humidity"],
                utc_now_iso(),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def fetch_recent_readings(db_path, limit):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT
                id,
                device_id,
                sensor_type,
                temperature_c,
                humidity,
                received_at
            FROM readings
            ORDER BY received_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        readings = [dict(row) for row in rows]
        readings.reverse()
        return readings
    finally:
        conn.close()


def validate_payload(payload):
    required_fields = (
        "device_id",
        "sensor_type",
        "temperature_c",
        "humidity",
    )
    for field in required_fields:
        if field not in payload:
            raise ValueError("Missing field: {}".format(field))

    validated = {
        "device_id": str(payload["device_id"]).strip(),
        "sensor_type": str(payload["sensor_type"]).strip(),
        "temperature_c": float(payload["temperature_c"]),
        "humidity": float(payload["humidity"]),
    }

    if not validated["device_id"]:
        raise ValueError("device_id must not be empty")
    if not validated["sensor_type"]:
        raise ValueError("sensor_type must not be empty")

    return validated


def render_template(template_name, **context):
    template = templates.get_template(template_name)
    return template.render(**context)


def build_dashboard_context(db_path):
    readings = fetch_recent_readings(db_path, DEFAULT_READINGS_LIMIT)
    latest = readings[-1] if readings else None
    return {
        "title": "ESP32 Collector",
        "readings": readings,
        "reading_count": len(readings),
        "latest": latest,
    }


class AppHandler(BaseHTTPRequestHandler):
    server_version = "ESP32Collector/1.0"

    def send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html, status=HTTPStatus.OK):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        route = urlparse(self.path).path

        if route == "/":
            self.send_html(render_template("dashboard.html", **build_dashboard_context(self.server.db_path)))
            return

        if route == "/chart":
            self.send_html(render_template("dashboard.html", **build_dashboard_context(self.server.db_path)))
            return

        if route == "/health":
            self.send_json({"status": "ok"})
            return

        if route == "/readings":
            readings = fetch_recent_readings(self.server.db_path, DEFAULT_READINGS_LIMIT)
            self.send_json({"readings": readings})
            return

        self.send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self):
        route = urlparse(self.path).path
        if route != "/metrics":
            self.send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)
            return

        content_length = self.headers.get("Content-Length")
        if not content_length:
            self.send_json({"error": "missing content length"}, status=HTTPStatus.LENGTH_REQUIRED)
            return

        try:
            raw_body = self.rfile.read(int(content_length))
            payload = json.loads(raw_body)
            reading = validate_payload(payload)
            row_id = insert_reading(self.server.db_path, reading)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
            return
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, status=HTTPStatus.BAD_REQUEST)
            return
        except Exception as exc:
            self.send_json(
                {"error": "server error", "detail": str(exc)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            return

        print(
            "[{}] stored reading id={} device={} temp_c={} humidity={}".format(
                utc_now_iso(),
                row_id,
                reading["device_id"],
                reading["temperature_c"],
                reading["humidity"],
            )
        )
        self.send_json({"status": "stored", "id": row_id}, status=HTTPStatus.CREATED)

    def log_message(self, format_string, *args):
        print(
            "[{}] {} {}".format(
                utc_now_iso(),
                self.address_string(),
                format_string % args,
            )
        )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect ESP32 sensor data and render a Jinja dashboard."
    )
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--db", default=DEFAULT_DB_PATH)
    return parser.parse_args()


def main():
    args = parse_args()
    db_path = Path(args.db).resolve()
    init_db(db_path)

    server = ThreadingHTTPServer((args.host, args.port), AppHandler)
    server.db_path = str(db_path)

    print("Metrics endpoint: http://{}:{}/metrics".format(args.host, args.port))
    print("Dashboard: http://{}:{}/chart".format(args.host, args.port))
    print("SQLite database:", db_path)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
