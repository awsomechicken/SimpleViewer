# linux dependancies:
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y python3-pip
# for OMXPlayer:
sudo apt-get install -y libdbus-1-dev
sudo apt-get install -y omxplayer
# for CEC:
sudo apt-get install -y libcec-dev build-essential python-dev

# python dependencies:
pip3 install pytz
pip3 install configparser
pip3 install omxplayer-wrapper
pip3 install git+https://github.com/trainman419/python-cec.git@0.2.7#egg=cec

# call setup.py:
cd setup_files
sudo python3 setup.py
