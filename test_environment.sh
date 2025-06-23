#!/bin/bash

echo "=========================================="
echo "Testing SDN Project Environment"
echo "=========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test 1: Check virtual environment
echo "1. Checking virtual environment..."
if [ -d "venv" ]; then
    print_status 0 "Virtual environment exists"
    source venv/bin/activate
    print_status 0 "Virtual environment activated"
else
    print_status 1 "Virtual environment NOT found - run ./setup_environment.sh"
    exit 1
fi

# Test 2: Check Python versions
echo ""
echo "2. Checking Python versions..."
if command -v python3 &> /dev/null; then
    PYTHON3_VERSION=$(python3 --version)
    print_status 0 "Python 3: $PYTHON3_VERSION"
else
    print_status 1 "Python 3 not found"
fi

if command -v python2.7 &> /dev/null; then
    PYTHON27_VERSION=$(python2.7 --version 2>&1)
    print_status 0 "Python 2.7: $PYTHON27_VERSION"
elif command -v python2 &> /dev/null; then
    PYTHON2_VERSION=$(python2 --version 2>&1)
    print_status 0 "Python 2: $PYTHON2_VERSION"
else
    print_warning "Python 2.7 not found - POX will show version warnings"
fi

# Test 3: Check system dependencies
echo ""
echo "3. Checking system dependencies..."
command -v mn &> /dev/null
print_status $? "Mininet"

command -v ovs-vsctl &> /dev/null
print_status $? "Open vSwitch"

sudo service openvswitch-switch status > /dev/null 2>&1
print_status $? "Open vSwitch service running"

command -v git &> /dev/null
print_status $? "Git"

# Test 4: Check POX installation
echo ""
echo "4. Checking POX installation..."
if [ -d "pox" ]; then
    print_status 0 "POX directory exists"
    if [ -f "pox/pox.py" ]; then
        print_status 0 "POX main file exists"
    else
        print_status 1 "POX main file missing"
    fi
    
    if [ -d "pox/pox/custom" ]; then
        print_status 0 "POX custom directory exists"
        if [ -f "pox/pox/custom/__init__.py" ]; then
            print_status 0 "POX custom __init__.py exists"
        else
            print_status 1 "POX custom __init__.py missing"
        fi
    else
        print_status 1 "POX custom directory missing"
    fi
else
    print_status 1 "POX not found - run ./setup_environment.sh"
fi

# Test 5: Check terminal emulators
echo ""
echo "5. Checking available terminal emulators..."
if command -v gnome-terminal &> /dev/null; then
    print_status 0 "gnome-terminal"
elif command -v xterm &> /dev/null; then
    print_status 0 "xterm"
elif command -v konsole &> /dev/null; then
    print_status 0 "konsole"
elif command -v mate-terminal &> /dev/null; then
    print_status 0 "mate-terminal"
else
    print_warning "No terminal emulator found - scripts will run in current terminal"
fi

# Test 6: Check Python imports
echo ""
echo "6. Testing Python imports..."
export PYTHONPATH="$(pwd):$PYTHONPATH"

python3 -c "import sys; sys.path.insert(0, '.'); from src.topologies.linear_topology import LinearTopology; print('✅ LinearTopology import successful')" 2>/dev/null
print_status $? "LinearTopology import"

python3 -c "import sys; sys.path.insert(0, '.'); from src.utils.logger import setup_logger; print('✅ Logger import successful')" 2>/dev/null
print_status $? "Logger import"

# Test 7: Check script permissions
echo ""
echo "7. Checking script permissions..."
[ -x "setup_environment.sh" ]
print_status $? "setup_environment.sh executable"

[ -x "setup_sudoers.sh" ]
print_status $? "setup_sudoers.sh executable"

[ -x "src/scripts/run_all.sh" ]
print_status $? "run_all.sh executable"

[ -x "src/scripts/run_pox.sh" ]
print_status $? "run_pox.sh executable"

[ -x "src/scripts/run_mininet.sh" ]
print_status $? "run_mininet.sh executable"

# Test 8: Check sudoers configuration (if exists)
echo ""
echo "8. Checking sudoers configuration..."
if [ -f "/etc/sudoers.d/mininet-$USER" ]; then
    print_status 0 "Sudoers file exists - no password prompts expected"
else
    print_warning "Sudoers not configured - you may be prompted for passwords"
    echo "   Run: ./setup_sudoers.sh to configure"
fi

echo ""
echo "=========================================="
echo "Environment Test Complete"
echo "=========================================="

# Final recommendation
echo ""
echo "📋 Next steps:"
echo "1. If any tests failed, run: ./setup_environment.sh"
echo "2. For no password prompts, run: ./setup_sudoers.sh"  
echo "3. To start the project, run: ./src/scripts/run_all.sh"
echo "4. Install Python 2.7 to eliminate POX warnings:"
echo "   sudo apt-get install python2.7 python2.7-dev" 