import RPi.GPIO as GPIO
import time
from time import sleep

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Proximity Sensor
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 22
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 37
#MAKE SURE TO GND!

L1 =  11
L2 =  13
R1 = 12
R2 = 24
#MotorPins, gives warnings, ignoring though
Motor1A1 = 7 
Motor1A2 = 8 
Motor1B1 = 19 
Motor1B2 = 21

Motor2A1 = 10 
Motor2A2 = 16
Motor2B1 = 18 
Motor2B2 = 23
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)

#MotorSetup & Code

#Motor 1!!!!!
GPIO.setup(Motor1A1,GPIO.OUT)
GPIO.setup(Motor1A2,GPIO.OUT)
GPIO.setup(Motor1B1,GPIO.OUT)
GPIO.setup(Motor1B2,GPIO.OUT)

#Motor 2!!!!!
GPIO.setup(Motor2A1,GPIO.OUT)
GPIO.setup(Motor2A2,GPIO.OUT)
GPIO.setup(Motor2B1,GPIO.OUT)
GPIO.setup(Motor2B2,GPIO.OUT)

forward_seq = ['1001', '0101', '0110', '1010']
reverse_seq = list(forward_seq) # to copy the list
reverse_seq.reverse()

def forwardL(delay, steps):
  for i in range(steps):
    for step in forward_seq:
      set_stepL(step)
      time.sleep(delay)
	  
def forwardR(delay, steps):
  for i in range(steps):
    for step in forward_seq:
      set_stepR(step)
      time.sleep(delay)

def backwardsL(delay, steps):
  for i in range(steps):
    for step in reverse_seq:
      set_stepL(step)
      time.sleep(delay)
	  
def backwardsR(delay, steps):
  for i in range(steps):
    for step in reverse_seq:
      set_stepR(step)
      time.sleep(delay)	

def set_stepL(step):
  GPIO.output(Motor1A1, step[0] == '1')
  GPIO.output(Motor1A2, step[1] == '1')
  GPIO.output(Motor1B1, step[2] == '1')
  GPIO.output(Motor1B2, step[3] == '1')
  
def set_stepR(step):
  GPIO.output(Motor2A1, step[0] == '1')
  GPIO.output(Motor2A2, step[1] == '1')
  GPIO.output(Motor2B1, step[2] == '1')
  GPIO.output(Motor2B2, step[3] == '1')

KeepGoing = True
MainGoing = True

#while(MainGoing): 
while(KeepGoing):
	ProximitySensorLeftHand = GPIO.input(37)
	ProximitySensorRightHand = GPIO.input(22)
	while ProximitySensorLeftHand == True:
	#if ProximitySensorLeftHand == False:
		#backwardsR(int(2)/1000.0, int(10))
		GPIO.output(L1, GPIO.HIGH)
		#GPIO.output(L1, GPIO.LOW)
		#GPIO.output(L2, GPIO.LOW)
		#set_stepL('0000')
		#continue
		break
	else:
		#forwardL(int(2)/1000.0, int(2))
		GPIO.output(L2, GPIO.HIGH)
		continue
	while ProximitySensorRightHand == True:
		GPIO.output(R1, GPIO.HIGH)
		#GPIO.output(R2, GPIO.LOW)
		#KeepGoing = True
		set_stepR('0000')
		break
	else:
		#backwardsR(int(2)/1000.0, int(2))
		GPIO.output(R2, GPIO.HIGH)
		continue
	#elif ProximitySensorLeftHand == True:
		#GPIO.output(L1, GPIO.HIGH)
		#set_stepL('1111')
		#print("Left Hand Seen!")
		#break
	#if ProximitySensorRightHand == False:
		#forwardL(int(2)/1000.0, int(10))
		#GPIO.output(L2, GPIO.LOW)
		#continue
	#elif ProximitySensorRightHand == True:
		#GPIO.output(L2, GPIO.HIGH)
		#set_stepR('1111')
		#print("Right Hand Seen!")
		#break
	#break
#else:
	#run code
	print("WE DID IT!!!!")
	#GPIO.output(L1, GPIO.LOW)
	#GPIO.output(R1, GPIO.LOW)
	#GPIO.output(L2, GPIO.HIGH)
