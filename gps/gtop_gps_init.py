#!/usr/bin/env python
"""
gps/gtop_gps_init.py - GTop GPS initialisation program
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
from time import sleep
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.serialport import SerialPort
from twisted.python import log
import sys
from argparse import ArgumentParser

class PmtkProtocolHandler(PmtkProtocol):
	def connectionMade(self):
		# bump up the baud rate
		self.pmtk_set_nmea_baudrate(self.target_baud)
		
		# wait here for a bit so that it switches proper.
		sleep(2)
		self.transport.setBaudRate(self.target_baud)
		
		# change update rate
		self.pmtk_set_nmea_updaterate(self.rate)
		#self.transport.flush()
		
		# we're done here, quit
		reactor.stop()


def boot(device, initial_baud, target_baud, rate):
	protocol = PmtkProtocolHandler()
	protocol.target_baud = target_baud
	protocol.rate = rate
	
	port = SerialPort(protocol, device, reactor, baudrate=initial_baud)

	
def main():
	parser = ArgumentParser()
	
	parser.add_argument(
		'-d', '--device',
		dest='device',
		help='Serial device where the GPS is located'
	)
	
	parser.add_argument(
		'-i', '--initial-baud',
		dest='initial_baud',
		type=int,
		default=9600,
		help='Default baud rate if the device is reset [default: %(default)s]'
	)
	
	parser.add_argument(
		'-t', '--target-baud',
		dest='target_baud',
		type=int,
		default=38400,
		help='Target baud rate for the GPS [default: %(default)s]'
	)
	
	parser.add_argument(
		'-r', '--rate',
		dest='rate',
		default=100,
		help='Number of milliseconds GPS should wait before sending updates [default: %(default)s]',
	)
	
	options = parser.parse_args()
	reactor.callWhenRunning(boot, options.device, options.initial_baud, options.target_baud, options.rate)
	reactor.run()

if __name__ == '__main__':
	main()
