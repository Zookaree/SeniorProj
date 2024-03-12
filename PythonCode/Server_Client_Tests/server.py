#!/usr/bin/python

import socket
import sys
import datetime
import time
import os
import re
import pickle
import json
import RPi.GPIO as GPIO
import pigpio

#Need to import Temperature Sensor and Distance Sensor Data eventually
#Probably Motor as well if possible
#Will also need to incoroporate some other libraries to consider
#other items such as joystick, etc.

UDP_IP = '127.0.0.1'
global UDP_PORT
UDP_PORT = 2345
BUFF_SIZE = 1024
ESC_GPIO_PIN = 12
ESC_PWM_FREQUENCY = 50
NEUTRAL_THROTTLE = 1500

#Function - distanceData()
#Function returns data taken from the 
#A02 distance sensor
#Parameters - None
def distanceData():
  distance = board.getDistance()
  print_distance(distance)
  #Delay time < 0.6s
  time.sleep(0.3)
  
#Function - set_throttle()
#Function declares the PWM signal sent
#to the T200 BlueRobotics Thruster where
#1100us is the maximum for reversal and
#1900us is the maximum for forward
#Parameters - throttle_us (a variable that 
#is the placeholder for PWM value being send to motor
def set_throttle(throttle_us):
    pi.set_servo_pulsewidth(ESC_GPIO_PIN, throttle_us)
    
#Function - temperatureData()
#Function returns the temperature data received
#from the DS18 temperature sensor
#Parameters - None
def temperatureData():
  temperature = sensor.get_temperature()
  print("The temp is %s celcius" % temperature)
  time.sleep(0.3)
  
#Function - print_distance()
#Function is a helper function to the A02
#distance sensor that prints distance and 
#various other help tasks
#Parameters - None
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
    
#Function - send_response()
#Function is a helper function to the server
#implementation of the server-client socket connection
#where it will send the reponse and data of the data 
#to the client
#Parameters - None
def send_response(response, sock, destination) :
    msg = bytes(response, 'utf-8')
    sock.sendto(msg, destination);

#Function - proc_request()
#Function is the bulk of the server code where it will
#process the requests sent by the client where the three
#commands are 'test', 'run', and 'exit'. 'run' mode is 
#the command that handles the full functionallity of WALL-C's
#movement and sensor data acquisition
#Parameters - cmd (a string received from the client), sock
#(the socket that is being communicated with), requester (the
#client that is requesting the data being sent to it)
def proc_request(cmd, sock, requester) : 
    #convert the cmd to a string
    #sensorData = sock
    cmd = bytes.decode(cmd, 'utf-8')
    now = datetime.datetime.now()
    #sensorDistance = {'distance' : distanceData()}
    print(now, "Processing: " + cmd)
    cmd = cmd.split()
    if cmd[0] == "test":
        #self explanatory duh
        print("This is a test print to let you know that the server was established")
        send_response("Test sent", sock, requester)
    elif cmd[0] == "run":
        print("WALL-C Activated")
        print("we made it here")
        while True:
            
            #Distance Data being sent via JSON
            sock.sendto(json.dumps(distanceData()).encode('utf-8'), requester)
            #Temperature Data being sent via JSON
            sock.sendto(json.dumps(temperatureData()).encode('utf-8'), requester)
            #Motor PWM signal being sent back from the client (might
            #want to just receive the data and not send it back just saying)
            receivedBytes = sock.recvfrom(4)
            tempThrottleVal = int(receivedBytes[0].decode())#.strip('\x00'))
            print(tempThrottleVal)
            set_throttle(tempThrottleVal)
            print("we set throttle again?")
            #set_throttle(int(receivedBytes[0].decode()))
    elif cmd[0] == "exit":
        #this command exits the server-client socket
        send_response("Server Exited", sock, requester)
    else:
        #This is just a catch all, should never get here unless intentional
        send_response("Data Not Sent", sock, requester)

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
    GPIO.setmode(GPIO.BOARD)
    pi = pigpio.pi()
    pi.set_PWM_frequency(ESC_GPIO_PIN, ESC_PWM_FREQUENCY)
    set_throttle(NEUTRAL_THROTTLE)
    
    dis_min = 0;
    dis_max = 4500;
    
    board.set_dis_range(dis_min, dis_max)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Internet UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    try:
        data, addr = sock.recvfrom(BUFF_SIZE)
        proc_request(data, sock, addr)

    except KeyboardInterrupt:
        pass
        
    finally:
        pi.set_servo_pulsewidth(ESC_GPIO_PIN, 0)
        pi.stop()
        
