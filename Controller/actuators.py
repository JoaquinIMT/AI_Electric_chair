#soruce: https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051 

import RPi.GPIO as GPIO
from time import sleep

#TODO: indicator leds usage

class Actuator():

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.Motor1A = 17
        self.Motor1B = 18
         
        self.Motor2A = 23
        self.Motor2B = 22
        self.seconds_buzz = 0.5
        self.buzz = 21
        self.setup()

        

    def setup(self):
        GPIO.setup(self.Motor1A,GPIO.OUT)
        GPIO.setup(self.Motor1B,GPIO.OUT)

        
        GPIO.setup(self.Motor2A,GPIO.OUT)
        GPIO.setup(self.Motor2B,GPIO.OUT)

        GPIO.setup(self.buzz,GPIO.OUT)
    
    def buzz_one():
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1

    def buzz_twice():
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1

    def buzz_tree():
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,True) #in1
        sleep(self.seconds_buzz)
        GPIO.output(self.buzz,False) #in1

    def motors_fw(self):
        #IZQUIERDA
        GPIO.output(self.Motor1A,True) #in1
        GPIO.output(self.Motor1B,False) #in2

        #DERECHA
        GPIO.output(self.Motor2A,False)#in3
        GPIO.output(self.Motor2B,True) #in4

    
    def motors_right(self, time_mils=1):
        GPIO.output(self.Motor1A,True)
        GPIO.output(self.Motor1B,False)

        GPIO.output(self.Motor2A,True)
        GPIO.output(self.Motor2B,False)

       # sleep(time_mils*0.001)

    def motors_left(self, time_mils=1):
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)

        
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.HIGH)

       # sleep(time_mils*0.001)
    
    def motors_bw(self):
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.HIGH)

        
        GPIO.output(self.Motor2A,GPIO.HIGH)
        GPIO.output(self.Motor2B,GPIO.LOW)

    
    def motors_stop(self):
        GPIO.output(self.Motor1A,GPIO.LOW)
        GPIO.output(self.Motor1B,GPIO.LOW)

        
        GPIO.output(self.Motor2A,GPIO.LOW)
        GPIO.output(self.Motor2B,GPIO.LOW)

    def clean_gpio(self):
        GPIO.cleanup()

""" motores = Actuator()
motores.setup()

while True:
    try:
        #motores.motors_fw()
        #motores.motors_bw()
    except:
        motores.clean_gpio()
 """