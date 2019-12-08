# SimpleViewer
Viewer application for SimpleSignage

To install, first install git: `sudo apt-get install git`, then clone the repository into /home/pi/: `git clone https://github.com/awsomechicken/SimpleViewer.git`, then `cd SimpleViewer`, and `./setup.sh`. You'll be prompted to enter the address of the server, enter the key for the screen, and then your timezone. Once the installation is finished, you'll be prompted to reboot your PI, please do so, and don't forget to update your password.

the following requirements (should) be taken care of by the setup.sh script, if ther eare problems, please try installing these manually:

_requires:_
libdbus-1-3
libdbus-1-dev
OMXPlayer
libcec-dev
build-essential
python3-dev
python3-pytz
python3-configparser
python3-omxplayer-wrapper
python3-cec
