import time
import sys
from time import sleep

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

#16, 18 - Front right
#15, 22 - Back right
#11, 13 - Front left
#29, 31 - Back left

def Move_Forward():
	print("Moving forward")
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.HIGH)
	GPIO.output(15, GPIO.HIGH)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(29, GPIO.LOW)
	GPIO.output(31, GPIO.HIGH)

def Move_Backwards():
	print("Moving backwards")
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.HIGH)
	GPIO.output(11, GPIO.HIGH)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(22, GPIO.HIGH)
	GPIO.output(29, GPIO.HIGH)
	GPIO.output(31, GPIO.LOW)

def Move_Left():
	print("Moving left")
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.HIGH)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(29, GPIO.LOW)
	GPIO.output(31, GPIO.LOW)

def Move_Right():
	print("Moving right")
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.HIGH)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(29, GPIO.LOW)
	GPIO.output(31, GPIO.HIGH)

def Stop():
	print("Stopping")
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(29, GPIO.LOW)
	GPIO.output(31, GPIO.LOW)

if len(sys.argv) != 2:
	print("Invalid argument format: Drive.py -[FILE_NAME]\n")
	exit(1)

def read_file(file):
	f = open(file, "r")
	instr = []
	line = f.readline()
	while True:
		line = line[:-1]
		if not line:
			break
		instr.append(line)
		line = f.readline()
	return instr

instructions = read_file(sys.argv[1][1:])

for i in instructions:
	if i == "MOVE FORWARD":
		Move_Forward()
	elif i == "MOVE BACKWARD":
		Move_Backwards()
	elif i == "MOVE LEFT":
		Move_Left()
	elif i == "MOVE RIGHT":
		Move_Right()
	sleep(1)
	Stop()
	sleep(1)

print("End")
GPIO.cleanup()
