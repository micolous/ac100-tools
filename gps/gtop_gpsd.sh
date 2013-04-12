#!/bin/sh

# Init gtop gps.  This defaults to 38400 baud / 10Hz target.
# Despite suggestions to the contrary, gpsd will pass on >1Hz report
# frequency.
python2 gtop_gps_init.py -d /dev/ttyAMA0

# Fix permissions on serial device so gpsd can read it only.
chmod 664 /dev/ttyAMA0

# gpsd doesn't seem to start up reliably as root, as we don't want it to send
# anything to the gps so do the user switching for it.
#
# Also make it constantly run and don't wait for a client, and don't fork,
# because we're going to run it in systemd.
sudo -u nobody gpsd -b -n -N /dev/ttyAMA0
