FROM python:3.11-slim-bookworm

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app
# Copy project to the build context
COPY . ./

# Create a virtual environment
# and install Python dependencies
RUN python3 -m venv env \
    && ./env/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE ${CONTAINER_WEB_PORT:-8081}

# Config file should be mounted at /etc/meshview/config.ini
VOLUME ["/etc/meshview"]

CMD ["./env/bin/python", "mvrun.py", "--config", "/etc/meshview/config.ini"]
