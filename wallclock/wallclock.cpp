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
#include <tm1640.h>
#endif

static tm1640_display* display;
static Calendar *calendar;
static const TimeZone *tzPacific;
static SimpleDateFormat *dfPacific;

void update_current_time() {
	UnicodeString uPacific;
	UErrorCode success = U_ZERO_ERROR;
	UDate curDate = calendar->getNow();
	
	dfPacific->format(curDate, uPacific, success);
	u_printf("Current Pacific: %S\n", uPacific.getTerminatedBuffer());
}


void loop() {
	for (;;) {
		
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
	
	calendar = Calendar::createInstance(success);

	//DateFormatSymbols* symbols = new DateFormatSymbols(Locale::getUS(), success);
	dfPacific = new SimpleDateFormat(UnicodeString("HH.MMHHMMEEE "), success);
	dfPacific->setTimeZone(*tzPacific);
	update_current_time();
	// run main loop
	//loop();
	return 0;
}
