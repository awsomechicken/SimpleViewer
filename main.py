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
        thereIsNewVid, filename = check_for_new(config)
        if thereIsNewVid:
            done = get_video(config, filename) # get the new video
        # begin!
        play_video(config)

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
            'key':'>>>>Register TV in "Screens" menu, then get the key from there',
            '# Time between the server checks':None,
            'update interval':30
        }
        config['SCREEN CONF'] = {
            'Width':'1920',
            'Height':'1080',
            'current show':'Show_0000000000.mp4'
        }
        save_config(config) #
        print("No config found, new config created; please go fill it in:\n\t", os.getcwd()+"/config")
        #conf = conf_load() # recurse
        return None # return Null to kill the program

def save_config(config):
    confPath = Path("./config") # config path
    with open(confPath, "w+") as cf: # write the default file
        config.write(cf) # write config file
        cf.close()

def check_for_new(config=None):
    print("checking for new video")
    serverHost = "http://%s/tv_check_for_new_content"%(config['SERVER CONF']['Server Address'])
    print(serverHost)
    # add unique ID in the Screens menu for TVUID where the first couple of chars are username and the rest are a "password"
    # for use in the auth section of a response
    servedFileName = ''

    deets = {'auth_token':config['SERVER CONF']['key']} # details for getting a response from the server (hint: uses the key)
    try:
        resp = requests.get(serverHost, params=deets)
        servedFileName = resp.text
        print("served:", servedFileName)

    except:
        print("Server not available")

    if len(servedFileName) > 0:
        isThereNew = not os.path.exists(servedFileName) # boolean for if there is new video
    else:
        isThereNew = False # otherwise there isn't a new video
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

    # now delete the old file:
    old_video = config['SCREEN CONF']['current video']
    os.remove(old_video)
    # and add the new file to the config:
    config['SCREEN CONF']['current video'] = localFileName
    save_config(config) # save the config

    return "done"


def play_video(config):
    print("starting presentation")
    # omxplayer -o hdmi _-eQ_8F4nzyiw.mp4 --win '0 0 1920 1080' --loop
    width = config['SCREEN CONF']['Width']
    height = config['SCREEN CONF']['Height']
    video_to_play = config['SCREEN CONF']['current video']
    print("File to play:", video_to_play)
    player = OMXPlayer(video_to_play, args=['--win', '0 0 %s %s'%(width, height), '--loop'])

    while True:
        thereIsNewVid, filename = check_for_new(config)
        if thereIsNewVid:
            done = get_video(config, filename) # get the new video
            player.quit()
            video_to_play = filename
            player = OMXPlayer(video_to_play, args=['--win', '0 0 %s %s'%(width, height), '--loop'])
        time.sleep(int(config['SERVER CONF']['update interval']))


if __name__ == "__main__":
    main_prog()
