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
# numrows = cursor.execute("SELECT * FROM machine")
numrows = cursor.execute("SELECT machine_model FROM machine")

# print "Selected %s rows" % numrows
print "Selected %s rows" % cursor.rowcount

# Date testing
# numrows2 = cursor.execute("SELECT * FROM reportdata")
# numrows2 = cursor.execute("SELECT FROM_UNIXTIME(timestamp, '%Y.%d.%m %h:%i:%s') from reportdata")
numrows2 = cursor.execute("SELECT * FROM reportdata WHERE timestamp >= NOW() - INTERVAL 5 MONTH")
print numrows2

# data = cursor.fetchall ()
# print data

# disconnect from server
db.close()
