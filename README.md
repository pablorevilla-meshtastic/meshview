
# Meshview
![Start Page](screenshots/animated.gif)

The project serves as a real-time monitoring and diagnostic tool for the Meshtastic mesh network. It provides detailed insights into network activity, including message traffic, node positions, and telemetry data.

### Version 3.0.4 — Late January 2026
- Database: multi‑DB support, PostgreSQL scripts, WAL config for SQLite, cleanup query timing fixes, removal of import time columns, and various time‑handling fixes.
- UI/UX: extensive updates to node.html, nodelist.html, top.html, and packet.html (paging, stats, distance, status/favorites), plus net view changes to 12‑hour window.
- API/logic: weekly mesh query fix, node list performance improvement, backwards‑compatibility and other bug fixes.
- MQTT reader: configurable skip‑node list and secondary decryption keys.
- Docs/ops: multiple documentation updates, updated site list, container workflow fixes/tests, README updates.

### Version 3.0.2 — January 2026
- Changes to the Database to will make it so that there is a need for space when updating to the latest. SQlite requires to rebuild the database when droping a column. ( we are droping some of the old columns) so make sure you have 1.2x the size of the db of space in your environment. Depending on how big your db is it would take a long time.
  
### Version 3.0.1 — December 2025

#### 🌐 Multi-Language Support (i18n)
- New `/api/lang` endpoint for serving translations  
- Section-based translation loading (e.g., `?section=firehose`)  
- Default language controlled via config file language section
- JSON-based translation files for easy expansion  
- Core pages updated to support `data-translate-lang` attributes  

### 🛠 Improvements
- Updated UI elements across multiple templates for localization readiness  
- General cleanup to support future language additions  

### Version 3.0.0 update - November 2025

**Major Infrastructure Improvements:**

* **Database Migrations**: Alembic integration for safe schema upgrades and database versioning
* **Automated Backups**: Independent database backup system with gzip compression (separate from cleanup)
* **Development Tools**: Quick setup script (`setup-dev.sh`) with pre-commit hooks for code quality
* **Docker Support**: Pre-built containers now available on GitHub Container Registry with automatic builds - ogarcia 

**New Features:**

* **Traceroute Return Path**: Log and display return path data for traceroute packets - jschrempp 
* **Microsecond Timestamps**: Added `import_time_us` columns for higher precision time tracking

**Technical Improvements:**

* Migration from manual SQL to Alembic-managed schema
* Container images use `uv` for faster dependency installation
* Python 3.13 support with slim Debian-based images
* Documentation collection in `docs/` directory
* API routes moved to separate modules for better organization
* /version and /health endpoints added for monitoring

See [README-Docker.md](README-Docker.md) for container deployment and [docs/](docs/) for technical documentation.

### Version 2.0.7 update - September 2025
* New database maintenance capability to automatically keep a specific number of days of data.
* Added configuration for update intervals for both the Live Map and the Firehose pages.

### Version 2.0.6 update - August 2025
* New Live Map (Shows packet feed live)
* New API /api/config (See API documentation)
* New API /api/edges (See API documentation)
* Adds edges to the map (click to see traceroute and neighbours)


### Version 2.0.4 update - August 2025
* New statistic page with more data.
* New API /api/stats (See API documentation).
* Inprovement on "See Everything" and "Conversation" pages.
* Tracking of replies with links to original message.

### Version 2.0.3 update - June 2025
* Moved more graphs to eCharts.
* Addedd smooth updating for "Conversations" and "See everything" sections.
* Now you can turn on and off "Quick Links".
* Network graphs are now dynamically generated depending on your mesh and the presets in use.
* Download node's packet information for the last 3 days to .csv file.
* Display distance traveled by packet.
### Key Features

* **Live Data Visualization**: Users can view real-time data from the mesh network, including text messages, GPS positions, and node information.

* **Interactive Map**: The site offers an interactive map displaying the locations of active nodes, helping users identify network coverage areas.

* **Mesh Graphs**: Visual representations of the network's structure and connectivity are available, illustrating how nodes are interconnected.

* **Packet Analysis**: Detailed information on individual data packets transmitted within the network can be accessed, including payload content and transmission paths.

* **Node Statistics**: Users can explore statistics related to network traffic, such as top contributors and message volumes.

Samples of currently running instances:

