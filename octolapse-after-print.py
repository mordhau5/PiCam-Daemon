#!/home/pi/oprint/bin/python
import socket, sys, os

#open connection
HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

#send the closing command
msg = "close"
s.sendall(msg.encode('utf-8'))
s.close()
sys.exit(0)
