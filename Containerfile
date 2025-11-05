# Build Image
# Uses python:3.13-slim because no native dependencies are needed for meshview itself
# (everything is available as a wheel)

FROM docker.io/python:3.13-slim AS meshview-build
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl patch && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user/group
ARG APP_USER=app
RUN useradd -m -u 10001 -s /bin/bash ${APP_USER}

# Install uv and put it on PATH system-wide
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
 && install -m 0755 /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app
RUN chown -R ${APP_USER}:${APP_USER} /app

# Copy deps first for caching
COPY --chown=${APP_USER}:${APP_USER} pyproject.toml uv.lock* requirements*.txt ./

# Optional: wheels-only to avoid slow source builds
ENV UV_NO_BUILD=1
RUN uv venv /opt/venv
# RUN uv sync --frozen
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN uv pip install --no-cache-dir --upgrade pip \
 && if [ -f requirements.txt ]; then uv pip install --only-binary=:all: -r requirements.txt; fi

# Copy app code
COPY --chown=${APP_USER}:${APP_USER} . .

# Created working directories with correct ownership/permissions
RUN mkdir -p /etc/meshview /var/lib/meshview /var/log/meshview \
 && chown -R ${APP_USER}:${APP_USER} /etc/meshview /var/lib/meshview /var/log/meshview

RUN patch sample.config.ini  < container/config.patch
RUN cp sample.config.ini /etc/meshview/config.ini
RUN chown ${APP_USER}:${APP_USER} /etc/meshview/config.ini

# Drop privileges
USER ${APP_USER}

ENTRYPOINT [ "uv", "run", "--active", "mvrun.py"]
CMD ["--pid_dir", "/tmp", "--py_exec", "/opt/venv/bin/python", "--config", "/etc/meshview/config.ini" ]

EXPOSE 8081
VOLUME [ "/etc/meshview", "/var/lib/meshview", "/var/log/meshview" ]

