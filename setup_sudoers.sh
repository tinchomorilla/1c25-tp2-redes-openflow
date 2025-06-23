#!/bin/bash

echo "=========================================="
echo "Configuring Sudoers for Mininet"
echo "=========================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please run this script as regular user, not root"
    exit 1
fi

# Create sudoers file for mininet
SUDOERS_FILE="/etc/sudoers.d/mininet-$USER"

echo "Creating sudoers configuration..."
echo "This will allow running Mininet commands without password prompts"

# Create the sudoers content
sudo tee "$SUDOERS_FILE" > /dev/null << EOF
# Allow $USER to run Mininet and network commands without password
$USER ALL=(ALL) NOPASSWD: /usr/bin/mn
$USER ALL=(ALL) NOPASSWD: /usr/bin/ovs-*
$USER ALL=(ALL) NOPASSWD: /usr/sbin/service openvswitch-switch *
$USER ALL=(ALL) NOPASSWD: /usr/bin/pkill
$USER ALL=(ALL) NOPASSWD: /usr/bin/fuser
$USER ALL=(ALL) NOPASSWD: /sbin/ip
$USER ALL=(ALL) NOPASSWD: /bin/kill
EOF

# Set proper permissions
sudo chmod 440 "$SUDOERS_FILE"

# Validate the sudoers file
if sudo visudo -c -f "$SUDOERS_FILE"; then
    echo "✅ Sudoers configuration created successfully!"
    echo "✅ File: $SUDOERS_FILE"
    echo "✅ You should no longer be prompted for passwords when running Mininet"
else
    echo "❌ Error in sudoers configuration. Removing file..."
    sudo rm -f "$SUDOERS_FILE"
    exit 1
fi

echo "=========================================="
echo "Configuration complete!"
echo "You can now run Mininet scripts without password prompts"
echo "==========================================" 