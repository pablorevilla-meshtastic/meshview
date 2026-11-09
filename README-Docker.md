# Running MeshView with Docker

MeshView container images are built automatically and published to GitHub Container Registry.
The examples below use a Bash-compatible shell and Docker Compose v2 (`docker compose`).

## Quick Start

Prepare the configuration and persistent directories before starting the container:

```bash
docker pull ghcr.io/pablorevilla-meshtastic/meshview:latest
mkdir -p meshview/{config,data,logs,backups}

# First-time setup only: extract the image's bundled configuration.
# --entrypoint bypasses the normal MeshView startup command.
docker run --rm --entrypoint cat \
  ghcr.io/pablorevilla-meshtastic/meshview:latest \
  /etc/meshview/config.ini > meshview/config/config.ini

# Edit MQTT settings, site settings, and backup options before starting.
nano meshview/config/config.ini

# On Linux, give the container user (UID 10001) ownership of writable data.
sudo chown -R 10001 meshview/data meshview/logs meshview/backups
sudo chmod -R u+rwX meshview/data meshview/logs meshview/backups
# The configuration stays owned by you and must be readable by the container.
chmod 755 meshview/config
chmod 644 meshview/config/config.ini

docker run -d \
  --name meshview \
  --restart unless-stopped \
  -p 8081:8081 \
  -v "$(pwd)/meshview/config:/etc/meshview:ro" \
  -v "$(pwd)/meshview/data:/var/lib/meshview" \
  -v "$(pwd)/meshview/logs:/var/log/meshview" \
  -v "$(pwd)/meshview/backups:/var/lib/meshview/backups" \
  ghcr.io/pablorevilla-meshtastic/meshview:latest
```

Run the config extraction only for a new installation: the redirection overwrites any
existing `config.ini`. On Docker Desktop, host file permissions may be managed differently;
the requirement is that UID 10001 can read the configuration and write data, logs, and backups.

Access the web interface at http://localhost:8081. Check startup with `docker logs -f meshview`.
Database migrations run automatically when MeshView starts.

## Volume Mounts

| Container path | Purpose | Host directory in the examples |
|----------------|---------|--------------------------------|
| `/etc/meshview` | Read-only configuration containing `config.ini` | `meshview/config` |
| `/var/lib/meshview` | SQLite database storage | `meshview/data` |
| `/var/log/meshview` | File logs, when enabled | `meshview/logs` |
| `/var/lib/meshview/backups` | Database backups, when enabled | `meshview/backups` |

An empty host configuration directory hides the image's bundled `config.ini` and prevents
startup. There is no fallback when a mounted configuration directory lacks that file.
If you omit the configuration mount entirely, the image's bundled configuration is used.

Stopping or restarting a container does not delete the database. Explicit host mounts make
it straightforward to preserve and reuse data when removing or recreating containers.
Without explicit mounts, the image declares anonymous volumes; do not rely on those being
automatically reused by a replacement container, and do not delete them if you need their data.

## Docker Compose

Use the preparation steps from Quick Start, but skip its `docker run -d` command.
Create `compose.yaml` **inside the `meshview` directory**, alongside `config`, `data`,
`logs`, and `backups`:

```yaml
services:
  meshview:
    image: ghcr.io/pablorevilla-meshtastic/meshview:latest
    container_name: meshview
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - ./config:/etc/meshview:ro
      - ./data:/var/lib/meshview
      - ./logs:/var/log/meshview
      - ./backups:/var/lib/meshview/backups
    environment:
      TZ: America/Los_Angeles
```

Start from that directory:

```bash
cd meshview
docker compose up -d
docker compose logs -f
```

Choose either Compose or `docker run` to manage the installation. If switching from the
Quick Start container to Compose, stop and remove the old container first, keeping its
host directories: `docker stop meshview` followed by `docker rm meshview`.

## Configuration

Edit the extracted `config.ini` rather than replacing it with a partial configuration.
Keep the container server listening on all interfaces:

```ini
[server]
bind = 0.0.0.0
port = 8081
```

Set your MQTT broker, topics, and credentials in the existing `[mqtt]` section. The broker
must be reachable from the container; `localhost` refers to the container itself.

Keep the database path inside the mounted data directory:

