#!/usr/bin/python

import socket
import sys
import datetime
import time
import os
import re
import pickle
import json

#Need to import Temperature Sensor and Distance Sensor Data eventually
#Probably Motor as well if possible
#Will also need to incoroporate some other libraries to consider
#other items such as joystick, etc.

UDP_IP = '127.0.0.1'
global UDP_PORT
UDP_PORT = 2345
BUFF_SIZE = 1024

def distanceData():
  distance = board.getDistance()
  print_distance(distance)
  #Delay time < 0.6s
  time.sleep(0.3)
    
def temperatureData():
  temperature = sensor.get_temperature()
  print("The temp is %s celcius" % temperature)
  time.sleep(0.3)

def print_distance(dis):
  if board.last_operate_status == board.STA_OK:
    print("Distance %d mm" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECKSUM:
    print("ERROR")
  elif board.last_operate_status == board.STA_ERR_SERIAL:
    print("Serial open failed!")
  elif board.last_operate_status == board.STA_ERR_CHECK_OUT_LIMIT:
    print("Above the upper limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_CHECK_LOW_LIMIT:
    print("Below the lower limit: %d" %dis)
  elif board.last_operate_status == board.STA_ERR_DATA:
    print("No data!")

def send_response(response, sock, destination) :
    msg = bytes(response, 'utf-8')
    sock.sendto(msg, destination);

def proc_request(cmd, sock, requester) : 
    #convert the cmd to a string
    #sensorData = sock
    cmd = bytes.decode(cmd, 'utf-8')
    now = datetime.datetime.now()
    #sensorDistance = {'distance' : distanceData()}
    print(now, "Processing: " + cmd)
    cmd = cmd.split()
    if cmd[0] == "test":
        print("This is a test print to let you know that the server was established")
        send_response("Test sent", sock, requester)
    elif cmd[0] == "run":
        while True:
            print("WALL-C Activated")
            #sensorDistance = {'distance' : distanceData()}
            sock.sendto(json.dumps(distanceData()).encode('utf-8'), requester)
            sock.sendto(json.dumps(temperatureData()).encode('utf-8'), requester)
    elif cmd[0] == "exit":
        send_response("Server Exited", sock, requester)
    else:
        send_response("Data Not Sent", sock, requester)
        #sensorTemp = {'temperature' : temperatureData()}
        #sock.sendto(json.dumps(distanceData()).encode('utf-8'), (UDP_IP, UDP_PORT))
        #sock.sendto(json.dumps(sensorTemp).encode('utf-8'), requester)

from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board
from w1thermsensor import W1ThermSensor

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

sensor = W1ThermSensor()
board = Board()
        
if __name__ == '__main__':
    if len(sys.argv) == 2:
        UDP_PORT = int(sys.argv[1])
        
    print ("UDP target IP:", UDP_IP)
    print ("UDP targer Port:", UDP_PORT)
    
    dis_min = 0;
    dis_max = 4500;
    
    board.set_dis_range(dis_min, dis_max)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        data, addr = sock.recvfrom(BUFF_SIZE) 
        proc_request(data, sock, addr)
