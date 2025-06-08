#!/bin/bash

# Clean up any existing network interfaces
ip link show | grep -o 's[0-9]-eth[0-9]' | while read interface; do
    ip link del $interface 2>/dev/null || true
done

# Start Open vSwitch service
service openvswitch-switch start

# Execute the command passed to docker run
exec "$@" 