- https://meshview.bayme.sh (SF Bay Area - USA)
- https://www.svme.sh (Sacramento Valley - USA)
- https://meshview.nyme.sh (New York - USA)
- https://meshview.socalmesh.org (Los Angenles - USA)
- https://map.wpamesh.net (Western Pennsylvania - USA)
- https://meshview.chicagolandmesh.org (Chicago - USA)
- https://meshview.mt.gt (Canada)
- https://canadaverse.org (Canada)
- https://meshview.meshtastic.es (Spain)
- https://view.mtnme.sh (North Georgia / East Tennessee - USA)
- https://meshview.lsinfra.de (Hessen - Germany)
- https://meshview.pvmesh.org (Pioneer Valley, Massachusetts - USA)
- https://meshview.louisianamesh.org (Louisiana - USA)
- https://www.swlamesh.com (Southwest Louisiana- USA)
- https://meshview.meshcolombia.co (Colombia)
- https://meshview-salzburg.jmt.gr (Salzburg / Austria)
- https://map.cromesh.eu (Coatia)
- https://view.meshdresden.eu (Dresden / Germany)
- https://meshview.meshoregon.com (Oregon - USA)
- https://meshview.gamesh.net (Georgia - USA)

---



### Updating from 2.x to 3.x
We are adding the use of Alembic. If using GitHub
Update your codebase by running the pull command
```bash
cd meshview
git pull origin master
```
Install Alembic in your environment
```bash
./env/bin/pip install alembic
```
Start your scripts or services. This process will update your database with the latest schema.

## Installing

### Using Docker (Recommended)

The easiest way to run MeshView is using Docker. Pre-built images are available from GitHub Container Registry.

See **[README-Docker.md](README-Docker.md)** for complete Docker installation and usage instructions.

### Manual Installation

Requires **`python3.13`** or above.

Clone the repo from GitHub:

```bash
git clone https://github.com/pablorevilla-meshtastic/meshview.git
cd meshview
```

#### Quick Setup (Recommended)

Run the development setup script:

```bash
./setup-dev.sh
```

This will:
- Create Python virtual environment
- Install all requirements
- Install development tools (pre-commit, pytest)
- Set up pre-commit hooks for code formatting
- Create config.ini from sample

#### Manual Setup

Create a Python virtual environment:

```bash
python3 -m venv env
```

Install the environment requirements:

```bash
./env/bin/pip install -r requirements.txt
```

Install `graphviz` on MacOS or Debian/Ubuntu Linux:

```bash
sudo apt-get install graphviz
```

Copy `sample.config.ini` to `config.ini`:

```bash
cp sample.config.ini config.ini
```

Edit `config.ini` to match your MQTT and web server settings:


```bash
nano config.ini
```

> **NOTE**
> On MacOS set the bind configuration line to 
> ```
> bind = 127.0.0.1
> ```

Example:

```ini
# -------------------------
# Server Configuration
# -------------------------
[server]
# The address to bind the server to. Use * to listen on all interfaces.
bind = *

# Port to run the web server on.
port = 8081

# Path to TLS certificate (leave blank to disable HTTPS).
tls_cert =

# Path for the ACME challenge if using Let's Encrypt.
acme_challenge =


# -------------------------
# Site Appearance & Behavior
# -------------------------
[site]
# The domain name of your site.
domain =

# Select language (this represents the name of the json file in the /lang directory)
language = es

# Site title to show in the browser title bar and headers.
title = Bay Area Mesh

# A brief message shown on the homepage.
message = Real time data from around the bay area and beyond.

# Starting URL when loading the index page.
starting = /chat

# Enable or disable site features (as strings: "True" or "False").
nodes = True
conversations = True
everything = True
graphs = True
stats = True
net = True
map = True
top = True

# Map boundaries (used for the map view).
# Defaults will show the San Francisco Bay Area
map_top_left_lat = 39
map_top_left_lon = -123
map_bottom_right_lat = 36
map_bottom_right_lon = -121

# Updates intervals in seconds, zero or negative number means no updates
# defaults will be 3 seconds
map_interval=3
firehose_interval=3

# Weekly net details
weekly_net_message = Weekly Mesh check-in. We will keep it open on every Wednesday from 5:00pm for checkins. The message format should be (LONG NAME) - (CITY YOU ARE IN) #BayMeshNet.
net_tag = #BayMeshNet

# -------------------------
# MQTT Broker Configuration
# -------------------------
[mqtt]
# MQTT server hostname or IP.
server = mqtt.bayme.sh

# Topics to subscribe to (as JSON-like list, but still a string).
topics = ["msh/US/bayarea/#", "msh/US/CA/mrymesh/#", "msh/US/CA/sacvalley"]

# Port used by MQTT (typically 1883 for unencrypted).
port = 1883

# MQTT username and password.
username = meshdev
password = large4cats


# -------------------------
# Database Configuration
# -------------------------
[database]
# SQLAlchemy async connection string.
# Examples:
#   sqlite+aiosqlite:///packets.db
#   postgresql+asyncpg://user:pass@host:5432/meshview
connection_string = sqlite+aiosqlite:///packets.db


# -------------------------
# Database Cleanup Configuration
# -------------------------
[cleanup]
# Enable or disable daily cleanup
enabled = False
# Number of days to keep records in the database
days_to_keep = 14
# Time to run daily cleanup (24-hour format)
hour = 2
minute = 00
# Run VACUUM after cleanup
vacuum = False


# -------------------------
# Logging Configuration
# -------------------------
[logging]
# Enable or disable HTTP access logs from the web server
# When disabled, request logs like "GET /api/chat" will not appear
# Application logs (errors, startup messages, etc.) are unaffected
# Set to True to enable, False to disable (default: False)
access_log = False
# Database cleanup logfile location
db_cleanup_logfile = dbcleanup.log
```

