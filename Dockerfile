FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget git graphviz && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV PATH="/opt/conda/bin:$PATH"
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /miniconda.sh && \
    bash /miniconda.sh -b -p /opt/conda && \
    rm /miniconda.sh

# Set work directory
WORKDIR /app

# Be sure to have done git submodule update --init --recursive
COPY . ./

# Create conda environment
RUN conda create -n meshview python=3.11 -y

# Activate environment and install dependencies
RUN /opt/conda/envs/meshview/bin/pip install -r /app/requirements.txt

#place sample config in place
RUN cp /app/sample.config.ini /app/config.ini

#change default to 8082
RUN sed -ie 's/port = 8081/port = 8082/g' /app/config.ini

# Expose the web server port
EXPOSE 8082

# Start the application using the conda environment
CMD ["/app/start.sh"]