/*
 * Stubbed version of libtm1640 for testing.
 */
#ifdef STUB_TM1640
#include "stub_tm1640.h"


tm1640_display* tm1640_init(int clock, int data) {
	tm1640_display* out;
	out = (tm1640_display*)malloc(sizeof(tm1640_display));
	memset((void*)out, 0, sizeof(tm1640_display));
	return out;
}

void tm1640_destroy(tm1640_display* display) {
	free(display);
}

void tm1640_displayClear(tm1640_display* display) {
	printf("TM1640: Cleared\n");
	memset((void*)display->displayBuffer, 0, 33);
}

void tm1640_displayOff(tm1640_display* display) {
	printf("TM1640: Display off\n");
}

void tm1640_displayOn(tm1640_display* display, char brightness) {
	printf("TM1640: Display on (%i brightness)\n", brightness);
}

int tm1640_displayWrite(tm1640_display* display, int offset, const char * string, char length, int invertMode) {
	if (length <= 0) {
		return -EINVAL;
	}

	// check that there are enough dots in there to make up the length
	if (offset + length > 16 && offset + length <= 32) {
		int dotCount = 0;
		for (int x=0; x<length; x++) {
			if (string[x] == '.' && (x==0 || string[x-1] != '.')) {
				dotCount++;
			}
		}
		
		if (offset + length - dotCount > 16) {
			return -EINVAL;
		}
	} else if (offset + length > 32) {
		return -EINVAL;
	}
	
	// write into the buffer!
	memcpy(display->displayBuffer + offset, string, length);
	
	printf("TM1640: %s\n", display->displayBuffer);
}


#endif

