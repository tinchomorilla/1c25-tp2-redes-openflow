#!/bin/bash

# Build the POX service
sudo docker-compose build pox

# Run POX container in a new terminal with proper environment
gnome-terminal -- bash -c "cd $(pwd) && sudo docker-compose up pox; exec bash"