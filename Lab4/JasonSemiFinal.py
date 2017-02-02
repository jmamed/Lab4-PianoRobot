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
#Pin setup L1->L7 is all left hand fingers R1->R7 is all right hand 
#fingers Pins 3, 5, 16, 18, 22, 19, 21, 23 are unavailable Left hand 
#pins
L1 = 11 
L2 = 13 
L3 = 15 
L4 = 29 
L5 = 31 
L6 = 33 
L7 = 35
#Right hand pins
R1 = 12 
R2 = 24 
R3 = 26 
R4 = 32 
R5 = 36 
R6 = 38
R7 = 40

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
#Solenoid setup LEFT HAND/FINGER SETUP
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
#MotorSetup & Code Motor 1!!!!!
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

####################################################################################
###################How string comparison is set up######################
#Hand positions with current value ranges prob will change. LS0 = 24->30 
#LS1 = 31->37 LS2 = 38->44 LS3 = 45->51 RS4 = 52->58 WRONG^ ALL WRONG 
#RS3 = 59->65 RS2 = 66->72 RS1 = 73->79 RS0 = 80->85 Left Hand
msg24_ON = mido.Message('note_on', note=24) msg24_OFF = 
mido.Message('note_off', note=24) msg25_ON = mido.Message('note_on', 
note=25) msg25_OFF = mido.Message('note_off', note=25) msg26_ON = 
mido.Message('note_on', note=26) msg26_OFF = mido.Message('note_off', 
note=26) msg27_ON = mido.Message('note_on', note=27) msg27_OFF = 
mido.Message('note_off', note=27) msg28_ON = mido.Message('note_on', 
note=28) msg28_OFF = mido.Message('note_off', note=28) msg29_ON = 
mido.Message('note_on', note=29) msg29_OFF = mido.Message('note_off', 
note=29) msg30_ON = mido.Message('note_on', note=30) msg30_OFF = 
mido.Message('note_off', note=30) msg31_ON = mido.Message('note_on', 
note=31) msg31_OFF = mido.Message('note_off', note=31) msg32_ON = 
mido.Message('note_on', note=32) msg32_OFF = mido.Message('note_off', 
note=32) msg33_ON = mido.Message('note_on', note=33) msg33_OFF = 
mido.Message('note_off', note=33) msg34_ON = mido.Message('note_on', 
note=34) msg34_OFF = mido.Message('note_off', note=34) msg35_ON = 
mido.Message('note_on', note=35) msg35_OFF = mido.Message('note_off', 
note=35) msg36_ON = mido.Message('note_on', note=36) msg36_OFF = 
mido.Message('note_off', note=36) msg37_ON = mido.Message('note_on', 
note=37) msg37_OFF = mido.Message('note_off', note=37) msg38_ON = 
mido.Message('note_on', note=38) msg38_OFF = mido.Message('note_off', 
note=38) msg39_ON = mido.Message('note_on', note=39) msg39_OFF = 
mido.Message('note_off', note=39) msg40_ON = mido.Message('note_on', 
note=40) msg40_OFF = mido.Message('note_off', note=40) msg41_ON = 
mido.Message('note_on', note=41) msg41_OFF = mido.Message('note_off', 
note=41) msg42_ON = mido.Message('note_on', note=42) msg42_OFF = 
mido.Message('note_off', note=42) msg43_ON = mido.Message('note_on', 
note=43) msg43_OFF = mido.Message('note_off', note=43) msg44_ON = 
mido.Message('note_on', note=44) msg44_OFF = mido.Message('note_off', 
note=44) msg45_ON = mido.Message('note_on', note=45) msg45_OFF = 
mido.Message('note_off', note=45) msg46_ON = mido.Message('note_on', 
note=46) msg46_OFF = mido.Message('note_off', note=46) msg47_ON = 
mido.Message('note_on', note=47) msg47_OFF = mido.Message('note_off', 
note=47) msg48_ON = mido.Message('note_on', note=48) msg48_OFF = 
mido.Message('note_off', note=48) msg49_ON = mido.Message('note_on', 
note=49) msg49_OFF = mido.Message('note_off', note=49) msg50_ON = 
mido.Message('note_on', note=50) msg50_OFF = mido.Message('note_off', 
note=50) msg51_ON = mido.Message('note_on', note=51) msg51_OFF = 
mido.Message('note_off', note=51)
#Right Hand
msg52_ON = mido.Message('note_on', note=52) msg52_OFF = 
mido.Message('note_off', note=52) msg53_ON = mido.Message('note_on', 
note=53) msg53_OFF = mido.Message('note_off', note=53) msg54_ON = 
mido.Message('note_on', note=54) msg54_OFF = mido.Message('note_off', 
note=54) msg55_ON = mido.Message('note_on', note=55) msg55_OFF = 
mido.Message('note_off', note=55) msg56_ON = mido.Message('note_on', 
note=56) msg56_OFF = mido.Message('note_off', note=56) msg57_ON = 
mido.Message('note_on', note=57) msg57_OFF = mido.Message('note_off', 
note=57) msg58_ON = mido.Message('note_on', note=58) msg58_OFF = 
mido.Message('note_off', note=58) msg59_ON = mido.Message('note_on', 
note=59) msg59_OFF = mido.Message('note_off', note=59) msg60_ON = 
mido.Message('note_on', note=60) msg60_OFF = mido.Message('note_off', 
note=60) msg61_ON = mido.Message('note_on', note=61) msg61_OFF = 
mido.Message('note_off', note=61) msg62_ON = mido.Message('note_on', 
note=62) msg62_OFF = mido.Message('note_off', note=62) msg63_ON = 
mido.Message('note_on', note=63) msg63_OFF = mido.Message('note_off', 
note=63) msg64_ON = mido.Message('note_on', note=64) msg64_OFF = 
mido.Message('note_off', note=64) msg65_ON = mido.Message('note_on', 
note=65) msg65_OFF = mido.Message('note_off', note=65) msg66_ON = 
mido.Message('note_on', note=66) msg66_OFF = mido.Message('note_off', 
note=66) msg67_ON = mido.Message('note_on', note=67) msg67_OFF = 
mido.Message('note_off', note=67) msg68_ON = mido.Message('note_on', 
note=68) msg68_OFF = mido.Message('note_off', note=68) msg69_ON = 
mido.Message('note_on', note=69) msg69_OFF = mido.Message('note_off', 
note=69) msg70_ON = mido.Message('note_on', note=70) msg70_OFF = 
mido.Message('note_off', note=70) msg71_ON = mido.Message('note_on', 
note=71) msg71_OFF = mido.Message('note_off', note=71) msg72_ON = 
mido.Message('note_on', note=72) msg72_OFF = mido.Message('note_off', 
note=72) msg73_ON = mido.Message('note_on', note=73) msg73_OFF = 
mido.Message('note_off', note=73) msg74_ON = mido.Message('note_on', 
note=74) msg74_OFF = mido.Message('note_off', note=74) msg75_ON = 
mido.Message('note_on', note=75) msg75_OFF = mido.Message('note_off', 
note=75) msg76_ON = mido.Message('note_on', note=76) msg76_OFF = 
mido.Message('note_off', note=76) msg77_ON = mido.Message('note_on', 
note=77) msg77_OFF = mido.Message('note_off', note=77) msg78_ON = 
mido.Message('note_on', note=78) msg78_OFF = mido.Message('note_off', 
note=78) msg79_ON = mido.Message('note_on', note=79) msg79_OFF = 
mido.Message('note_off', note=79) msg80_ON = mido.Message('note_on', 
note=80) msg80_OFF = mido.Message('note_off', note=80) msg81_ON = 
mido.Message('note_on', note=81) msg81_OFF = mido.Message('note_off', 
note=81) msg82_ON = mido.Message('note_on', note=82) msg82_OFF = 
mido.Message('note_off', note=82) msg83_ON = mido.Message('note_on', 
note=83) msg83_OFF = mido.Message('note_off', note=83) msg84_ON = 
mido.Message('note_on', note=84) msg84_OFF = mido.Message('note_off', 
note=84)
###############################################################################
#Defines how to move between positions#
###############################################################################
#Electric keyboard broken into 9 sections <-backward# LS0, LS1, LS2, 
#LS3, RS4, RS3, RS2, RS1, RS0 forward ->#
LS0 = 0 
LS1 = 1 
LS2 = 2 
LS3 = 3
 
