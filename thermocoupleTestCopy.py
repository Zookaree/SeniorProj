import time
import board
import digitalio
#in order to use adafruit_max31855 library you have to follow these steps:
# learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
# if you are using another machine or a computer to code with this code, I am unsure how to
# get this library
import adafruit_max31855
import sys
#Must have source env/bin/active on
spi = board.SPI()
cs_1 = digitalio.DigitalInOut(board.D5) #GPIO 5
cs_2 = digitalio.DigitalInOut(board.D17) #GPIO 17
cs_3 = digitalio.DigitalInOut(board.D27) #GPIO 27
cs_4 = digitalio.DigitalInOut(board.D22) #GPIO 22

#ALL OF THESE SHARE THE SAME spi, clk and MISO PIN
max31855_1 = adafruit_max31855.MAX31855(spi, cs_1) 
max31855_2 = adafruit_max31855.MAX31855(spi, cs_2)
max31855_3 = adafruit_max31855.MAX31855(spi, cs_3)
max31855_4 = adafruit_max31855.MAX31855(spi, cs_4)

#def proc_temp(temperature):
#	tempFarenheit = temperature * 9/5 + 32
#	print("Temperature: {} C {} F ".format(temperature, tempFarenheit))
	

int_val = 0

#this line prints the time when file is ran:
# YEAR-MONTH-DAY__HOUR-MINUTE-SECOND
moment = time.strftime("%Y-%b-%d__%H_%M_%S", time.localtime())

dataFile = open('output'+moment+'.txt', 'w')

while True:
	#Solves for Celcius Temperature per sensor
	tempCelcius_1 = max31855_1.temperature
	tempCelcius_2 = max31855_2.temperature
	tempCelcius_3 = max31855_3.temperature
	tempCelcius_4 = max31855_4.temperature
	
	#Solves for Farenheit Temperature per sensor
	tempFarenheit_1 = tempCelcius_1 * 9/5 + 32
	tempFarenheit_2 = tempCelcius_2 * 9/5 + 32
	tempFarenheit_3 = tempCelcius_3 * 9/5 + 32
	tempFarenheit_4 = tempCelcius_4 * 9/5 + 32
	
	#Outputs the sensor data to a text file that is updated everytime it is ran
	
	#print("Sensor 5 Data")
	dataFile.write("Temperature: {} C {} F \n".format(tempCelcius_1, tempFarenheit_1))
	#print("Sensor 17 Data")
	dataFile.write("Temperature: {} C {} F \n".format(tempCelcius_2, tempFarenheit_2))
	#print("Sensor 27 Data")
	dataFile.write("Temperature: {} C {} F \n".format(tempCelcius_3, tempFarenheit_3))
	#print("Sensor 22 Data")
	dataFile.write("Temperature: {} C {} F \n".format(tempCelcius_4, tempFarenheit_4))
	#This line is used to delimit readings when looking at data.txt file output
	dataFile.write("-\n")
	
	#CHANGE THIS IF YOU WANT MORE READINGS i.e. .1 = 1/10 of a second, .05 = 1/20 of a second, etc.
	time.sleep(.1) 
	#int_val += 1
	#print("This is the", int_val, "iteration")
