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
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# disconnect from server
db.close()
