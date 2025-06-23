#!/bin/bash

echo "=========================================="
echo "Starting SDN Project"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Start the POX controller in a new terminal
echo "Starting POX Controller..."
bash src/scripts/run_pox.sh

# Wait for the controller to initialize
echo "Waiting for controller to initialize..."
sleep 5

# Start Mininet topology in another terminal
echo "Starting Mininet Topology..."
bash src/scripts/run_mininet.sh

echo "=========================================="
echo "Both controller and topology are starting"
echo "Check the individual terminals for output"
echo "==========================================" 