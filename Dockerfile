FROM python:3-slim

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y graphviz && \
    rm -rf /var/lib/apt/lists/*

# set the work dir
WORKDIR /opt/meshview

# Set environment variables
ENV VIRTUAL_ENV=/opt/meshview/env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create and activate virtual environment
RUN python3 -m venv $VIRTUAL_ENV
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8081

# Command to run the application using mvrun.py
CMD ["python", "mvrun.py"]
