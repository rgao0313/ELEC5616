# Run via `python injection.py` -- compatible with Python 2 and Python 3
from __future__ import print_function
# If raw_input doesn't exist, we're in Python 3 (which uses `input`)
try:
    raw_input
except NameError:
    raw_input = input

import sqlite3
import sys

def database_setup():
    cur.execute("""CREATE TABLE Users(Id INT,
        username TEXT,
        password TEXT,
        status TEXT,
        admin INT
    )""")
    cur.execute("""INSERT INTO Users
        VALUES(1, 'Hulk', 'greengrocer', 'SMASHING THINGS', 0)""")
    cur.execute("""INSERT INTO Users
        VALUES(2, 'Bobby', 'lolcats', 'serving tables', 1)""")
    conn.commit()

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
database_setup()

username = raw_input(">>> Enter your username... ")
password = raw_input(">>> Enter your password... ")
# This code is vulnerable to SQL injection
# Specifically, type ' OR 1=1/* when prompted for the username
# cur.execute("""SELECT 1 FROM Users
#    WHERE username = '%s' AND password = '%s'""" % (username, password))
# This is the fix to prevent SQL injection during login.
cur.execute("""SELECT 1 FROM Users
    WHERE username = ? AND password = ?""",(username, password))
#cur.execute("""SELECT 1 FROM Users WHERE username = '%s' AND password = '%s'""" ,(username, password))
if cur.fetchone():
    print("You've successfully logged in as %s" % username)
else:
    print("Your username or password was incorrect")

print()
username = raw_input(">>> Find out the status for which user? ")
# This code is vulnerable to SQL injection
# Specifically, type ' UNION SELECT password FROM Users WHERE usernam='Bobby';/* when prompted for the user you want a status for
# cur.execute("SELECT status FROM Users WHERE username = '%s'" % username)
# This is the fix to prevent SQL injection
cur.execute("SELECT status FROM Users WHERE username = ?", (username,))

data = cur.fetchone()
if data:
    print("User %s is %s" % (username, data[0]))
else:
    print("No such user...")

conn.close()
