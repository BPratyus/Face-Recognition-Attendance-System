# Face-Recognition-Attendance-System
Attendance System based on the Face_recognition module 

## For Deployment on Windows
[***main.py***](main.py)

## For Deployment on RPi 4+
[***FaceRecog.py***](FaceRecog.py)

## Devlopment Server using Flask

Uses [***index.html***](/templates/index.html) in `templates` and [***style.css***](/static/style.css) in `static` folders for rendering
- ***app.py*** for running the server
- A subprocess called from main file for parallel process execution

## Performance
- On Desktop face recognition is seameless under light and dark conditions
  
  ![Light Conditions](https://raw.githubusercontent.com/Prats-23/Face-Recognition-Attendance-System/main/Performance%201.jpg)
  
  ![Dark Conditions](https://raw.githubusercontent.com/Prats-23/Face-Recognition-Attendance-System/main/Performance%202.png)
  
  ## Front-End 
    A Flask server to view the latest Attendance Detail and download it in .CSV form and upload new face Encodings data to the Rpi
    
    ![Webpage](https://raw.githubusercontent.com/Prats-23/Face-Recognition-Attendance-System/main/Flask%20Server.jpg)
