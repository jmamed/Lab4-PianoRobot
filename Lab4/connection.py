#import Libraries
import RPi.GPIO as GPIO
import time
import pyrebase
from pyrebase import pyrebase

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
GPIO.setup(29, GPIO.OUT)

#Firebase Database Intialization
db = firebase.database()

#While loop to run until user kills program
while(True):
    #Get value of LED 
    led = db.child("led").get()

    #Sort through children of LED(we only have one)
    for user in led.each():
        #Check value of child(which is 'state')
        if(user.val() == "OFF"):
            #If value is off, turn LED off
            GPIO.output(29, False)
        else:
            #If value is not off(implies it's on), turn LED on
            GPIO.output(29, True)

        #0.1 Second Delay
        time.sleep(0.1)
