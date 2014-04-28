#!/usr/bin/env python

import zmq
from datetime import datetime
#import ipdb
import sqlite3

DATABASE = 'base.db'
db = sqlite3.connect(DATABASE)
cur = db.cursor()

try:
    cur.execute("CREATE TABLE presion(dateTime INT, presion INT)")
    db.commit()
except Exception:
    pass

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000")
#socket.connect("tcp://10.10.10.202:5000")
socket.setsockopt(zmq.SUBSCRIBE, "ecobici1 presion")
while True:
    d = socket.recv().split()
    print  ' '.join(d[2:])
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("insert into presion values( '%s' , %s)" % ( ahora, ' '.join(d[2:]) ))
    db.commit()
