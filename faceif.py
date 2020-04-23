import dlib
import pygame
import sys
import cv2
import imutils
import math
import time
from collections import deque
import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt


# Camera resolution, recommended ratio 16:9
# CAMERA_WIDTH = 640
# CAMERA_HEIGHT = 480


class FACE(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.time_start = time.time()

        # show and set camera stat
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.sizew = self.cap.get(3)
        self.sizeh = self.cap.get(4)
        print(self.sizew, self.sizeh)
        self.detector = dlib.get_frontal_face_detector()
        self.xCenter = 320
        self.yCenter = 240
        self.faceS = 0
        self.ifTrack = False
        self.facecount = 0
        self.nofacecount = 0
        self.resetyet = True

    def getCap(self):
        return self.cap.isOpened()

    def endCam(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def observe(self):
        ret, frame = self.cap.read()

        face_rects, scores, idx = self.detector.run(frame, 0)
        self.time_end = time.time()
        # flip video
        # frame_flip = cv2.flip(frame, 1)

        faceS0 = 0
        # read data
        for i, d in enumerate(face_rects):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            self.faceS = (y2 - y1) * (x2 - x1)
            print("original data:", x1, x2, y1, y2)

            # show center position
            if self.faceS > faceS0:
                self.xCenter = int((x1 + x2) / 2)
                self.yCenter = int((y1 + y2) / 2)
                faceS0 = self.faceS

        if len(scores) == 0:
            self.xCenter = 320
            self.yCenter = 240
            self.faceS = 0

        if self.faceS < 15000 and self.ifTrack == True:
            self.nofacecount = self.nofacecount + 1
        elif self.faceS >= 15000 and self.ifTrack == False:
            self.facecount = self.facecount +1
        else:
            self.nofacecount = 0
            self.facecount = 0

        # show the result
        # cv2.imshow("Face Detection", frame)

    def updateifTrack(self):
        if self.nofacecount >= 20:
            print("There is no one to track")
            self.ifTrack = False
            self.resetyet = False
            self.nofacecount = 0
            self.facecount = 0
        elif self.facecount >= 5:
            self.ifTrack = True
            print("Start tracking now")
            self.facecount = 0
            self.nofacecount = 0


    def getxCenter(self):
        return self.xCenter

    def getyCenter(self):
        return self.yCenter

    def getfacecount(self):
        return self.facecount

    def getnofacecount(self):
        return self.nofacecount

    def getfaceS(self):
        return self.faceS

    def getifTrack(self):
        return self.ifTrack

    def getresetyet(self):
        return self.resetyet

    def setresetyet(self, yet):
        self.resetyet = yet

# faces = FACE()
#
# while (faces.getCap()):
#     faces.observe()
#     faces.updateifTrack()
#     xCenter = faces.getxCenter()
#     yCenter = faces.getyCenter()
#     faceS = faces.getfaceS()
#     ifTrack = faces.getifTrack()
#     resetyet = faces.getresetyet()
#     facecount = faces.getfacecount()
#     nofacecount = faces.getnofacecount()
#     print("(", "position: ", xCenter, yCenter, "faceS: ", faceS, "facecount: ", facecount, "nofacecount: ", nofacecount,
#           ifTrack, ")")
#
#     if ifTrack==True:
#         xEncode = str(xCenter) + "a"
#         yEncode = str(yCenter) + "a"
#
#         print(xEncode, yEncode)
#     elif ifTrack == False and resetyet == False:
#         xEncode = str(999) + "a"
#         yEncode = str(999) + "a"
#
#         print(xEncode, yEncode)
#         faces.setresetyet(True)
#     else:
#         xEncode = str(320) + "a"
#         yEncode = str(240) + "a"
#
#         print(xEncode, yEncode)
