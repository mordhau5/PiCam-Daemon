#!/home/pi/oprint/bin/python
import picamera
import os, io, base64, time, threading, socket
import daemon, daemon.runner

max_receive_len = 200 #this should be reasonably long so that client can send the full filepath

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setup socket
PORT = 10000 # port 10000
HOST = '127.0.0.1' # runs on local host
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this allows us to override port, prevents error
serversocket.bind((HOST, PORT)) # lock server to this port and host
serversocket.listen(1) # don't accept more than one simultaneous client for safety purposes

# thread handler waits here for "commands" from the client
def handle(clientsocket):
    while 1:
        buffer = clientsocket.recv(max_receive_len) 
        command = buffer.decode("utf-8")
        command = command.strip()
        print("recieved: "+command)
        args = command.split(";")

        cmd = args[0]
        if len(args) > 1:
            path = args[1]
        else:
            path = ""

        # Receive the SNAP command. Take a picture with PiCam.
        if cmd == 'snap':
            start = time.time()
            camera.capture(path)
            finish = start - time.time()
            print(finish)
            print('Picture Taken! Saved to '+path)

        if cmd == 'ack':
            print('Acknowledged. Hello!')

        if cmd == 'close':  #close the camera gracefully and close daemon
            print('Closing PiCam and daemon')
            camera.close()
            exit()

        if len(cmd) == 0: break #do nothing

# open and configure Camera before waiting for thread to start. The camera maintains these settings from the daemon's launch and on.
camera = picamera.PiCamera()

# This section WILL be different for each application. Here you'll configure your camera for consistent snapshots, 
# which is one of the keys to a smooth timelapse. 
# If your scene will not be static (ie long running prints in a room with natural sunlight), you may want to consider moving 
# this section to inside the below loop and keeping auto-exposure and awb gains on, and removing the sleep of course.
# See this page for documentation on PiCam and camera options: https://picamera.readthedocs.io/en/release-1.12/
##################################
### CAMERA CONFIG ################
##################################
camera.resolution = (4056, 3040)
camera.shutter_speed = 6000000
camera.iso = 10
time.sleep(5) #give camera a couple seconds to gather metering data before disabling auto-exposure and awb gains.
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
##################################

# Wait for a socket connection and process the input until the connection closes, but keep the engine (camera) warm :)
while 1:
    print('Camera server running')
    # accept connections from outside, in order to receive commands
    (clientsocket, address) = serversocket.accept()
    ct = threading.Thread(target=handle, args=(clientsocket,))
    ct.run() # this can be run(), because it can be scaled.

    print('Camera thread starting.')
    camThread = threading.Thread()
    while camThread.is_alive():
        camThread.join(1)
    camThread.run() # this must be start(), otherwise PiCam will crash. This is because PiCam cannot receive more than 1 connection.
    print('Camera thread ended')