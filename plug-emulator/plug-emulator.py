#!/usr/bin/env python2
# ============================================================
# File: plug-emulator.py
# Description: This sends plug formatted data to the server
# Created by Henry Crute
# 2/5/2015
# ============================================================

import socket
import sys
import time
import getopt

from random import randint

from socket import error as SocketError
import errno

#Create a unix timer 14 digits
start = time.time() * 10000

def usage():
	print 'Usage: '+sys.argv[0]+' [-hwvit --help --wattage --voltage --current --temperature]'

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
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
		pass
		return

def send_temperature(plug, temperature):
	data = bytearray(b"L00TTlIt00000000000000P00000005000000C01D00X")
	copy_size(44, data)
	copy_count(1, data)
	copy_watt(temperature, data)
	curr_time = int((time.time() * 10000) - start)
	copy_time(curr_time, data, 21)
	print data
	try:
		num = plug.send(data)
		#print num
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise # Not error we are looking for
		pass
		return

def send_voltage(plug):
	return

def send_current(plug):
	return

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hwvit",
			["help", "wattage", "voltage", "current", "temperature"])
	except getopt.GetoptError as err:
		#print help information and exit
		print str(err)
		usage()
		sys.exit(2)
	watt_arg = False
	volt_arg = False
	curr_arg = False
	temp_arg = False
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-v", "--voltage"):
			volt_arg = True
		elif o in ("-w", "--wattage"):
			watt_arg = True
		elif o in ("-i", "--current"):
			curr_arg = True
		elif o in ("-t", "--temperature"):
			temp_arg = True
		else:
			assert False, "unhandled option"
	
	#connects to server
	plugsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	plugsocket.connect(("db.sead.systems", 9000))
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
		random_temperature = randint(30, 70)
		if (watt_arg):
			send_wattage(plugsocket, random_wattage)
		if (temp_arg):
			send_temperature(plugsocket, random_temperature)
		if (volt_arg):
			send_voltage(plugsocket)
		if (curr_arg):
			send_current(plugsocket)
		time.sleep(5)

	#closes the socket at the end
	plugsocket.close()
	
if __name__ == "__main__":
	main()
