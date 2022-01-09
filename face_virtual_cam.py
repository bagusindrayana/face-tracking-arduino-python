import pyvirtualcam
from pyvirtualcam import PixelFormat
import struct
import cv2
import serial,time
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
pref_width = 640
pref_height = 480
pref_fps = 30
cap.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
cap.set(cv2.CAP_PROP_FPS, pref_fps)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)


#========== change the serial port here ==========
ArduinoSerial=serial.Serial('COM10',9600, timeout = 0.1)

time.sleep(1)
x1 = 0 
x2 = 0
y1 = 0
y2 = 0
while cap.isOpened():
    with pyvirtualcam.Camera(width, height, fps, fmt=PixelFormat.BGR) as cam:
            print('Virtual camera device: ' + cam.device)
            while True:
                ret, frame = cap.read()
                frame=cv2.flip(frame,1)
                frame2 = frame.copy()

                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces= face_cascade.detectMultiScale(gray,1.1,6)  #detect the face
                for x,y,w,h in faces:
                    #sending coordinates to Arduino
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

                cv2.rectangle(frame,(640//2-60,480//2-60),
                            (640//2+60,480//2+60),
                            (255,255,255),3)

                cv2.imshow('face_detection',frame)
                cv2.imshow('normal',frame2)
                cam.send(frame2)
                cam.sleep_until_next_frame()
    
                if cv2.waitKey(10)&0xFF== ord('q'):
                    break
cap.release()
cv2.destroyAllWindows()