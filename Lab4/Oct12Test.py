import RPi.GPIO as GPIO
import time
from time import sleep 
import mido 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

########################################################################################
#Pin setup

#L1->L7 is all left hand fingers
#R1->R7 is all right hand fingers
#Pins 3, 5, 16, 18, 22, 19, 21, 23 are unavailable

#Left hand pins
L1 =  11
L2 =  13
L3 =  15
L4 =  29
L5 =  31
L6 =  33    
L7 =  35

#Right hand pins
R1 =  12
R2 =  24
R3 =  26
R4 =  32
R5 =  36
R6 =  38    
R7 =  40

#MotorPins, gives warnings, ignoring though
Motor1A1 = 7
Motor1A2 = 8
Motor1B1 = 19
Motor1B2 = 21

#GND = 6

Motor2A1 = 10
Motor2A2 = 16
Motor2B1 = 18
Motor2B2 = 23

#######################################################################################
#Solenoid setup & Code?

#LEFT HAND/FINGER SETUP
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(L3,GPIO.OUT)
GPIO.setup(L4,GPIO.OUT)
GPIO.setup(L5,GPIO.OUT)
GPIO.setup(L6,GPIO.OUT)
GPIO.setup(L7,GPIO.OUT)

#RIGHT HAND/FINGER SETUP
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)
GPIO.setup(R3,GPIO.OUT)
GPIO.setup(R4,GPIO.OUT)
GPIO.setup(R5,GPIO.OUT)
GPIO.setup(R6,GPIO.OUT)
GPIO.setup(R7,GPIO.OUT)

####################################################################################
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


forward_seq = ['1011', '1111', '1110', '1010']
reverse_seq = list(forward_seq) # to copy the list
reverse_seq.reverse()

def forward(delay, steps):
  for i in range(steps):
    for step in forward_seq:
      set_step(step)
      time.sleep(delay)

def backwards(delay, steps):
  for i in range(steps):
    for step in reverse_seq:
      set_step(step)
      time.sleep(delay)


def set_step(step):
  GPIO.output(Motor1A1, step[0] == '1')
  GPIO.output(Motor1B1, step[1] == '1')
  GPIO.output(Motor2B1, step[2] == '1')
  GPIO.output(Motor2B2, step[3] == '1')

#Need a check state of stepper motor, check notebook for idea.

#while True:
  set_step('0000')
  delay = input("Delay between steps (milliseconds)?")
  steps = input("How many steps forward? ")
  forward(int(delay) / 1000.0, int(steps))
  set_step('0000')
  steps = input("How many steps backwards? ")
  backwards(int(delay) / 1000.0, int(steps))

sleep(1)

print("SOLENOID TIME for R1")

sleep(1)
GPIO.output(R1, GPIO.HIGH)
sleep(10)

GPIO.output(R1, GPIO.LOW)
print "Solenoid now off"

print "Stopping program now"

sleep(1)

GPIO.cleanup()

		
		
