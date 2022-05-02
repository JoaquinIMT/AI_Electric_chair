#soruce: https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051 

import RPi.GPIO as GPIO
from time import sleep

#TODO: indicator leds usage

class Actuator():

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.Motor1A = 16
        self.Motor1B = 18
        self.Motor1E = 22
        
        self.Motor2A = 23
        self.Motor2B = 21
        self.Motor2E = 19
        self.setup()

    def setup(self):
        GPIO.setup(self.Motor1A,GPIO.OUT)
        GPIO.setup(self.Motor1B,GPIO.OUT)
        GPIO.setup(self.Motor1E,GPIO.OUT)
        
        GPIO.setup(self.Motor2A,GPIO.OUT)
        GPIO.setup(self.Motor2B,GPIO.OUT)
        GPIO.setup(self.Motor2E,GPIO.OUT)
    
    def motors_fw(self):
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
        
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
    
    def motors_right(self, time_mils=1):
        GPIO.output(self.Motor1A,GPIO.HIGH)
        GPIO.output(self.Motor1B,GPIO.LOW)
        GPIO.output(self.Motor1E,GPIO.HIGH)
        
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        sleep(time_mils*0.001)

    def motors_left(self, time_mils=1):
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)
        GPIO.output(self.Motor1E,GPIO.HIGH)
        
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.HIGH)
        sleep(time_mils*0.001)
    
    def motors_bw(self):
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)
        GPIO.output(self.Motor1E,GPIO.HIGH)
        
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)
        GPIO.output(self.Motor2E,GPIO.HIGH)
    
    def motors_stop(self):
        GPIO.output(self.Motor1E,GPIO.LOW)
        GPIO.output(self.Motor2E,GPIO.LOW)

    def clean_gpio(self):
        GPIO.cleanup()