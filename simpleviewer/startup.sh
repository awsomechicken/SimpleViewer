#!/bin/sh
nohup python3 /home/pi/SimpleViewer/simpleviewer/main.py /home/pi/SimpleViewer/simpleviewer/ > /home/pi/simpleviewer.out 2> /home/pi/simpleviewer.err < /dev/null &
