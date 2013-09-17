import json
import time
import ipdb
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, render_template, request, g


app = Flask(__name__)
DATABASE = 'base.db'
db = sqlite3.connect(DATABASE)
cur = db.cursor()

epoch = datetime(1970, 1, 1)
maxID = cur.execute("select max(id) from bicis").fetchall()[0][0] + 1
boardDebug = False
# ipdb.set_trace()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sensor", methods=['POST', 'GET'])
def sensor():
    global boardDebug
    if 'debug' in request.args.keys():
        if request.args['debug']=='true':
            boardDebug = True
        else:
            boardDebug = False
        return "Debuging: %s" % boardDebug
    else:
        if boardDebug:
            print request.data
            return "debug"
        else:
            print request.data
            dato = json.loads(request.data)
            ahora = datetime.now() - epoch
            cur.execute("insert into bicis values(" + maxID + "," + dato["tiempo"] + "," + ahora + "," + dato["pasadas"] + ");")
            maxID += 1
            return "clear"

@app.route("/totem", methods=['POST', 'GET'])
def totem():
    respuesta = str(cur.execute("select sum(pasadas) from bicis").fetchall()[0][0])
    return "#####" + "0" * (5-len(respuesta)) + respuesta

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)





#cur.execute("CREATE TABLE bicis(id INT, dateTime INT, millis INT, pasadas INT)")
