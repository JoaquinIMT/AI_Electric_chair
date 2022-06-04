from Controller import actuators
from Face_Gestures import predictor, Facemesh_V2
from Communication import store_value
import threading

face_mesh = Facemesh_V2()
face_values = store_value.StoreValues()
actuator = actuators.Actuator()

thread1 = threading.Thread(target=predictor.do_classification,args=(face_mesh,face_values,100))
#thread2 = threading.Thread(target=delayer,args=(2,))

thread1.start()
#thread2.start()

while True: 
    if face_values.esperar_instruccion:
        if face_values.mout == 'boca_abierta' and face_values.eye == 'ojo_derecho':
            face_values.esperar_instruccion = False
            print("EMPIEZA PROGRAMAAAAA, ESPERANDO INSTRUCCION")
    else:
        if face_values.mout == 'sonrisa':
            print("actuator.motors_fw()")
            #actuator.motors_fw()
        if face_values.eye == 'ojo_derecho' and face_mesh.mout == 'neutral':
            print("actuator.motors_right()")
            #actuator.motors_right()
        if face_values.eye == 'ojo_izquierdo' and face_mesh.mout == 'neutral':
            print("actuator.motors_left()")
            #actuator.motors_left()
        