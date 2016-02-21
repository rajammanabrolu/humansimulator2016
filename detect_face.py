#coding=utf-8
import numpy as np
import cv2
import os
import time

class face_detect:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haar-eyes.xml')
        self.cam = cv2.VideoCapture(0)
        self.moving_frame_count = 0
        self.red_average = 0
        self.red_initial = 0
        self.size_average = 0
        self.size_initial = 0
        self.gap = 0
        self.no_eyes = True

    def eye_strain(self, frame):
        if self.gap < 7 and self.moving_frame_count >= 600:
            print("EYE")
            return True

    def posture(self, frame):
        if self.size_average >= (1.25 * self.size_initial) and self.size_initial != 0:
            print("POSE")
            return True

def main():
    detect = face_detect()
    pose = "POSE"
    eye = "EYE"
    f = open('./healthdeskrc', 'r')
    interval = int(f.read())
    while(detect.cam.isOpened()):
        ret, frame = detect.cam.read()
        if detect.red_initial == 0 and detect.red_average > 0 and detect.moving_frame_count > 1:
            detect.red_initial = detect.red_average
        if detect.size_initial == 0 and detect.size_average > 0 and detect.moving_frame_count > 2:
            detect.size_initial = detect.size_average
        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.blur(gray, (5, 5))
            faces = detect.face_cascade.detectMultiScale(gray, 1.3, 5)
            if detect.eye_strain(frame):
                os.system("." + "/terminal-notifier.app/Contents/MacOS/terminal-notifier -title \'Health Desk\' -message \'Rest your eyes! 👁 \' -appIcon \'./Medical.Icon.png\' -group \'+\'")
                time.sleep(interval)
            elif detect.posture(frame):
                os.system("." + "/terminal-notifier.app/Contents/MacOS/terminal-notifier -title \' Health Desk \' -message \'Try not to slouch! 🙇 \' -appIcon \'./Medical.Icon.png\' -group \'+\'")
                time.sleep(interval)
            #for each face
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                face_gray = gray[y:y+h, x:x+w]
                face_color = frame[y:y+h, x:x+w]
                eyes = detect.eye_cascade.detectMultiScale(face_gray)
                if len(eyes) < 1 and detect.no_eyes != True:
                    detect.gap += 1
                elif len(eyes) >= 1:
                    detect.no_eyes = False
                size = w * h
                detect.size_average = ((detect.moving_frame_count * detect.size_average) + size)/(detect.moving_frame_count + 1)
                for (ex,ey,ew,eh) in eyes:
                    red = cv2.mean(frame[ey:ey+eh, ex:ex+ew])[2]
                    detect.red_average = ((detect.moving_frame_count * detect.red_average) + red)/(detect.moving_frame_count + 1)
                    detect.moving_frame_count += 1
                    if detect.moving_frame_count > 600:
                        detect.moving_frame_count = 0
                    cv2.rectangle(face_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            #cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detect.cam.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__": main()
