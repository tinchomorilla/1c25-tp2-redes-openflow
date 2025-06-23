#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Check if Mininet is installed
if ! command -v mn &> /dev/null; then
    echo "Error: Mininet is not installed. Please install Mininet first:"
    echo "  sudo apt-get install mininet"
    exit 1
fi

# Check if Open vSwitch is running
if ! sudo service openvswitch-switch status > /dev/null 2>&1; then
    echo "Starting Open vSwitch service..."
    sudo service openvswitch-switch start
fi

# Clean up any existing network interfaces
echo "Cleaning up existing network interfaces..."
sudo mn -c > /dev/null 2>&1

# Activate virtual environment
source venv/bin/activate

# Run Mininet in a new terminal with proper environment
gnome-terminal -- bash -c "
    cd $(pwd)
    source venv/bin/activate
    export PYTHONPATH=\$(pwd)/src:\$PYTHONPATH
    echo 'Starting Mininet Topology...'
    sudo -E python3 src/topologies/linear_topology.py 3
    exec bash
" 