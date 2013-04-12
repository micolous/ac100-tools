#!/usr/bin/env python
"""
gps/gpsd.py - DBus GPS service
Copyright 2013 Michael Farrell <http://micolous.id.au/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from gtop_protocol import PmtkProtocol
from twisted.internet.error import ReactorAlreadyInstalledError
from twisted.internet import glib2reactor
from time import sleep

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
	dbus_api = None
	
	def connectionMade(self):
		#self.transport.flush()
		self.transport.setBaudRate(9600)

		# bump up the baud rate
		self.pmtk_set_nmea_baudrate(38400)
		sleep(2)

		self.transport.setBaudRate(38400)
		print "changing update rate"
		# change update rate
		self.pmtk_set_nmea_updaterate(100)
		#self.transport.flush()
		
	def on_transit_data(self, dt, lat, lng, speed, course, variation):
		#print dt, lat, lng, speed, course, variation

		if not self.dbus_api: return
		self.dbus_api.on_location(dt.isoformat()+'+00:00', lat, lng, speed, course, variation)
		

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
	api = GpsdService(name, protocol)
	
	port = SerialPort(protocol, device, reactor, baudrate=9600)
	#protocol.port = port
	print 'Service started....'

def main():
	parser = ArgumentParser()
	
	parser.add_argument(
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
	
