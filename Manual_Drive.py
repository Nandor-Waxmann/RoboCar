import time
import sys
import RPi.GPIO as GPIO
from sshkeyboard import listen_keyboard

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

def move(key):
	if key == 'w':
		print("Moving forward")
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(22, GPIO.LOW)
		GPIO.output(29, GPIO.LOW)
		GPIO.output(31, GPIO.HIGH)
	elif key == 's':
		print("Moving backwards")
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.HIGH)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(22, GPIO.HIGH)
		GPIO.output(29, GPIO.HIGH)
		GPIO.output(31, GPIO.LOW)
	elif key == 'a':
		print("Moving left")
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(22, GPIO.LOW)
		GPIO.output(29, GPIO.LOW)
		GPIO.output(31, GPIO.LOW)
	elif key == 'd':
		print("Moving right")
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
		GPIO.output(29, GPIO.LOW)
		GPIO.output(31, GPIO.HIGH)
	elif key == 'left':
		print("Moving backwards to the left")
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.HIGH)
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(22, GPIO.HIGH)
		GPIO.output(29, GPIO.LOW)
		GPIO.output(31, GPIO.LOW)
	elif key == 'right':
		print("Moving backwards to the right")
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
		GPIO.output(29, GPIO.HIGH)
		GPIO.output(31, GPIO.LOW)

def stop(key):
	print("Stopping")
	GPIO.output(16, GPIO.LOW)
	GPIO.output(18, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)
	GPIO.output(29, GPIO.LOW)
	GPIO.output(31, GPIO.LOW)

listen_keyboard(
	on_press = move,
	on_release = stop,
)

print("End")
GPIO.cleanup()
