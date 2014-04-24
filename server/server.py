#!/usr/bin/env python
#encoding:utf-8

import sqlite3
#import ipdb
from datetime import datetime,timedelta
from flask import Flask, render_template, request, g
import json

app = Flask(__name__)
app.debug=True
DATABASE = '../analisis/base.db'
lastPing = (None, None) 
restartear = False

@app.errorhandler(404)
def page_not_found(error):
    return 'Esta no es la página que estas buscando', 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/totem", methods=['POST', 'GET'])
def totem():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now','localtime'));").fetchall()[0][0]
    anio = 13 + cur.execute("select count(*) from bicis where strftime('%Y',millis)=strftime('%Y', date('now','localtime'));").fetchall()[0][0]/7500
    global lastPing
    lastPing = (request.remote_addr, datetime.now())
    global restartear
    if int(datetime.now().strftime("%H%M%S")) < 1:
        restartear = True
    if restartear == False:
        return "#####" + " " * (5-len(str(dia))) + str(dia) + "0" * (2-len(str(anio))) + str(anio)
    else:
        restartear = False
        return "####R" + " " * (5-len(str(dia))) + str(dia) + "0" * (2-len(str(anio))) + str(anio)
    cur.close() 
    db.close()

@app.route("/dia", methods=['POST', 'GET'])
def dia():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    dia = cur.execute("select count(*) from bicis where strftime('%Y%m%d',millis)=strftime('%Y%m%d', date('now','localtime'));").fetchall()[0][0]
    return str(dia)
    cur.close() 
    db.close()

@app.route("/sensor", methods=['POST', 'GET'])
def sensor():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    presion = cur.execute("select * from presion order by rowid desc limit 1").fetchall()[0]
    estado = "ERROR desconocido en el status del sensor"
    try:
        estado =  (datetime.now() - datetime.strptime(presion[0], "%Y-%m-%d %H:%M:%S")).total_seconds() < 5000 and "OK" or "ERROR: no se estan recibiendo datos desde el sensor" 
    except:
        pass
    return json.dumps( [ estado, presion] )
    cur.close() 
    db.close()


@app.route("/restartotem", methods=['POST', 'GET'])
def restartotem():
    global restartear
    restartear = True
    return str("Restaring in 5...")

@app.route("/semana", methods=['POST', 'GET'])
def semana():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    semana = cur.execute("select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);").fetchall()
    return json.dumps(semana)
    cur.close() 
    db.close()

@app.route("/dashboard.json", methods=['POST', 'GET'])
def dashboard_data():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()


    #promedio x dia de la semana mes actual:
    queries={}
    # queries['semana'] = "select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);"
    queries= {
        'diasemana_actual' : {
            'name':"Bicis por día esta semana",
            'q':"""select dow, avg(avg_ct) from (select strftime("%w",millis) dow , count(*) avg_ct from bicis where strftime("%Y-%m",millis) = strftime("%Y-%m",date('now'))  group by strftime("%Y-%m-%d",millis)) group by dow"""
        },
        'prom_diario_mensual' : {
             'name' : "Bicis por día promedio", 
             'q':"""select mes, avg(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis where date(millis) > "2012" group by strftime("%Y-%m-%d",millis)) group by mes;"""
        },

        'prom_porhora_hoy': {
            'name':'Bicis por hora del día, hoy',
            'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where strftime("%Y-%m-%d",millis) = strftime("%Y-%m-%d", date('now','localtime')) group by strftime("%Y-%m-%d-%H",millis)) group by hora;"""
        },

        'prom_porhora_anioactual': {
            'name':'Promedio por hora del día, año actual',
            'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where strftime("%Y",millis) = strftime("%Y", date('now')) group by strftime("%Y-%m-%d-%H",millis)) group by hora;"""
        },


        'totales_mensual': {
            'name':"Bicis por mes",
            'q': """select mes, sum(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis where strftime("%Y",millis) >= "2013" group by strftime("%Y-%m-%d",millis)) group by mes;"""
        },

        'prom_porhora_historico': {
            'name':"promedio por hora, historico",
            'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where strftime("%Y",millis) >= "2013" group by strftime("%Y-%m-%d-%H",millis)) group by hora;"""
        }
    }

    data = [ (k, v['name'], cur.execute(v['q']).fetchall() ) for (k,v) in queries.iteritems()]
    return json.dumps(data)
    cur.close() 
    db.close()



@app.route("/lastping", methods=['POST', 'GET'])
def lastping():
    return "%s : %s" % lastPing

@app.route("/totemstatus", methods=['GET'])
def totemstatus():
    try:
        if ((datetime.now() - lastPing[1]) < timedelta(seconds=30)):
            return 'Totem OK', 200 
    except:
        pass
    return 'Totem fuera de servicio. Hace mas de 30 segundos que no se conecta. Contactar a DGGOBE', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)

#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
