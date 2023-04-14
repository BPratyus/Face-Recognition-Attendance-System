import os
import time
from datetime import datetime
from csv import writer

import cv2
import face_recognition
import numpy as np
import pickle

names = []

def encode():
    encodeListKnown = findEncodings(images)
    print('Encoded List:', encodeListKnown)

    data = dict(zip(classNames, encodeListKnown))
    print('dictionary', data)
    with open('listfile.data', 'wb') as filehandle:
        pickle.dump(data, filehandle, protocol=pickle.HIGHEST_PROTOCOL)
    # print(data)
    print('Encoding Complete')
    return encodeListKnown


# from PIL import ImageGrab

path = '.\Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img,num_jitters=3)[0]
        encodeList.append(encode)
       
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            # print(nameList)
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

nameList = []
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

# with  open('listfile.data','rb') as filehandle:
#     data=pickle.load(filehandle)

if os.stat("listfile.data").st_size != 0:
    with open('listfile.data', 'rb') as filehandle:
        data = pickle.load(filehandle)
        # for x, y in data:
        names = (list(data.keys()))
        # print(names)
        encodeListKnown = list(data.values())
        # print(encodeListKnown)


    if names == classNames:
        print("Previous Encoding used")
    else:
        encodeListKnown = encode()
else:
    encodeListKnown = encode()




cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS,number_of_times_to_upsample=2)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=0.5)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:

            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
