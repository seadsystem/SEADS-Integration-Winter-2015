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

#copies the size to the message little endian
def copy_size(size, message):
	message[1] = (size & 0xFF)
	message[2] = (size >> 8)

#copies the time to the message, string formatted
def copy_time(time, message, index):
	while time:
		time, message[index] = divmod(time, 10)
		message[index] += 48
		#print message[index]
		index -= 1
		#print index

#copies the count into count index
def copy_count(count, message):
	message[38] = (count & 0xFF)
	message[39] = (count >> 8)

#copies the wattage into data index
def copy_watt(wattage, message):
	message[41] = wattage
	message[42] = 0

#loops and receives until gets config
def recv_conf(plug):
	while 1:
		configuration = plug.recv(1000)
		print configuration
		if "@K" in configuration:
			break

#formats and sends the data from wattage
def send_wattage(plug, wattage):
	data = bytearray(b"L00TWlIt00000000000000P00000005000000C01D00X")
	copy_size(44, data)
	copy_count(1, data)
	copy_watt(wattage, data)
	curr_time = int((time.time() * 10000) - start)
	copy_time(curr_time, data, 21)
	print data
	try:
		num = plug.send(data)
		#print num
		time.sleep(5)
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
		pass
		return

#connects to server
plugsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
plugsocket.connect(("db.sead.systems", 9000))
#Create a unix timer 14 digits
start = time.time() * 10000
print "start qeuals: %14d" % (start)
#Make header data - timestamp and serial are ascii encoded
header = bytearray(b"L00THS111111t00000000000500X")
copy_size(28, header)
curr_time = int((time.time() * 10000) - start)
#print "curr qeuals: %14d" % (curr_time)
copy_time(curr_time, header, 26)
print header
#Send header data
plugsocket.sendall(header)
#Receive configuration from server
recv_conf(plugsocket)
#Send random wattage data
for i in range(10):
	random_wattage = randint(50,200)
	send_wattage(plugsocket, random_wattage)

#closes the socket at the end
plugsocket.close()
