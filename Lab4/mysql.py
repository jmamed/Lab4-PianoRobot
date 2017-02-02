#!/usr/bin/python

import pymysql
import time

for i in range(5):
    userID = "1"
    eventName = "Event " + str(i)
    eventDate = time.strftime("%m-%d-%Y")
    eventTime = time.strftime("%H:%M:%S")

    if (i == 5):
        i = 1
        break
    else:
        print eventName
        i += 1
        pass

#event_info = (userID, eventName, eventDate, eventTime)

#connection = pymysql.connect(user='root', passwd='Sithlord3', host='130.211.203.234', database='keep_it_safe')

#cur = connection.cursor()

#cur.execute("INSERT INTO events(userID, eventName, eventDate, eventTime) VALUES (%s, %s, %s, %s)",  event_info)

#connection.commit()

#cur.execute("""SELECT * FROM events WHERE userID= %s """, (userID))
#for i in range(0, int(cur.rowcount)):
 #   row = cur.fetchone()
 #   print row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4]

#connection.close()