---

## NOTE (PostgreSQL setup)**  
If you want to use PostgreSQL instead of SQLite:

Install PostgreSQL for your OS.  
Create a user and database:
```
`CREATE USER meshview WITH PASSWORD 'change_me';`
`CREATE DATABASE meshview OWNER meshview;`
```
Update `config.ini` example:
```
`connection_string = postgresql+asyncpg://meshview:change_me@localhost:5432/meshview`
```

## Running Meshview

Start the database manager:

```bash
./env/bin/python startdb.py
```

Start the web server:

```bash
./env/bin/python main.py
```

> **NOTE**  
> You can specify a custom config file with the `--config` flag:
>
> ```bash
> ./env/bin/python startdb.py --config /path/to/config.ini
> ./env/bin/python main.py --config /path/to/config.ini
> ```

Open in your browser: http://localhost:8081/

---

## Running Meshview with `mvrun.py`

- `mvrun.py` starts both `startdb.py` and `main.py` in separate threads and merges the output.
- It accepts several command-line arguments for flexible deployment.

```bash
./env/bin/python mvrun.py
```

**Command-line options:**
- `--config CONFIG` - Path to the configuration file (default: `config.ini`)
- `--pid_dir PID_DIR` - Directory for PID files (default: `.`)
- `--py_exec PY_EXEC` - Path to the Python executable (default: `./env/bin/python`)

**Examples:**
```bash
# Use a specific config file
./env/bin/python mvrun.py --config /etc/meshview/config.ini

# Store PID files in a specific directory
./env/bin/python mvrun.py --pid_dir /var/run/meshview

# Use a different Python executable
./env/bin/python mvrun.py --py_exec /usr/bin/python3
```

---

## Setting Up Systemd Services (Ubuntu)

To run Meshview automatically on boot, create systemd services for `startdb.py` and `main.py`.
> **NOTE**  
> You need to change the "User" and "/path/to/meshview" for your instance of the code on each service.

### 1. Service for `startdb.py`

Create:

```bash
sudo nano /etc/systemd/system/meshview-db.service
```

Paste:

```ini
[Unit]
Description=Meshview Database Initializer
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/meshview
ExecStart=/path/to/meshview/env/bin/python /path/to/meshview/startdb.py --config /path/to/meshview/config.ini
Restart=always
RestartSec=5
User=yourusername

[Install]
WantedBy=multi-user.target
```

### 2. Service for `main.py`

Create:

```bash
sudo nano /etc/systemd/system/meshview-web.service
```

Paste:

```ini
[Unit]
Description=Meshview Web Server
After=network.target meshview-db.service

[Service]
Type=simple
WorkingDirectory=/path/to/meshview
ExecStart=/path/to/meshview/env/bin/python /path/to/meshview/main.py --config /path/to/meshview/config.ini
Restart=always
RestartSec=5
User=yourusername

[Install]
WantedBy=multi-user.target
```

### 3. Enable and start the services

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable meshview-db
sudo systemctl enable meshview-web
sudo systemctl start meshview-db
sudo systemctl start meshview-web
```

### 4. Check status

```bash
systemctl status meshview-db
systemctl status meshview-web
```

**TIP**  
After editing `.service` files, always run:

```bash
sudo systemctl daemon-reload
```

