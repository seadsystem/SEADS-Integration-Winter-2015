#!/usr/bin/env python2
# ============================================================
# File: raineagletalk.py
# Description: Gets summation used between ~5 minute intervals
# Created by Henry Crute
# 8/4/2014
# Modified by Andrew Ringer on 2/12/15
# ============================================================

import sys
import socket
sys.path.insert(0, '/home/pi/eagle/pi/neighborhood')
import RainEagle
import EagleSearch
import time

raineagle = None

def get_instantaneous(id):
	demand = int(device_data['InstantaneousDemand']['Demand'], 16)
	multiplier = int(device_data['InstantaneousDemand']['Multiplier'], 16)
	divisor = int(device_data['InstantaneousDemand']['Divisor'], 16)
	timestamp = int(device_data['InstantaneousDemand']['TimeStamp'], 16)
	#checks to see if multiplier or divisor is 0
	if (multiplier == 0): multiplier = 1
	if (divisor == 0): divisor = 1
	if demand > 0x7fffffff:
		# Value is negative.
		# Hex 0x7fffffff is the maximum value an 8-bit signed int can have.
		# This method bitwise-ORs the energyInput1 value against
		#   a negative 8-bit mask to obtain the negative value.
		actualDemand = (float(demand) | ~0xffffffff) * float(multiplier) / float(divisor)
	else:
		actualDemand = float(demand) * float(multiplier) / float(divisor)
	return actualDemand

def format_print(cs, sumfile):
	for elem in cs:
		timestamp = int(elem['TimeStamp'], 16)
		value = elem['Value']
		sumfile.write(str(timestamp) + "," + str(value) + "\n")
	sumfile.close()
	exit(0)

def eagle_search():
	addresses = EagleSearch.return_addresses()[0]
	for ip in addresses:
		try:
			raineagle = RainEagle.Eagle(debug=0, addr=ip)
			print("Accepted IP: %s" % ip)
			return raineagle
		except:
			e = sys.exc_info()[0]
			print "error: %s" % e

def try_get_data():
	while 1:
		try:
			data = raineagle.get_device_data()
			return data
		except:
			e = sys.exc_info()[0]
			print "error: %s" % e
			raineagle = eagle_search()

def send_data(send_data):
	#init a connection to the server
	plugsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	plugsocket.connect(("db.sead.systems", 9000))

	#TODO: actually look at what the server sends

	header_size = 28
	header = bytearray(b"L00THS100000t00000000000500X")
	header[1] = (header_size & 0xFF)
	header[2] = (header_size >> 8)

	#TODO: timestamp

	print header
	plugsocket.sendall(header)

	data_size = 44
	data = bytearray(b"L00TWlIt00000000000000P00000005000000C01D01X")
	data[1] = (data_size & 0xFF)
	data[2] = (data_size >> 8)
	data[38] = 1
	data[39] = 0
	data[41] = (send_data & 0xFF)
	data[42] = ((send_data & 0xFF00) >> 8)

	#TODO: timestamp

	print data
	plugsocket.sendall(data)
	plugsocket.close()

raineagle = eagle_search()
#raineagle = RainEagle.Eagle(debug=0, addr=address)
#ret_data = raineagle.list_devices()

#/macId = ret_data['DeviceInfo']['DeviceMacId']
#print macId

#comparison variables for demand
previousDemand = 0
previousTimestamp = 0
#comparison variables for summations
tempdata = try_get_data()
tempdata = tempdata['CurrentSummation']
sumTimestamp = int(tempdata['TimeStamp'], 16)
sumReceived = int(tempdata['SummationReceived'], 16) * int(tempdata['Multiplier'], 16) / float(int(tempdata['Divisor'], 16))
sumDelivered = int(tempdata['SummationDelivered'], 16) * int(tempdata['Multiplier'], 16) / float(int(tempdata['Divisor'], 16))

counter = 0 #counter for looping

while 1:
	file = open('sample.txt', 'a')
	#######################obtains demand for kWh calculation
	'''
	try:
		device_data = raineagle.get_instantaneous_demand(macId)
	except:
		e = sys.exc_info()[0]
		print "Error: %s" % e
		file.close()
		continue
	actualDemand = get_instantaneous(device_data)
	timestamp = int(device_data['InstantaneousDemand']['TimeStamp'], 16)
	if ((previousDemand != actualDemand) and (previousTimestamp != timestamp)):
		previousDemand = actualDemand
		previousTimestamp = timestamp
	 	#sys.stdout.write("%d,%.3f\n" % (timestamp, actualDemand))
	#else:
		#print "these are the same :("
	'''
	#######################obtains summation values after 12 demand counts
	if (counter == 19):
		try:
			device_data = raineagle.get_device_data()
		except:
			e = sys.exc_info()[0]
			print "error: %s" % e
			#try to search for eagle, and resets ip's
			raineagle = eagle_search()
			#ret_data = raineagle.list_devices()
			#macId = ret_data['DeviceInfo']['DeviceMacId']
			file.close()
			continue

		summation = device_data['CurrentSummation']
		multiplier = int(summation['Multiplier'], 16)
		divisor = int(summation['Divisor'], 16)
		delivered = int(summation['SummationDelivered'], 16)
		received = int(summation['SummationReceived'], 16)
		timestamp = int(summation['TimeStamp'], 16)

		if multiplier == 0:
			multiplier = 1
		if divisor == 0:
			divisor = 1

		reading_received = received * multiplier / float(divisor)
		reading_delivered = delivered * multiplier / float(divisor)
		timeDiff = (timestamp - sumTimestamp)
		receivedkWh = (reading_received - sumReceived)
		deliveredkWh = (reading_delivered - sumDelivered)
		#print "previousSum (r, d) = " + str(sumReceived) + ", " + str(sumDelivered)

		#sendstr = "timestamp = " + str(timestamp + 946684800) + "#\n"
		#print "sending %s" % sendstr
		#file.write(sendstr)

		#sendstr = "timestamp - sumTimestamp = " + str(timeDiff) + "#\n"
		#print "sending %s" % sendstr
		#file.write(sendstr)

		#sendstr = "delivered - received = " + str(deliveredkWh - receivedkWh) + "#\n"
		#print "sending %s" % sendstr
		#file.write(sendstr)

		#data = (data * 3600 * 40) / sample_duration
		data = deliveredkWh - receivedkWh
		#TODO: division by 0 issue
		data = (data * 3600 * 40 * 1000) / timeDiff
		print "sending data " + str(int(data))
		send_data(int(data))

		sumTimestamp = timestamp
		sumReceived = reading_received
		sumDelivered = reading_delivered
		counter = 0
	else:
		counter = counter + 1

	#ending of loop
	file.close()
	time.sleep(15)

