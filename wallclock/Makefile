all: wallclock wallclock-test

wallclock: wallclock.c
	gcc -o wallclock wallclock.c -lm -ltm1640 -std=c11

wallclock-test: stub_tm1640.c stub_tm1640.h wallclock.c
	gcc -o wallclock-test stub_tm1640.c wallclock.c -lm -DSTUB_TM1640 -std=c11
