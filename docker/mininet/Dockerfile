FROM sdn-project-base:latest

# Install git and other build dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    iputils-ping \
    python \
    python3 \
    iperf \
    x11-apps \
    x11-utils \
    x11-xserver-utils \
    xterm \
    && rm -rf /var/lib/apt/lists/*

# Clone and install Mininet with all dependencies
RUN git clone https://github.com/mininet/mininet.git && \
    cd mininet && \
    ./util/install.sh -a

# Copy the entire project
COPY . /app

# Copy and set up entrypoint script
COPY docker/mininet/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the working directory
WORKDIR /app

# Add the project root to Python path
ENV PYTHONPATH=/app/src

# Configure X11
ENV DISPLAY=:0
ENV XAUTHORITY=/root/.Xauthority

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Set the command to run the linear topology with Python 2
CMD ["python2", "-m", "src.topologies.main"]
