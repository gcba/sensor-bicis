#!/usr/bin/env python

import sqlite3
#import ipdb
from datetime import datetime
from flask import Flask, render_template, request, g


app = Flask(__name__)
DATABASE = '../analisis/base.db'



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/totem", methods=['POST', 'GET'])
def totem():
	db = sqlite3.connect(DATABASE)
	cur = db.cursor()
	dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
	anio = cur.execute("select count(*) from bicis where strftime('%Y',millis)=strftime('%Y', date('now'));").fetchall()[0][0]/7500
	return "#####" + " " * (5-len(str(dia))) + str(dia) + "0" * (2-len(str(anio))) + str(anio)
	cur.close() 
	db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)

#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
