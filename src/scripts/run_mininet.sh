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

# CLEANUP: Kill any remaining Mininet processes (but be more selective)
echo "Cleaning up Mininet processes..."
sudo pkill -f "python.*mininet" 2>/dev/null || true

# CLEANUP: Remove any stale OVS bridges (but preserve system bridges)
echo "Cleaning up Open vSwitch bridges..."
for bridge in $(sudo ovs-vsctl list-br 2>/dev/null | grep -E '^s[0-9]+$'); do
    sudo ovs-vsctl del-br "$bridge" 2>/dev/null || true
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

# Detect available terminal emulator
TERMINAL_CMD=""
if command -v gnome-terminal &> /dev/null; then
    TERMINAL_CMD="gnome-terminal --"
elif command -v xterm &> /dev/null; then
    TERMINAL_CMD="xterm -e"
elif command -v konsole &> /dev/null; then
    TERMINAL_CMD="konsole -e"
elif command -v mate-terminal &> /dev/null; then
    TERMINAL_CMD="mate-terminal --"
else
    echo "Warning: No terminal emulator found. Running in current terminal..."
    TERMINAL_CMD=""
fi

echo "Using terminal: $TERMINAL_CMD"
echo "PYTHONPATH: $PYTHONPATH"

# Run Mininet in a new terminal if available, otherwise in current terminal
if [ -n "$TERMINAL_CMD" ]; then
    echo "Opening new terminal for Mininet..."
    $TERMINAL_CMD bash -c "
        cd $(pwd)
        source venv/bin/activate
        export PYTHONPATH=\$(pwd):\$PYTHONPATH
        echo '=========================================='
        echo 'Mininet Terminal Started'
        echo '=========================================='
        echo 'Current directory: \$(pwd)'
        echo 'PYTHONPATH: \$PYTHONPATH'
        echo 'Python version: \$(python3 --version)'
        echo 'Starting Mininet Topology...'
        echo '=========================================='
        
        # Test the import first
        python3 -c 'import sys; sys.path.insert(0, \".\"); from src.topologies.linear_topology import LinearTopology; print(\"✅ Import successful\")'
        
        if [ \$? -eq 0 ]; then
            echo 'Imports OK, starting topology...'
            sudo -E env PATH=\$PATH PYTHONPATH=\$PYTHONPATH python3 src/topologies/linear_topology.py 3
        else
            echo '❌ Import failed. Check the error above.'
        fi
        
        echo '=========================================='
        echo 'Press Enter to close this terminal...'
        read
    " &
else
    echo "Running Mininet in current terminal..."
    echo "=========================================="
    echo "Current directory: $(pwd)"
    echo "PYTHONPATH: $PYTHONPATH"
    echo "Python version: $(python3 --version)"
    echo "Starting Mininet Topology..."
    echo "=========================================="
    
    # Test the import first
    python3 -c 'import sys; sys.path.insert(0, "."); from src.topologies.linear_topology import LinearTopology; print("✅ Import successful")'
    
    if [ $? -eq 0 ]; then
        echo "Imports OK, starting topology..."
        sudo -E env PATH=$PATH PYTHONPATH=$PYTHONPATH python3 src/topologies/linear_topology.py 3
    else
        echo "❌ Import failed. Check the error above."
        exit 1
    fi
fi

echo "Mininet process initiated..."
echo "Check the terminal window for topology output" 