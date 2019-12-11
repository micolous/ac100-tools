// Stubbed version of libtm1640-rpi for testing.
// Copyright 2013 FuryFire
// Copyright 2013, 2019 Michael Farrell <http://micolous.id.au/>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
#ifdef STUB_TM1640
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

typedef struct {
	char displayBuffer[33];
} tm1640_display;

#define DIN_PIN 2
#define SCLK_PIN 1

/**
 * Initialises the display.
 *
 * @param clockPin WiringPi pin identifier to use for clock (SCLK)
 * @param dataPin WiringPi pin identifier to use for data (DIN)
 *
 * @return NULL if wiringPiSetup() fails (permission error)
 * @return pointer to tm1640_display on successful initialisation.
 */
tm1640_display* tm1640_init(int clockPin, int dataPin);

/**
 * Destroys (frees) the structure associated with the connection to the TM1640.
 *
 * @param display TM1640 display connection to dispose of.
 */
void tm1640_destroy(tm1640_display* display);

/**
 * @private
 * Flips 7-segment characters vertically, for display in a mirror.
 *
 * @param input Bitmask of segments to flip.
 * @return Bitmask of segments flipped vertically.
 */
char tm1640_invertVertical(char input);

/**
 * displayWrite
 *
 * @param display TM1640 display to write to
 * @param offset offset on the display to start writing from
 * @param string string to write to the display
 * @param length length of the string to write to the display
 * @param invertMode invert mode to apply to text written to the display
 *
 * @return -EINVAL if invertMode is invalid
 * @return -EINVAL if offset + length > 16
 * @return 0 on success.
 */
int tm1640_displayWrite(tm1640_display* display, int offset, const char * string, char length, int invertMode);

/**
 * @private
 * Converts an ASCII character into 7 segment binary form for display.
 *
 * @param ascii Input ASCII byte to translate.
 * @return 0 if there is no translation available.
 * @return bitmask of segments that represents the input character.
 */
char tm1640_ascii_to_7segment(char ascii);

/**
 * Clears the display
 *
 * @param display TM1640 display to clear
 */
void tm1640_displayClear(tm1640_display* display);

/**
 * Turns on the display and sets the brightness level
 *
 * @param display TM1640 display to set brightness of
 * @param brightness Brightness to set (1 is lowest, 7 is highest)
 */
void tm1640_displayOn(tm1640_display* display, char brightness);

/**
 * Turns off the display preserving display data.
 *
 * @param display TM1640 display to turn off
 */
void tm1640_displayOff(tm1640_display* display);
#endif

