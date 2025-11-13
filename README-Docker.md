# Running MeshView with Docker

MeshView container images are built automatically and published to GitHub Container Registry.

## Quick Start

Pull and run the latest image:

```bash
docker pull ghcr.io/pablorevilla-meshtastic/meshview:latest

docker run -d \
  --name meshview \
  -p 8081:8081 \
  -v ./config:/etc/meshview \
  -v ./data:/var/lib/meshview \
  -v ./logs:/var/log/meshview \
  ghcr.io/pablorevilla-meshtastic/meshview:latest
```

Access the web interface at: http://localhost:8081

## Volume Mounts

The container uses three volumes for persistent data:

| Volume | Purpose | Required |
|--------|---------|----------|
| `/etc/meshview` | Configuration files | Yes |
| `/var/lib/meshview` | Database storage | Recommended |
| `/var/log/meshview` | Log files | Optional |

### Configuration Volume

Mount a directory containing your `config.ini` file:

```bash
-v /path/to/your/config:/etc/meshview
```

If no config is provided, the container will use the default `sample.config.ini`.

### Database Volume

Mount a directory to persist the SQLite database:

```bash
-v /path/to/your/data:/var/lib/meshview
```

**Important:** Without this mount, your database will be lost when the container stops.

### Logs Volume

Mount a directory to access logs from the host:

```bash
-v /path/to/your/logs:/var/log/meshview
```

## Complete Example

Create a directory structure and run:

```bash
# Create directories
mkdir -p meshview/{config,data,logs,backups}

# Copy sample config (first time only)
docker run --rm ghcr.io/pablorevilla-meshtastic/meshview:latest \
  cat /etc/meshview/config.ini > meshview/config/config.ini

# Edit config.ini with your MQTT settings
nano meshview/config/config.ini

# Run the container
docker run -d \
  --name meshview \
  --restart unless-stopped \
  -p 8081:8081 \
  -v $(pwd)/meshview/config:/etc/meshview \
  -v $(pwd)/meshview/data:/var/lib/meshview \
  -v $(pwd)/meshview/logs:/var/log/meshview \
  ghcr.io/pablorevilla-meshtastic/meshview:latest
```

## Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  meshview:
    image: ghcr.io/pablorevilla-meshtastic/meshview:latest
    container_name: meshview
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - ./config:/etc/meshview
      - ./data:/var/lib/meshview
      - ./logs:/var/log/meshview
      - ./backups:/var/lib/meshview/backups  # For database backups
    environment:
      - TZ=America/Los_Angeles  # Set your timezone
```

Run with:

```bash
docker-compose up -d
```

## Configuration

### Minimum Configuration

Edit your `config.ini` to configure MQTT connection:

```ini
[mqtt]
server = mqtt.meshtastic.org
topics = ["msh/US/#"]
port = 1883
username =
password =

[database]
connection_string = sqlite+aiosqlite:///var/lib/meshview/packets.db
```

### Database Backups

To enable automatic daily backups inside the container:

```ini
[cleanup]
backup_enabled = True
backup_dir = /var/lib/meshview/backups
backup_hour = 2
backup_minute = 00
```

Then mount the backups directory:

```bash
-v $(pwd)/meshview/backups:/var/lib/meshview/backups
```

## Available Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest build from the main branch |
| `dev-v3` | Development branch |
| `v1.2.3` | Specific version tags |

## Updating

Pull the latest image and restart:

```bash
docker pull ghcr.io/pablorevilla-meshtastic/meshview:latest
docker restart meshview
```

Or with docker-compose:

```bash
docker-compose pull
docker-compose up -d
```

## Logs

View container logs:

```bash
docker logs meshview

# Follow logs
docker logs -f meshview

# Last 100 lines
docker logs --tail 100 meshview
```

## Troubleshooting

### Container won't start

Check logs:
```bash
docker logs meshview
```

### Database permission issues

Ensure the data directory is writable:
```bash
chmod -R 755 meshview/data
```

### Can't connect to MQTT

1. Check your MQTT configuration in `config.ini`
2. Verify network connectivity from the container:
   ```bash
   docker exec meshview ping mqtt.meshtastic.org
   ```

### Port already in use

Change the host port (left side):
```bash
-p 8082:8081
```

Then access at: http://localhost:8082

## Building Your Own Image

If you want to build from source:

```bash
git clone https://github.com/pablorevilla-meshtastic/meshview.git
cd meshview
docker build -f Containerfile -t meshview:local .
```

## Security Notes

- The container runs as a non-root user (`app`, UID 10001)
- No privileged access required
- Only port 8081 is exposed
- All data stored in mounted volumes

## Support

- GitHub Issues: https://github.com/pablorevilla-meshtastic/meshview/issues
- Documentation: https://github.com/pablorevilla-meshtastic/meshview
