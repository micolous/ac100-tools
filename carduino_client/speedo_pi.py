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
from isodate import parse_datetime
from dateutil.tz import gettz
from tm1640 import TM1640, INVERT_MODE_VERTICAL

tzlocal = gettz('Australia/Adelaide')

display = TM1640()
display.on()
display.clear()

SHOW_CLOCK_DOT = ''

def on_location(dt, speed, course, fix):
	global SHOW_CLOCK_DOT
	now = parse_datetime(dt).astimezone(tzlocal)

	if now.microsecond < 100000:
		# whole second, toggle the dot
		SHOW_CLOCK_DOT = '' if SHOW_CLOCK_DOT else '.'

	if now.microsecond == 0 and now.second == 0:
		# reset display if it loses connection / sync
		display.on()
	clock = '%02d%s%02d' % (now.hour, SHOW_CLOCK_DOT, now.minute)

	if fix:
		if course <= 22.5:
			d = 'N '
		elif course <= 67.5:
			d = 'NE'
		elif course <= 112.5:
			d = 'E '
		elif course <= 157.5:
			d = 'SE'
		elif course <= 202.5:
			d = 'S '
		elif course <= 247.5:
			d = 'SW'
		elif course <= 292.5:
			d = 'W '
		elif course <= 337.5:
			d = 'NW'
		else:
			d = 'N '

		m = '%s      %03.0f %s' % (clock, speed, d)
	else:
		# padding is automatically applied so don't do it again
		m = clock

	m += (16 - len(m)) * ' '
	print m
	display.write(m, invert_mode=INVERT_MODE_VERTICAL)

session = gps.gps()
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
for report in session:
	if report['class'] == 'TPV':
		# this is what we want
		speed = (report['speed'] * gps.MPS_TO_KPH) if 'speed' in report else 0
		course = report['track'] if 'track' in report else 0
		on_location(report['time'], speed, course, report['mode'] >= 2)
