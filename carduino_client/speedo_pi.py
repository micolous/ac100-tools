#!/usr/bin/env python

#import gps
from time import sleep
import dbus
from datetime import datetime
import dateutil.parser
from dateutil.tz import tzlocal
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
import gobject
from tm1640 import TM1640, INVERT_MODE_VERTICAL

tzlocal = tzlocal()

display = TM1640()
display.on()
display.clear()

bus = dbus.SystemBus()

#carduino = bus.get_object('au.id.micolous.carduino.CarduinoService', '/')
#iface = dbus.Interface(carduino, dbus_interface='au.id.micolous.carduino.CarduinoInterface')
gpsd = bus.get_object('au.id.micolous.carduino.GpsdService', '/')
g_iface = dbus.Interface(gpsd, dbus_interface='au.id.micolous.carduino.GpsdInterface')

#power = bus.get_object('org.freedesktop.UPower', '/org/freedesktop/UPower/devices/line_power_ac')
#p_iface = dbus.Interface(power, dbus_interface='org.freedesktop.UPower.Device')
#p_get_property = lambda x: power.Get('org.freedesktop.UPower.Device', x, dbus_interface='org.freedesktop.DBus.Properties')

TEMPERATURE = 0.
LAT = LONG = SPEED = COURSE = 0.

def on_temperature(temperature, sender=None):
	global TEMPERATURE
	
	# FIXME: handle negative temperatures properly
	# FIXME: summer
	TEMPERATURE = abs(temperature)

SHOW_CLOCK_DOT = False
POWER_STATE = True

def on_power_changed(sender=None):
	global POWER_STATE
	POWER_STATE = True #bool(p_get_property('Online'))

def on_location(dt, lat, lng, speed, course, variation, sender=None):
	global LAT, LONG, SPEED, BEARING, SHOW_CLOCK_DOT, POWER_STATE
	
	now = dateutil.parser.parse(dt).astimezone(tzlocal)
	
	if now.microsecond == 0:
		# whole second, toggle the dot and hide the display if there's no power
		#SHOW_CLOCK_DOT = not SHOW_CLOCK_DOT
		if not POWER_STATE:
			# no mains power, hide display
			#iface.seven_writestr_mirror(' ' * 16)
			return

	if now.microsecond == 0 and now.second == 0:
		# reset display if it loses connection / sync
		display.on()


	# don't write anything if there was no power on the last whole second
	if not POWER_STATE:
		return

	#if 'speed' in report:
	if lat and long:
		# convert speed from m/s to km/h
		# speed *= 3.6 # 3600 / 1000
		
		if course <= 22.5:
			d = 'N '
		elif 22.5 <= course <= 67.5:
			d = 'NE'
		elif 67.5 <= course <= 112.5:
			d = 'E '
		elif 112.5 <= course <= 157.5:
			d = 'SE'
		elif 157.5 <= course <= 202.5:
			d = 'S '
		elif 202.5 <= course <= 247.5:
			d = 'SW'
		elif 247.5 <= course <= 292.5:
			d = 'W '
		elif 292.5 <= course <= 337.5:
			d = 'NW'
		else:
			d = 'N '
		
		
		m = '%02d%02d      %03.0f %s' % (now.hour, now.minute, speed, d)
	else:
		m = '%02d%02d           ' % (now.hour, now.minute)
	
	
	print "sending to screen..."
	#d = '%02.2f  %03.2f' % (report['lat'], report['lon'])
	
	m += (16 - len(m)) * ' '
	print m
	display.write(m, invert_mode=INVERT_MODE_VERTICAL)
	#system('tm1640 write \'%s\'' % m)
	#iface.seven_writestr_mirror(m)


#iface.connect_to_signal(
#	'on_temperature',
#	on_temperature,
#	sender_keyword='sender'
#)


g_iface.connect_to_signal(
	'on_location', 
	on_location,
	sender_keyword='sender'
)


#p_iface.connect_to_signal(
#	'Changed',
#	on_power_changed,
#	sender_keyword='sender'
#)

#gps_s = gps.gps(host='localhost', port='2947')
#gps_s.stream(flags=gps.WATCH_JSON)

on_power_changed()

loop = gobject.MainLoop()
#context = loop.get_context()

loop.run()
#$while 1:
#SHOW_CLOCK_DOT = True
#for report in gps_s:
#while 1:
#	# take this chance to pump gobject
#	#context.iteration(False)
#	
#	if report['class'] != 'TPV':
#		continue
#		
#	SHOW_CLOCK_DOT = not SHOW_CLOCK_DOT
#	print repr(report)
#	
#	now = datetime.now()
#	
