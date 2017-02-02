#This is a python program to try and translate midi input into GPIO
#Deriven from pseudo code idea.


from time import sleep
 
import RPi.GPIO as GPIO
import mido
import re
import operator
from mido import MidiFile
from parse import *

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

########################################################################################
#Pin setup

#L1->L7 is all left hand fingers
#R1->R7 is all right hand fingers
#Pins 1->5, 27,28, are unusable

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
  GPIO.output(Motor1A2, step[1] == '1')
  GPIO.output(Motor1B1, step[2] == '1')
  GPIO.output(Motor2B2, step[3] == '1')

#Need a check state of stepper motor, check notebook for idea.

#while True:
  set_step('0000')
  delay = raw_input("Delay between steps (milliseconds)?")
  steps = raw_input("How many steps forward? ")
  forward(int(delay) / 1000.0, int(steps))
  set_step('0000')
  steps = raw_input("How many steps backwards? ")
  backwards(int(delay) / 1000.0, int(steps))



####################################################################################

#Midi Message Decoder Program
mid = MidiFile('test.mid')
print mid

#Hand positions with current value ranges prob will change.
#L0 = 24->33
#L1 = 34->41
#L2 = 42->50
#L3 = 51->59
#R3 = 60->67
#R2 = 68->76
#R1 = 77->84


msg24_ON = mido.Message('note_on', note=24)
msg24_OFF = mido.Message('note_off', note=24)
#Fill in this space 25->59
msg60_ON = mido.Message('note_on', note=60)
msg60_OFF = mido.Message('note_off', note=60)
#Fill in this space 61->83
msg84_ON = mido.Message('note_on', note=84)
msg84_OFF = mido.Message('note_off', note=84)

LS0 = 0
LS1 = 1
LS2 = 2
LS3 = 3

RS0 = 0
RS1 = 1
RS2 = 2
RS3 = 3
RS4 = 4

for message in MidiFile('test.mid').play(): 
#Jason - need to make this probably user input or selectable or else you'll just have multiple scripts with only the file name changing.
	if LS0 < LS1 < LS2 < LS3 and RS0 < RS1 < RS2 < RS3 < RS4:
		if message.type == ('note_on'):
			if message.note == msg24_ON.note:
			#move stepper to position L0
				GPIO.output(R1, GPIO.HIGH)
				print "R1 Solenoid activated"
				sleep(1)
				print message
			elif message.note == msg60_ON.note:
				#move stepper to position R3
				sleep(0.2)
				print "Hand has moved"
				GPIO.output(R1, GPIO.HIGH)
				sleep(1)
				print message
			elif message.note == msg84_ON.note:
				#move stepper to position R1
				sleep(0.2)
				print "Hand was moved"
				GPIO.output(R1, GPIO.HIGH)
				sleep(1)
				print message
		elif message.type == ('note_off'):
			if message.note == msg24_OFF.note:
				GPIO.output(R1, GPIO.LOW)
				print "R1 Solenoid De-activated"
				sleep(1)
				print message
			elif message.note == msg60_OFF.note:
				GPIO.output(R1, GPIO.LOW)
				print "De-activate solenoid"
				sleep(1)
				print message
			elif message.note == msg84_OFF.note:
				GPIO.outpu(R1, GPIO.LOW)
				print "De-activate solenoid"
				sleep(1)
				print message

GPIO.cleanup()

		
		
