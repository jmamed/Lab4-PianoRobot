#cd /home/pi/Lab4

# System and GPIO imports
import RPi.GPIO as GPIO
import time
from time import sleep

# MySQL import
#---------------------------------------------------------------------------------------------------------------------------------
import pymysql
userID = "1"
eventName = "Event "
eventDate = time.strftime("%m-%d-%Y")
eventTime = time.strftime("%H:%M:%S")
event_info = (userID, eventName, eventDate, eventTime)
connection = pymysql.connect(user='root', passwd='wooker94', host='104.197.85.66', database='pianorobot')

cur = connection.cursor()
#---------------------------------------------------------------------------------------------------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


#L1->L8 is all left hand fingers
#R1->R8 is all right hand fingers

#Pins 16, 18, 22, 19, 21, 23 are unavailable

L1 =  11
L2 =  13
L3 =  15 
L4 =  3  #27 no go
L5 =  29
L6 =  31
L7 =  33
L8 =  35
L9 =  37

R1 =  12
R2 =  24
R3 =  26
R4 =  5 #28 no go
R5 =  32
R6 =  36
R7 =  38
R8 =  40
R9 =  7  #1 no go

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




print "All fingers down"


GPIO.output(L1,GPIO.HIGH)

GPIO.output(L2,GPIO.HIGH)

GPIO.output(L3,GPIO.HIGH)

GPIO.output(L4,GPIO.HIGH)

GPIO.output(L5,GPIO.HIGH)

GPIO.output(L6,GPIO.HIGH)


GPIO.output(L7,GPIO.HIGH)

GPIO.output(L8,GPIO.HIGH)

GPIO.output(L9,GPIO.HIGH)


GPIO.output(R1,GPIO.HIGH)

GPIO.output(R2,GPIO.HIGH)

GPIO.output(R3,GPIO.HIGH)

GPIO.output(R4,GPIO.HIGH)

GPIO.output(R5,GPIO.HIGH)

GPIO.output(R6,GPIO.HIGH)

GPIO.output(R7,GPIO.HIGH)

GPIO.output(R8,GPIO.HIGH)

GPIO.output(R9,GPIO.HIGH)



sleep(10)



print "Left hand backup"


GPIO.output(L1,GPIO.LOW)

GPIO.output(L2,GPIO.LOW)

GPIO.output(L3,GPIO.LOW)

GPIO.output(L4,GPIO.LOW)

GPIO.output(L5,GPIO.LOW)

GPIO.output(L6,GPIO.LOW)


GPIO.output(L7,GPIO.LOW)

GPIO.output(L8,GPIO.LOW)

GPIO.output(L9,GPIO.LOW)


sleep(10)



print "Left hand down, right hand backup"



GPIO.output(L1,GPIO.HIGH)

GPIO.output(L2,GPIO.HIGH)

GPIO.output(L3,GPIO.HIGH)

GPIO.output(L4,GPIO.HIGH)

GPIO.output(L5,GPIO.HIGH)

GPIO.output(L6,GPIO.HIGH)


GPIO.output(L7,GPIO.HIGH)

GPIO.output(L8,GPIO.HIGH)

GPIO.output(L9,GPIO.HIGH)


GPIO.output(R1,GPIO.LOW)

GPIO.output(R2,GPIO.LOW)

GPIO.output(R3,GPIO.LOW)

GPIO.output(R4,GPIO.LOW)

GPIO.output(R5,GPIO.LOW)

GPIO.output(R6,GPIO.LOW)

GPIO.output(R7,GPIO.LOW)

GPIO.output(R8,GPIO.LOW)

GPIO.output(R9,GPIO.LOW)

sleep(10)

print "Left hand backup"


GPIO.output(L1,GPIO.LOW)

GPIO.output(L2,GPIO.LOW)

GPIO.output(L3,GPIO.LOW)

GPIO.output(L4,GPIO.LOW)

GPIO.output(L5,GPIO.LOW)

GPIO.output(L6,GPIO.LOW)


GPIO.output(L7,GPIO.LOW)

GPIO.output(L8,GPIO.LOW)

GPIO.output(L9,GPIO.LOW)

sleep(2)


#------------------------------------------------------------------------------        
#finally:
#except KeyboardInterrupt:
GPIO.cleanup()
