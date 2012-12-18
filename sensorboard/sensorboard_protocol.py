#!/usr/bin/env python

from twisted.protocols.basic import LineReceiver
from twisted.python import log
from struct import unpack
from math import atan2, pi

class SensorboardProtocol(LineReceiver):
	"""
	Twisted stackAR sensorboard protocol library.
	
	Adapted from http://svn.stackunderflow.com/svn/public/stackAR/Hardware/sensorboard.py
	
	"""
	delimiter = '\xFE'
	
	def connectionMade(self):
		# issue wake-up command
		self.transport.write('a')
		
	def lineReceived(self, line):
		if not line.startswith('\xFF') or len(line) != 19:
			return
			
		# now parse the data
		values = unpack('<9h', line[1:])
		
		magX, magY, magZ = values[:3]
		
		angle = atan2(magZ, magX) * (180./pi) + 90.
		
		if angle < 0:
			angle += 360
		
		values += (angle,)
		
		self.on_sensor_reading(*values)
	
	
	def on_sensor_reading(self, magX, magY, magZ, accX, accY, accZ, gyroX, gryoY, gyroZ, compass_angle):
		"""
		This function is called whenever a new sensor reading is available.
		
		Note: this blocks reading more data, and it comes in at up to 50Hz.
		"""
		log.msg('sensor: %3.1fd %4i %4i %4i  %4i %4i %4i  %4i %4i %4i' % (compass_angle, magX, magY, magZ, accX, accY, accZ, gyroX, gryoY, gyroZ))

if __name__ == '__main__':
	from argparse import ArgumentParser
	from twisted.internet import reactor
	from twisted.internet.serialport import SerialPort
	import sys
	
	parser = ArgumentParser()
	
	parser.add_argument('-d', '--device', dest='device', default='/dev/ttyUSB0', help='Device to read sensor data from [default: %(default)s]')
	
	options = parser.parse_args()
	log.startLogging(sys.stdout)
	
	protocol = SensorboardProtocol()
	SerialPort(protocol, options.device, reactor, baudrate=115200)
	reactor.run()

		