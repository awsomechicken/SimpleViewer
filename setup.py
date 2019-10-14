#!/usr/bin/env python3
# setup the simple viewer
import sys
def setup_system():
    print('things and stuff')

# do things in /etc.init.d/
def make_startup():
    print("HOLY CRAP")

def doshit(input_param):
    print("more CRAP", input_param)

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
    #setup_system()