RS0 = 0
RS1 = 1 
RS2 = 2 
RS3 = 3 
RS4 = 4 

def Left_forward():
	if LX = 3
		forwardL(int(100)/1000.0, int(50)) #100/1000 = speed, 50 = pos1
	elif LX = 2
		forwardL(int(100)/1000.0, int(100))
	elif LX = 1
		forwardL(int(100)/1000.0, int(150))
		
def Left_backward():
	if LX = 3
		backwardsL(int(100)/1000.0, int(50))
	elif LX = 2
		backwardsL(int(100)/1000.0, int(100))
	elif LX = 1
		backwardsL(int(100)/1000.0, int(150)) 

def Right_forward():
	if RX = 4
		forwardR(int(100)/1000.0, int(50))
	elif RX = 3
		forwardR(int(100)/1000.0, int(100))
	elif RX = 2
		forwardR(int(100)/1000.0, int(150))
	elif RX = 1
		forwardR(int(100)/1000.0, int(200))
		
def Right_backward():
	if RX = 4
		backwardsR(int(100)/1000.0, int(50))
	elif RX = 3
		backwardsR(int(100)/1000.0, int(100))
	elif RX = 2
		backwardsR(int(100)/1000.0, int(150))
	elif RX = 1
		backwardsR(int(100)/1000.0, int(200))
		
