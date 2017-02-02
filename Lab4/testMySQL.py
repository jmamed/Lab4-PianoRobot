# System and GPIO imports
import RPi.GPIO as GPIO
import time
from time import sleep

# MySQL import
#-----------------------------------------------------------------------------------------------------------------------$
import pymysql
userID = "1"
eventName = "Event "
eventDate = time.strftime("%m-%d-%Y")
eventTime = time.strftime("%H:%M:%S")
event_info = (userID, eventName, eventDate, eventTime)
connection = pymysql.connect(user='root', passwd='wooker94', host='104.197.175.47', database='piano_robot')

cur = connection.cursor()


#---------------------------------------------------------------------------------------------------------------------$
GPIO.cleanup()
