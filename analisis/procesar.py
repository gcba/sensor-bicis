#!/usr/bin/env python
"""
Procesar floats que entran por stdin con el Filter de bicicletas y sacar un output compatible con el comando :

feedgnuplot --stream  1 --lines --dataid --autolegend -xlen 5000  

"""
from filter import Filter

if __name__ == "__main__":

  import sys
  import csv
  from math import log
  
  f=Filter()
  for e in sys.stdin :
      try:
        e = float(e)
      except:
        continue
      
      detect=f.Procesar(e)
      

      if ( (f.datalen % 400) == 0):
        print "replot" 
      print "0\t%s" % e
      print "1\t%s" % f.ma
      if detect:
         print "2 %s" % e
         sys.stderr.write("picos: %s\t" % f.count)
         sys.stderr.writelines("bicis: %s\n" % f.bicis)
         #sys.stderr.writelines("prev: %s\n" % f.prevDetects)
      print "3 %s" % (f.vari + f.ma)

 
