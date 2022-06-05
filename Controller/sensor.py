import RPi.GPIO as GPIO
import time


class Sensor():
    def __init__(self):
        self.trig = 10 ### trig
        self.echo = 9 ## echo
        GPIO.setmode(GPIO.BCM)

    def setup(self):
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

    def sense(self):
        pass
    
    def calculate_distance(self):
        pass