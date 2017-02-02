#This program starts by setting up all fingers and both motors
#Then one by one places the fingers down. Moves the motors forward and backward. Then one by one again places fingers down

import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

L1 =  11
L2 =  13
L3 =  15 
L4 =  29
L5 =  31
L6 =  33
L7 =  35

R1 =  12
R2 =  24
R3 =  26
R4 =  32
R5 =  36
R6 =  38
R7 =  40

Motor1A1 = 7
Motor1A2 = 8
Motor1B1 = 19 
Motor1B2 = 21

Motor2A1 = 10
Motor2A2 = 16
Motor2B1 = 18
Motor2B2 = 23

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




print "All fingers down"
GPIO.output(L1,GPIO.HIGH)
sleep(.5)
GPIO.output(L1,GPIO.LOW)
GPIO.output(L2,GPIO.HIGH)
sleep(.5)
GPIO.output(L2, GPIO.LOW)
GPIO.output(L3,GPIO.HIGH)
sleep(.5)
GPIO.output(L3,GPIO.LOW)
GPIO.output(L4,GPIO.HIGH)
sleep(.5)
GPIO.output(L4,GPIO.LOW)
GPIO.output(L5,GPIO.HIGH)
sleep(.5)
GPIO.output(L5,GPIO.LOW)
GPIO.output(L6,GPIO.HIGH)
sleep(.5)
GPIO.output(L6,GPIO.LOW)
GPIO.output(L7,GPIO.HIGH)
sleep(.5)
GPIO.output(L7,GPIO.LOW)
GPIO.output(R1,GPIO.HIGH)
sleep(.5)
GPIO.output(R1,GPIO.LOW)
GPIO.output(R2,GPIO.HIGH)
sleep(.5)
GPIO.output(R2,GPIO.LOW)
GPIO.output(R3,GPIO.HIGH)
sleep(.5)
GPIO.output(R3,GPIO.LOW)
GPIO.output(R4,GPIO.HIGH)
sleep(.5)
GPIO.output(R4,GPIO.LOW)
GPIO.output(R5,GPIO.HIGH)
sleep(.5)
GPIO.output(R5,GPIO.LOW)
GPIO.output(R6,GPIO.HIGH)
sleep(.5)
GPIO.output(R6,GPIO.LOW)
GPIO.output(R7,GPIO.HIGH)
sleep(.5)
GPIO.output(R7,GPIO.LOW)


sleep(2)
#print "Add motor movement here"
set_stepL('0000')
set_stepR('0000')
print "forward left hand and right hand"
forwardL(int(2)/1000.0, int(100))
forwardR(int(2)/1000.0, int(100))
print "sleep"
sleep(0.1)
set_stepL('0000')
set_stepR('0000')
print "backwards left hand and right hand"
backwardsL(int(2)/1000.0, int(100))#delay 100ms, 20 steps
backwardsR(int(2)/1000.0, int(100))
print "sleep"
sleep(0.1)

sleep(1)

GPIO.cleanup()
