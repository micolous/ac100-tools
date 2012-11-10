#!/usr/bin/env python
import pygame
from pygame.locals import *
from os import system

pygame.init()
pygame.joystick.init()
pygame.mixer.quit()

screen = pygame.display.set_mode((100,100))

x=0
for x in range(pygame.joystick.get_count()):
  js = pygame.joystick.Joystick(x)
  js.init()
  x+=1

print "running with %d joystick(s)..." % x
keep_running = True
paused = True
while keep_running:
  if pygame.event.peek():
    for event in pygame.event.get():
      if event.type == QUIT:
        keep_running = False
        break
      elif event.type == JOYBUTTONDOWN:
        print "got button press on %s, button %s" % (event.joy, event.button)
        
        if event.button == 0:
          system('DISPLAY=:100 mpris-remote next') # next
        elif event.button == 1:
          if paused:
            system('DISPLAY=:100 mpris-remote play') # play/pause
          else:
            system('DISPLAY=:100 mpris-remote pause')
          paused = not paused
        elif event.button == 2:
          system('DISPLAY=:100 mpris-remote prev')
          
         
  # sleep
  pygame.time.wait(100)
  # pump  
  pygame.event.pump()

print "bye"
