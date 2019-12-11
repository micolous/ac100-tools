.PHONY: all clean install

all: wallclock wallclock-test

wallclock: wallclock.cpp
	c++ -std=c++11 -o wallclock wallclock.cpp -ltm1640 `pkg-config --libs --cflags icu-uc icu-io`

wallclock-test: stub_tm1640.cpp stub_tm1640.h wallclock.cpp
	c++ -std=c++11 -o wallclock-test stub_tm1640.cpp wallclock.cpp -DSTUB_TM1640 `pkg-config --libs --cflags icu-uc icu-io`

install: wallclock wallclock-test
	install -o0 -g0 wallclock wallclock-test /usr/local/bin/

clean:
	rm -f wallclock wallclock-test
