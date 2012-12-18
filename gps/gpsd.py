#!/usr/bin/env python

from gtop_protocol import PmtkProtocol
from twisted.internet.error import ReactorAlreadyInstalledError
from twisted.internet import glib2reactor

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

DBUS_INTERFACE = 'au.id.micolous.carduino.GpsdInterface'
DBUS_SERVICE = 'au.id.micolous.carduino.GpsdService'
DBUS_PATH = '/'

class PmtkProtocolHandler(PmtkProtocol):
	def connectionMade(self):
		self.dbus_api = None
		
		# bump up the baud rate
		self.pmtk_set_nmea_baudrate(38400)
		self.transport.setBaudRate(38400)
		
		# change update rate
		self.pmtk_set_nmea_updaterate(100)
		
	def on_transit_data(self, dt, lat, lng, speed, course, variation):
		if not self.dbus_api: return
		self.dbus_api.on_location(dt.isoformat(), lat, lng, speed, course, variation)
		

class GpsdService(dbus.service.Object):
	"""
	Simple gpsd
	"""
	
	def __init__(self, bus, protocol, object_path=DBUS_PATH):
		self.proto = protocol
		self.proto.dbus_api = self
		dbus.service.Object.__init__(self, bus, object_path)
	
	@dbus.service.signal(dbus_interface=DBUS_INTERFACE, signature='sddddd')
	def on_location(self, dt, lat, lng, speed, course, variation):
		pass


def boot_dbus(device):
	bus = dbus.SystemBus()
	name = dbus.service.BusName(DBUS_SERVICE, bus=bus)
	protocol = PmtkProtocolHandler()
	api = CarduinoService(name, protocol)
	
	port = SerialPort(protocol, device, reactor, baudrate=9600)
	#protocol.port = port

def main():
	parser = ArgumentParser()
	
	parser.add_option(
		'-d', '--device',
		dest='device',
		help='Serial device where the GPS is located'
	)
	
	options = parser.parse_args()

	DBusGMainLoop(set_as_default=True)
	reactor.callWhenRunning(boot_dbus, options.device)
	reactor.run()

if __name__ == '__main__':
	main()
	
