# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

from csv import writer
from datetime import datetime
import os
import cv2
import face_recognition
import picamera
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import requests
import pickle
# from myapp import app
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzz=23
GPIO.setup(buzz,GPIO.OUT)

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.rotation=180
output = np.empty((240, 320, 3), dtype=np.uint8)

path = './Training_images'
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
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

names = []

def encode(fpath):
    encodeListKnown = findEncodings(images)
    print('Encoded List:', encodeListKnown)

    data = dict(zip(classNames, encodeListKnown))
    print('dictionary', data)
    with open(fpath, 'wb') as filehandle:
        pickle.dump(data, filehandle, protocol=pickle.HIGHEST_PROTOCOL)
    # print(data)
    print('Encoding Complete')
    return encodeListKnown

def markAttendance(name):
    
    with open('./Attendance.csv', 'a') as f:
        writerobj = writer(f)

        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')

        writerobj.writerow([name, dtString])
   

        # url = "https://api.thingspeak.com/update.json"
        # query = {'field1': name,'field2': now.strftime('%H:%M:%S'), 'key':'40G2MFXTNCO6VJ24' }
        # headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}

        # x = requests.post(url,data=query)
        # print(x.text)

        GPIO.output(buzz,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzz,GPIO.LOW)

nameList = []
NameRep = []

# encodeListKnown = findEncodings(images)
# print('Encoding Complete')
fpath = "./listfile.data"
if os.stat(fpath).st_size != 0:
    with open(fpath, 'rb') as filehandle:
        data = pickle.load(filehandle)
        # for x, y in data:
        names = (list(data.keys()))
        # print(names)
        encodeListKnown = list(data.values())
        # print(encodeListKnown)


    if names == classNames:
        print("Previous Encoding used")
    else:
        encodeListKnown = encode(fpath)
else:
    encodeListKnown = encode(fpath)

GPIO.output(buzz,GPIO.HIGH)
sleep(1)
GPIO.output(buzz,GPIO.LOW)

sudo_pass = 'root'
command='python ./myapp.py'
command=command.split()
cmd1=subprocess.Popen(['echo',sudo_pass], stdout=subprocess.PIPE)
subprocess.Popen(['sudo','-S']+command,stdin=cmd1.stdout)
# os.system("sudo python app.py")
# app.index()
# Load a sample picture and learn how to recognize it.
# print("Loading known face image(s)")
# obama_image = face_recognition.face_locations("Pratyus.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(encodeListKnown, face_encoding)
        faceDis = face_recognition.face_distance(encodeListKnown, face_encoding)
        matchIndex = np.argmin(faceDis)
        name = "<Unknown Person>"

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            if name not in nameList:
                NameRep.append(name)
                if len(NameRep)>2 :
                    NameRep.clear()
                    nameList.append(name)
                    markAttendance(name)
            print(name)

        # print("I see someone named {}!".format(name))