#!/bin/bash

echo "=========================================="
echo "Starting Mininet with Cleanup"
echo "=========================================="

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

# CLEANUP: Clean up any existing Mininet processes and networks
echo "Cleaning up existing Mininet networks..."
sudo mn -c 2>/dev/null || true

# CLEANUP: Kill any remaining Mininet processes
echo "Cleaning up Mininet processes..."
sudo pkill -f mininet 2>/dev/null || true
sudo pkill -f "python.*mininet" 2>/dev/null || true

# CLEANUP: Remove any stale OVS bridges
echo "Cleaning up Open vSwitch bridges..."
for bridge in $(sudo ovs-vsctl list-br 2>/dev/null); do
    sudo ovs-vsctl del-br "$bridge" 2>/dev/null || true
done

# CLEANUP: Clean network namespaces
sudo ip netns list 2>/dev/null | while read ns; do
    sudo ip netns delete "$ns" 2>/dev/null || true
done

# Check if Open vSwitch is running
if ! sudo service openvswitch-switch status > /dev/null 2>&1; then
    echo "Starting Open vSwitch service..."
    sudo service openvswitch-switch start
fi

# Wait for cleanup to complete
sleep 2

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH to include the project root
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run Mininet in a new terminal with proper environment and no sudo password prompt
gnome-terminal -- bash -c "
    cd $(pwd)
    source venv/bin/activate
    export PYTHONPATH=\$(pwd):\$PYTHONPATH
    echo 'Starting Mininet Topology...'
    echo 'PYTHONPATH: \$PYTHONPATH'
    # Use sudo -E to preserve environment variables and avoid repeated password prompts
    sudo -E env PATH=\$PATH PYTHONPATH=\$PYTHONPATH python3 src/topologies/linear_topology.py 3
    exec bash
"

echo "Mininet starting..."
echo "Check the new terminal window for topology output" 