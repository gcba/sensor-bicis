#!/usr/bin/env python
"""
Procesar floats que entran por stdin con el Filter de bicicletas y sacar un output compatible con el comando :

feedgnuplot --stream  1 --lines --dataid --autolegend -xlen 5000  

"""
from filter import Filter
from datetime import datetime
import zmq

if __name__ == "__main__":

# inicializar zmq server
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind("tcp://127.0.0.1:5000")
# eventos que van a ir por broadcast   
  sensor = 'ecobici1'
  events = ['bici', "pico"]
 

  import sys
  import csv
  from math import log
  
  f=Filter()
  c=0
  for e in sys.stdin :
      try:
        t = e.split()[1]
        e = float(e.split()[0])
      except:
        continue
      c=f.count
      detect=f.Procesar(e)

      if (f.count>c):
        socket.send("ecobici1 pico %s %s" % (t, f.count) )
        print "2 %s" % e

      if ( (f.datalen % 10) == 0):
        print "replot" 
      print "0\t%s" % e
      print "1\t%s" % f.ma
      if detect:
         socket.send("ecobici1 bici %s " % (t) )
         print "2 %s" % e
         sys.stderr.write("picos: %s\t" % f.count)
         sys.stderr.writelines("bicis: %s\n" % f.bicis)
         #sys.stderr.writelines("prev: %s\n" % f.prevDetects)
      print "3 %s" % (f.vari + f.ma)

 
