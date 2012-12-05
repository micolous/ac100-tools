#!/usr/bin/env python

import gps
from time import sleep
import dbus
from datetime import datetime
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()

carduino = bus.get_object('au.id.micolous.carduino.CarduinoService', '/')
iface = dbus.Interface(carduino, dbus_interface='au.id.micolous.carduino.CarduinoInterface')
gps_s = gps.gps(host='localhost', port='2947')
gps_s.stream(flags=gps.WATCH_JSON)

#$while 1:
for report in gps_s:
	if report['class'] != 'TPV':
		continue
	print repr(report)
	
	# convert speed from m/s to km/h
	speed = report['speed'] * 3.6 # 3600 / 1000
	
	if report['track'] <= 22.5:
		d = 'N '
	elif 22.5 <= report['track'] <= 67.5:
		d = 'NE'
	elif 67.5 <= report['track'] <= 112.5:
		d = 'E '
	elif 112.5 <= report['track'] <= 157.5:
		d = 'SE'
	elif 157.5 <= report['track'] <= 202.5:
		d = 'S '
	elif 202.5 <= report['track'] <= 247.5:
		d = 'SW'
	elif 247.5 <= report['track'] <= 292.5:
		d = 'W '
	elif 292.5 <= report['track'] <= 337.5:
		d = 'NW'
	else:
		d = 'N '
		
	
	
	print "sending to screen..."
	#d = '%02.2f  %03.2f' % (report['lat'], report['lon'])
	now = datetime.now()
	d = '%02d%02d    %03.0f %s' % (now.hour, now.minute, speed, d)
	
	d += (16 - len(d)) * ' '
	print d
	iface.seven_writestr_mirror(d)
	