###############################################################################
###############################################################################
##############################  Main_Program ##################################
###############################################################################	
###############################################################################
#Midi Message Decoder Program
mid = MidiFile('mary.mid') print mid
			
for message in MidiFile('mary.mid').play(): #test.mid
#Jason - need to make this probably user input or selectable or else 
#you'll just have multiple scripts with only the file name changing.
	if LS0 < LS1 < LS2 <LS3 and RS0 < RS1 < RS2 < RS3 < RS4: #Prob 
useless
		if message.type == ('note_on'):
		set_step('0000')
		LX = 0
		RX = 0
		Current_LeftHandPos = 0
		Current_RightHandPos = 0
		Next_LeftHandPos = 0
		Next_RightHandPos = 0
			if message.note == msg24_ON.note:
				Next_LeftHandPos = LS0 #change this
				if Current_LeftHandPos < Next_LeftHandPos:
					LX = Next_LeftHandPos - Current_LeftHandPos
					Left_forward(LX)
					sleep(1)
					GPIO.output(L1, GPIO.HIGH) #change this
					print "R1 Solenoid activated"
					sleep(1) #This is in seconds.
					Current_LeftHandPos = L0 #change this
					print message
				elif Current_LeftHandPos > Next_LeftHandPos:
					LX = Current_LeftHandPos - Next_LeftHandPos
					Left_backward(LX)
					sleep(1)
					GPIO.output(L1, GPIO.HIGH) #change this
					print "R1 Solenoid activated"
					sleep(1)
					Current_LeftHandPos = L0 #change this
					print message
				elif Current_LeftHandPos = Next_LeftHandPos:
					sleep(1)
					GPIO.output(L1, GPIO.HIGH) #change this
					print "R1 Solenoid activated"
					sleep(1)
					Current_LeftHandPos = L0 #change this
					print message
			elif message.note == msg60_ON.note:
				Next_RightHandPos = RS3
				if Current_RightHandPos < Next_RightHandPos:
					RX = Next_LeftHandPos - Current_LeftHandPos
					Right_backward(RX)
					sleep(1)
					GPIO.output(R1, GPIO.HIGH)#change this
					print "R1 Solenoid activated"
					sleep(1) #This is in seconds.
					Current_RightHandPos = RS3#change this
					print message
				elif Current_LeftRightPos > Next_RightHandPos:
					RX = Current_RightHandPos - Next_RightHandPos
					Right_forward(RX)
					sleep(1)
					GPIO.output(R1, GPIO.HIGH) #change this
					print "R1 Solenoid activated"
					sleep(1)
					Current_RightHandPos = RS3 #change this
					print message
				elif Current_LeftHandRight = Next_RightHandPos:
					#dont move!
					print "Left hand don't move"
					GPIO.output(R1, GPIO.HIGH) #change this
					print "R1 Solenoid activated"
					sleep(1)
					Current_RightHandPos = RS3 #change this
					print message
			elif message.note == msg84_ON.note:
				#move stepper to position R1
				sleep(0.2)
				print "Hand was moved"
				GPIO.output(R1, GPIO.HIGH)
				sleep(1)
				print message
			
			
	elif message.type == ('note_off'):
	
		#Left Hand
		
		if message.note == msg24_OFF.note:
			GPIO.output(L1, GPIO.LOW)
			print "R1 Solenoid De-activated"
			sleep(1)
			print message
		elif message.note == msg25_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg26_OFF.note:
			GPIO.output(L2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg27_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg28_OFF.note:
			GPIO.output(L3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg29_OFF.note:
			GPIO.output(L4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg30_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg31_OFF.note:
			GPIO.output(L5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg32_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg33_OFF.note:
			GPIO.output(L1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg34_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg35_OFF.note:
			GPIO.output(L2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg36_OFF.note:
			GPIO.output(L3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg37_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg38_OFF.note:
			GPIO.output(L4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg39_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg40_OFF.note:
			GPIO.output(L5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg41_OFF.note:
			GPIO.output(L1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg42_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg43_OFF.note:
			GPIO.output(L2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg44_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg45_OFF.note:
			GPIO.output(L3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg46_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg47_OFF.note:
			GPIO.output(L4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg48_OFF.note:
			GPIO.output(L5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg49_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg50_OFF.note:
			GPIO.output(L1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg51_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		
		
		#Right Hand
		
		
		elif message.note == msg52_OFF.note:
			GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg53_OFF.note:
			GPIO.output(R2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg54_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg55_OFF.note:
			GPIO.output(R3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg56_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg57_OFF.note:
			GPIO.output(R4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg58_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg59_OFF.note:
			GPIO.output(R5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg60_OFF.note:
			GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg61_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "R1 Solenoid De-activated"
			sleep(1)
			print message
		elif message.note == msg62_OFF.note:
			GPIO.output(R2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg63_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg64_OFF.note:
			GPIO.output(R3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg65_OFF.note:
			GPIO.output(R4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg66_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg67_OFF.note:
			GPIO.output(R5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg68_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg69_OFF.note:
			GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg70_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg71_OFF.note:
			GPIO.output(R2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg72_OFF.note:
			GPIO.output(R3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg73_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg74_OFF.note:
			GPIO.output(R4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg75_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg76_OFF.note:
			GPIO.output(R5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg77_OFF.note:
			GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg78_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg79_OFF.note:
			GPIO.output(R2, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg80_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg81_OFF.note:
			GPIO.output(R3, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg82_OFF.note:
			#GPIO.output(R1, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg83_OFF.note:
			GPIO.output(R4, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message
		elif message.note == msg84_OFF.note:
			GPIO.outpu(R5, GPIO.LOW)
			print "De-activate solenoid"
			sleep(1)
			print message 

GPIO.cleanup()
###############################################################################			
		
