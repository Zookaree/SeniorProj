#!/usr/bin/env python3
#####################################################################################
# Filename    : LogicAnalyzer_UART.py
# Description : Logic_Analyzer_With_UART
# Author      : Bob Fryer / Digital Shack
# modification: 22 Feb 2020
#####################################################################################
#####################################################################################
# Import the required Python Libraries
#####################################################################################
import  serial, time 
import  RPi.GPIO as GPIO
#####################################################################################
# Initialise the Serial Port (ttys0) and flush any serial data from the buffers
#####################################################################################
ser  =  serial.Serial(port  =  "/dev/serial0" , baudrate = 9600 , timeout = 2 )
if  (ser.isOpen()  ==  False):
    ser. open ()                                       # check and open Serial0
ser.flushInput()                                       # clear the UART Input buffer
ser.flushOutput()                                      # clear the UART output buffer
#####################################################################################
# Define our one and only variable
#####################################################################################
echostring  =  "Talking to ourselves!"
#####################################################################################
# Define our main task
#####################################################################################
def echotest():
    while (True):                                      # loop
        ser.flushInput()                    # Clear UART Input buffer
        ser.flushOutput()                              # Clear UART Output buffer
        ser.write(echostring.encode())                 # write our String in bytes
        print ('What we sent: ', echostring)           # Print what we sent
        time.sleep(0.5)                                # give it a sec to be recvd
        echostringrec = ser.readline().decode("utf-8") # read the rec buffer as UTF8
        print ('What we received: ', echostringrec)    # Print what we received
#####################################################################################
# Define our DESTROY Function
#####################################################################################
def destroy():
    ser.close ()                                          # Closes the serial port
    print ("test complete")
#####################################################################################
# Finally the code for the MAIN program
#####################################################################################
if __name__ == '__main__':                                 # Program entry point
    try:
        echotest()                                         # call echotest function
    except KeyboardInterrupt:                              # Watches for Ctrl-C
        destroy()                                          # call destroy function
    finally:
        destroy()                                          # call destroy function