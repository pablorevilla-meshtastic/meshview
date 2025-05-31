# MeshView Docker Container

This Dockerfile builds a containerized version of the [MeshView](https://github.com/pablorevilla-meshtastic/meshview) application. It uses a lightweight Python environment and sets up the required virtual environment as expected by the application.

## Image Details

- **Base Image**: `python:3.12-slim`
- **Working Directory**: `/app`
- **Python Virtual Environment**: `/app/env`
- **Exposed Port**: `8081`

## Build Instructions

Build the Docker image:

```bash
docker build -t meshview-docker .
```

## Run Instructions

Copy the example configuration and modify:

```bash
# Copy the sample from this repository
cp sample.config.ini config.ini
# Modify with your text editor of choice
nano config.ini
```

Run the container:

```bash
docker run -d --name meshview-docker -v ./config.ini:/etc/meshview/config.ini -p 8081:8081 meshview-docker
```

This maps container port `8081` to your host, and uses the locally stored configuration you modified in the previous step.

The application runs via:

```bash
/app/env/bin/python /app/mvrun.py
```

## Web Interface

Once the container is running, you can access the MeshView web interface by visiting:

http://localhost:8081

If running on a remote server, replace `localhost` with the host's IP or domain name:

http://<host>:8081

Ensure that port `8081` is open and not blocked by a firewall or security group.

## Run with docker-compose

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` to point to your local `config.ini` and `packets.db` files.

Create `packets.db` file if it does not exist, before passing to the container.
```bash
touch ./packets.db
```
### Start compose

From the location where `meshview` was cloned.
Start compose in the background:
```bash
docker compose up -d
```
