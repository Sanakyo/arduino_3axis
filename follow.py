import cv2
import numpy as np
import pyfirmata as pf
import time

arduino = pf.Arduino('COM12')
servos = [arduino.get_pin('d:4:s'), arduino.get_pin('d:3:s'), arduino.get_pin('d:2:s')]
servoNames = ["Bottom Servo", "Middle Servo", "Top Servo"]

defaultServoDegrees = [50, 90, 180]

for index, servo in enumerate(servos):
    servo.write(defaultServoDegrees[index])
time.sleep(1)
print("Servos set to default position. (50, 90, 180)")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    height, width, channels = frame.shape
    center_x = int(width / 2)
    center_y = int(height / 2)
    cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)
    cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 2)

    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        degree = int(abs(((x + (w / 2)) / width) * 90))
        servos[0].write(degree)
        print(degree)
        
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
