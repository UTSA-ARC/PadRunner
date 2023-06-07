import RPi.GPIO as gpio
import time
import threading
import queue

from config import *
from functions import *

gpio.setmode(gpio.BOARD)

for pin in PINS.values(): # Iterate through relay pins and make each an output
    gpio.setup(pin, gpio.OUT)

try:
    
    while True:
        for x in range(5):
            gpio.output(in1, True)
            time.sleep(0.1)
            gpio.output(in1, False)
            gpio.output(in2, True)
            time.sleep(0.1)
            gpio.output(in2, False)
        

        gpio.output(in1,True)
        gpio.output(in2,True)
        

        for x in range(4):
            gpio.output(in1, True)
            time.sleep(0.05)
            gpio.output(in1, False)
            time.sleep(0.05)
        gpio.output(in1,True)

        for x in range(4):
            gpio.output(in2, True)
            time.sleep(0.05)
            gpio.output(in2, False)
            time.sleep(0.05)
        gpio.output(in2,True)

except KeyboardInterrupt:
    
    gpio.cleanup()