# Face-Recognition-Attendance-System
A face recognition attendance system is a computerized system that uses facial recognition technology to capture and record employee attendance. This system works by using a camera to capture an image of an person's face, and then analyzing that image to verify the person's identity. If the system recognizes the person, it will record their attendance for that day in a CSV File.
> [NOTE!]
> We are using [Face_Recognition](https://github.com/ageitgey/face_recognition) module to deploy this
## For Deployment on Windows
[***main.py***](main.py)

## For Deployment on RPi 4+
[***FaceRecog.py***](FaceRecog.py)

## Devlopment Server using Flask

Uses [***index.html***](/templates/index.html) in `templates` and [***style.css***](/static/style.css) in `static` folders for rendering
- [***app.py***](app.py) for running the server
- A subprocess called from main file for parallel process execution

## Performance
- On Desktop face recognition is seameless under light and dark conditions
  
  ![Light Conditions](/images/Performance_1.jpg)
  
  ![Dark Conditions](/images/Performance_2.png)
  
  ## Front-End 
    A Flask server to view the latest Attendance Detail and download it in .CSV form and upload new face Encodings data to the Rpi
    
    ![Webpage](/images/Flask_Server.jpg)
