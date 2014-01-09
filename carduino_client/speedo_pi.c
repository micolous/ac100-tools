/*
carduino_client/speedo_pi.c - Port of speedo_pi.py to C
Copyright 2013-2014 Michael Farrell <http://micolous.id.au/>

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

Building:
  $ gcc -o speedo_pi speedo_pi.c -lgps -lm -ltm1640

*/
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <tgmath.h>

#include <gps.h>
#include <tm1640.h>

static struct gps_data_t gpsdata;
static tm1640_display* display;

void get_direction(double course, char* sdirection) {
	if (course <= 22.5)
		memcpy(sdirection, "N ", 3);
	else if (course <= 67.5)
		memcpy(sdirection, "NE", 3);
	else if (course <= 112.5)
		memcpy(sdirection, "E ", 3);
	else if (course <= 157.5)
		memcpy(sdirection, "SE", 3);
	else if (course <= 202.5)
		memcpy(sdirection, "S ", 3);
	else if (course <= 247.5)
		memcpy(sdirection, "SW", 3);
	else if (course <= 292.5)
		memcpy(sdirection, "W ", 3);
	else if (course <= 337.5)
		memcpy(sdirection, "NW", 3);
	else 
		memcpy(sdirection, "N ", 3);
}


void on_location(struct gps_data_t *gpsdata) {
	static double int_time, old_int_time;
	static bool first = true;
	static bool show_seperator = true;
	char sclockbit[6];
	char sdisplayOut[18];
	char sdirection[3];
	
	// set display output to all null
	// because the string input is variable length.
	memset(sdisplayOut, 17, 0);
	
	int_time = gpsdata->fix.time;
	
	if ((int_time == old_int_time) || gpsdata->fix.mode < MODE_2D)
		// repeat packet or bad fix
		return;
	
	time_t timet_time = (time_t)gpsdata->fix.time;
	
	struct tm* local_time = localtime(&timet_time);
	
	// flip seperator
	if (fmod(int_time, 1.) < 0.05) {
		show_seperator = !show_seperator;
		if (local_time->tm_sec == 0)
			// reinit display because sometimes it looses connection
			tm1640_displayOn(display, 7);
	}
	
	// Clock
	strftime(sclockbit, sizeof(sclockbit), (show_seperator ? "%H.%M" : "%H%M"), local_time);

	// Bearing
	get_direction(gpsdata->fix.track, sdirection);
	
	// Construct display string
	sprintf(sdisplayOut, "%s      %03.0f %s", sclockbit, gpsdata->fix.speed * MPS_TO_KPH, sdirection);
	printf("display: '%s' \n", sdisplayOut);
	
	tm1640_displayWrite(display, 0, sdisplayOut, strlen(sdisplayOut), INVERT_MODE_VERTICAL);
	
	old_int_time = int_time;
}

void loop() {
	unsigned int flags = WATCH_ENABLE;
	gps_stream(&gpsdata, flags, NULL);

	for (;;) {
		if (!gps_waiting(&gpsdata, 5000000)) {
			fprintf(stderr, "error waiting\n");
			break;
		} else {
			// read gps
			gps_read(&gpsdata);
			on_location(&gpsdata);
		}
	}
	
	gps_close(&gpsdata);
}
	
int main(int argc, char** argv) {
	// Just connect to the GPSd on localhost
	while (gps_open("localhost", "2947", &gpsdata) != 0) {
		fprintf(stderr, "cannot connect to gpsd, sleeping...\n");
		sleep(1);
	}

	// start tm1640
	display = tm1640_init(1, 0);
	if (display == NULL) {
		fprintf(stderr, "error initialising display\n");
		return EXIT_FAILURE;
	}
	
	tm1640_displayOn(display, 7);

	// run main loop
	loop();
	return 0;
}
