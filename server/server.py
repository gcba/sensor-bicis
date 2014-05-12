#!/usr/bin/env python
#encoding:utf-8

import sqlite3
#import ipdb
from datetime import date,datetime,timedelta
from flask import Flask, render_template, request, g
import json

app = Flask(__name__)
app.debug=True
DATABASE = '../base.db'
lastPing = (None, None) 
#ultima vez que consultamos el total de bicis de anio (ayer):
lastAnio = datetime.combine(date.today() - timedelta(1), datetime.min.time())
bicisAnio = 0 
restartear = False

@app.errorhandler(404)
def page_not_found(error):
    return 'Esta no es la página que estas buscando', 404

@app.route("/")
def index():
    #return render_template('index.html')
    return " "

@app.route("/totem", methods=['POST', 'GET'])
def totem():
    sdia = dia() 
    sanio = str(13 + int(anio()) / 7500)
    print "queries listos"
    global lastPing
    lastPing = (request.remote_addr, datetime.now())
    global restartear
    if int(datetime.now().strftime("%H%M%S")) < 1:
        restartear = True

    restByte = "#"
    if restartear :
        restByte = "R"
        restartear = False
            
    print "fin"
    return  "####"+ restByte + " " * (5-len(sdia)) + sdia + "0" * (2-len(sanio)) + str(sanio)

def bicisentre(desde,hasta):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    q = "select count(*) from bicis where millis > '{desde}' and millis < '{hasta}' ;".format(desde=desde,hasta=hasta)
    total = cur.execute(q).fetchall()[0][0]
    cur.close() 
    db.close()
    return str(total)
   

@app.route("/anio", methods=['POST', 'GET'])
def anio():
    # implementamos una especie de cache porque el query es pesado
    global lastAnio, bicisAnio
    ahora = datetime.now()
    if ( ahora - lastAnio ).total_seconds() > 60*60*12 :
        lastAnio = ahora
        este = date(date.today().year,1,1).strftime('%Y-%m-%d')
        proximo = date(date.today().year + 1 ,1,1).strftime('%Y-%m-%d')
        bicisAnio = bicisentre(este,proximo) 
    return bicisAnio

@app.route("/dia", methods=['POST', 'GET'])
def dia():
    hoy = date.today().strftime("%Y-%m-%d")
    maniana = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    return bicisentre(hoy,maniana) 

@app.route("/sensor", methods=['POST', 'GET'])
def sensor():
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    presion = cur.execute("select * from presion order by rowid desc limit 1").fetchall()[0]
    estado = "ERROR desconocido en el status del sensor"
    try:
        estado =  (datetime.now() - datetime.strptime(presion[0], "%Y-%m-%d %H:%M:%S")) < timedelta(minutes=5) and "OK" or "ERROR: no se estan recibiendo datos desde el sensor" 
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

    hoy = date.today().strftime("%Y-%m-%d")
    maniana = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    #promedio x dia de la semana mes actual:
    queries={}
    # queries['semana'] = "select count(*), strftime('%Y-%m-%d',millis) from bicis group by strftime('%Y%m%d', millis);"
    queries= {
        '1prom_porhora_hoy': {
            'name':'Bicis por hora hoy',
            'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where millis > "{desde}" and millis < "{hasta}"  group by strftime("%Y-%m-%d-%H",millis)) group by hora;""".format(desde=hoy, hasta=maniana)
        },

        # '2diasemana_actual' : {
        #     'name':"Ultimos 7 dias",
        #     'q':"""select case cast (strftime('%w', millis) as integer)  when 0 then 'dom' when 1 then 'lu' when 2 then 'mar' when 3 then 'mi' when 4 then 'jue' when 5 then 'vi' when 6 then 'sa' else '???' end as  dow , count(*)  from bicis where (julianday("now") - julianday(millis)) < 10  group by dow order by millis"""
        # },
        # '3prom_diario_mensual' : {
        #      'name' : "Cantidad de bicis por día en los ultimos meses", 
        #      'q':"""select mes, avg(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis where date(millis) > "2012" group by strftime("%Y-%m-%d",millis)) group by mes;"""
        # },


        # '4prom_porhora_anioactual': {
        #     'name':'Promedio por hora del día',
        #     'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where strftime("%Y",millis) = strftime("%Y", date('now')) group by strftime("%Y-%m-%d-%H",millis)) group by hora;"""
        # },


        # '5totales_mensual': {
        #     'name':"Bicis por mes",
        #     'q': """select mes, sum(avg_ct) from (select strftime("%Y-%m",millis) mes , count(*) avg_ct from bicis where strftime("%Y",millis) >= "2013" group by strftime("%Y-%m-%d",millis)) group by mes;"""
        # },

        # 'prom_porhora_historico': {
        #     'name':"promedio por hora, historico",
        #     'q': """select hora, avg(avg_ct) from (select strftime("%H",millis) hora , count(*) avg_ct from bicis where strftime("%Y",millis) >= "2013" group by strftime("%Y-%m-%d-%H",millis)) group by hora;"""
        # }
    }

    data = [ (k, v['name'], cur.execute(v['q']).fetchall() ) for (k,v) in sorted(queries.iteritems())]
    cur.close() 
    db.close()
    return json.dumps(data)



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
    app.run(host="0.0.0.0", port=8080, threaded=False, use_reloader=False)

#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
