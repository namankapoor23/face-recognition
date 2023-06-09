import cv2
import numpy as np
import os
import IPython.display as ipd
import webbrowser as wb
import urllib.request

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size=0.5):

    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi


# Open Webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Pass face to prediction model
        # "results" comprises of a tuple containing the label and the confidence value
        results = model.predict(face)
        print(results)
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is User'

        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)

        if confidence > 80:
            #os.system("docker run  -d -i -t --name vimalos ubuntu:latest")
            print('Its Naman')
            request_url = urllib.request.urlopen('https://ynaek9ry5j.execute-api.ap-south-1.amazonaws.com/test/unlock')
            print(request_url)
            # cv2.imshow('Face Recognition', image )
            break
            #webbrowser.open('http://google.com/')

        else:
            cv2.putText(image, "i dont know", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            request_url = urllib.request.urlopen('https://ynaek9ry5j.execute-api.ap-south-1.amazonaws.com/test/lock')
            cv2.imshow('Face Recognition', image )

    except:
        cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        request_url = urllib.request.urlopen('https://ynaek9ry5j.execute-api.ap-south-1.amazonaws.com/test/lock')
        cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.imshow('Face Recognition', image )
        pass

    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break

cap.release()
cv2.destroyAllWindows()

