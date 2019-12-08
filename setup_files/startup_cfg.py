# make SimpleViewer run at startup
# do things in /etc.init.d/
def make_startup():
    #print("HOLY CRAP")
    rc_local = ""
    with open("/etc/rc.local", "r") as rc:
        rc_local = rc.read() # read the rc.local file
        rc.close()

    # the exit 0 is ALways at the end, replace it with a string being sure to add exit 0 to the end of the new string:

    startup = "nohup /home/pi/SimpleViewer/simpleviewer/startup.sh &\n\nexit 0"

    rc_local = rc_local.replace("exit 0", startup)

    with open("/etc/rc.local", "w") as rc:
        rc.write(rc_local)
        rc.close()

    print("autostart configuration complete, please reboot your pi, and don't forget to update passwords")


if __name__ == "__main__":
    make_startup() # do the thing
