#!/usr/bin/python

import pymysql
import time


# Declare parameters to temporarily store data to insert into MySQL database
name = "Hello"

# Put all declared variables into one variable
send_data = name

# Enter your MySQL connection information
connection = pymysql.connect(user='root', passwd='wooker94', host='104.197.175.47', database='piano_robot')

# Place a cursor to parse through the MySQL database
cur = connection.cursor()

# Use cursor to execute MySQL Queries such as SELECT, INSERT, DELETE, UPDATE
# Here we use the cursor to execute a query to INSERT data into the MySQL database

# Key things to note: 'test' is the name of the table inside the piano_robot database
#                     VALUES(%s) is saying "Insert data that is in STRING format"
#                     'send_data' contains the name "Hello" from above
cur.execute("INSERT INTO test(name) VALUES (%s)",  send_data)

# Commit the changes to the database
connection.commit()

# close the connection
connection.close()

#cur.execute("""SELECT * FROM events WHERE userID= %s """, (userID))
#for i in range(0, int(cur.rowcount)):
#    row = cur.fetchone()
#    print row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4]
