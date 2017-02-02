import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BOARD)

coil_A_1_pin = 10 #10, 7
coil_A_2_pin = 16 #16, 8
coil_B_1_pin = 18 #18, 19
coil_B_2_pin = 23 #23, 21

R1 = 12
L5 = 31
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(L5, GPIO.OUT)

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

forward_seq = ['1010', '0110', '0101', '1001']
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
  GPIO.output(coil_A_1_pin, step[0] == '1')
  GPIO.output(coil_A_2_pin, step[1] == '1')
  GPIO.output(coil_B_1_pin, step[2] == '1')
  GPIO.output(coil_B_2_pin, step[3] == '1')

while True:
  	set_step('0000')
	print "forward"
	backwards(int(2)/1000.0, int(60))
	GPIO.output(R1, GPIO.HIGH)
	#GPIO.output(L5, GPIO.HIGH)
	print "sleep"
	sleep(5)	
	set_step('0000')
	print "backward"
	GPIO.output(L5, GPIO.LOW)
	GPIO.output(R1, GPIO.LOW)
	sleep(0.5)
	forward(int(2)/1000.0, int(60))#delay 100ms, 20 steps
	print "sleep"	
	sleep(2)
