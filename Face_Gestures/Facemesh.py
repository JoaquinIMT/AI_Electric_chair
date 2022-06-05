import cv2
import mediapipe as mp
import pandas as pd
import xgboost as xgb


mp_face_mesh = mp.solutions.face_mesh

class Facemesh:
    def __init__(self, label=None, classifier=None, import_df=True):
        left_eye = [263, 249, 390, 373, 374, 380, 381, 382, 362, 466, 388, 387, 386, 385, 384, 398]
        left_eyebrow = [276, 283, 282, 295, 285, 300, 293, 334, 296, 336]
        lips = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 185, 40, 39, 37, 0, 267, 269, 270, 409, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 191, 80, 81, 82, 13, 312, 311, 310, 415]
        right_eye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 246, 161, 160, 159, 158, 157, 173]
        right_eyebrow = [46, 53, 52, 65, 55, 70, 63, 105, 66, 107]
        left_iris = [474, 475, 476, 477]
        right_iris = [469, 470, 471, 472]
        centers_iris = [468, 473]
        self.eyes_gestures_kps = left_eye + left_eyebrow + right_eye + right_eyebrow
        self.kps = self.eyes_gestures_kps + lips
        self.eyes_kps = self.eyes_gestures_kps + left_iris + right_iris
        self.mouth = lips
        mp_face_mesh = mp.solutions.face_mesh
        self.label = label
        self.import_df = import_df
        self.face_mesh = mp_face_mesh.FaceMesh(  max_num_faces=1,
                                            refine_landmarks=True,
                                            min_detection_confidence=0.5,
                                            min_tracking_confidence=0.5)
        self.class_names = ['boca_abierta','neutral', 'ojo_derecho', 'ojo_izquierdo', 'sonrisa']
        classifiers = {
            'eye_gesture_prediction': {
                'class_names' : ['neutral','ojo_derecho','ojo_izquierdo'],
                'file_name' : '/home/pi/Documents/AI_Electric_chair/Face_gestures/modelos/eye_gesture_model_8.json',
                'columns': [2, 3, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 94, 95, 96, 97, 98, 99, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117, 118, 119, 120, 121, 122, 123, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 182, 183],
                'df_name': 'eyes_gestures_ds.csv',
                'kps' : self.eyes_gestures_kps
            },
            'kps_original': {
                'class_names':['boca_abierta','neutral', 'ojo_derecho', 'ojo_izquierdo', 'sonrisa'],
                'file_name' : 'modelos/model_2.json',
                'columns' : list(range(184)),
                'kps' : self.kps
            },
            'lips_gesture_prediction': {
                'class_names': ['boca_abierta', 'neutral', 'sonrisa'],
                'file_name' : '/home/pi/Documents/AI_Electric_chair/Face_gestures/modelos/lips_gesture_model_4.json',
                'columns': [0, 1, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 26, 27, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 64, 65, 86, 87, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 152, 153, 174, 175, 176, 177, 178, 179, 180, 181],
                'df_name': 'lips_ds.csv',
                'kps' : self.mouth
            }
        }
        if classifier:
            self.classifier = classifiers[classifier]
            self.load_xgboost_model() 
        
        
    def load_xgboost_model(self):
        file_name = self.classifier['file_name']
        model = xgb.Booster()
        model.load_model(file_name)
        self.xgb_model = model
        
    def get_image_landmarks(self,image):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)  ##Magic happening
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return results
            
    def insert_dataframe(self, points):
        df_name = self.classifier['df_name']
        df = pd.DataFrame(points).transpose()
        df.columns = self.classifier['columns']+[184]
        df.to_csv(df_name,mode='a',header=not self.import_df, index = False) 
        
                        
    def draw_image_kps(self,image,facial_landmarks):
        height, width, _ = image.shape
        points = []
        for i in range(len(facial_landmarks.landmark)):
            if i in self.classifier['kps']:
                pt= facial_landmarks.landmark[i]
                points.append(pt.x)
                points.append(pt.y)
                x = int(pt.x * width)
                y = int(pt.y * height)
                cv2.circle(image, (x, y), 1, (0, 100, 255), -1)
        return points
    
    def show_image(self, image):
        cv2.imshow("Image", image)
        cv2.waitKey(1)
    
    def draw_and_insert_kps(self,image,facial_landmarks):
        points = self.draw_image_kps(image,facial_landmarks)
        points.append(self.label)
        cv2.flip(image, 1)
        self.show_image(image)
        self.insert_dataframe(points)
    
    def draw_and_predict_gesture(self,image,facial_landmarks):
        points = self.draw_image_kps(image,facial_landmarks)
        df = self.assemble_df(points)
        prediction = self.predict_gesture(df)
        cv2.flip(image, 1)
        cv2.putText(image,prediction,(200,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        self.show_image(image)
        
    def predict_gesture(self,df):
        formatted_df = xgb.DMatrix(df)
        prediction = int(self.xgb_model.predict(formatted_df))
        return self.classifier['class_names'][prediction]
    
    def assemble_df(self, points):
        df = pd.DataFrame(points).transpose()
        df.columns = self.classifier['columns']
        return df
