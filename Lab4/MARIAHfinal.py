#!/usr/bin/python

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
connection = pymysql.connect(user='root', passwd='Sithlord3', host='130.211.203.234', database='keep_it_safe')

cur = connection.cursor()
#---------------------------------------------------------------------------------------------------------------------------------

# LCD import
#---------------------------------------------------------------------------------------------------------------------------------
from lcd import *
#---------------------------------------------------------------------------------------------------------------------------------


# Lock Solenoid Setup
#---------------------------------------------------------------------------------------------------------------------------------
LOCK_Solenoid = 14

def unlockDoor():

  GPIO.setmode(GPIO.BCM)

  #Set Pin for Solenoid as OUTPUT
  GPIO.setup(LOCK_Solenoid, GPIO.OUT)

  #Unlock Position
  GPIO.output(LOCK_Solenoid, GPIO.HIGH)
  sleep(2)
  

def lockDoor():

  GPIO.setmode(GPIO.BCM)

  #Set Pin for Solenoid as OUTPUT
  GPIO.setup(LOCK_Solenoid, GPIO.OUT)

  #Lock Position
  GPIO.output(LOCK_Solenoid, GPIO.LOW)
  sleep(2)
#---------------------------------------------------------------------------------------------------------------------------------


# KEYPAD import
#---------------------------------------------------------------------------------------------------------------------------------
from matrix_keypad import RPi_GPIO
kp = RPi_GPIO.keypad(columnCount = 3)

def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r


# User Create Pin Function
#---------------------------------------------------------------------------------------------------------------------------------
def createPin():

    passcode = "0000"
    
    d1 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d1))

    d2 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d1)+str(d2))

    d3 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d1)+str(d2)+str(d3))

    d4 = digit()
    sleep(0.2)

    passcode = (str(d1)+str(d2)+str(d3)+str(d4))

    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(passcode)

    return passcode

# Check pins for match function
#---------------------------------------------------------------------------------------------------------------------------------
def checkPin():

    check = "0000"
    
    d5 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d5))

    d6 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d5)+str(d6))

    d7 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(d5)+str(d6)+str(d7))

    d8 = digit()
    sleep(0.2)

    check = (str(d5)+str(d6)+str(d7)+str(d8))

    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(check)

    return check
#---------------------------------------------------------------------------------------------------------------------------------

def pin_init():

    lcd_byte(LCD_LINE_1,LCD_CMD)
    lcd_string("Set a new pin: ")

    # Call createPin func
    new_pin = createPin()
    
    while(True):

      lcd_byte(LCD_LINE_2,LCD_CMD)
      lcd_string("")
      
      # Call checkPin func
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string("Enter again: ")
      check_pin = checkPin()
      
      if (check_pin == new_pin):
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string("Pin is set!")
        sleep(2)
        # Clear display
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string("")
        lcd_byte(LCD_LINE_2,LCD_CMD)
        lcd_string("")
        return new_pin
      else:
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string("Pin not match!")
        lcd_byte(LCD_LINE_2,LCD_CMD)
        lcd_string("")
        sleep(2)

#---------------------------------------------------------------------------------------------------------------------------------

def enter_Pin():

    dig1 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(dig1))

    dig2 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(dig1)+str(dig2))

    dig3 = digit()
    sleep(0.2)
    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(""+str(dig1)+str(dig2)+str(dig3))

    dig4 = digit()
    sleep(0.2)

    tmp_pin = (str(dig1)+str(dig2)+str(dig3)+str(dig4))

    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string(tmp_pin)

    lcd_byte(LCD_LINE_2,LCD_CMD)
    lcd_string("")

    return tmp_pin

try:
  # Initialize LCD
  lcd_init()

  attempt = 0
    
  # Display Hello to user
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Hello!")
  sleep(3)

  # initialize pin creation
  new_pin = pin_init()

  # Let user enter their new pin to unlock safe
  # Send some text
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Enter pin:")
    
  while(True):
    
    pin_entered = enter_Pin()
    
    # Check if the pin that was entered matches with the user's current pin
    if (pin_entered == new_pin):
      attempt = 0
      lcd_byte(LCD_LINE_1,LCD_CMD)
      
      lcd_string("Unlocking Safe")
      unlockDoor()
      
      cur.execute("INSERT INTO events(userID, eventName, eventDate, eventTime) VALUES (%s, %s, %s, %s)",  event_info)
      connection.commit()
      
      cur.execute("""SELECT * FROM events WHERE userID= %s """, (userID))
      for i in range(0, int(cur.rowcount)):
        row = cur.fetchone()
        print row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4]

      connection.close()
      sleep(3)
      lockDoor()
      
    else:
      attempt += 1
      lcd_byte(LCD_LINE_1,LCD_CMD)
      lcd_string("Try again!")
      
      if (attempt == 4):
        lcd_byte(LCD_LINE_1,LCD_CMD)
        lcd_string("Too many tries!")
        attempt = 0
        exit

        
#finally:
except KeyboardInterrupt:
    GPIO.cleanup()
