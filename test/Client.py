#!/usr/local/bin/python
# encoding: utf-8
'''
@author: Cenbylin
'''
import socket
import sys

HOST, PORT = "localhost", 9999
data = "aaa"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
sock.connect((HOST, PORT))
sock.sendall(bytes(data + "\n"))
# Receive data from the server and shut down
received = str(sock.recv(1024))


print("Sent:     {}".format(data))
print("Received: {}".format(received))