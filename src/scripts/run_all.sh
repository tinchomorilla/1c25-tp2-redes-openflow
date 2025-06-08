#!/bin/bash

# Start the controller in a new terminal
gnome-terminal -- bash -c "python3 src/pox/pox.py log.level --DEBUG controller.learning_switch; exec bash"

# Wait for the controller to initialize
echo "Waiting for controller to initialize..."
sleep 5

# Start the topology in another terminal
gnome-terminal -- bash -c "sudo python3 src/topologies/linear_topology.py 3; exec bash" 