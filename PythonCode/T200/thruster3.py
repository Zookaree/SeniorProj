import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ESC_GPIO_PIN = 12

ESC_PWM_FREQUENCY = 1500

ESC_THROTTLE_REVERSE = 1100
ESC_THROTTLE_FORWARD = 1900

GPIO.setup(ESC_GPIO_PIN, GPIO.OUT)
pwm = GPIO.PWM(ESC_GPIO_PIN, ESC_PWM_FREQUENCY)
pwm.start(50)

def set_throttle(throttle_us):
	cycle = throttle_us / 20000.0 * 100
	pwm.ChangeDutyCycle(cycle)
	
try:
	
	set_throttle(ESC_THROTTLE_REVERSE)
	time.sleep(5)
	
	set_throttle(ESC_THROTTLE_FORWARD)
	time.sleep(5)
	
except KeyboardInterrupt:
	pass
	
finally:
	pwm.stop()
	GPIO.cleanup()
