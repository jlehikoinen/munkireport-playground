#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import MySQLdb

# Environment variables
host_ip = os.environ["MYSQL_PORT_3306_TCP_ADDR"]
db_user = os.environ["MYSQL_ENV_MYSQL_USER"]
db_passwd = os.environ["MYSQL_ENV_MYSQL_PASSWORD"]
db_name = os.environ["MYSQL_ENV_MYSQL_DATABASE"]

# Open database connection
db = MySQLdb.connect(host_ip, db_user, db_passwd, db_name)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data

# disconnect from server
db.close()
