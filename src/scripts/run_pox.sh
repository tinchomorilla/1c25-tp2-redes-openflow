#!/bin/bash

echo "=========================================="
echo "Starting POX Controller with Cleanup"
echo "=========================================="

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

# CLEANUP: Kill any existing POX processes
echo "Cleaning up existing POX processes..."
pkill -f "pox.py" 2>/dev/null || true
pkill -f "python.*pox" 2>/dev/null || true

# CLEANUP: Kill processes using port 6633 (OpenFlow default port)
echo "Freeing up port 6633..."
sudo fuser -k 6633/tcp 2>/dev/null || true

# Wait a moment for cleanup to complete
sleep 2

# Check if Python 2.7 is available
if command -v python2.7 &> /dev/null; then
    PYTHON_CMD="python2.7"
elif command -v python2 &> /dev/null; then
    PYTHON_CMD="python2"
else
    echo "Warning: Python 2.7 not found, using python3 (may cause warnings)"
    PYTHON_CMD="python3"
fi

echo "Using Python: $PYTHON_CMD"

# Activate virtual environment
source venv/bin/activate

# Run POX controller in a new terminal with proper environment
gnome-terminal -- bash -c "
    cd $(pwd)
    source venv/bin/activate
    echo 'Starting POX Controller with $PYTHON_CMD...'
    $PYTHON_CMD pox/pox.py log.level --DEBUG custom.main --rules_path=pox/pox/custom/rules.json
    exec bash
"

echo "POX Controller starting..."
echo "Check the new terminal window for controller output"