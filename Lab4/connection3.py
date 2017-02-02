#import Libraries
import RPi.GPIO as GPIO
import time
import pyrebase
from time import sleep
#import Robot_Control #Sub file which includes the decoder function, motor and solenoid controls.
#from Robot_Control import *
#import os
#import subsongFile #Now call the function in this file!
#import HardCode?

#import time
#from time import sleep
#import RPi.GPIO as GPIO
import mido
import re
import operator
from mido import MidiFile
#from parse import *

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
###################################################


#Firebase Configuration
config = {
  "apiKey": "apiKey",
  "authDomain": "pianorobotwithfirebase-16599.firebaseapp.com",
  "databaseURL": "https://pianorobotwithfirebase-16599.firebaseio.com",
  "storageBucket": "pianorobotwithfirebase-16599.appspot.com"
}

firebase = pyrebase.initialize_app(config)

#GPIO Setup
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

#Proximity Sensor
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 22
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 37
#MAKE SURE TO GND!

#Firebase Database Intialization
db = firebase.database()		
	
def iOS_Inputs(I): #Function to check the Database(Firebase) for commands from the iOS app!
	if I == 0:
		song = db.child("song").get()
		#Sort through children of song
		#Assign child from Firebase a variable
		#In this case, "song" is the child in the firebase of which state we are looking for.	
		for user in song.each():
			#Check value of child (which is the 'state')
			if (user.val() == "STOP"): #This the Red Stop Button on IOS App!!!!
				try:
					time.sleep(2)
					print("Sleep for 1 second intervals until new command issued!")
				except KeyboardInterrupt:
					print("Keyboard Interrupt called. Possible error or user action.")
			elif (user.val() == "RESTART"):
				#If song1 is entered, play function with that song
				#break #or raise exception
				return

###############Song options below!!!!!!!!################
#Found a flaw, if user switches from song1 to song2 without resetting then hands won't
#reset back to the starting position. Add a comment that before changing songs hit restart button
#first on iOS app before selecting the next song?
			elif (user.val() == "song1"):
				#If song1 is entered, play function with that song
				try:
					DecodeMidiProgram(2)
				except KeyboardInterrupt:
					print("filename1.py exited")
			elif (user.val() == "song2"):
				try:
					DecodeMidiProgram(3)
				except KeyboardInterrupt:
					print("filename1.py exited")
			
			#0.1 Second Delay
			time.sleep(0.1)
	

####################################
#New idea, two while loops. First while loop runs the code. 2nd while loop,
#When "break" occurs will restart the code. 
#When inner while loop breaks, then reset hand positions.
#When outer while loop breaks, this program ends.
#What if Motor reset is a function???


#This is a python program to try and translate midi input into GPIO
#Deriven from pseudo code idea.

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

Motor2A1 = 10 
Motor2A2 = 16
Motor2B1 = 18 
Motor2B2 = 23

#Proximity Sensor
ProximitySensorLeftHand = 37
ProximitySensorRightHand = 22
#MAKE SURE TO GND!


#######################################################################################
#Solenoid setup

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
  
  
  
################################################################################
############################Zero out hand Positions#############################

GPIO.setup(ProximitySensorLeftHand, GPIO.OUT) #pin 3
GPIO.setup(ProximitySensorRightHand, GPIO.OUT) #pin 5


#################################################################################  



####################################################################################

###################How string comparison is set up###################### 

#Hand positions with current value ranges prob will change.
#LS0 = 24->30
#LS1 = 31->37
#LS2 = 38->44
#LS3 = 45->51
#RS4 = 52->58		WRONG^ ALL WRONG
#RS3 = 59->65
#RS2 = 66->72
#RS1 = 73->79
#RS0 = 80->85

