#!/usr/bin/python
print "Content-type:text/plain"
print ""

import socket
import sys
import os
import cgi, cgitb

form = cgi.FieldStorage()

cmd = form.getvalue('cmd')

def send_message(message, remote_ip):
    
    #create an AF_INET, STREAM socket(TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code:' + str(msg[0]) + ', Error message : ' + msg[1]
        sys.exit()
    
    print "Socket Created"
    
    host = remote_ip
    port = 8888
    
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print "Hostname could not be resolved. Exiting"
        sys.exit()
    
    print "Ip address of " + host + " is " + remote_ip
    #connect to remote server
    try:
        s.connect((remote_ip, port))
    except socket.error, msg:
        print "Error code:" + str(msg[0]) + ', Error message :' + msg[1]
        sys.exit()

    print "Socket Connected to " + host + " on ip " + remote_ip
   
    #send some data to remote server
    try:
        #send the whole string
        s.sendall(message)
    except socket.error:
        print "send failed"
        sys.exit()
    
    print "Message sent successfully"
    
    #now receive data
    reply = s.recv(4096)
    
    print reply
    
    #close 
    s.close()

def close_chat():
   os.system('killall -KILL chat_server.py') 

def connect_remote(remote_ip):
    #create an AF_INET, STREAM socket(TCP)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code:' + str(msg[0]) + ', Error message : ' + msg[1]
        sys.exit()
    
    print "Socket Created"
    
    host = remote_ip
    port = 8888
    
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print "Hostname could not be resolved. Exiting"
        sys.exit()
    
    print "Ip address of " + host + " is " + remote_ip
    #connect to remote server
    try:
        s.connect((remote_ip, port))
    except socket.error, msg:
        print "Error code:" + str(msg[0]) + ', Error message :' + msg[1]
        sys.exit()

    print "Socket Connected to " + host + " on ip " + remote_ip

    s.close()

#def clear_history():

if __name__ == "__main__":
    if cmd == "send_msg":
        message = form.getvalue('msg')
        remote_ip = form.getvalue('remote_ip')
        send_message(message, remote_ip)
    elif cmd == "close_chat":
        close_chat()
    elif cmd == "connect_remote":
        remote_ip = form.getvalue('remote_ip')
        connect_remote(remote_ip)
        

