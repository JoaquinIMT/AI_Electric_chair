class OptionTaker():
    def __init__(self):
        pass

    def input_process(self,face_input,obstacule_input,sensors_input):
        #TODO: Reci ve face parameters, obstacule parameters, sensor parameters AND homogenize its values to something to analize
        self.input_dict = {
            "face":0,
            "obstacule":0,
            "sensor":0
        }
        pass

    def desicion_maker(self):
        #TODO: Case scenario value analizis
        #face has signal
        #Obstacule distance above treshold
        #Sensor OK
        #DO MOVEMENT
        pass

    def face_status(self):
        #IF PAUSE, stop sensing obstacules from camera
        #IF IN MOVEMENT KEEP SENSOR ACTIVE.