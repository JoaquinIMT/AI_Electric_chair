import pandas as pd
import xgboost as xgb
import mediapipe as mp
from Face_Gestures.Facemesh import Facemesh


mp_face_mesh = mp.solutions.face_mesh

class Facemesh_V2(Facemesh):
    def __init__(self,store_values):
        self.store_values = store_values
        super().__init__()
        self.make_kps_dict()
    
    def make_kps_dict(self):
        self.whole_face = {
            'eye_gesture_prediction': {
                'class_names' : ['neutral','ojo_derecho','ojo_izquierdo'],
                'file_name' : 'Face_gestures/modelos/eye_gesture_model_8.json',
                'columns': [2, 3, 10, 11, 18, 19, 20, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 94, 95, 96, 97, 98, 99, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117, 118, 119, 120, 121, 122, 123, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 182, 183],
                'df_name': 'eyes_gestures_ds.csv',
                'kps' : self.eyes_gestures_kps
            },
            'lips_gesture_prediction': {
                'class_names': ['boca_abierta', 'neutral', 'sonrisa'],
                'file_name' : 'Face_gestures/modelos/lips_gesture_model_4.json',
                'columns': [0, 1, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 26, 27, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 64, 65, 86, 87, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 114, 115, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 152, 153, 174, 175, 176, 177, 178, 179, 180, 181],
                'df_name': 'lips_ds.csv',
                'kps' : self.mouth
            }
        }
        self.whole_face['kps'] = self.kps
        self.load_models('eye_gesture_prediction')
        self.load_models('lips_gesture_prediction')
    
    def load_models(self,classifier_name):
        file_name = self.whole_face[classifier_name]['file_name']
        model = xgb.Booster()
        model.load_model(file_name)
        self.whole_face[classifier_name]['xgb'] = model
    
    def print_and_predict_gestures(self,image,facial_landmarks):
        points = self.get_points(image.shape,facial_landmarks)
        df_eyes, df_mouth = self.assemble_dfs(points)
        eye_prediction = self.predict_gesture(df_eyes,'eye_gesture_prediction')
        mouth_prediction = self.predict_gesture(df_mouth,'lips_gesture_prediction')
        self.store_values.put_next_sign(mouth_prediction, eye_prediction)
        self.store_values.evaluate_sign()
        print(self.store_values.mout,self.store_values.eye)
        #print("EYE PREDICTION",eye_prediction,"MOUTH PREDICTION",mouth_prediction)
    
    def assemble_dfs(self,points):
        dfs = pd.DataFrame(points).transpose()
        df_eyes = dfs[self.whole_face['eye_gesture_prediction']['columns']]
        df_mouth = dfs[self.whole_face['lips_gesture_prediction']['columns']]
        return df_eyes, df_mouth 
    
    def get_points(self,shape,facial_landmarks):
        height, width, _ = shape
        points = []
        for i in range(len(facial_landmarks.landmark)):
            if i in self.whole_face['kps']:
                pt= facial_landmarks.landmark[i]
                points.append(pt.x)
                points.append(pt.y)
                x = int(pt.x * width)
                y = int(pt.y * height)
        return points
        
    def predict_gesture(self,df,classifier_name):
        formatted_df = xgb.DMatrix(df)
        prediction = int(self.whole_face[classifier_name]['xgb'].predict(formatted_df))
        return self.whole_face[classifier_name]['class_names'][prediction]
