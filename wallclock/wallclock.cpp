/*
wallclock/wallclock.cpp
Copyright 2013-2015, 2019 Michael Farrell <http://micolous.id.au/>

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
#include <unicode/udat.h>
#include <unicode/unistr.h>
#include <unicode/ustdio.h>

#ifdef STUB_TM1640
#include "stub_tm1640.h"
#else
extern "C" {
#include <tm1640.h>
}
#endif

using icu::Calendar;
using icu::SimpleDateFormat;
using icu::TimeZone;
using icu::UnicodeString;

static tm1640_display* display;
static const TimeZone *tzA, *tzB, *tzC, *tzD;
static SimpleDateFormat *dfA, *dfB, *dfC, *dfD;

void update_current_time(int mode) {
	UnicodeString uA, uB, uC, uD;
	UErrorCode success = U_ZERO_ERROR;
	Calendar *calendar = Calendar::createInstance(success);
	UDate curDate = calendar->getNow();// * 1000;
	//printf("%f\n", curDate);
	char buf[33];
	int size = mode == 0 ? 5 : 4;

	dfA->format(curDate, uA);
	dfB->format(curDate, uB);
	dfC->format(curDate, uC);
	dfD->format(curDate, uD);

	memset(buf, 0, sizeof(buf));
	int offset = mode * size + (mode > 0 ? 1 : 0);
	uA.extract(offset, size, buf);
	uB.extract(offset, size, buf+size);
	uC.extract(offset, size, buf+(size*2));
	uD.extract(offset, size, buf+(size*3));

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

const TimeZone* getTimeZoneOrDie(const char* id) {
	const TimeZone* tz = TimeZone::createTimeZone(id);
	if (TimeZone::getUnknown() == *tz) {
		fprintf(stderr, "Timezone `%s` is unknown.\n", id);
		return NULL;
	}
	return tz;
}

int main(int argc, char** argv) {
	UErrorCode success = U_ZERO_ERROR;

	if (argc != 5) {
		fprintf(stderr, "must specify exactly 4 timezone identifiers:\n");
		fprintf(stderr, "%s 'Australia/Perth' 'Australia/Adelaide' 'Australia/Brisbane' 'Australia/Sydney'\n", argv[0]);
		return EXIT_FAILURE;
	}

	// load tzdata
	if ((tzA = getTimeZoneOrDie(argv[1])) == NULL) {
		return EXIT_FAILURE;
	}
	if ((tzB = getTimeZoneOrDie(argv[2])) == NULL) {
		return EXIT_FAILURE;
	}
	if ((tzC = getTimeZoneOrDie(argv[3])) == NULL) {
		return EXIT_FAILURE;
	}
	if ((tzD = getTimeZoneOrDie(argv[4])) == NULL) {
		return EXIT_FAILURE;
	}

	dfA = new SimpleDateFormat(UnicodeString("HH.mmHHmmEEE "), success);
	dfA->setTimeZone(*tzA);
	dfB = (SimpleDateFormat*)dfA->clone();
	dfB->setTimeZone(*tzB);
	dfC = (SimpleDateFormat*)dfA->clone();
	dfC->setTimeZone(*tzC);
	dfD = (SimpleDateFormat*)dfA->clone();
	dfD->setTimeZone(*tzD);

	// start tm1640
	display = tm1640_init(SCLK_PIN, DIN_PIN);
	if (display == NULL) {
		fprintf(stderr, "error initialising display\n");
		return EXIT_FAILURE;
	}

	tm1640_displayOn(display, 7);
	tm1640_displayClear(display);

	// run main loop
	loop();
	return 0;
}
