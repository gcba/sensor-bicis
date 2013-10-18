#!/usr/bin/env python
#encoding:latin-1
"""
Procesar floats que entran por stdin con el Filter de bicicletas y sacar un output compatible con el comando :

feedgnuplot --stream  1 --lines --dataid --autolegend -xlen 5000  

"""
from filter import Filter
import datetime
import zmq

if __name__ == "__main__":

# inicializar zmq server
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind("tcp://127.0.0.1:5000")
# eventos que van a ir por broadcast   
  sensor = 'ecobici1'
  events = ['bici', "pico"]
 
# fecha completamente arbitraria que es cuando se prendió el arduino por ultima vez (para convertir  millis() en una fecha)
  inicio = datetime.datetime(2013, 10, 11, 15, 33, 43, 898829)

  import sys
  import csv
  from math import log
  
  f=Filter()
  f.umbral = 15
  c=0
  for e in sys.stdin :
      try:
        t = e.split()[1]
        e = float(e.split()[0])
      except:
        continue
      strtime = ( inicio+datetime.timedelta(milliseconds=int(t)) ).strftime('%m-%d %H:%M:%S') 
      c=f.count
      detect=f.Procesar(e)

      if (f.count>c):
        socket.send("ecobici1 pico %s %s" % (t, f.count) )
        # imprimir x, curva-id, valor
        print "%s 2 %s" % (strtime,e)

      if ( (f.datalen % 10) == 0):
        print "replot" 
      print "%s 0 %s" % (strtime,e)
      print "%s 1 %s" % (strtime, f.umbral*f.vari + f.ma)
      print "%s 4 %s" % (strtime, f.maLP)
      if detect:
         socket.send("ecobici1 bici %s " % (t) )
         print "%s 3 %s" % (strtime,e)
         sys.stderr.write("picos: %s\t" % f.count)
         sys.stderr.writelines("bicis: %s\n" % f.bicis)
         #sys.stderr.writelines("prev: %s\n" % f.prevDetects)

      
   
