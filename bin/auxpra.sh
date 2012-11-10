#!/bin/sh
xpra start :100 --start-child=audacious --xvfb='Xvfb +extension Composite -screen 0 1024x600x24+32 -nolisten tcp -noreset -auth $XAUTHORITY'
#DISPLAY=:100 audacious