## 5. Database Maintenance
### Database maintnance can now be done via the script itself here is the section from the configuration file.
- Simple to setup
- It will not drop any packets
```
# -------------------------
# Database Cleanup Configuration
# -------------------------
[cleanup]
# Enable or disable daily cleanup
enabled = False
# Number of days to keep records in the database
days_to_keep = 14
# Time to run daily cleanup (24-hour format)
hour = 2
minute = 00
# Run VACUUM after cleanup
vacuum = False

# -------------------------
# Logging Configuration
# -------------------------
[logging]
# Enable or disable HTTP access logs from the web server
access_log = False
# Database cleanup logfile location
db_cleanup_logfile = dbcleanup.log
```
Once changes are done you need to restart the script for changes to load.

### Alternatively we can do it via your OS (This example is Ubuntu like OS)
- Create and save bash script below. (Modify /path/to/file/ to the correct path)
- Name it cleanup.sh
- Make it executable.
```bash
#!/bin/bash

DB_FILE="/path/to/file/packets.db"

# Stop DB service
sudo systemctl stop meshview-db.service
sudo systemctl stop meshview-web.service

sleep 5
echo "Run cleanup..."
# Run cleanup queries
sqlite3 "$DB_FILE" <<EOF 
DELETE FROM packet
WHERE import_time_us IS NOT NULL
  AND import_time_us < (strftime('%s','now','-14 days') * 1000000);
SELECT 'packet deleted: ' || changes();
DELETE FROM packet_seen
WHERE import_time_us IS NOT NULL
  AND import_time_us < (strftime('%s','now','-14 days') * 1000000);
SELECT 'packet_seen deleted: ' || changes();
DELETE FROM traceroute
WHERE import_time_us IS NOT NULL
  AND import_time_us < (strftime('%s','now','-14 days') * 1000000);
SELECT 'traceroute deleted: ' || changes();
DELETE FROM node
WHERE last_seen_us IS NULL
   OR last_seen_us < (strftime('%s','now','-14 days') * 1000000);
SELECT 'node deleted: ' || changes();
VACUUM;
EOF

# Start DB service
sudo systemctl start meshview-db.service
sudo systemctl start meshview-web.service

echo "Database cleanup completed on $(date)"

```
- If you are using PostgreSQL, use this version instead (adjust credentials/DB name):
```bash
#!/bin/bash

DB_NAME="meshview"
DB_USER="meshview"
DB_HOST="localhost"
DB_PORT="5432"

# Stop DB service
sudo systemctl stop meshview-db.service
sudo systemctl stop meshview-web.service

sleep 5
echo "Run cleanup..."
# Run cleanup queries
psql "postgresql://${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}" <<'EOF'
WITH deleted AS (
  DELETE FROM packet
  WHERE import_time_us IS NOT NULL
    AND import_time_us < (EXTRACT(EPOCH FROM (NOW() - INTERVAL '14 days')) * 1000000)
  RETURNING 1
)
SELECT 'packet deleted: ' || COUNT(*) FROM deleted;

WITH deleted AS (
  DELETE FROM packet_seen
  WHERE import_time_us IS NOT NULL
    AND import_time_us < (EXTRACT(EPOCH FROM (NOW() - INTERVAL '14 days')) * 1000000)
  RETURNING 1
)
SELECT 'packet_seen deleted: ' || COUNT(*) FROM deleted;

WITH deleted AS (
  DELETE FROM traceroute
  WHERE import_time_us IS NOT NULL
    AND import_time_us < (EXTRACT(EPOCH FROM (NOW() - INTERVAL '14 days')) * 1000000)
  RETURNING 1
)
SELECT 'traceroute deleted: ' || COUNT(*) FROM deleted;

WITH deleted AS (
  DELETE FROM node
  WHERE last_seen_us IS NULL
     OR last_seen_us < (EXTRACT(EPOCH FROM (NOW() - INTERVAL '14 days')) * 1000000)
  RETURNING 1
)
SELECT 'node deleted: ' || COUNT(*) FROM deleted;

VACUUM;
EOF

# Start DB service
sudo systemctl start meshview-db.service
sudo systemctl start meshview-web.service

echo "Database cleanup completed on $(date)"
```
- Schedule running the script on a regular basis. 
- In this example it runs every night at 2:00am.

Open scheduler:
```bash
sudo crontab -e
```
Add schedule to the bottom of the file (modify /path/to/file/ to the correct path):
```bash
0 2 * * * /path/to/file/cleanup.sh >> /path/to/file/cleanup.log 2>&1
```

Check the log file to see it the script run at the specific time.

---

## Testing

MeshView includes a test suite using pytest. For detailed testing documentation, see [README-testing.md](README-testing.md).

Quick start:
```bash
./env/bin/pytest tests/test_api_simple.py -v
```

---

## Technical Documentation

For more detailed technical documentation including database migrations, architecture details, and advanced topics, see the [docs/](docs/) directory.
