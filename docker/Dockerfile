FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies (graphviz required, git for cloning)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git graphviz && \
    rm -rf /var/lib/apt/lists/*

# Clone the repo with submodules
RUN git clone --recurse-submodules https://github.com/pablorevilla-meshtastic/meshview.git /app

# Create virtual environment
RUN python -m venv /app/env

# Upgrade pip and install requirements in venv
RUN /app/env/bin/pip install --no-cache-dir --upgrade pip && \
    /app/env/bin/pip install --no-cache-dir -r /app/requirements.txt

# Copy sample config
RUN cp /app/sample.config.ini /app/config.ini

# Expose port
EXPOSE 8081

# Config file should be mounted at /etc/meshview/config.ini
VOLUME ["/etc/meshview"]

# Run the app via venv
CMD ["/app/env/bin/python", "/app/mvrun.py", "--config", "/etc/meshview/config.ini"]
