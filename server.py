import socket
import time
import Adafruit_PCA9685

# Server information
TCP_IP = 'raspberrypi.local'
TCP_PORT_x = 9982
TCP_PORT_y = TCP_PORT_x + 1
BUFFER_SIZE = 4096
print ('connected')

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
# Reset camera position
pulseX = 350
pulseY = 200
print('Moving servo to original position.')
pwm.set_pwm(0, 0, pulseX)
pwm.set_pwm(15, 0, pulseY)

# Server set up
print('Binding address to ', TCP_IP, ':', TCP_PORT_x)
xSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
xSocket.bind((TCP_IP, TCP_PORT_x))
xSocket.listen(1)
print('Binding Successful!')

print('Binding address to ', TCP_IP, ':', TCP_PORT_y)
ySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ySocket.bind((TCP_IP, TCP_PORT_y))
ySocket.listen(1)
print('Binding Successful!')

# Establish connection with client
connX, addrX = xSocket.accept()
print('Connection address:', addrX)
connY, addrY = ySocket.accept()
print('Connection address:', addrY)

dataX = b'0'
dataY = b'0'

while 1:
    # Receiving data
    dataX = connX.recv(BUFFER_SIZE)
    dataY = connY.recv(BUFFER_SIZE)
    xRaw = str(dataX)
    yRaw = str(dataY)
    print("Received data:", xRaw, yRaw)
    i=0
    xCenter=0
    while(1):
        if xRaw[i]=="a":
            break
        xCenter=xCenter*10+int(xRaw[i])
        i=i+1
    
    j=0
    yCenter=0
    while(1):
        if yRaw[j]=="a":
            break
        yCenter=yCenter*10+int(yRaw[j])
        j=j+1
        
    if xCenter == 999:
        pulseX = 350
        print('Moving servo to original position.')
        pwm.set_pwm(0, 0, pulseX)


    elif xCenter > 430:
        pulseXdt = xCenter*8/210 -14
        pulseX = pulseX - pulseXdt
        if pulseX < 150:
            pulseX = 150
            print("Face out of range")
        print("Turning left", pulseX)
        pwm.set_pwm(0, 0, pulseX)

    elif xCenter < 210:
        pulseXdt = -xCenter*8/210 + 10
        pulseX = pulseX + pulseXdt
        if pulseX > 600:
            pulseX = 600
            print("Face out of range")
        print("Turning right", pulseX)
        pwm.set_pwm(0, 0, pulseX)
        
    else:
        print("no need to move")

    if yCenter == 999:
        pulseY = 200
        print('Moving servo to original position.')
        pwm.set_pwm(15, 0, pulseY)


    elif yCenter <170:
        pulseYdt = -yCenter*2/170 + 4
        pulseY = pulseY - pulseYdt
        if pulseY < 190:
            pulseY = 190
            print("Face out of range")
        print("Turning up", pulseY)
        pwm.set_pwm(15, 0, pulseY)

    elif yCenter >310:
        pulseYdt = yCenter*2/170 -1.64
        pulseY = int(pulseY + pulseYdt)
        if pulseY > 240:
            pulseY = 240
            print("Face out of range")
        print("Turning down", pulseY)
        pwm.set_pwm(15, 0, pulseY)
        
    else:
        print("no need to move")


    if xCenter == -1:
        break
    time.sleep(0.01)

# Shut down connection
xSocket.close()
ySocket.close()
