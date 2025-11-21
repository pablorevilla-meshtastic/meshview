# AI Agent Guidelines for Meshview

This document provides context and guidelines for AI coding assistants working on the Meshview project.

## Project Overview

Meshview is a real-time monitoring and diagnostic tool for Meshtastic mesh networks. It provides web-based visualization and analysis of network activity, including:

- Real-time packet monitoring from MQTT streams
- Interactive map visualization of node locations
- Network topology graphs showing connectivity
- Message traffic analysis and conversation tracking
- Node statistics and telemetry data
- Packet inspection and traceroute analysis

## Architecture

### Core Components

1. **MQTT Reader** (`meshview/mqtt_reader.py`) - Subscribes to MQTT topics and receives mesh packets
2. **Database Manager** (`meshview/database.py`, `startdb.py`) - Handles database initialization and migrations
3. **MQTT Store** (`meshview/mqtt_store.py`) - Processes and stores packets in the database
4. **Web Server** (`meshview/web.py`, `main.py`) - Serves the web interface and API endpoints
5. **API Layer** (`meshview/web_api/api.py`) - REST API endpoints for data access
6. **Models** (`meshview/models.py`) - SQLAlchemy database models
7. **Decode Payload** (`meshview/decode_payload.py`) - Protobuf message decoding

### Technology Stack

- **Python 3.13+** - Main language
- **aiohttp** - Async web framework
- **aiomqtt** - Async MQTT client
- **SQLAlchemy (async)** - ORM with async support
- **Alembic** - Database migrations
- **Jinja2** - Template engine
- **Protobuf** - Message serialization (Meshtastic protocol)
- **SQLite/PostgreSQL** - Database backends (SQLite default, PostgreSQL via asyncpg)

### Key Patterns

- **Async/Await** - All I/O operations are asynchronous
- **Database Migrations** - Use Alembic for schema changes (see `docs/Database-Changes-With-Alembic.md`)
- **Configuration** - INI file-based config (`config.ini`, see `sample.config.ini`)
- **Modular API** - API routes separated into `meshview/web_api/` module

## Project Structure

```
meshview/
├── alembic/              # Database migration scripts
├── docs/                 # Technical documentation
├── meshview/             # Main application package
│   ├── static/          # Static web assets (HTML, JS, CSS)
│   ├── templates/       # Jinja2 HTML templates
│   ├── web_api/         # API route handlers
│   └── *.py            # Core modules
├── main.py              # Web server entry point
├── startdb.py           # Database manager entry point
├── mvrun.py             # Combined runner (starts both services)
├── config.ini           # Runtime configuration
└── requirements.txt     # Python dependencies
```

## Development Workflow

### Setup

1. Use Python 3.13+ virtual environment

### Running

- **Database**: `./env/bin/python startdb.py`
- **Web Server**: `./env/bin/python main.py`
- **Both**: `./env/bin/python mvrun.py`


## Code Style

- **Line length**: 100 characters (see `pyproject.toml`)
- **Linting**: Ruff (configured in `pyproject.toml`)
- **Formatting**: Ruff formatter
- **Type hints**: Preferred but not strictly required
- **Async**: Use `async def` and `await` for I/O operations

## Important Files

### Configuration
- `config.ini` - Runtime configuration (server, MQTT, database, cleanup)
- `sample.config.ini` - Template configuration file
- `alembic.ini` - Alembic migration configuration

### Database
- `meshview/models.py` - SQLAlchemy models (Packet, Node, Traceroute, etc.)
- `meshview/database.py` - Database initialization and session management
- `alembic/versions/` - Migration scripts

### Core Logic
- `meshview/mqtt_reader.py` - MQTT subscription and message reception
- `meshview/mqtt_store.py` - Packet processing and storage
- `meshview/decode_payload.py` - Protobuf decoding
- `meshview/web.py` - Web server routes and handlers
- `meshview/web_api/api.py` - REST API endpoints

### Templates
- `meshview/templates/` - Jinja2 HTML templates
- `meshview/static/` - Static files (HTML pages, JS, CSS)

## Common Tasks

### Adding a New API Endpoint

1. Add route handler in `meshview/web_api/api.py`
2. Register route in `meshview/web.py` (if needed)
3. Update `docs/API_Documentation.md` if public API

### Database Schema Changes

1. Modify models in `meshview/models.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration in `alembic/versions/`
4. Test migration: `alembic upgrade head`
5. **Never** modify existing migration files after they've been applied

### Adding a New Web Page

1. Create template in `meshview/templates/`
2. Add route in `meshview/web.py`
3. Add navigation link if needed (check existing templates for pattern)
4. Add static assets if needed in `meshview/static/`

### Processing New Packet Types

1. Check `meshview/decode_payload.py` for existing decoders
2. Add decoder function if new type
3. Update `meshview/mqtt_store.py` to handle new packet type
4. Update database models if new data needs storage


## Key Concepts

### Meshtastic Protocol
- Uses Protobuf for message serialization
- Packets contain various message types (text, position, telemetry, etc.)
- MQTT topics follow pattern: `msh/{region}/{subregion}/#`

### Database Schema
- **packet** - Raw packet data
- **node** - Mesh node information
- **traceroute** - Network path information
- **packet_seen** - Packet observation records

### Real-time Updates
- Web pages use Server-Sent Events (SSE) for live updates
- Map and firehose pages auto-refresh based on config intervals
- API endpoints return JSON for programmatic access

## Best Practices

1. **Always use async/await** for database and network operations
2. **Use Alembic** for all database schema changes
3. **Follow existing patterns** - check similar code before adding new features
4. **Update documentation** - keep `docs/` and README current
5. **Test migrations** - verify migrations work both up and down
6. **Handle errors gracefully** - log errors, don't crash on bad packets
7. **Respect configuration** - use `config.ini` values, don't hardcode

## Common Pitfalls

- **Don't modify applied migrations** - create new ones instead
- **Don't block the event loop** - use async I/O, not sync
- **Don't forget timezone handling** - timestamps are stored in UTC
- **Don't hardcode paths** - use configuration values
- **Don't ignore MQTT reconnection** - handle connection failures gracefully

## Resources

- **Main README**: `README.md` - Installation and basic usage
- **Docker Guide**: `README-Docker.md` - Container deployment
- **API Docs**: `docs/API_Documentation.md` - API endpoint reference
- **Migration Guide**: `docs/Database-Changes-With-Alembic.md` - Database workflow
- **Contributing**: `CONTRIBUTING.md` - Contribution guidelines

## Version Information

- **Current Version**: 3.0.0 (November 2025)
- **Python Requirement**: 3.13+
- **Key Features**: Alembic migrations, automated backups, Docker support, traceroute return paths


## Rules for robots
- Always run ruff check and ruff format after making changes (only on python changes)


---

When working on this project, prioritize:
1. Maintaining async patterns
2. Following existing code structure
3. Using proper database migrations
4. Keeping documentation updated
5. Testing changes thoroughly



