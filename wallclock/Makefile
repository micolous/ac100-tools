.PHONY: all clean

all: wallclock wallclock-test

wallclock: wallclock.cpp
	c++ -o wallclock wallclock.cpp -ltm1640 `pkg-config --libs --cflags icu-uc icu-io`

wallclock-test: stub_tm1640.c stub_tm1640.h wallclock.cpp
	c++ -o wallclock-test stub_tm1640.c wallclock.cpp -DSTUB_TM1640 `pkg-config --libs --cflags icu-uc icu-io`

clean:
	rm -f wallclock wallclock-test

