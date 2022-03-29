import cv2
import socket
from matplotlib import pyplot as plt
import socket
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils
import numpy as np
import mediapipe as mp
import os  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf

import keras
from sklearn.preprocessing import MinMaxScaler


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

##### parámetros de openCV
blob_detector_params = cv2.SimpleBlobDetector_Params()
blob_detector_params.filterByArea = True
blob_detector_params.maxArea = 150
blob_detector = cv2.SimpleBlobDetector_create(blob_detector_params)



class Variable:
    def _init_(self):
        self.value = 0


def deteccion_facial(faces,frame):
    
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        return frame

def visualizar():
    global cap,cicle_looping,imgcounter
    
    ret,frame = cap.read()

    image = frame
    if ret == True:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        # Image
        height, width, _ = image.shape
        def preprocess_img(img):
            img = cv2.resize(img, (80,80))
            X = [img]
            X = np.array(X).reshape(-1, 80, 80, 3)
            X = X/255.0
            return X
        def locateref(arr,j,face_landmarks,width=width,height=height):
            pt2 = face_landmarks.landmark[arr[j]]
            x1,y1 = int(pt2.x * width),int(pt2.y * height)
            return x1,y1
        drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        eye_coords = []
       
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        # mp_drawing.draw_landmarks(
                        #     image=image,
                        #     landmark_list=face_landmarks,
                        #     connections=mp_face_mesh.FACEMESH_IRISES,
                        #     landmark_drawing_spec=drawing_spec,)
                        image_width = image.shape[1]
                        image_heigth = image.shape[0]   
                        blank_image = np.zeros((image_heigth,image_width,3), np.uint8)
                        blank_image = blank_image + 255
                        points = []
            
                        # landmarks_indexs = np.arange(0,470)
                        # for j,lmk_index in enumerate(landmarks_indexs):
                        #     x,y = locateref([lmk_index],0,face_landmarks)
                        #     points.append([x,y])
        
                        # points_n = np.array(points)
                        # x_Ulimit,x_DLimit = np.max(points_n[:,0]),np.min(points_n[:,0])
                        # y_Ulimit,y_DLimit = np.max(points_n[:,1]),np.min(points_n[:,1])
                        # for point in points:
                        #     blank_image[point[1]][point[0]] = (0,0,0)
                        # blank_image = blank_image[y_DLimit:y_Ulimit,x_DLimit:x_Ulimit]
                        landmarks_indexs = np.arange(0,470)
                        fronzenset = np.array([(61, 146), (146, 91), (91, 181), (181, 84), (84, 17),
                           (17, 314), (314, 405), (405, 321), (321, 375),
                           (375, 291), (61, 185), (185, 40), (40, 39), (39, 37),
                           (37, 0), (0, 267),
                           (267, 269), (269, 270), (270, 409), (409, 291),
                           (78, 95), (95, 88), (88, 178), (178, 87), (87, 14),
                           (14, 317), (317, 402), (402, 318), (318, 324),
                           (324, 308), (78, 191), (191, 80), (80, 81), (81, 82),
                           (82, 13), (13, 312), (312, 311), (311, 310),
                           (310, 415), (415, 308)])
                        landmarks_indexs = fronzenset[:,1]
                        landmarks_indexs = np.append(landmarks_indexs,fronzenset[0][0])
                        for lmk_index in landmarks_indexs:
                            x,y = locateref([lmk_index],0,face_landmarks)
                            points.append([x,y])
                        points = np.array(points)
                        points_n = points
                            
                     
                        x_Ulimit,x_DLimit = np.max(points_n[:,0]),np.min(points_n[:,0])
                        y_Ulimit,y_DLimit = np.max(points_n[:,1]),np.min(points_n[:,1])
                        for point in points:
                            blank_image[point[1]][point[0]] = (0,0,0)
                        blank_image = blank_image[y_DLimit:y_Ulimit,x_DLimit:x_Ulimit]
        #frame = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #blank_image = cv2.resize(blank_image,(80,80))
        #blank_image = blank_image[118:364,203:436]
        # imagefile = 'images1\ptarget\image'+str(imgcounter)+'.jpg'
        # if(imgcounter<100):
        #     cv2.imwrite(imagefile, blank_image) 
        #     print('saving.. ',imagefile)
        # imgcounter = imgcounter + 1
        

         
        model = keras.models.load_model('testmodel1.h5')
        image_for_prediction = preprocess_img(blank_image)
        prediction = model.predict(image_for_prediction)
        print(prediction)
        if prediction < 0.66:
            status = 'nokiss'
            cv2.rectangle(image, (round(image_width/2) - 110,20), (round(image_width/2) + 110, 80), (38,38,38), -1)
            cv2.putText(image, status, (round(image_width/2)-80,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_4)
        else:
            status = 'kiss'
            cv2.rectangle(image, (round(image_width/2) - 110,20), (round(image_width/2) + 110, 80), (38,38,38), -1)
            cv2.putText(image, status, (round(image_width/2)-104,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2, cv2.LINE_4)

        cv2.imshow("Image", image)
        if cv2.waitKey(1) == ord('q'):

            cap.release()
            cv2.destroyAllWindows()
            cicle_looping = False
       
def main():
    global cap,cicle_looping,imgcounter 
    cicle_looping = True  
    imgcounter = 0  
    cap = cv2.VideoCapture(0)
    while(cicle_looping):
        visualizar()


main()