import RPi.GPIO as gpio
import time

in1 = 16
in2 = 18

gpio.setmode(gpio.BOARD)

gpio.setup(in1, gpio.OUT)
gpio.setup(in2, gpio.OUT)


gpio.output(in1, False)
gpio.output(in2, False)


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