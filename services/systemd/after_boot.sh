#!/bin/sh -e

# start DHC for SIM7600L
sudo dhclient -v usb0

# Restart Docker Containers
docker stop $(docker ps -a -q)
docker run -d -p 8000:8000 --privileged shifi23/car-interface:latest
