#!/usr/bin/python
# ============================================================
# File: client.py
# Description: This sends the file called temp to the server
# Created by Henry Crute
# 6/30/2014
# ============================================================

import socket
import sys

#connects to server
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("db.sead.systems", 8089))
#opens file to be read
file = open("temp", "rb")
segment = file.read(1024)
while (segment):
   clientsocket.send(segment)
   segment = file.read(1024)
clientsocket.close()