#Left Hand
msg36_ON = mido.Message('note_on', note=36)
msg36_OFF = mido.Message('note_off', note=36)
msg37_ON = mido.Message('note_on', note=37)
msg37_OFF = mido.Message('note_off', note=37)
msg38_ON = mido.Message('note_on', note=38)
msg38_OFF = mido.Message('note_off', note=38)
msg39_ON = mido.Message('note_on', note=39)
msg39_OFF = mido.Message('note_off', note=39)
msg40_ON = mido.Message('note_on', note=40)
msg40_OFF = mido.Message('note_off', note=40)
msg41_ON = mido.Message('note_on', note=41)
msg41_OFF = mido.Message('note_off', note=41)
msg42_ON = mido.Message('note_on', note=42)
msg42_OFF = mido.Message('note_off', note=42)
msg43_ON = mido.Message('note_on', note=43)
msg43_OFF = mido.Message('note_off', note=43)
msg44_ON = mido.Message('note_on', note=44)
msg44_OFF = mido.Message('note_off', note=44)
msg45_ON = mido.Message('note_on', note=45)
msg45_OFF = mido.Message('note_off', note=45)
msg46_ON = mido.Message('note_on', note=46)
msg46_OFF = mido.Message('note_off', note=46)
msg47_ON = mido.Message('note_on', note=47)
msg47_OFF = mido.Message('note_off', note=47)
msg48_ON = mido.Message('note_on', note=48)
msg48_OFF = mido.Message('note_off', note=48)
msg49_ON = mido.Message('note_on', note=49)
msg49_OFF = mido.Message('note_off', note=49)
msg50_ON = mido.Message('note_on', note=50)
msg50_OFF = mido.Message('note_off', note=50)
msg51_ON = mido.Message('note_on', note=51)
msg51_OFF = mido.Message('note_off', note=51)
msg52_ON = mido.Message('note_on', note=52)
msg52_OFF = mido.Message('note_off', note=52)
msg53_ON = mido.Message('note_on', note=53)
msg53_OFF = mido.Message('note_off', note=53)
msg54_ON = mido.Message('note_on', note=54)
msg54_OFF = mido.Message('note_off', note=54)
msg55_ON = mido.Message('note_on', note=55)
msg55_OFF = mido.Message('note_off', note=55)
msg56_ON = mido.Message('note_on', note=56)
msg56_OFF = mido.Message('note_off', note=56)

#Right Hand

msg57_ON = mido.Message('note_on', note=57)
msg57_OFF = mido.Message('note_off', note=57)
msg58_ON = mido.Message('note_on', note=58)
msg58_OFF = mido.Message('note_off', note=58)
msg59_ON = mido.Message('note_on', note=59)
msg59_OFF = mido.Message('note_off', note=59)
msg60_ON = mido.Message('note_on', note=60)
msg60_OFF = mido.Message('note_off', note=60)
msg61_ON = mido.Message('note_on', note=61)
msg61_OFF = mido.Message('note_off', note=61)
msg62_ON = mido.Message('note_on', note=62)
msg62_OFF = mido.Message('note_off', note=62)
msg63_ON = mido.Message('note_on', note=63)
msg63_OFF = mido.Message('note_off', note=63)
msg64_ON = mido.Message('note_on', note=64)
msg64_OFF = mido.Message('note_off', note=64)
msg65_ON = mido.Message('note_on', note=65)
msg65_OFF = mido.Message('note_off', note=65)
msg66_ON = mido.Message('note_on', note=66)
msg66_OFF = mido.Message('note_off', note=66)
msg67_ON = mido.Message('note_on', note=67)
msg67_OFF = mido.Message('note_off', note=67)
msg68_ON = mido.Message('note_on', note=68)
msg68_OFF = mido.Message('note_off', note=68)
msg69_ON = mido.Message('note_on', note=69)
msg69_OFF = mido.Message('note_off', note=69)
msg70_ON = mido.Message('note_on', note=70)
msg70_OFF = mido.Message('note_off', note=70)
msg71_ON = mido.Message('note_on', note=71)
msg71_OFF = mido.Message('note_off', note=71)
msg72_ON = mido.Message('note_on', note=72)
msg72_OFF = mido.Message('note_off', note=72)
msg73_ON = mido.Message('note_on', note=73)
msg73_OFF = mido.Message('note_off', note=73)
msg74_ON = mido.Message('note_on', note=74)
msg74_OFF = mido.Message('note_off', note=74)
msg75_ON = mido.Message('note_on', note=75)
msg75_OFF = mido.Message('note_off', note=75)
msg76_ON = mido.Message('note_on', note=76)
msg76_OFF = mido.Message('note_off', note=76)
msg77_ON = mido.Message('note_on', note=77)
msg77_OFF = mido.Message('note_off', note=77)
msg78_ON = mido.Message('note_on', note=78)
msg78_OFF = mido.Message('note_off', note=78)
msg79_ON = mido.Message('note_on', note=79)
msg79_OFF = mido.Message('note_off', note=79)
msg80_ON = mido.Message('note_on', note=80)
msg80_OFF = mido.Message('note_off', note=80)
msg81_ON = mido.Message('note_on', note=81)
msg81_OFF = mido.Message('note_off', note=81)
msg82_ON = mido.Message('note_on', note=82)
msg82_OFF = mido.Message('note_off', note=82)
msg83_ON = mido.Message('note_on', note=83)
msg83_OFF = mido.Message('note_off', note=83)
msg84_ON = mido.Message('note_on', note=84)
msg84_OFF = mido.Message('note_off', note=84)
msg85_ON = mido.Message('note_on', note=85)
msg85_OFF = mido.Message('note_off', note=85)
msg86_ON = mido.Message('note_on', note=86)
msg86_OFF = mido.Message('note_off', note=86)
msg87_ON = mido.Message('note_on', note=87)
msg87_OFF = mido.Message('note_off', note=87)
msg88_ON = mido.Message('note_on', note=88)
msg88_OFF = mido.Message('note_off', note=88)
msg89_ON = mido.Message('note_on', note=89)
msg89_OFF = mido.Message('note_off', note=89)
msg90_ON = mido.Message('note_on', note=90)
msg90_OFF = mido.Message('note_off', note=90)
msg91_ON = mido.Message('note_on', note=91)
msg91_OFF = mido.Message('note_off', note=91)
msg92_ON = mido.Message('note_on', note=92)
msg92_OFF = mido.Message('note_off', note=92)
msg93_ON = mido.Message('note_on', note=93)
msg93_OFF = mido.Message('note_off', note=93)
msg94_ON = mido.Message('note_on', note=94)
msg94_OFF = mido.Message('note_off', note=94)
msg95_ON = mido.Message('note_on', note=95)
msg95_OFF = mido.Message('note_off', note=95)
msg96_ON = mido.Message('note_on', note=96)
msg96_OFF = mido.Message('note_off', note=96)


