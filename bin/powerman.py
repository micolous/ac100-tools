#!/usr/bin/env python
import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
import gobject
from os import system

system_bus = dbus.SystemBus()

power = system_bus.get_object('org.freedesktop.UPower', 
  '/org/freedesktop/UPower/devices/line_power_ac')
  
iface = dbus.Interface(power, dbus_interface='org.freedesktop.UPower.Device')
get_property = lambda x: power.Get('org.freedesktop.UPower.Device', x, dbus_interface='org.freedesktop.DBus.Properties')

def power_changed(sender=None):
  online = bool(get_property('Online'))
  print 'online = %r' % online
  if online:
    system('sudo shutdown -cv')
  else:
    system('sudo shutdown -Pv +2 &')
  

iface.connect_to_signal('Changed', power_changed, sender_keyword='sender')

power_changed()

loop = gobject.MainLoop()
loop.run()
