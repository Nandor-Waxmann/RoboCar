import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

# 16, 18 - Front Right
# 15, 22 - Back Right
# 11, 13 - Front Left
# 29, 31 - Back Left

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")

port = 8888

s.bind(('', port))
print("Socket bound to %s" %port)

s.listen(5)
print ("Waiting for connection...")

c, addr = s.accept()
print('Got connection from', addr)

def Move_Forward():
    print("Moving Forwards")
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)

def Move_Backwards():
    print("Moving Backwards")
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)

def Move_Left():
    print("Moving Left")
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)

def Move_Right():
    print("Moving Right")
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)

def Stop():
    print("Stopping...")
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)

while True:
    data = c.recv(1024).decode("utf-8")
    print("Message received:", data)

    if data == "Equilateral Triangle":
        Move_Forward()
    elif data == "Rectangle":
        Move_Backwards()
    elif data == "Regular Pentagon":
        Move_Right()
    elif data == "Regular Hexagon":
        Move_Left()
    elif data == "Quit":
        c.close()
        break
