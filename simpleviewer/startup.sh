#!/bin/sh
cd /home/pi/SimpleViewer/simpleviewer/

nohup python3 ./main.py /home/pi/SimpleViewer/simpleviewer/ > /home/pi/simpleviewer.out 2>/home/pi/simpleviewer.err < /dev/null &
