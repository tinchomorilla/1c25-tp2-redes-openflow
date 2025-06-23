#!/bin/bash

echo "=========================================="
echo "Setting up SDN Project Environment"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Clone POX if it doesn't exist
if [ ! -d "pox" ]; then
    echo "Cloning POX controller..."
    git clone https://github.com/noxrepo/pox.git pox
else
    echo "POX already exists."
fi

# Copy controller files to POX directory
echo "Setting up POX controller files..."
mkdir -p pox/pox/custom
cp src/controller/*.py pox/pox/custom/
cp src/controller/rules.json pox/pox/custom/

# Check if Mininet is installed
if ! command -v mn &> /dev/null; then
    echo "=========================================="
    echo "WARNING: Mininet is not installed."
    echo "Please install Mininet manually:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install mininet"
    echo "  OR"
    echo "  git clone https://github.com/mininet/mininet.git"
    echo "  cd mininet && sudo ./util/install.sh -a"
    echo "=========================================="
else
    echo "Mininet is already installed."
fi

# Check if Open vSwitch is installed
if ! command -v ovs-vsctl &> /dev/null; then
    echo "=========================================="
    echo "WARNING: Open vSwitch is not installed."
    echo "Please install Open vSwitch manually:"
    echo "  sudo apt-get install openvswitch-switch"
    echo "=========================================="
else
    echo "Open vSwitch is already installed."
fi

echo "=========================================="
echo "Setup complete!"
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo "==========================================" 