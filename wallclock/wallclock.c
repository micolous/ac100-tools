/*
wallclock/wallclock.c
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
#include <time.h>
#include <tgmath.h>

#ifdef STUB_TM1640
#include "stub_tm1640.h"
#else
#include <tm1640.h>
#endif

static tm1640_display* display;


void loop() {
	for (;;) {
		
	}
}
	
int main(int argc, char** argv) {


	// start tm1640
	display = tm1640_init(1, 0);
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
