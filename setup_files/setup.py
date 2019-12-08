#!/usr/bin/env python3
# setup the simple viewer
import sys, configparser, pytz
from pathlib import Path

def setup_system():
    #print('things and stuff')
    make_inital_config()

def make_inital_config():
    # make config:
    config = configparser.ConfigParser()
    # load up the config with useful stuff:
    config['SERVER CONF'] = {
        'Server Address':'127.0.0.1:8000',
        'key':'>>>>Register TV in "Screens" menu, then get the key from there',
        '# Time between the server checks':0,
        'update interval (seconds)':30
    }
    config['SCREEN CONF'] = {
        'Width':'1920',
        'Height':'1080',
        'current video':'Show_0000000000.mp4'
    }
    config['SCHEDULE'] = {
        '# If your screen supports HDMI CEC, these can be used:':0,
        'Use CEC':True,
        'timezone':'America/Los_Angeles',
        '# Times are in 24-hour format':0,
        'Turn On':'08:45:00',
        'Turn Off':'17:15:00'
    }

    print("Please input the Server address in the form: \"address:port\":")
    server_addr = str(input()) # get the server address
    if len(server_addr) < 5:
        print("Server address is too short to be real, please re-enter:")
        server_addr = str(input()) # get the server address
    config['SERVER CONF']['Server Address'] = server_addr

    print("Please enter the screen key, found in the 'Screens' menu:")
    scrkey = str(input())
    config['SERVER CONF']['key'] = scrkey

    # configure Time Zone
    print("what is your timezone?")
    for tz in pytz.all_timezones:
        print(tz)
    print("what is your timezone?")
    timezone = str(input())
    TZ = "blank" # time zone to be stored:
    for tz in pytz.all_timezones:
        if tz.lower() == timezone.lower():
            TZ = tz

    if TZ == "blank": # sanity-checck
        print("no legal timezone entered, assuming UTC (Universal Coordinated Time)")
        TZ = "UTC"

    config['SCHEDULE']['timezone'] = TZ # save the config

    # now save the config:
    confPath = Path("/home/pi/SimpleViewer/simpleviewer/config") # config path
    with open(confPath, "w+") as cf: # write the default file
        config.write(cf) # write config file
        cf.close()


if __name__ == '__main__':
    #globals()[sys.argv[1]](sys.argv[2])
    setup_system()
