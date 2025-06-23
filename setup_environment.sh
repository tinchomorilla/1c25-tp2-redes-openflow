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

# Check if Python 2.7 is installed (needed for POX)
if ! command -v python2.7 &> /dev/null && ! command -v python2 &> /dev/null; then
    echo "=========================================="
    echo "WARNING: Python 2.7 is not installed."
    echo "POX works best with Python 2.7. To install:"
    echo "  sudo apt-get install python2.7 python2.7-dev"
    echo "  Or:"
    echo "  sudo apt-get install python2 python2-dev"
    echo "Continuing with Python 3 (may show warnings)"
    echo "=========================================="
else
    echo "Python 2.7 found - excellent for POX compatibility!"
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
    echo "POX already exists. Updating..."
    cd pox && git pull && cd ..
fi

# Copy controller files to POX directory
echo "Setting up POX controller files..."
mkdir -p pox/pox/custom
cp src/controller/*.py pox/pox/custom/
cp src/controller/rules.json pox/pox/custom/

# Create __init__.py file in custom directory to make it a Python module
echo "Creating __init__.py for custom module..."
touch pox/pox/custom/__init__.py

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

# Setup sudoers for Mininet (optional, reduces password prompts)
echo "=========================================="
echo "OPTIONAL: To avoid password prompts for Mininet commands,"
echo "you can add these lines to /etc/sudoers (run 'sudo visudo'):"
echo ""
echo "# Allow mininet commands without password"
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/mn"
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/ovs-*"
echo "$USER ALL=(ALL) NOPASSWD: /usr/sbin/service openvswitch-switch *"
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/pkill"
echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/fuser"
echo "$USER ALL=(ALL) NOPASSWD: /sbin/ip"
echo "=========================================="

echo "=========================================="
echo "Setup complete!"
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo "==========================================" 