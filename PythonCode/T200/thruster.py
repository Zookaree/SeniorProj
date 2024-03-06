from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x40)

#1100us --> 272 Full Power Reverse
#1500us --> 387 Stopped
#1900us --> 502 Full Power Forward

signal = 387
signalDir = 1
looping = True
logic = False

pwm.setPWMFreq(int(60 * 0.9))
pwm.setPWM(0, 0, 387)
time.sleep(3)
print("ESC Initialized")

try:
	while(looping):
		if (signal == 502):
			signalDir = 1
		if (signal == 272):
			signalDir = 1
			logic = True
		if (signal == 387 and logic == True):
			looping = False
			
		pwm.setPWM(0, 0, signal)
		time.sleep(0.2)
		
		#print(signal)
		signal += signalDir
		
except KeyboardInterrupt:
	print("User Cancelled")
	
finally:
	pwm.setPWM(0,0,0)
	quit()
