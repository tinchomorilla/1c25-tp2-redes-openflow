#!/bin/bash

# Build the Mininet service
sudo docker-compose build mininet

# Run Mininet container in a new terminal with proper environment
# Using the container name 'sdn-project-mininet' as defined in docker-compose.yml
gnome-terminal -- bash -c "cd $(pwd) && sudo docker-compose run --rm --name sdn-project-mininet -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -e PYTHONPATH=/app/src mininet; exec bash" 