###############################################################################
#Defines how to move between positions#
###############################################################################
#Electric keyboard broken into 8 main sections
#Sub sections = 10

#<-backward#
#LS0, LS1, LS2, RS3, RS2, RS1, RS0, SRS0
#SLS0, SLS1, SLS2, SLS3, SLS4, SRS5, SRS4, SRS3, SRS2, SRS1
#forward ->#


SLS0 = 0 #This is the true far left position!!!!!!!!!!!!
LS0 = 0.1
LS1 = 1.1
LS2 = 2.1 

SRS0 = 0 #This is the true far right position!!!!!!!!! 
RS0 = 0.8
RS1 = 1.8	
RS2 = 2.8 
RS3 = 3.8 

SLS1 = 0.4
SLS2 = 0.8
SLS3 = 1.4 	
SLS4 = 2.0

#checked this
SRS1 = 0.2 
SRS2 = 1.0 
SRS3 = 1.4 
SRS4 = 2.2 
SRS5 = 3.2 

##############Need this not sure where it should go.
set_stepL('0000')
set_stepR('0000')
LX = 0 
RX = 0 
Current_LeftHandPos = 0 
Current_RightHandPos = 0
Next_LeftHandPos = 0 
Next_RightHandPos = 0 

def Left_forward(LX):
	if LX == 3: 
		forwardL(int(2)/1000.0, int(300)) #100/1000 = speed, 50 = pos1
	elif LX == 2:
		forwardL(int(2)/1000.0, int(200))
	elif LX == 1: 
		forwardL(int(2)/1000.0, int(100))
	elif LX == 2.5:
		forwardL(int(2)/1000.0, int(250))
	elif LX == 2.1: 
		forwardL(int(2)/1000.0, int(210))
	#1.9
	elif LX == 1.5:
		forwardL(int(2)/1000.0, int(150))
	elif LX == 1.1: 
		forwardL(int(2)/1000.0, int(110))
	
	#0.9
	#0.5
		
