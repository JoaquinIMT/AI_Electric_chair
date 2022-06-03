import Facemesh_V2
import cv2

cap = cv2.VideoCapture(0)
#lips_gesture_prediction, kps_original, eye_gesture_prediction

face_mesh = Facemesh_V2()
num_frames = 0
max_frames = 500
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue
    
    if num_frames>=max_frames:
        break
    else:
        num_frames+=1
   
    multi_face_lm = face_mesh.get_image_landmarks(image)
    if multi_face_lm.multi_face_landmarks:
        for face_landmarks in multi_face_lm.multi_face_landmarks:
            face_mesh.print_and_predict_gestures(image,face_landmarks)
cv2.destroyAllWindows()
cap.release()