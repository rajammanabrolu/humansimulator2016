import cv2
import numpy as np
import imutils

class Heart():
    self.cam = cv2.VideoCapture(0)
    self.red = []
    self.blue = []
    self.green = []

    def readFrames(self):
        for i in range (500):
            frame = self.cam.read()
            blue[i], green[i], red[i] = cv2.mean(frame)[:3]
        self.cam.release()

    def 

