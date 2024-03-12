import pigpio
import time

ESC_GPIO_PIN = 12

ESC_PWM_FREQUENCY = 50

NEUTRAL_THROTTLE = 1500

pi = pigpio.pi()

def set_throttle(throttle_us):
	pi.set_servo_pulsewidth(ESC_GPIO_PIN, throttle_us)

try: 
	pi.set_PWM_frequency(ESC_GPIO_PIN, ESC_PWM_FREQUENCY)
	set_throttle(NEUTRAL_THROTTLE)
	time.sleep(5)
	
	set_throttle(1550)
	time.sleep(7)
	
except KeyboardInterrupt:
	pass
	
finally:
	pi.set_servo_pulsewidth(ESC_GPIO_PIN, 0)
	pi.stop()
