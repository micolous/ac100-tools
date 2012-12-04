#!/usr/bin/env python

import Geoclue
from time import sleep
import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

bus = dbus.SystemBus()

carduino = bus.get_object('au.id.micolous.carduino.CarduinoService', '/')
iface = dbus.Interface(carduino, dbus_interface='au.id.micolous.carduino.CarduinoInterface')

while 1:
	print "getting position..."
	location = Geoclue.DiscoverLocation()
	location.init()
	position = location.get_location_info()
	
	print "sending to screen..."
	d = '%02.2f  %03.2f' % (position['latitude'], position['longitude'])
	d += (16 - len(d)) * ' '
	print d
	iface.seven_writestr_mirror(d)
	
	print "napping..."
	sleep(1.)
