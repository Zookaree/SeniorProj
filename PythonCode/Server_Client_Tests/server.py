#!/usr/bin/python

import socket
import sys
import datetime
import time
#Need to import Temperature Sensor and Distance Sensor Data eventually
#Probably Motor as well if possible
#Will also need to incoroporate some other libraries to consider
#other items such as joystick, etc.


UDP_IP = '127.0.0.1'
global UDP_PORT
UDP_PORT = 2345
BUFF_SIZE = 1024

def proc_request(cmd, sock, requester) : 
    #convert the cmd to a string
    cmd = bytes.decode(cmd, 'utf-8')
    now = datetime.datetime.now()
    print(now, "Processing: " + cmd)
    cmd = cmd.split()
    if cmd[0] == "test":
        print("This is a test print to let you\
        know that the server was established")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        UDP_PORT = int(sys.argv[1])
        
    print ("UDP target IP:", UDP_IP)
    print ("UDP targer Port:", UDP_PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    #get data from client, addr is who sent it (i.e. rpi client)
    #FOR UDP CONNECTIONS, LISTEN AND ACCEPT DO NOT NEED TO HAPPEN
    #BECASUSE UDP YOU DONT NEED TO VERIFY A CONNECTIONS
    
    try:
        while True:
            data, addr = sock.recvfrom(BUFF_SIZE) 
            proc_request(data, sock, addr)
        
    except KeyboardInterrupt:
        print("Failed. Cleaning GPIO")
        GPIO.cleanup()
        
    conn.close()
    sock.close()
