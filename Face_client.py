import socket
import keyboard
import time
import sys
# import custom function

import faceif


# Connect to target IP
TCP_IP = 'raspberrypi.local'
TCP_PORT_x = 9982
TCP_PORT_y = TCP_PORT_x + 1
BUFFER_SIZE = 4096

# Establish connection
print('Establishing connection...\n(', TCP_IP, ':', TCP_PORT_x,')')
xSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
xSocket.connect((TCP_IP, TCP_PORT_x))
print('Connection established!')
print('Establishing connection...\n(', TCP_IP, ':', TCP_PORT_y,')')
ySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ySocket.connect((TCP_IP, TCP_PORT_y))
print('Connection established!')

# Initiate face recognition
faces = faceif.FACE()

while(faces.getCap()):
    faces.observe()
    faces.updateifTrack()
    xCenter = faces.getxCenter()
    yCenter = faces.getyCenter()
    faceS = faces.getfaceS()
    ifTrack = faces.getifTrack()
    resetyet = faces.getresetyet()
    facecount = faces.getfacecount()
    nofacecount = faces.getnofacecount()
    print("(", "position: ", xCenter, yCenter, "faceS: ", faceS, "facecount: ", facecount, "nofacecount: ", nofacecount, ifTrack, ")")

    if ifTrack==True:
        xEncode = str(xCenter) + "a"
        yEncode = str(yCenter) + "a"
        xSocket.send(str(xEncode).encode('utf-8'))
        ySocket.send(str(yEncode).encode('utf-8'))
        print(xEncode, yEncode)
    elif ifTrack == False and resetyet == False:
        xEncode = str(999) + "a"
        yEncode = str(999) + "a"
        xSocket.send(str(xEncode).encode('utf-8'))
        ySocket.send(str(yEncode).encode('utf-8'))
        print(xEncode, yEncode)
        faces.setresetyet(True)
    else:
        xEncode = str(320) + "a"
        yEncode = str(240) + "a"
        xSocket.send(str(xEncode).encode('utf-8'))
        ySocket.send(str(yEncode).encode('utf-8'))
        print(xEncode, yEncode)


    # xEncode = str(xCenter) + "a"
    # yEncode = str(yCenter) + "a"
    # xSocket.send(str(xEncode).encode('utf-8'))
    # ySocket.send(str(yEncode).encode('utf-8'))
    # print(xEncode, yEncode)

    # Terminate process
    # if keyboard.is_pressed('q'):
    #     xSocket.send(str(-1).encode('utf-8'))
    #     break
    time.sleep(0.01)

xSocket.close()
ySocket.close()
