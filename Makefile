
all:
	# nothing to compile, try "install".
	
install:
	install -o0 -g0 bin/ac100-backlight /usr/bin/
	install -m644 -o0 -g0 udev/99-ac100-backlight-permissions.rules /etc/udev/rules.d/
