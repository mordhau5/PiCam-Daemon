#!/home/pi/oprint/bin/python
import os

#check if PiCamD is running, and start it if not

st = os.system('systemctl --user is-active PiCamD')
if st == 768:
    os.system('systemctl --user start PiCamD')