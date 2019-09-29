#!/usr/bin/env python3
# Main program for displaying the signage videos
# Simple Signasge project

# using omxplayer-wrapper
try:
    from omxplayer.player import OMXPlayer
except Exception as e:

    print("OMXPlayer wrapper not found, please install: \n\t~$ pip3 install omxplayer-wrapper\n\nSee:\n\thttps://python-omxplayer-wrapper.readthedocs.io/en/latest/")

from pathlib import Path
# configuration parser library, included as part of python
# https://docs.python.org/3/library/configparser.html
import configparser
import time, os, requests, random, string, shutil

# use HDMI CEC to control the TV:
# https://www.linuxuprising.com/2019/07/raspberry-pi-power-on-off-tv-connected.html

def main_prog():
    print("starting player")

    # load configuration
    config = conf_load()

    if not(config == None):
        # check the configuration, suggest error fix
        print(config['SERVER CONF']['Server Address'])
        # quirie the server
        #thereIsNewVid, filename = check_for_new(config)
        #if thereIsNewVid:
        #    done = get_video(config, filename) # get the new video
        # begin!
        #play_video(filename)
        play_video('Show_1569200803.mp4')

def conf_load():
    print("load conf")
    config = configparser.ConfigParser()
    confPath = Path("./config")
    print("Conf path exists:", os.path.exists(confPath))
    if os.path.exists(confPath):
    # read the configuration file
        config.read(confPath)
        config.sections()
        return config

    else: # if no config file exists:
        # build the default settings
        config['SERVER CONF'] = {
            'Server Address':'127.0.0.1:8000',
            'TV Width':'1920',
            'TV Height':'1080',
            'key':'>>>>Register TV in "Screens" menu, then get the key from there'
        }

        with open(confPath, "w+") as cf: # write the default file
            config.write(cf) # write config file
            cf.close()
        print("No config found, new config created; please go fill it in:\n\t", os.getcwd()+"/config")
        #conf = conf_load() # recurse
        return None # return Null to kill the program


def check_for_new(config=None):
    print("checking for new video")
    serverHost = "http://%s/tv_check_for_new_content"%(config['SERVER CONF']['Server Address'])
    print(serverHost)
    # add unique ID in the Screens menu for TVUID where the first couple of chars are username and the rest are a "password"
    # for use in the auth section of a response
    deets = {'auth_token':config['SERVER CONF']['key']} # details for getting a response from the server (hint: uses the key)
    try:
        resp = requests.get(serverHost, params=deets)
        servedFileName = resp.text
        print("served:", servedFileName)

    except ConnectionRefusedError:
        print("Server not available")

    isThereNew = not os.path.exists(servedFileName) # boolean for if there is new video

    print("have we new file?", isThereNew)

    return isThereNew, servedFileName # return the name of the newest file

def get_video(config, localFileName):
    print("getting video from server")

    serverHost = "http://%s/tv_get_new_content"%(config['SERVER CONF']['Server Address'])
    deets = {'auth_token':config['SERVER CONF']['key']} # details for getting a response from the server
    # using RAW and shutil
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests

    with requests.get(serverHost, stream=True, params=deets) as req:
        with open(localFileName, 'wb') as f:
            shutil.copyfileobj(req.raw, f)

    return "done"


def play_video(localFileName):
    print("starting presentation")
    # omxplayer -o hdmi _-eQ_8F4nzyiw.mp4 --win '0 0 1920 1080' --loop

    player = OMXPlayer(localFileName)
    player.set_aspect_mode('streach')
    player.set_video_pos(0, 0, 1920, 1080)

    #time.sleep(1500)
    #player.quit()

if __name__ == "__main__":
    main_prog()
