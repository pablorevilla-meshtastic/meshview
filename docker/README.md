# MeshView Docker Container

> **Note:** This directory contains legacy Docker build files.
>
> **For current Docker usage instructions, please see [README-Docker.md](../README-Docker.md) in the project root.**

## Current Approach

Pre-built container images are automatically built and published to GitHub Container Registry:

```bash
docker pull ghcr.io/pablorevilla-meshtastic/meshview:latest
```

See **[README-Docker.md](../README-Docker.md)** for:
- Quick start instructions
- Volume mount configuration
- Docker Compose examples
- Backup configuration
- Troubleshooting

## Legacy Build (Not Recommended)

If you need to build your own image for development:

```bash
# From project root
docker build -f Containerfile -t meshview:local .
```

The current Containerfile uses:
- **Base Image**: `python:3.13-slim` (Debian-based)
- **Build tool**: `uv` for fast dependency installation
- **User**: Non-root user `app` (UID 10001)
- **Exposed Port**: `8081`
- **Volumes**: `/etc/meshview`, `/var/lib/meshview`, `/var/log/meshview`
