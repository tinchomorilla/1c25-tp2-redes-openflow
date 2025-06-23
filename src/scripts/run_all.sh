#!/bin/bash

echo "=========================================="
echo "Starting SDN Project with Full Cleanup"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup_environment.sh first."
    exit 1
fi

# Global cleanup first
echo "Performing global cleanup..."

# Kill any existing POX processes
pkill -f "pox.py" 2>/dev/null || true
pkill -f "python.*pox" 2>/dev/null || true

# Clean Mininet
sudo mn -c 2>/dev/null || true

# Kill Mininet processes
sudo pkill -f mininet 2>/dev/null || true
sudo pkill -f "python.*mininet" 2>/dev/null || true

# Free up OpenFlow port
sudo fuser -k 6633/tcp 2>/dev/null || true

# Wait for cleanup
sleep 3

# Start the POX controller in a new terminal
echo "Starting POX Controller..."
bash src/scripts/run_pox.sh

# Wait for the controller to initialize
echo "Waiting for controller to initialize..."
sleep 8

# Start Mininet topology in another terminal
echo "Starting Mininet Topology..."
bash src/scripts/run_mininet.sh

echo "=========================================="
echo "Both controller and topology are starting"
echo "Check the individual terminals for output"
echo ""
echo "Troubleshooting tips:"
echo "- If POX shows Python version warnings, install Python 2.7"
echo "- If Mininet asks for password, run: chmod +x setup_sudoers.sh && ./setup_sudoers.sh"
echo "- If import errors occur, make sure PYTHONPATH is set correctly"
echo "==========================================" 