#!/usr/bin/python
# ============================================================
# File: plug-emulator.py
# Description: This sends plug formatted data to the server
# Created by Henry Crute
# 2/5/2015
# ============================================================

import socket
import sys
import time

#connects to server
plugsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
plugsocket.connect(("db.sead.systems", 9000))
#TODO: Create a unix timer 14 digits
start = time.time() * 10000
print "start qeuals: %14d" % (start)
#TODO: Make header data - timestamp and serial are ascii encoded
header_size = 28
header = bytearray(b"L00THS111111t00000000000500X")
header[1] = (header_size & 0xFF)
header[2] = (header_size >> 8)
print header[2]
print header[1]
print header
#TODO: Send header data
plugsocket.send(header)
#TODO: Receive configuration from server
configuration = plugsocket.recv(1000)
print configuration
configuration = plugsocket.recv(1000)
print configuration
configuration = plugsocket.recv(1000)
print configuration
#TODO: Send all the data I want to send (loop)
for i in range(10):
	time.sleep(0.5)
	print "time: %14d" % ((time.time() * 10000) - start)

#file = open("temp", "rb")
#segment = file.read(1024)
#while (segment):
#plugsocket.send(segment)
#segment = file.read(1024)

#closes the socket at the end
plugsocket.close()
