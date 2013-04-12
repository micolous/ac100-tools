
from twisted.protocols.basic import LineReceiver
from struct import pack
from datetime import datetime
from time import sleep

def pmtk_checksum(i):
	o = 0
	for c in i: o ^= ord(c)
	return '%02X' % o


class PmtkProtocol(LineReceiver):
	"""
	Implements a twisted protocol for communicating with PMTK G.top GPS
	
	Reference: http://learn.adafruit.com/adafruit-ultimate-gps/downloads-and-resources
	"""

	delimiter = '\n'
	def connectionMade(self):
		# increase baud rate
		#self.pmtk_set_nmea_baudrate(38400)
		#self.transport.setBaudRate(38400)
		
		# change update rate
		#self.pmtk_set_nmea_updaterate(100)
		
	
		# don't do anything when connecting.
		pass
	
	def lineReceived(self, line):
		# got data from the gps
		
		# do nothing
		#print "recv: %s" % line
		line = line.strip()
		try:
			if line.startswith('$GPRMC'): # only handles gprmc so skip some others
				# parse NMEA sentence
				word, checksum = line[1:].split('*', 2)
				
				# validate
				real_checksum = pmtk_checksum(word)
				if real_checksum != checksum:
					raise ValueError, 'Invalid checksum, expected %r but got %r' % (real_checksum, checksum)
				
				# now parse some
				args = word.split(',')
				
				#if args[0] == 'GPRMC':
				self.on_gprmc(args[1:])
				#elif args[0] == '
		except:
			# parse error
			pass
			
	def on_gprmc(self, args):
		# check if valid
		if args[1] != 'A': return
	
		# parse out the time
		#t = datetime.strptime(args[0][:6], '%H%M%S')
		# parse the date
		dt = datetime.strptime(args[8] + args[0][:6], '%d%m%y%H%M%S')

		if len(args[0]) > 6:
			dt = dt.replace(microsecond = int(float(args[0][6:]) * 1000000.))
		
		if dt.year < 2000:
			dt = dt.replace(year=2000 + (dt.year % 100))
		
		#dt = datetime.combine(d.date(), t.time())
		
		# now parse the location.
		lat_deg = int(args[2][:2])
		lat_min = float(args[2][2:])
		lng_deg = int(args[4][:3])
		lng_min = float(args[4][3:])
		
		lat = lat_deg + (lat_min / 60.)
		lng = lng_deg + (lng_min / 60.)
		if args[3] == 'S': lat *= -1
		if args[5] == 'W': lng *= -1
		
		# convert speed to km/h
		speed = float(args[6]) * 1.852	
		course = float(args[7])
		if args[9]:
			variation = float(args[9])
			if args[10] == 'W': variation *= -1
		else:
			variation = 0.
		
		self.on_transit_data(dt, lat, lng, speed, course, variation)
		
	def on_transit_data(self, dt, lat, lng, speed, course, variation):
		print 'td: %r %r,%r @%sm/s %sd v%sd' % (dt, lat, lng, speed, course, variation)
	
	def pmtk_cmd(self, cmd, *args):
		o = 'PMTK%s,%s' % (cmd, ','.join((str(x) for x in args)))
		o = '$%s*%s' % (o, pmtk_checksum(o))
		
		#print "send: %s" % o
		self.transport.writeSomeData('\r\n\r\n' + o + '\r\n')
		sleep(1)
		
	def pmtk_set_nmea_baudrate(self, baud):
		if baud not in (4800, 9600, 14400, 19200, 38400, 57600, 115200):
			raise ValueError, 'That is not a valid baud rate.'
			
		self.pmtk_cmd(251, baud)
		#self.transport.setBaudRate(baud)
	
	def pmtk_set_nmea_updaterate(self, millis):
		if not (100 <= millis <= 10000):
			raise ValueError, 'Update rate must be between 100 and 10000 milliseconds'
		
		self.pmtk_cmd(220, millis)
