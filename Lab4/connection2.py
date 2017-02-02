#import Libraries
import RPi.GPIO as GPIO
import time
import pyrebase
from time import sleep

############################################
#May need this too pull the files required before executing them.
#import sys
#sys.argv = ['song1', 'song2', 'song3']

#import os
import SongTemplate #Sub file which equals each individual song scripts (I think 4 songs total)
#import subsongFile #Now call the function in this file!

#import HardCode
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
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Proximity Sensor
ProximitySensorLeftHand = GPIO.input(22)
ProximitySensorRightHand = GPIO.input(37)
GPIO.setup(ProximitySensorLeftHand, GPIO.IN) #pin 22
GPIO.setup(ProximitySensorRightHand, GPIO.IN) #pin 37
#MAKE SURE TO GND!

#Firebase Database Intialization
db = firebase.database()		
		
if ProximitySensorLeftHand == 0 && ProximitySensorRightHand == 0:
	DecodeMidiProgram(0) #Move Left Hand
elif ProximitySensorLeftHand == 1 && ProximitySensorRightHand == 0:
	DecodeMidiProgram(1) #Move Right hand
elif ProximitySensorLeftHand == 0 && ProximitySensorRightHand == 1:
	DecodeMidiProgram(0) #Move Left Hand
elif ProximitySensorLeftHand == 1 && ProximitySensorRightHand == 1:

	#Used to be a while(true) here
	#Assign child from Firebase a variable
	#In this case, "song" is the child in the firebase of which state we are looking for.
	song = db.child("song").get()
	
	#Sort through children of song 
	for user in song.each():
		#Check value of child (which is the 'state')
		if (user.val() == "STOP"): #This the Red Stop Button on IOS App!!!!
			try:
				time.sleep(2)
				print("Sleep for 1 second intervals until new command issued!")
			except KeyboardInterrupt:
				print("Keyboard Interrupt called. Possible error or user action.")
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
				print("filename1.py exited)
			
			
		#0.1 Second Delay
		time.sleep(0.1)
			
			