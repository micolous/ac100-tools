#!/usr/bin/env python
import pygame
from pygame.locals import *
from os import system

pygame.init()
pygame.joystick.init()
pygame.mixer.quit()

screen = pygame.display.set_mode((100,100))

for x in range(pygame.joystick.get_count()):
  js = pygame.joystick.Joystick(x)
  js.init()

print "running..."
keep_running = True
while keep_running:
  if pygame.event.peek():
    for event in pygame.event.get():
      if event.type == QUIT:
        keep_running = False
        break
      elif event.type == JOYBUTTONDOWN:
        print "got button press on %s, button %s" % (event.joy, event.button)
        
        if event.button == 0:
          system('mocp -f') # next
        elif event.button == 1:
          system('mocp -G') # play/pause
        elif event.button == 2:
          system('mocp -r')
          
         
  # sleep
  pygame.time.wait(100)
  # pump  
  pygame.event.pump()

print "bye"
