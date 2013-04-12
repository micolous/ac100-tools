#!/usr/bin/env python
"""
carduino_client/speedo_pi.py - Implementation of speedo on TM1640
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
import gps
from time import sleep
from datetime import datetime
import dateutil.parser
from dateutil.tz import tzlocal
from tm1640 import TM1640, INVERT_MODE_VERTICAL

tzlocal = tzlocal()

display = TM1640()
display.on()
display.clear()

SHOW_CLOCK_DOT = False

def on_location(dt, speed, course, fix):
	global SHOW_CLOCK_DOT
	
	now = dateutil.parser.parse(dt).astimezone(tzlocal)
	
	if now.microsecond == 0:
		# whole second, toggle the dot and hide the display if there's no power
		SHOW_CLOCK_DOT = not SHOW_CLOCK_DOT

	if now.microsecond == 0 and now.second == 0:
		# reset display if it loses connection / sync
		display.on()
	
	if fix:
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
	
	m += (16 - len(m)) * ' '
	print m
	display.write(m, invert_mode=INVERT_MODE_VERTICAL)

session = gps.gps()
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
for report in session:
	if report['class'] == 'TPV':
		# this is what we want
		on_location(report['time'], report['speed'] * 1.852, report['track'], report['mode'] >= 2)
