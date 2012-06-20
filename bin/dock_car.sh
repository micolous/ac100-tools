#!/bin/sh
ME="michael"

# wait for usb devices to settle
sleep 5s

# start up music
sudo -u $ME mocp -U

# start up gps
service gpsd start

# start up bbmop
DISPLAY=:0 sudo -u $ME bbmop.py &

