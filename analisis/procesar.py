#!/usr/bin/env python
#encoding:latin-1
"""
Procesar floats que entran por stdin con el Filter de bicicletas y sacar un output compatible con el comando :

feedgnuplot --stream  1 --lines --dataid --autolegend -xlen 5000  

"""
from filter import Filter
import dateutil.parser
import argparse
from datetime import datetime,timedelta
import zmq
import sys
import select

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--inicio', help='Fecha de inicio de los datos')
    args=parser.parse_args()

    # inicializar zmq server
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://0.0.0.0:5000")
    # eventos que van a ir por broadcast   
    sensor = 'ecobici1'
    events = ['bici', "pico"]
     
    # fecha completamente arbitraria que es cuando se prendió el arduino por ultima vez (para convertir  millis() en una fecha)
    if vars(args)['inicio']:
        inicio = dateutil.parser.parse(args.inicio)
    else:
        inicio = datetime.now()

    f=Filter()
    f.umbral = 5 
    last_time = datetime.now()
    pressure_report_interval = timedelta(seconds=5)
    for e in sys.stdin :
        try:
            t = int(e.split()[1])
            e = float(e.split()[0])
            # solo segundos
            #strtime = (inicio+datetime.timedelta(milliseconds=int(t)) ).strftime('%m-%d %H:%M:%S') 
            # segundos con fraccion
            if vars(args)['inicio']:
                strtime = "%s" %  (inicio+timedelta(milliseconds=int(t)) )
            else:
                strtime = "%s" %  (datetime.now())

        except:
            continue
        detect, biciPosta, bici = f.Procesar(e, t)

        #if ( (f.datalen % 10) == 0):
        #    print "replot" 
        print "%s 0 %s" % (strtime, e )
        print "%s 1 %s" % (strtime,  f.vari   )
        print "%s 4 %s" % (strtime, f.ma2  )
        if detect:
            print "%s 2 %s" % (strtime, e )
            socket.send("ecobici1 pico %s %s" % (t, f.count) )
            if biciPosta:
                print "%s 3 %s" % (strtime, e )
                socket.send("ecobici1 iciPosta %s " % (t) )
            if bici:
                print "%s 8 %s" % (strtime, e )
                socket.send("ecobici1 bici %s " % (strtime) )
            sys.stderr.write("picos: %s\t" % f.count)
            sys.stderr.writelines("bicis: %s\n" % f.bicis)
            sys.stderr.writelines("bicis: %s\n" % f.bicis1)
            #sys.stderr.writelines("prev: %s\n" % f.prevDetects)
        
        now = datetime.now()
        if ( (now - last_time ) > pressure_report_interval) : 
            last_time = now
            socket.send("ecobici1 presion %s" % (e) )




