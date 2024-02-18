# -*- coding:utf-8 -*-

'''!
  @n --------------------------------------------
  @n sensor pin |         raspberry pi          |
  @n     VCC    |            5V/3V3             |
  @n     GND    |             GND               |
  @n     RX     |          (BCM)14 TX           |
  @n     TX     |          (BCM)15 RX           |
  @n --------------------------------------------
'''

import sys
import os
import time
import socket
import re

def clientFunc():
  s = socket.socket()  # Create a socket object
  port = 8080  # Reserve a port for your service every new transfer wants a new port or you must wait.

  s.connect(('localhost', port))
  x = 0

  st = str(x)
  byt = st.encode()
  s.send(byt)

  # send message for hundred times
  while x < 100:
    st = str(x)
    byt = st.encode()
    s.send(byt)
    print(x)

    data = s.recv(1024)
    if data:
      print(data)
      x += 1
      break
    else:
      print('no data received')

  print('closing')
  s.close()
  
def distanceData():
  distance = board.getDistance()
  print_distance(distance)
  #Delay time < 0.6s
  time.sleep(0.3)
    
def temperatureData():
  temperature = sensor.get_temperature()
  print("The temp is  %s celcius" % temperature)
  time.sleep(1)
  
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_RaspberryPi_A02YYUW import DFRobot_A02_Distance as Board
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
board = Board()

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

if __name__ == "__main__":
  #Minimum ranging threshold: 0mm
  dis_min = 0 
  #Highest ranging threshold: 4500mm  
  dis_max = 4500 
  board.set_dis_range(dis_min, dis_max)

  
  while True:
    distanceData()
    temperatureData()
    