def Left_backward(LX):
	if LX == 3: 
		backwardsL(int(2)/1000.0, int(300))
	elif LX == 2:
		backwardsL(int(2)/1000.0, int(200))
	elif LX == 1: 
		backwardsL(int(2)/1000.0, int(100))
	elif LX == 2.5:
		backwardsL(int(2)/1000.0, int(250))
	elif LX == 2.1: 
		backwardsL(int(2)/1000.0, int(210))
	elif LX == 1.5:
		backwardsL(int(2)/1000.0, int(150))
	elif LX == 1.1: 
		backwardsL(int(2)/1000.0, int(110))

def Right_forward(RX):
	if RX == 4:
		forwardR(int(2)/1000.0, int(400))
	elif RX == 3: 
		forwardR(int(2)/1000.0, int(300))
	elif RX == 2:
		forwardR(int(2)/1000.0, int(200))
	elif RX == 1:
		forwardR(int(2)/1000.0, int(100))
	#In between cases
	elif RX == 3.5: 
		forwardR(int(2)/1000.0, int(350))
	elif RX == 2.5:
		forwardR(int(2)/1000.0, int(250))
	elif RX == 1.5: 
		forwardR(int(2)/1000.0, int(150))
	elif RX == 1.1: 
		forwardR(int(2)/1000.0, int(110))
	elif RX == 0.5:
		forwardR(int(2)/1000.0, int(50))
		
def Right_backward(RX):
	if RX == 4:
		backwardsR(int(2)/1000.0, int(400))
		return
	elif RX == 3: 
		backwardsR(int(2)/1000.0, int(300))
		return
	elif RX == 2:
		backwardsR(int(2)/1000.0, int(200))
	elif RX == 1:
		backwardsR(int(2)/1000.0, int(100))
	#In between cases
	elif RX == 3.5: 
		backwardsR(int(2)/1000.0, int(350))
	elif RX == 2.5:
		backwardsR(int(2)/1000.0, int(250))
	elif RX == 1.5: 
		backwardsR(int(2)/1000.0, int(150))
	elif RX == 1.1: 
		backwardsR(int(2)/1000.0, int(110))
	elif RX == 0.5:
		backwardsR(int(2)/1000.0, int(50))
		
###############################################################################

###############################################################################
##############################  Main_Program  #################################	
###############################################################################	

###############################################################################

#Midi Message Decoder Program

##########Print Full message###############
#mid = MidiFile('c-major-scale.mid')
#print(mid)		
	
######################	
	
#What if i import this python script and execute the Decode MidiProgram???? Use it as a function
#instead of executing the file itself, just run the function.
#And every song has its on function so DecodeMidiProgram1, DecodeMidiProgram2, etc.


def FingerFlush(F):
	#Clear Solenoids
	if F == 0:
		GPIO.output(R1, GPIO.LOW)
		GPIO.output(R2, GPIO.LOW)
		GPIO.output(R3, GPIO.LOW)
		GPIO.output(R4, GPIO.LOW)
		GPIO.output(R5, GPIO.LOW)
		GPIO.output(R6, GPIO.LOW)
		GPIO.output(R7, GPIO.LOW)
		GPIO.output(L1, GPIO.LOW)
		GPIO.output(L2, GPIO.LOW)
		GPIO.output(L3, GPIO.LOW)
		GPIO.output(L4, GPIO.LOW)
		GPIO.output(L5, GPIO.LOW)
		GPIO.output(L6, GPIO.LOW)
		GPIO.output(L7, GPIO.LOW)
	return
	

