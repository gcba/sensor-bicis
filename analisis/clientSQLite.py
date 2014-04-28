#!/usr/bin/env python

import zmq
from datetime import datetime
#import ipdb
import sqlite3

DATABASE = 'base.db'
db = sqlite3.connect(DATABASE)
cur = db.cursor()
if True:#try:
#    cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
#    db.commit()
#except Exception:
    maxID = 1 + cur.execute("select max(id) from bicis").fetchall()[0][0] 

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000")
#socket.connect("tcp://10.10.10.202:5000")
socket.setsockopt(zmq.SUBSCRIBE, "ecobici1 bici")
while True:
    d = socket.recv().split()
    print  ' '.join(d[2:])
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    maxID += 1
    cur.execute("insert into bicis values( %s , '%s' ,  '%s', %s)" % (maxID, ahora, ' '.join(d[2:]), 1))
    db.commit()
