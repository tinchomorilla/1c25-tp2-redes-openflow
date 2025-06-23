#!/bin/bash

echo "Starting Mininet Topology..."

# Basic cleanup
sudo mn -c > /dev/null 2>&1

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH 
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run the main topology script
sudo -E env PATH=$PATH PYTHONPATH=$PYTHONPATH python3 src/topologies/main.py 3 