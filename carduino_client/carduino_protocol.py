
from twisted.protocols.basic import LineReceiver
from struct import pack

DIGIT_FONT = {
	' ': 0,
	'0': 1 + 2 + 4 + 8 + 16 + 32,
	'1': 2 + 4,
	'2': 1 + 2 + 8 + 16 + 64,
	'3': 1 + 2 + 4 + 8 + 64,
	'4': 2 + 4 + 32 + 64,
	'5': 1 + 4 + 8 + 32 + 64,
	'6': 1 + 4 + 8 + 16 + 32 + 64,
	'7': 1 + 2 + 4,
	'8': 1 + 2 + 4 + 8 + 16 + 32 + 64,
	'9': 1 + 2 + 4 + 8 + 32 + 64,
	#'.': 128,
	
	# from TM16XXFonts.h
	'N': 55,
	'E': 121,
	'S': 1 + 4 + 8 + 32 + 64,
	'W': 29,
	
	'c': 88,
}


def digit_reflect(d):
	# keep centre and dot
	o = d & 0xC0
	
	# swap top and bottom
	o |= (d & 0x01) << 3
	o |= (d & 0x08) >> 3
	
	# swap lefts
	o |= (d & 0x02) << 1
	o |= (d & 0x04) >> 1
	
	# swap rights
	o |= (d & 0x10) << 1
	o |= (d & 0x20) >> 1
	
	return o


class CarduinoProtocol(LineReceiver):
	"""
	Implements a twisted protocol for communicating with Carduino
	
	"""

	delimiter = '\n'
	def connectionMade(self):
		# issue reset command
		
		# send it 17 times in case gpsd has decided to shit on our parade
		self.transport.write('\\' * 17)
	
	def lineReceived(self, line):
		# got data from the carduino
		
		if line.startswith('TEMP '):
			print "temperature packet: %s" % line
		
	
	def lcd_clear(self):
		self.transport.write('\x40')
	
	def lcd_home(self):
		self.transport.write('\x41')
	
	def lcd_display_off(self):
		self.transport.write('\x42')
	
	
	def lcd_write(self, s):
		s = str(s)
		assert len(s) <= 16, "string length is longer than 16 bytes"
		assert len(s) > 0, "string length must be at least 1 byte"
		
		# write the length seg
		self.transport.write(pack('B', len(s) - 1) + s)
	
	def lcd_gotoxy(self, x, y):
		assert 0 <= y <= 1, "y co-ordinate must be in range 0 .. 1"
		assert 0 <= x <= 15, "x co-ordinate must be in range 0 .. 15"
		
		c = 0x20 | (y << 4) | x
		
		self.transport.write(pack('B', c))
	

	def seven_getsegs(self, s):		
		d = []
		for c in s:
			if c in DIGIT_FONT:
				d.append(DIGIT_FONT[c])
			elif c == '.':
				# add dot to previous digit
				d[-1] |= 128
			else:
				d.append(DIGIT_FONT[' '])
			
		return d

	def seven_writestr(self, s):		
		s = str(s)
		if s.startswith('.'):
			s = ' ' + s
		
		assert 0 < len(s.replace('.', '')) <= 16, 'string length must be 1 .. 16'
		d = self.seven_getsegs(s)
		
		self.seven_writesegs(d)
		
	def seven_writestr_mirror(self, s):
		s = str(s)
		if s.startswith('.'):
			s = ' ' + s

		assert 0 < len(s.replace('.', '')) <= 16, 'string length must be 1 .. 16'
		d = [digit_reflect(c) for c in self.seven_getsegs(s)]
		
		self.seven_writesegs(d)
	
	def seven_writesegs(self, d):
		d = [int(c) for c in d]
		assert 0 < len(d)	<= 16, 'array length must be 1 .. 16'
		
		d = ''.join(chr(c) for c in d)
		
		self.transport.write(pack('B', 0xA0 | (len(d) - 1)) + d)
		
		
		
