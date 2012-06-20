#!/bin/sh
ME="michael"

# stop music playing
sudo -u $ME mocp -P

# kill any processes that might block sleep, or not wake properly
service gpsd stop
killall kismet_server

# kill bbmop.py
pkill -9 -f bbmop.py

# sleep laptop
pm-suspend
