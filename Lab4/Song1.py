#First attempt at a song or scale or chord.

import RPi.GPIO as GPIO

from time import sleep


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#L1->L8 is all left hand fingers
#R1->R8 is all right hand fingers
#Pins 16, 18, 22, 19, 21, 23 are unavailable

#Left hand pins
L1 =  11
L2 =  13
L3 =  15 
L4 =  3
L5 =  29
L6 =  31
L7 =  33
L8 =  35
L9 =  37
#Right hand pins
R1 =  12
R2 =  24
R3 =  26
R4 =  5
R5 =  32
R6 =  36
R7 =  38
R8 =  40
R9 =  7

#MotorPins, gives warnings, ignoring though
Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 19
Motor2B = 21
Motor2E = 23


#LEFT HAND/FINGER SETUP
GPIO.setup(L1,GPIO.OUT)
GPIO.setup(L2,GPIO.OUT)
GPIO.setup(L3,GPIO.OUT)
GPIO.setup(L4,GPIO.OUT)
GPIO.setup(L5,GPIO.OUT)
GPIO.setup(L6,GPIO.OUT)
GPIO.setup(L7,GPIO.OUT)
GPIO.setup(L8,GPIO.OUT)
GPIO.setup(L9,GPIO.OUT)


#RIGHT HAND/FINGER SETUP
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)
GPIO.setup(R3,GPIO.OUT)
GPIO.setup(R4,GPIO.OUT)
GPIO.setup(R5,GPIO.OUT)
GPIO.setup(R6,GPIO.OUT)
GPIO.setup(R7,GPIO.OUT)
GPIO.setup(R8,GPIO.OUT)
GPIO.setup(R9,GPIO.OUT)

#MotorSetup
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)


print "Move to position 2 from position 0"

GPIO.output(Motor1A,GPIO.HIGH)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)

GPIO.output(Motor2A,GPIO.HIGH)
GPIO.output(Motor2B,GPIO.LOW)
GPIO.output(Motor2E,GPIO.HIGH)

sleep(2) #Then stop motors
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)

print "play CHORD 1"

GPIO.output(L1,GPIO.HIGH)

GPIO.output(L3,GPIO.HIGH)

GPIO.output(L5,GPIO.HIGH)


GPIO.output(R2,GPIO.HIGH)

GPIO.output(R4,GPIO.HIGH)

GPIO.output(R6,GPIO.HIGH)


sleep(5) #play chord

print "Release CHORD 1"

GPIO.output(L1,GPIO.LOW)

GPIO.output(L3,GPIO.LOW)

GPIO.output(L5,GPIO.LOW)


GPIO.output(R2,GPIO.LOW)

GPIO.output(R4,GPIO.LOW)

GPIO.output(R6,GPIO.LOW)

sleep(0.2)

print "Move to position 1 from position 2"

GPIO.output(Motor1A,GPIO.LOW)

GPIO.output(Motor1B,GPIO.HIGH)

GPIO.output(Motor1E,GPIO.HIGH)



GPIO.output(Motor2A,GPIO.LOW)

GPIO.output(Motor2B,GPIO.HIGH)

GPIO.output(Motor2E,GPIO.HIGH)
sleep(1)

#Then stop motors
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)
sleep(.5)

print "Playing CHORD 2"

GPIO.output(L1,GPIO.HIGH)

GPIO.output(L3,GPIO.HIGH)

GPIO.output(L5,GPIO.HIGH)


GPIO.output(R2,GPIO.HIGH)

GPIO.output(R4,GPIO.HIGH)

GPIO.output(R6,GPIO.HIGH)

sleep(5) # play chord

print "Release CHORD 2"

GPIO.output(L1,GPIO.LOW)

GPIO.output(L3,GPIO.LOW)

GPIO.output(L5,GPIO.LOW)


GPIO.output(R2,GPIO.LOW)

GPIO.output(R4,GPIO.LOW)

GPIO.output(R6,GPIO.LOW)

sleep(0.5)


print "Move to position 0 from position 1"

GPIO.output(Motor1E,GPIO.HIGH)

GPIO.output(Motor2E,GPIO.HIGH)

sleep(1)

#Then stop motors
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)
sleep(.5)

print "Play Chord 3"

GPIO.output(L1,GPIO.HIGH)

GPIO.output(L3,GPIO.HIGH)

GPIO.output(L5,GPIO.HIGH)


GPIO.output(R2,GPIO.HIGH)

GPIO.output(R4,GPIO.HIGH)

GPIO.output(R6,GPIO.HIGH)


sleep(5) #play chord

print "Release Chord 3"

GPIO.output(L1,GPIO.LOW)

GPIO.output(L3,GPIO.LOW)

GPIO.output(L5,GPIO.LOW)


GPIO.output(R2,GPIO.LOW)

GPIO.output(R4,GPIO.LOW)

GPIO.output(R6,GPIO.LOW)

sleep(0.2)


print "MOTOR STOP CHECK BEFORE CLEAR"


GPIO.output(Motor1E, GPIO.LOW)

GPIO.output(Motor2E, GPIO.LOW)

sleep(0.2)

print "Stopping program now"

sleep(2)

GPIO.cleanup()
