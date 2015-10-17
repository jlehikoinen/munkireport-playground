#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import MySQLdb

# Docker machine IP
host_ip = os.environ["HOST_IP"]

# Open database connection
db = MySQLdb.connect(host_ip,"admin","admin","munkireport" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
numrows = cursor.execute("SELECT * FROM machine")

print "Selected %s rows" % cursor.rowcount

query = cursor.execute("SELECT serial_number FROM machine")
data = cursor.fetchall ()
# print data

for row in data:
    print row[0]

# disconnect from server
db.close()
