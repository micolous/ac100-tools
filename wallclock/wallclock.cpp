/*
wallclock/wallclock.cpp
Copyright 2013-2015 Michael Farrell <http://micolous.id.au/>

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

*/
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <unicode/utypes.h>
#include <unicode/calendar.h>
#include <unicode/datefmt.h>
#include <unicode/dtfmtsym.h>
#include <unicode/locid.h>
#include <unicode/smpdtfmt.h>
#include <unicode/timezone.h>
#include <unicode/unistr.h>
#include <unicode/ustdio.h>

#ifdef STUB_TM1640
#include "stub_tm1640.h"
#else
extern "C" {
#include <tm1640.h>
}
#endif

static tm1640_display* display;
static const TimeZone *tzPacific, *tzZurich, *tzTokyo, *tzSydney;
static SimpleDateFormat *dfPacific, *dfZurich, *dfTokyo, *dfSydney;

void update_current_time(int mode) {
	UnicodeString uPacific, uZurich, uTokyo, uSydney;
	UErrorCode success = U_ZERO_ERROR;
	Calendar *calendar = Calendar::createInstance(success);
	UDate curDate = calendar->getNow();// * 1000;
	printf("%f\n", curDate);
	char buf[33];
	int size = mode == 0 ? 5 : 4;

	dfPacific->format(curDate, uPacific);
	dfZurich->format(curDate, uZurich);
	dfTokyo->format(curDate, uTokyo);
	dfSydney->format(curDate, uSydney);

	memset(buf, 0, sizeof(buf));
	int offset = mode * size + (mode > 0 ? 1 : 0);
	uPacific.extract(offset, size, buf);
	uZurich.extract(offset, size, buf+size);
	uTokyo.extract(offset, size, buf+(size*2));
	uSydney.extract(offset, size, buf+(size*3));

	//printf("screen = %s\n", buf);
	tm1640_displayWrite(display, 0, buf, size*4, 0);
}


void loop() {
	int mode = 0;
	for (;;) {
		update_current_time(mode >= 59 ? 2 : (mode % 2));
		mode++;

		if (mode > 59) {
			mode = 0;
		}

		sleep(1);
	}
}
	
int main(int argc, char** argv) {
	UErrorCode success = U_ZERO_ERROR;

	// start tm1640
	display = tm1640_init(1, 0);
	if (display == NULL) {
		fprintf(stderr, "error initialising display\n");
		return EXIT_FAILURE;
	}
	
	tm1640_displayOn(display, 7);
	tm1640_displayClear(display);

	// load tzdata
	tzPacific = TimeZone::createTimeZone("America/Los_Angeles");
	tzZurich = TimeZone::createTimeZone("Europe/Zurich");
	tzTokyo = TimeZone::createTimeZone("Asia/Tokyo");
	tzSydney = TimeZone::createTimeZone("Australia/Sydney");

	dfPacific = new SimpleDateFormat(UnicodeString("HH.mmHHmmEEE "), success);
	dfPacific->setTimeZone(*tzPacific);
	dfZurich = (SimpleDateFormat*)dfPacific->clone();
	dfZurich->setTimeZone(*tzZurich);
	dfTokyo = (SimpleDateFormat*)dfPacific->clone();
	dfTokyo->setTimeZone(*tzTokyo);
	dfSydney = (SimpleDateFormat*)dfPacific->clone();
	dfSydney->setTimeZone(*tzSydney);

	// run main loop
	loop();
	return 0;
}
