import sys
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt

from utils import *
from PIL import Image
from age_and_gender import *

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

predictor = AgeAndGender()
predictor.load_shape_predictor('models/shape_predictor_5_face_landmarks.dat')
predictor.load_dnn_gender_classifier('models/dnn_gender_classifier_v1.dat')
predictor.load_dnn_age_predictor('models/dnn_age_predictor_v1.dat')

video = (len(sys.argv) == 2)
out = None
if video:
    cap = cv2.VideoCapture(sys.argv[1])
else:
    cap = cv2.VideoCapture(0)

with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        (h, w) = image.shape[:2]

        if out is None and video:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi', fourcc, 24.0, (w, h))

        if not success:
            print("Ignoring empty camera frame.")
            if len(sys.argv) == 2: break
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image)
        results = face_detection.process(image)

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        faces = []
        if results.detections:
            for detection in results.detections:
                try:
                    (left, top), (right, bottom) = get_bbox(image, detection)
                except:
                    continue
                faces.append((top, right, bottom, left))
                cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
                # Flip the image horizontally for a selfie-view display.

        results_dnn = predictor.predict(pil_img, faces)
        for info in results_dnn:
            left, top, right, bottom = info['face']
            gender = "Homem" if info['gender']['value'].title() == "Male" else "Mulher"
            gender_conf = info['gender']['confidence']
            age = info['age']['value']
            age_conf = info['age']['confidence']

            cv2.rectangle(image, (left, top), (right, bottom), 
                            (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, f"Genero: {gender} ({gender_conf}%)", 
                    (left-10, top-30), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.putText(image, f"Idade: {age} ({age_conf}%)", 
                    (left-10, top-10), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

        #cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, f"Pessoas: {len(faces)}", (10, image.shape[0]-20), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA);
        resized = cv2.resize(image, (int(1.6*w), int(1.6*h)), interpolation = cv2.INTER_AREA)
        cv2.imshow('Face Detection + Age and Gender', resized)
        if video: out.write(image)
        if cv2.waitKey(5) & 0xFF == 27:
          break

cap.release()
if video: out.release()
cv2.destroyAllWindows()