#!/usr/bin/python

import socket
import thread

LOCAL_IP = socket.gethostbyname(socket.gethostname()) # Gets local IP address

IP_ADDRESS_LIST = [] # Holds all the IP addresses

vlock = thread.allocate_lock() # Thread lock for IP_ADDRESS_LIST

NICKNAME_DICT = {LOCAL_IP:LOCAL_IP} # Dictionary that is mapped as ip_addr to nickname

PORT = 7721 # Port to send packets on

DEBUG = 1

def PrintToScreen(str):
	print str

# Purpose: This is a major function.  It handles all incoming packets in a seperate thread (so the user
#           can still input content).
# Example Input: None
# Returns: None
# Error Returns: None
# Comments: This is a complex function
def ListenToSocket():
	global PORT
	global LOCAL_IP
	global IP_ADDRESS_LIST
	global vlock
	global NICKNAME_DICT

	PrintToScreen(('Nick: '+NICKNAME_DICT[LOCAL_IP], 'Local IP:'+LOCAL_IP, 'Port:'+str(PORT), IP_ADDRESS_LIST))

	while 1:
		d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Make main socket, notice it is a datagram socket
		d.bind(('', PORT)) # Make it listen to the port we specified
		while 1:
			data, addr = d.recvfrom(1024) # Recieve up to 1 Megabyte and put it in data, addr[0] contains senders ip addr.
			if not data: break # if no data, stop
			if not addr[0] in IP_ADDRESS_LIST and addr[0] != LOCAL_IP: # if addr is not in our master list and if its not our own...
				vlock.acquire()  # Lock global list to not corrupt memory
				IP_ADDRESS_LIST.append(addr[0]) # append ip addr to list
				NICKNAME_DICT[addr[0]] = addr[0] # append new nickname
				vlock.release() # Release lock
				SendSyncSuggestion() # tell others we just got a new guy (connection)

			if data[:16] == r'\sync_suggestion': # A peer notifies us that they got a new connection
				SyncRequest() # request that all our peers sync
				PrintToScreen(NICKNAME_DICT[addr[0]] + ' has joined.')
				continue

			if data[:5] == r'\quit':
				vlock.acquire()
				IP_ADDRESS_LIST.remove(addr[0])
				del NICKNAME_DICT[addr[0]]
				vlock.release()


			if data[:13] == r'\sync_request': # someone replied to our sync_suggestion
				dbg('got sync request') # Debug Only
				SyncData() # give all peers our data
				continue

			if data[:10] == r'\sync_data': # our peers have sent us their sync data
				dbg('got sync data')
				TEMP_IP_ADDR_LIST = str(data[11:]).split('|') # take string of ip addresses and turn it into a list
				dbg(TEMP_IP_ADDR_LIST) # Debug Only
				for temp_ip in TEMP_IP_ADDR_LIST:
					if not temp_ip in IP_ADDRESS_LIST and temp_ip != LOCAL_IP: # if ip addr is not in our list and isn't our own ip...
						vlock.acquire()  # Lock global list to not corrupt memory
						IP_ADDRESS_LIST.append(temp_ip) # append ip to list
						vlock.release() # Release lock
				continue

			if data[:10] == r'\nick_data': # Someone changed their nickname and sent their nickname sync data
				dbg('got nick sync data')
				TEMP_NICKNAME_LIST = str(data[11:]).split(';')
				dbg('TEMP_NICKNAME_LIST = ' + str(TEMP_NICKNAME_LIST))
				for temp_nick in TEMP_NICKNAME_LIST:
					dbg('temp_nick = '+ temp_nick)
					small_list = temp_nick.split('|')
					dbg(small_list)
					dbg('key: ' + small_list[0] + 'value: ' + small_list[1])
					vlock.acquire() # lock thread access to variable
					NICKNAME_DICT[small_list[0]] = small_list[1] # IP Address key, actual value for values
					vlock.release() # release lock
				continue

			if data[:7] == r'\pubkey':
				global PubKey_OtherGuy, PubKey_string
				if len(PubKey_OtherGuy) != 0:
					continue
				PubKey_OtherGuy = tuple(map(int, data[8:-1].split(','))) # Take string and turn it into a tuple full of ints
				try:

					e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					e.sendto('\pubkey'+PubKey_string, (addr[0], PORT))
					e.close()
				except:

					dbg(str(('\pubkey'+ PubKey_string, addr[0], PORT)))
					PrintToScreen('Could not send Public Key to: ' + addr[0])
				continue


			if data[:10] == r'\encrypted':
				try:
					data = decrypt(data[10:])
				except:
					PrintToScreen('Cannot decrypt message')
					if DEBUG == 1:
						traceback.print_exc()
					continue
				try:
					data = unsign(data)
				except:
					PrintToScreen('Cannot unsign message.  The message was most likely not sent by the person you think it is (Man in the Middle attack possible)')
					if DEBUG == 1:
						traceback.print_exc()
					continue

				PrintToScreen(NICKNAME_DICT[addr[0]] + '**: ' + str(data))

				continue

			PrintToScreen(NICKNAME_DICT[addr[0]] + ': ' + str(data))

		d.close()


