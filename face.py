#import all the required modules
import struct
import cv2
import serial,time
#Setup Communication path for arduino (In place of 'COM5' put the port to which your arduino is connected)
#========== change the serial port here ==========
ArduinoSerial=serial.Serial('COM10',9600, timeout = 0.1)
time.sleep(2)
print("Connected to arduino...")
#importing the Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#To capture the video stream from webcam.
cap = cv2.VideoCapture(0)
#Read the captured image, convert it to Gray image and find faces
#cv2.namedWindow('img',cv2.WINDOW_NORMAL)
while 1:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    frame2 = frame.copy()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces= face_cascade.detectMultiScale(gray,1.1,6)
    for (x,y,w,h) in faces:
        
        xx = (x+w//2)
        yy = (y+h//2)
        
        
        if(xx > (640/2)+60):
            # up
            x1 = 1
            x2 = 0
        elif(xx < (640/2)-60):
            # down
            x1 = 0
            x2 = 1
        else:
            # center
            x1 = 0
            x2 = 0


        if(yy > (480/2)+60):
            # right
            y1 = 1
            y2 = 0
        elif(yy < (480/2)-60):
            # left
            y1 = 0
            y2 = 1
        else:
            # center
            y1 = 0
            y2 = 0

        cv2.circle(frame,(x+w//2,y+h//2),2,(0,255,0),2)

        # sending byte data to Arduino
        if(1 in [x1,x2,y1,y2]):
            ArduinoSerial.write(struct.pack('>BBBB',x1,x2,y1,y2))
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        else:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
#Display the stream.
    cv2.imshow('img',frame)
#Hit 'Esc' to terminate execution 
    k = cv2.waitKey(30) & 0xff
    if k == 27:
       break