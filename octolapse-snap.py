#!/home/pi/oprint/bin/python
import socket, sys, os
from time import sleep

#Pull in the Octolapse command-line ARGS
SNAPSHOT_NUMBER=int(sys.argv[1])
DELAY_SECONDS=float(sys.argv[2])
DATA_DIRECTORY=sys.argv[3]
SNAPSHOT_DIRECTORY=sys.argv[4]
SNAPSHOT_FILENAME=sys.argv[5]
SNAPSHOT_FULL_PATH=sys.argv[6]
OCTOLAPSE_DIRECTORY="/home/pi/.octoprint/"

# Check to see if the snapshot directory exists
if not os.path.exists(SNAPSHOT_DIRECTORY):
    print("Creating directory: "+SNAPSHOT_DIRECTORY)
    os.makedirs(SNAPSHOT_DIRECTORY)

# Wait for stabalization
sleep(DELAY_SECONDS)

#Open connection to Daemon
HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

#Tell the Server we want a snapshot, and where
msg = "snap;"+SNAPSHOT_FULL_PATH
s.sendall(msg.encode('utf-8'))

#Wait for snapshot to exist
while not os.path.exists(SNAPSHOT_FULL_PATH):
    print("not yet")

#We're Done!
s.close()
sys.exit(0)