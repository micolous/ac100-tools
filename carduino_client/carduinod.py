#!/usr/bin/env python

from carduino_protocol import CarduinoProtocol
from twisted.internet.error import ReactorAlreadyInstalledError
from twisted.internet import glib2reactor

# installing the glib2 reactor breaks sphinx autodoc
# this patches around the issue.
try:
	glib2reactor.install()
except ReactorAlreadyInstalledError:
	pass
	
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.serialport import SerialPort
from twisted.python import log
import sys
import dbus
import dbus.service
import gobject
from dbus.mainloop.glib import DBusGMainLoop
from argparse import ArgumentParser

DBUS_INTERFACE = 'au.id.micolous.carduino.CarduinoInterface'
DBUS_SERVICE = 'au.id.micolous.carduino.CarduinoService'
DBUS_PATH = '/'

class CarduinoService(dbus.service.Object):
	"""
	Carduino service object for DBus.
	"""
	
	def __init__(self, bus, protocol, object_path=DBUS_PATH):
		self.proto = protocol
		self.proto.dbus_api = self
		dbus.service.Object.__init__(self, bus, object_path)


	@dbus.service.method(dbus_interface=DBUS_INTERFACE, in_signature='s', out_signature='')
	def lcd_write(self, s):
		self.proto.lcd_write(s)
		
	@dbus.service.method(dbus_interface=DBUS_INTERFACE, in_signature='s', out_signature='')
	def seven_writestr(self, s):
		self.proto.seven_writestr(s)

	@dbus.service.method(dbus_interface=DBUS_INTERFACE, in_signature='s', out_signature='')
	def seven_writestr_mirror(self, s):
		self.proto.seven_writestr_mirror(s)

	
	
	


def boot_dbus():
	bus = dbus.SystemBus()
	name = dbus.service.BusName(DBUS_SERVICE, bus=bus)
	protocol = CarduinoProtocol()
	api = CarduinoService(name, protocol)
	
	SerialPort(protocol, '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AH00ZL76-if00-port0', reactor, baudrate=9600)

def main():
	DBusGMainLoop(set_as_default=True)
	reactor.callWhenRunning(boot_dbus)
	reactor.run()

if __name__ == '__main__':
	main()
	
