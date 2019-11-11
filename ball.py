# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import pandas as pd
import matplotlib.pyplot as plt

class BALL(object):
    def __init__(self):
        # construct the argument parse and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                        help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=64,
                        help="max buffer size")
        self.args = vars(ap.parse_args())

        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        self.greenLower = (29, 86, 6)
        self.greenUpper = (150, 255, 255)
        self.pts = deque(maxlen=self.args["buffer"])
        self.ifkeep = True
        self.ballX = 320
        self.ballY = 240
        self.radius = 0

        # if a video path was not supplied, grab the reference
        # to the webcam
        if not self.args.get("video", False):
            self.camera = cv2.VideoCapture(0)
            self.camera.set(3, 640)
            self.camera.set(4, 480)
            self.sizew = self.camera.get(3)
            self.sizeh = self.camera.get(4)
            print(self.sizew, self.sizeh)

        # otherwise, grab a reference to the video file
        else:
            self.camera = cv2.VideoCapture(self.args["video"])

        # Creating a Pandas DataFrame To Store Data Point
        Data_Features = ['x', 'y', 'time']
        self.Data_Points = pd.DataFrame(data=None, columns=Data_Features, dtype=float)

        # Reading the time in the begining of the video.
        self.start = time.time()

    def getball(self):
        # grab the current frame
        (grabbed, frame) = self.camera.read()

        # Reading The Current Time
        current_time = time.time() - self.start

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if self.args.get("video") and not grabbed:
            self.ifkeep = False
            return

        # resize the frame, blur it, and convert it to the HSV
        # color space
        # frame = imutils.resize(frame, width=900)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            print(int(x), int(y), int(radius))
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if (radius < 300) & (radius > 10):
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                # print(int(x), int(y), int(radius))
                self.ballX = int(x)
                self.ballY = int(y)
                self.radius = int(radius)

                # Save The Data Points
                self.Data_Points.loc[self.Data_Points.size / 3] = [x, y, current_time]

        # update the points queue
        self.pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(self.pts)):
            # if either of the tracked points are None, ignore
            # them
            if self.pts[i - 1] is None or self.pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(self.args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            self.ifkeep = False
            return

    def getifkeep(self):
        return self.ifkeep

    def getballX(self):
        return self.ballX

    def getballY(self):
        return self.ballY

    def getradius(self):
        return self.radius

    def terminate(self):
        self.camera.release()
        cv2.destroyAllWindows()

balls = BALL()
while(balls.getifkeep()):
    balls.getball()
    xCenter = balls.getballX()
    yCenter = balls.getballY()
    ballrad = balls.getradius()
    print("(", xCenter, yCenter, ballrad, ")")
    # xSocket.send(str(xCenter).encode('utf-8'))
    # ySocket.send(str(yCenter).encode('utf-8'))

    # Terminate process
    time.sleep(0.1)