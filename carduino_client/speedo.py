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

TEMPERATURE = 0.

def on_temperature(temperature, sender=None):
	global TEMPERATURE
	TEMPERATURE = temperature

iface.connect_to_signal(
	'on_temperature',
	on_temperature,
	sender_keyword='sender'
)


gps_s = gps.gps(host='localhost', port='2947')
gps_s.stream(flags=gps.WATCH_JSON)



#$while 1:
show_clock_dot = True
for report in gps_s:
	if report['class'] != 'TPV':
		continue
		
	show_clock_dot = not show_clock_dot
	print repr(report)
	
	now = datetime.now()
	if 'speed' in report:
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
			
		m = '%02d%s%02d %02.0f %03.0f %s' % (now.hour, ('.' if show_clock_dot else ''), now.minute, TEMPERATURE, speed, d)
	else:
		m = '%02d%s%02d %02.0f        ' % (now.hour, ('.' if show_clock_dot else ''), now.minute, TEMPERATURE)
	
	
	print "sending to screen..."
	#d = '%02.2f  %03.2f' % (report['lat'], report['lon'])
	
	m += (16 - len(m)) * ' '
	print m
	iface.seven_writestr_mirror(m)
	
