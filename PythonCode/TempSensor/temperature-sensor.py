import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temp is  %s celcius" % temperature)
    time.sleep(1)
