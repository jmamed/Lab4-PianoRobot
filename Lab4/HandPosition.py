import RPi.GPIO as GPIO

from time import sleep


GPIO.setmode(GPIO.BOARD)



Motor1A = 16

Motor1B = 18

Motor1E = 22



Motor2A = 19

Motor2B = 21

Motor2E = 23


GPIO.setup(Motor1A,GPIO.OUT)

GPIO.setup(Motor1B,GPIO.OUT)

GPIO.setup(Motor1E,GPIO.OUT)



GPIO.setup(Motor2A,GPIO.OUT)

GPIO.setup(Motor2B,GPIO.OUT)

GPIO.setup(Motor2E,GPIO.OUT)



print "Going Forwards"



GPIO.output(Motor1A,GPIO.HIGH)

GPIO.output(Motor1B,GPIO.LOW)

GPIO.output(Motor1E,GPIO.HIGH)



GPIO.output(Motor2A,GPIO.HIGH)

GPIO.output(Motor2B,GPIO.LOW)

GPIO.output(Motor2E,GPIO.HIGH)



sleep(2)



print "Going backwards"


GPIO.output(Motor1A,GPIO.LOW)

GPIO.output(Motor1B,GPIO.HIGH)

GPIO.output(Motor1E,GPIO.HIGH)



GPIO.output(Motor2A,GPIO.LOW)

GPIO.output(Motor2B,GPIO.HIGH)

GPIO.output(Motor2E,GPIO.HIGH)



sleep(2)



print "Now Stop"



GPIO.output(Motor1E, GPIO.LOW)

GPIO.output(Motor2E, GPIO.LOW)



GPIO.cleanup()