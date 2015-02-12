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

from random import randint

from socket import error as SocketError
import errno

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
curr_time = int((time.time() * 10000) - start)
print "curr qeuals: %14d" % (curr_time)
j = 26
while curr_time:
	curr_time, header[j] = divmod(curr_time, 10)
	header[j] += 48
	print header[j]
	j-=1
print header
#TODO: Send header data
plugsocket.sendall(header)
#TODO: Receive configuration from server
while 1:
	configuration = plugsocket.recv(1000)
	print configuration
	if "@K" in configuration:
		break
#TODO: Send all the data I want to send (loop)
for i in range(10):
	data_size = 44
	data = bytearray(b"L00TWlIt00000000000000P00000005000000C01D00X")
	data[1] = (data_size & 0xFF)
	data[2] = (data_size >> 8)
	data[38] = 1
	data[39] = 0
	data[41] = randint(50,200)
	data[42] = 0
	j = 21
	curr_time = int((time.time() * 10000) - start)
	while curr_time:
		curr_time, data[j] = divmod(curr_time, 10)
		data[j] += 48
		print data[j]
		j-=1
	print data
	try:
		num = plugsocket.send(data)
		#print num
		time.sleep(5)
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
		pass
		plugsocket.close()
		break

#closes the socket at the end
plugsocket.close()