#Define DecoderProgram function
def DecodeMidiProgram(X):
	if X == 0: #Move left hand
		forwardL(int(2)/1000.0, int(10))
		return
		#Interrupt if finish early????? Maybe if more than 1 step at a time.
	elif X == 1:#Move Right hand
		backwardsR(int(2)/1000.0, int(10))
		return
	elif X == 2: #Run Decoder Program
		for message in MidiFile('silent_night_easy.mid').play(): #test.mid
		#Jason - need to make this probably user input or selectable or else you'll just have multiple scripts with only the file name changing.
			if message.type == ('note_on'):
		##########Left Hand##############	
				if message.note == msg36_ON.note:
					Next_LeftHandPos = LS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg37_ON.note:
					Next_LeftHandPos = SLS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg38_ON.note:
					Next_LeftHandPos = LS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg39_ON.note:
					Next_LeftHandPos = SLS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg40_ON.note:
					Next_LeftHandPos = LS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg41_ON.note:
					Next_LeftHandPos = LS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg42_ON.note:
					Next_LeftHandPos = SLS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg43_ON.note:
					Next_LeftHandPos = LS0				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg44_ON.note:
					Next_LeftHandPos = SLS2				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg45_ON.note:
					Next_LeftHandPos = LS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg46_ON.note:
					Next_LeftHandPos = SLS2				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg47_ON.note:
					Next_LeftHandPos = LS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg48_ON.note:
					Next_LeftHandPos = LS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25) 
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg49_ON.note:
					Next_LeftHandPos = LS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg50_ON.note:
					Next_LeftHandPos = LS1				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg51_ON.note:
					Next_LeftHandPos = SLS3				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = SLS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = SLS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg52_ON.note:
					Next_LeftHandPos = LS2				#change this
					if Current_LeftHandPos < Next_LeftHandPos:
						LX = Next_LeftHandPos - Current_LeftHandPos
						Left_forward(LX)
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_LeftHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos > Next_LeftHandPos:
						LX = Current_LeftHandPos - Next_LeftHandPos
						Left_backward(LX)
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_LeftHandPos == Next_LeftHandPos:
						sleep(0.25)
						GPIO.output(L1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_LeftHandPos = LS2		#change this
						print(message)
						FingerFlush(0)				
################Fix motor logic this down to right hand## copy paste fail	53->59 fucked up###########			
				elif message.note == msg53_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg54_ON.note:
					Next_RightHandPos = SLS4
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SLS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SLS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SLS4		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg55_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg56_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg57_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg58_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg59_ON.note:
					Next_RightHandPos = LS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(L5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = LS2		#change this
						print(message)
						FingerFlush(0)

						#Fix above stuff
		############Right Hand####################
			
				elif message.note == msg60_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg61_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg62_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg63_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg64_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush
				elif message.note == msg65_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg66_ON.note:
					Next_RightHandPos = SRS5
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg67_ON.note:
					Next_RightHandPos = RS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg68_ON.note:
					Next_RightHandPos = SRS5
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS5		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg69_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg70_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg71_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg72_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg73_ON.note:
					Next_RightHandPos = SRS4
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg74_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg75_ON.note:
					Next_RightHandPos = SRS4
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS4		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg76_ON.note:
					Next_RightHandPos = RS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg77_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg78_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg79_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg80_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg81_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg82_ON.note:
					Next_RightHandPos = SRS3
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS3		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS3		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg83_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg84_ON.note:
					Next_RightHandPos = RS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg85_ON.note:
					Next_RightHandPos = SRS2
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS2		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS2		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg86_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R1, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg87_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg88_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg89_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg90_ON.note:
					Next_RightHandPos = SRS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg91_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R4, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg92_ON.note:
					Next_RightHandPos = SRS1
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R7, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS1		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg93_ON.note:
					Next_RightHandPos = RS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R5, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = RS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg94_ON.note:
					Next_RightHandPos = SRS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R6, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg95_ON.note:
					Next_RightHandPos = SRS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R2, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
				elif message.note == msg96_ON.note:
					Next_RightHandPos = SRS0
					if Current_RightHandPos < Next_RightHandPos:
						RX = Next_RightHandPos - Current_RightHandPos
						Right_backward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25) #This is in seconds.
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos > Next_RightHandPos:
						RX = Current_RightHandPos - Next_RightHandPos
						Right_forward(RX)
						sleep(0.25)
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
					elif Current_RightHandPos == Next_RightHandPos:
						#dont move!
						GPIO.output(R3, GPIO.HIGH)		#change this
						sleep(0.25)
						Current_RightHandPos = SRS0		#change this
						print(message)
						FingerFlush(0)
			
			elif message.type == ('note_off'):
			
				#Left Hand
				
				if message.note == msg36_OFF.note:
					GPIO.output(L2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg37_OFF.note:
					GPIO.output(L6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg38_OFF.note:
					GPIO.output(L3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg39_OFF.note:
					GPIO.output(L7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg40_OFF.note:
					GPIO.output(L4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg41_OFF.note:
					GPIO.output(L5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg42_OFF.note:
					GPIO.output(L6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg43_OFF.note:
					GPIO.output(L1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg44_OFF.note:
					GPIO.output(L6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg45_OFF.note:
					GPIO.output(L2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg46_OFF.note:
					GPIO.output(L7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg47_OFF.note:
					GPIO.output(L3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg48_OFF.note:
					GPIO.output(L4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg49_OFF.note:
					GPIO.output(L7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg50_OFF.note:
					GPIO.output(L5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg51_OFF.note:
					GPIO.output(L7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg52_OFF.note:
					GPIO.output(L1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)		
				elif message.note == msg53_OFF.note:
					GPIO.output(L2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg54_OFF.note:
					GPIO.output(L6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					pprint(message)
				elif message.note == msg55_OFF.note:
					GPIO.output(L3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg56_OFF.note:
					GPIO.output(L6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg57_OFF.note:
					GPIO.output(L4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg58_OFF.note:
					GPIO.output(L7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg59_OFF.note:
					GPIO.output(L5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				
				#Right Hand
				
				elif message.note == msg60_OFF.note:
					GPIO.output(R1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg61_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg62_OFF.note:
					GPIO.output(R2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg63_OFF.note:
					GPIO.output(R7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg64_OFF.note:
					GPIO.output(R3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg65_OFF.note:
					GPIO.output(R4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg66_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg67_OFF.note:
					GPIO.output(R5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg68_OFF.note:
					GPIO.output(R7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg69_OFF.note:
					GPIO.output(R1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg70_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg71_OFF.note:
					GPIO.output(R2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg72_OFF.note:
					GPIO.output(R3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg73_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg74_OFF.note:
					GPIO.output(R4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg75_OFF.note:
					GPIO.output(R7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg76_OFF.note:
					GPIO.output(R5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg77_OFF.note:
					GPIO.output(R1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg78_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg79_OFF.note:
					GPIO.output(R2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg80_OFF.note:
					GPIO.output(R7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg81_OFF.note:
					GPIO.output(R3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg82_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg83_OFF.note:
					GPIO.output(R4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg84_OFF.note:
					GPIO.output(R5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg85_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg86_OFF.note:
					GPIO.output(R1, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg87_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg88_OFF.note:
					GPIO.output(R2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg89_OFF.note:
					GPIO.output(R3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg90_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg91_OFF.note:
					GPIO.output(R4, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg92_OFF.note:
					GPIO.output(R7, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg93_OFF.note:
					GPIO.output(R5, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg94_OFF.note:
					GPIO.output(R6, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg95_OFF.note:
					GPIO.output(R2, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
				elif message.note == msg96_OFF.note:
					GPIO.output(R3, GPIO.LOW)
					print("De-activate solenoid")
					sleep(0.1)
					print(message)
	elif X == 3: #Call Hardcoded song function
		return #dont know if this is needed
		

def LeftReady(L):
	if L == 0:
		ProximitySensorLeftHand = GPIO.input(37)
		if ProximitySensorLeftHand == True:
			#set_stepL('0000')
			#GPIO.output(L1, GPIO.HIGH)
			print("Left Hand ready")
			sleep(1)
			return
		elif ProximitySensorLeftHand == False:
			DecodeMidiProgram(0) #Move Left hand
			print("Left hand not ready")
		
def RightReady(R):
	if R == 0:
		ProximitySensorRightHand = GPIO.input(22)		
		if ProximitySensorRightHand == False:
			DecodeMidiProgram(1) #Move Right Hand
			print("Right Hand not ready")
		elif ProximitySensorRightHand == True:
			#GPIO.output(R1, GPIO.HIGH)
			set_stepR('1111')
			print("Right hand ready")
			GPIO.output(R1, GPIO.HIGH)
			sleep(1)
			return
		
while(True): #When code starts, this loop will continue forever
#################################	
	RightReady(0)
	#LeftReady(0)
	print("Both hands ready now? And proceed?")
	sleep(5)
    #iOS_Inputs(0) 

		#When function returns then robot hands resets and waits to call this function 
		#again to issue new commands. If state is left on RESTART then cycle continues.
		#Maybe issuing a command that the state changes to STOP after 5-10 secs on app code?
		#0.1 Second Delay
	#time.sleep(0.1)
	#except KeyboardInterrupt:
		#print("Program terminated on RPI keyboard?")			

GPIO.cleanup()

###############################################################################	
