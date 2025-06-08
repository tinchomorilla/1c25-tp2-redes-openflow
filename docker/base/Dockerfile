FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install common dependencies
RUN apt-get update && apt-get install -y \
    python2 \
    python2.7 \
    python2.7-dev \
    python3-pip \
    git \
    sudo \
    curl \
    x11-apps \
    xterm \
    gnome-terminal \
    dbus \
    dbus-x11 \
    at-spi2-core \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libdconf1 \
    libatk-adaptor \
    libatk-bridge2.0-dev \
    libatspi2.0-dev \
    # Mininet dependencies
    socat \
    iperf \
    telnet \
    ethtool \
    help2man \
    pyflakes3 \
    pylint \
    pep8 \
    net-tools \
    python-pexpect \
    python-tk \
    openssh-client \
    psmisc \
    iproute2 \
    cgroup-tools \
    && rm -rf /var/lib/apt/lists/*

# Install pip for Python 2
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
    python2 get-pip.py && \
    rm get-pip.py

# Set environment variables
ENV DISPLAY=:0
ENV NO_AT_BRIDGE=1
ENV DBUS_SESSION_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
ENV PYTHONPATH=/usr/local/lib/python2.7/dist-packages:/usr/local/lib/python2.7/site-packages

# Create startup script
RUN echo '#!/bin/bash\n\
    mkdir -p /var/run/dbus\n\
    dbus-daemon --system --fork\n\
    sleep 2\n\
    exec /bin/bash' > /start.sh && chmod +x /start.sh

# Set the working directory
WORKDIR /app 