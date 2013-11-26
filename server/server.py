#!/usr/bin/env python

import json
import time
import ipdb
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template, request, g


app = Flask(__name__)
DATABASE = '../analisis/base.db'
db = sqlite3.connect(DATABASE)
cur = db.cursor()


@app.route("/")
def index():
    return render_template('index.html')

#boardDebug = False
#@app.route("/sensor", methods=['POST', 'GET'])
#def sensor():
#    global boardDebug
#    if 'debug' in request.args.keys():
#        if request.args['debug']=='true':
#            boardDebug = True
#        else:
#            boardDebug = False
#        return "Debuging: %s" % boardDebug
#    else:
#        if boardDebug:
#            print request.data
#            return "debug"
#        else:
#            print request.data
#            dato = json.loads(request.data)
#            ahora = datetime.utcnow().strftime("%s") 
#            maxID = 1 + cur.execute("select max(id) from bicis").fetchall()[0][0] 
#            cur.execute("insert into bicis values( %s , %s ,  %s, %s)" % (maxID,dato["tiempo"],  ahora , dato["pasadas"] ) )
#            db.commit()
#            return "clear"

@app.route("/totem", methods=['POST', 'GET'])
def totem():
    dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
    anio = cur.execute("select count(*) from bicis where strftime('%Y',millis)=strftime('%Y', date('now'));").fetchall()[0][0]/7500
    if (dia > 0):
        return "#####" + "0" * (5-len(dia)) + dia
    else:
        dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
        return "#####" + "0" * (5-len(dia)) + dia


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
