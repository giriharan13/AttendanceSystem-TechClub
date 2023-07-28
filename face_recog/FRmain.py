import os

import cv2
import pickle
import face_recognition
import dlib
from face_recog.livenessdetect.test import test
#added
import numpy as np
import argparse
import warnings
import time

path1 = os.environ["pathToEncodedFile"]
path2 = os.environ["pathToAntiSpoofModels"]

#Loading the pickle file
file = open(path1,"rb")
encodeListKnownWithFolders = pickle.load(file)
file.close()
encodeListKnown,ImageFolders = encodeListKnownWithFolders
print(ImageFolders)


'''cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)'''

def validate(frame,date):
    #while True:
    label = test(image=frame, model_dir=path2, device_id=0)
    valid = False if label!=1 else True

    imgS = cv2.resize(frame,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    font = cv2.FONT_HERSHEY_SIMPLEX

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS,faceCurrentFrame)
    FaceDistance = []
    status = []
    for encodeFace,faceLoc in zip(encodeCurrentFrame,faceCurrentFrame):
        for encodings in encodeListKnown:
            matches = face_recognition.compare_faces(encodings,encodeFace)
            dis = face_recognition.face_distance(encodings,encodeFace)
            FaceDistance.append(min(dis))
        print("Face Distances:",FaceDistance)
    name = None
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        name = ImageFolders[FaceDistance.index(min(FaceDistance))]
        color = (255, 0, 0)
        stroke = 2
        if(min(FaceDistance)<0.6):
            cv2.putText(frame,name+"["+str(date)+"]",(50,50),font,1,color,stroke,cv2.LINE_AA)
            status.append(1)
        else:
            cv2.putText(frame, "Face not recognized", (50, 50), font, 1, color, stroke, cv2.LINE_AA)
            status.append(-1)
    except:
        cv2.putText(frame, "No face detected", (50, 50), font, 1,(255, 0, 0) , 2, cv2.LINE_AA)
        status.append(0)

    #cv2.imshow("hello",img)
    cv2.waitKey(1)
    return [frame,status[0],valid,name]

cap = None

def create():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

'''def scan():
    # while True:
    success, img = cap.read()

    label = test(image=img,
                 model_dir=path2,
                 device_id=0)
    valid = "(fake)" if label != 1 else "(real)"

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    font = cv2.FONT_HERSHEY_SIMPLEX

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)
    FaceDistance = []
    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurrentFrame):
        for encodings in encodeListKnown:
            matches = face_recognition.compare_faces(encodings, encodeFace)
            dis = face_recognition.face_distance(encodings, encodeFace)
            FaceDistance.append(min(dis))
        print("Face Distances:", FaceDistance)
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        name = ImageFolders[FaceDistance.index(min(FaceDistance))]
        color = (255, 0, 0)
        stroke = 2
        if (min(FaceDistance) < 0.6):
            cv2.putText(img, name + valid, (50, 50), font, 1, color, stroke, cv2.LINE_AA)
        else:
            cv2.putText(img, "Face not recognized", (50, 50), font, 1, color, stroke, cv2.LINE_AA)
    except:
        cv2.putText(img, "No face detected", (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    #cv2.imshow("hello", img)
    cv2.waitKey(10)

    ret,jpeg = cv2.imencode('.jpg',img)
    return [img,jpeg.tobytes()]'''


def scan():
    # while True:
    success, img = cap.read()
    cv2.waitKey(10)

    ret,jpeg = cv2.imencode('.jpg',img)
    return [img,jpeg.tobytes()]

def delete():
    cap.release()