```ini
[database]
connection_string = sqlite+aiosqlite:////var/lib/meshview/packets.db
```

The four slashes after `sqlite+aiosqlite:` specify an absolute Linux path. PostgreSQL
is also supported with a connection string such as
`postgresql+asyncpg://user:pass@host:5432/meshview`.

After configuration changes, restart the application with `docker restart meshview`, or
`docker compose restart meshview` for a Compose installation.

### Database Backups

Enable backups in the existing `[cleanup]` section:

```ini
[cleanup]
backup_enabled = True
backup_dir = /var/lib/meshview/backups
backup_hour = 2
backup_minute = 00
```

Both startup examples mount this directory to `meshview/backups` on the host. Backups
remain disabled until you enable them in the configuration.

## Available Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest build from the repository's default branch |
| Branch name | Builds published for that branch |
| `3.0.6` | Example version tag; use a version published in the registry |

## Updating

For a Compose installation, run from the directory containing `compose.yaml`:

```bash
docker compose pull
docker compose up -d
```

For a `docker run` installation, run from the same parent directory used in Quick Start:

```bash
docker pull ghcr.io/pablorevilla-meshtastic/meshview:latest
docker stop meshview
docker rm meshview

docker run -d \
  --name meshview \
  --restart unless-stopped \
  -p 8081:8081 \
  -v "$(pwd)/meshview/config:/etc/meshview:ro" \
  -v "$(pwd)/meshview/data:/var/lib/meshview" \
  -v "$(pwd)/meshview/logs:/var/log/meshview" \
  -v "$(pwd)/meshview/backups:/var/lib/meshview/backups" \
  ghcr.io/pablorevilla-meshtastic/meshview:latest
```

Preserve any custom ports, mounts, or environment settings when recreating the container.
Do not repeat the first-time configuration extraction during updates. Pulling an image
and merely restarting an existing container does not switch it to the new image.

## Logs

```bash
docker logs meshview
docker logs -f meshview
docker logs --tail 100 meshview
```

For Compose installations, `docker compose logs -f meshview` also works.

## Troubleshooting

### Container won't start

Check `docker logs meshview`. Verify that the mounted `config` directory contains a
readable `config.ini`, and that the database and log directories are writable by UID 10001.

### Docker Desktop reports mounts denied

Make sure the installation directory is shared with Docker Desktop under Settings →
Resources → File Sharing. Bind-mount source paths must exist on the Docker daemon's
host; a remote daemon cannot mount directories that exist only on your client.

### Database permission issues

From the parent directory containing `meshview`, repair writable directory ownership:

```bash
sudo chown -R 10001 meshview/data meshview/logs meshview/backups
sudo chmod -R u+rwX meshview/data meshview/logs meshview/backups
```

Setting permissions to `755` alone does not let UID 10001 write to directories owned
by another user. SQLite also needs to create journal/WAL files beside the database.

### Can't connect to MQTT

Check the broker hostname, port, credentials, and topics in `config.ini`.
Test DNS resolution and a TCP connection using Python, which is included in the image:

```bash
# Replace the hostname and port with your configured broker.
docker exec meshview /opt/venv/bin/python -c \
  'import socket; s = socket.create_connection(("mqtt.meshtastic.org", 1883), timeout=10); print("TCP connection successful"); s.close()'
```

This checks network connectivity, not MQTT authentication or topic permissions.
The image does not include `ping`.

### Port already in use

Change the host port (left side) to `8082`, keeping the container port at `8081`:

```bash
-p 8082:8081
```

For Compose, use `"8082:8081"` under `ports`. Access http://localhost:8082.

## Building Your Own Image

```bash
git clone https://github.com/pablorevilla-meshtastic/meshview.git
cd meshview
docker build -f Containerfile -t meshview:local .
```

Use `meshview:local` instead of the registry image in the setup and run commands.

## Security Notes

- The container runs as a non-root user (`app`, UID 10001).
- No privileged access is required.
- The examples publish port 8081 on the host; configuration is mounted read-only.
- Database, file logs, and backups use the mounted directories shown above.

## Support

- GitHub Issues: https://github.com/pablorevilla-meshtastic/meshview/issues
- Documentation: https://github.com/pablorevilla-meshtastic/meshview
