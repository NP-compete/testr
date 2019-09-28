#!/usr/bin/python

import socket
import sys
import os
from thread import *

'''
f = open('text', 'w')
f.write(os.environ.get('QUERY_STRING'))
f.close()
'''
HOST = ''
PORT = 8888

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code:' + str(msg[0]) + ', Error message : ' + msg[1]
    sys.exit()

print "Socket Created"

#bind
try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print "Bind failed. Error Code : " + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print "Socket bind complete"

s.listen(10)

print "Socket now listening"

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n')# send() only takes string

    #infinite loop so function do not terminate and thread do not end
    while True:
        data = conn.recv(1024)
        reply = "OK..." + data
        if not data:
            break
        f = open('text', 'a')
        message = "<p>" + data + "</p>" + "\n"
        f.write(data)
        f.close()

        conn.sendall(reply)
    #come out of loop
    conn.close()

#now keep talking with client
while 1:
    #wait to accept a connect - blocking call
    conn, addr = s.accept()

    #display client information
    print "Connected with " + addr[0] + ":" + str(addr[1])

    #start new thread takes 1st argument as a function name to be run. send is the tuple
    start_new_thread(clientthread,(conn,))
    
s.close()
