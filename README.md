ac100-tools / carpc
===================

This repository contains some scripts for managing my Car PC.  Scripts relating to the Toshiba AC100 sporked from http://ac100.grandou.net

This contains a bunch of other code as I iterate through developing my car PC.

I experimented with doing carpc stuff with Arduino + Toshiba AC100.  At the moment both of these units aren't wired in and I'm running on a Raspberry Pi.

The current configuration consists of:

- Raspberry Pi, connected to USB 12v adapter
- Adafruit "Ultimate GPS" running at 10Hz connected to TTL serial on RPi, siphoning power from RPi
- TM1640 LCD display controller

There is still the AC100 sitting around and some other periphrials which I want to eventually get running again.  AC100 may be ideal for running servers as it has more CPU power than the RPi.

Early prototypes also included a temperature sensor.  I also have another sensor board that was from another project which acts as an accellerometer.

