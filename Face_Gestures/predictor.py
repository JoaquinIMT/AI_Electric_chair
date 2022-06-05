import cv2

#lips_gesture_prediction, kps_original, eye_gesture_prediction

def do_classification(face_mesh, max_frames = 500):
    cap = cv2.VideoCapture(0)
    num_frames = 0
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
                face_mesh.draw_and_predict_gesture(image,face_landmarks)
    cv2.destroyAllWindows()
    cap.release()
    face_mesh.store_values.finished = True
    print("FINISHING PREDICTION")
