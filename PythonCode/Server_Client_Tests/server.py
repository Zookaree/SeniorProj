import RPi.GPIO as GPIO
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

if __name__ == '__main__':
    if len(sys.argv) == 1:
        UDP_PORT = int(sys.argv[1])
        
    print ("UDP target IP:", UDP_IP)
    print ("UDP targer Port:", UDP_PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    #get data from client, addr is who sent it (i.e. rpi client)
    sock.listen(9)
    conn, address = sock.accept()
    #data, addr = sock.recvfrom(BUFF_SIZE) 
    
    print("Connected to address:", address)
    
    try:
        while True:
            result = instance.read();
            if result.is_valid():
                print("Last Valid Input: " + str(datetime.datetime.now()))
                print("Server sent data!!")
                conn.send(0)
                time.sleep(6)
        
    except KeyboardInterrupt:
        print("Failed. Cleaning GPIO")
        GPIO.cleanup()
        
    conn.close()
    sock.close()
