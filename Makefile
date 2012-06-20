
all:
	# nothing to compile, try "install".
	
install:
	install -o0 -g0 bin/ac100-backlight /usr/bin/
	install -m644 -o0 -g0 udev/99-ac100-backlight-permissions.rules /etc/udev/rules.d/
	service udev reload

install_car:
	# special scripts we only need for the carpc stuff
	install -o0 -g0 bin/bbmop.py /usr/bin/
	install -o0 -g0 bin/dock_car.sh /usr/bin/
	install -o0 -g0 bin/undock_car.sh /usr/bin/
	install -m644 -o0 -g0 udev/99-car.rules /etc/udev/rules.d/
	service udev reload	
