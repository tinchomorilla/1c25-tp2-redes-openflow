#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Check if POX exists
if [ ! -d "pox" ]; then
    echo "Error: POX not found. Please run setup_environment.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run POX controller in a new terminal with proper environment
gnome-terminal -- bash -c "
    cd $(pwd)
    source venv/bin/activate
    echo 'Starting POX Controller...'
    python3 pox/pox.py log.level --DEBUG custom.main --rules_path=pox/pox/custom/rules.json
    exec bash
"