from Controller.actuators import Actuator
from Face_Gestures.predictor import do_classification
from Face_Gestures.Facemesh_V2 import Facemesh_V2
from Communication.store_value import StoreValues
from Controller.sensor import Sensor
import threading
from time import sleep

face_values = StoreValues()
face_mesh = Facemesh_V2(face_values,classifier='lips_gesture_prediction')
actuator = Actuator()


def do_logic(face_values,actuator):
    while True:
        sleep(0.5)
        if face_values.esperar_instruccion:
            if face_values.mout == 'sonrisa':
                face_values.esperar_instruccion = False
                print("========================EMPIEZA PROGRAMAAAAA, ESPERANDO INSTRUCCION")
        else:
            if face_values.mout == 'boca_abierta' and not face_values.obstacule_detected:
                print("========================actuator.motors_fw()")
                face_values.finish_process = True
                actuator.motors_fw()
            elif face_values.eye == 'ojo_derecho' and face_values.mout == 'neutral':
                print("========================actuator.motors_right()")
                face_values.finish_process = True
                actuator.motors_right()
            elif face_values.eye == 'ojo_izquierdo' and face_values.mout == 'neutral':
                print("========================actuator.motors_left()")
                face_values.finish_process = True
                actuator.motors_left()

            if face_values.finish_process and face_values.eye == 'neutral' and face_values.mout == 'neutral':
                actuator.motors_stop()
                face_values.esperar_instruccion = True

        if face_values.finished:
            break

def do_sensing(face_values,actuator,limit_distance=25):
    ultrasonic = Sensor()
    
    while True:
        distance = ultrasonic.sense()
        
        if distance < limit_distance:
            actuator.motors_stop()
            face_values.obstacule_detected = True
        elif face_values.obstacule_detected:
            face_values.obstacule_detected = False
        
        sleep(1)
        if face_values.finished:
            break
        
thread1 = threading.Thread(target=do_logic,args=(face_values,actuator))
thread2 = threading.Thread(target=do_sensing,args=(face_values,actuator))

thread1.start()
thread2.start()

do_classification(face_mesh,500)