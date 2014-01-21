#!/usr/bin/env python
#encoding:utf-8

import sqlite3
#import ipdb
from datetime import datetime
from flask import Flask, render_template, request, g, jsonify

app = Flask(__name__)
app.debug=True
DATABASE = '../analisis/base.db'
lastPing = ""


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/totem", methods=['POST', 'GET'])
def totem():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
    anio = cur.execute("select count(*) from bicis where strftime('%Y',millis)=strftime('%Y', date('now'));").fetchall()[0][0]/7500
    global lastPing
    lastPing = "%s: %s" % (request.remote_addr, datetime.now())
    return "#####" + " " * (5-len(str(dia))) + str(dia) + "0" * (2-len(str(anio))) + str(anio)
    cur.close() 
    db.close()

@app.route("/dia", methods=['POST', 'GET'])
def dia():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now'));").fetchall()[0][0]
    return str(dia)
    cur.close() 
    db.close()

@app.route("/semana", methods=['POST', 'GET'])
def semana():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    semana = cur.execute("select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);").fetchall()
    return jsonify(semana)
    cur.close() 
    db.close()

@app.route("/dashboard.json", methods=['POST', 'GET'])
def dashboard_data():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()


    #promedio x dia de la semana mes actual:
    queries={}
    queries['semana'] = "select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);"
    queries['diasemana_actual'] = """select dow, avg(avg_ct) from (select strftime("%w",millis) dow , count(*) avg_ct from bicis where strftime("%Y-%m",millis) = strftime("%Y-%m",date('now'))  group by strftime("%Y-%m-%d",millis)) group by dow"""

    #hoy
    queries['prom_diasemana_actual'] = """select count(*) from bicis where date(millis) = date('now');"""

# promedio diario mensual
    queries['prom_diario_mensual'] = """select mes, avg(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis  group by strftime("%Y-%m-%d",millis)) group by mes;"""

    #Totales mensuales
    queries['totales_mensual'] = """select mes, sum(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis where strftime("%Y",millis) >= "2013" group by strftime("%Y-%m-%d",millis)) group by mes;"""

# Promedio por hora del día, año actual
    queries['prom_porhora_anioactual'] = """select strftime("%H",millis) hour , count(*) avg_ct from bicis where strftime("%Y",millis) = strftime("%Y",date('now'))  group by strftime("%H",millis);"""

    # promedio por hora, historico
    queries['prom_porhora_historico'] = """select strftime("%H",millis) hour , count(*) avg_ct from bicis where strftime("%Y",millis) > "2012"  group by strftime("%H",millis);"""

    data = [ (k, cur.execute(v).fetchall() ) for (k,v) in queries.iteritems()]
    return jsonify(data)
    cur.close() 
    db.close()



@app.route("/lastping", methods=['POST', 'GET'])
def lastping():
    return lastPing

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)

#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
