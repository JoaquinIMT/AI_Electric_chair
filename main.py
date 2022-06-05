#from Controller.actuators import Actuator
from Face_Gestures.predictor import do_classification
from Face_Gestures.Facemesh_V2 import Facemesh_V2
from Communication.store_value import StoreValues
import threading
from time import sleep

face_values = StoreValues()
face_mesh = Facemesh_V2(face_values,classifier='lips_gesture_prediction')
#actuator = Actuator()


def do_logic(face_values):
    while True:
        sleep(0.5)
        if face_values.esperar_instruccion:
            if face_values.mout == 'sonrisa':
                face_values.esperar_instruccion = False
                print("========================EMPIEZA PROGRAMAAAAA, ESPERANDO INSTRUCCION")
        else:
            if face_values.mout == 'boca_abierta':
                print("========================actuator.motors_fw()")
                face_values.esperar_instruccion = True
                #actuator.motors_fw()
            if face_values.eye == 'ojo_derecho' and face_values.mout == 'neutral':
                print("========================actuator.motors_right()")
                face_values.esperar_instruccion = True
                #actuator.motors_right()
            if face_values.eye == 'ojo_izquierdo' and face_values.mout == 'neutral':
                print("========================actuator.motors_left()")
                face_values.esperar_instruccion = True
                #actuator.motors_left()
        if face_values.finished:
            break

thread1 = threading.Thread(target=do_logic,args=(face_values,))
#thread2 = threading.Thread(target=delayer,args=(2,))

thread1.start()

#thread2.start()
do_classification(face_mesh,500)