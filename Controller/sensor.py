import RPi.GPIO as GPIO
import time


class Sensor():
    def __init__(self):
        self.trig = 10 ### trig
        self.echo = 9 ## echo
        GPIO.setmode(GPIO.BCM)
        self.pulse_start=0
        self.pulse_end=0
        self.setup()

    def setup(self):
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

    def sense(self):
        GPIO.output(self.trig,False)
        time.sleep(0.000002)
        GPIO.output(self.trig,True)
        time.sleep(0.00001)
        GPIO.output(self.trig,False)
        while GPIO.input(self.echo)==0:
            self.pulse_start=time.time()
        while GPIO.input(self.echo):
            self.pulse_end=time.time()
        return self.calculate_distance()
    
    def calculate_distance(self):
        # distance=(0.034/2)*self.pulse_end
        self.pulse_duration=self.pulse_end-self.pulse_start
        distance=self.pulse_duration*17150
        distance = round(distance,2)

        #print('Distancia',distance,'cm')
        return distance

"""ultrasonic = Sensor()
#ultrasonic.setup()


while True: 
    try:
        distance = ultrasonic.sense()
        #distance =ultrasonic.calculate_distance()
        print('distancia aqui',distance)

    except KeyboardInterrupt:
        GPIO.cleanup() """



# while True:
#     try:
#         GPIO.output(pito,True) #in1

#     except:
#         GPIO.cleanup()
