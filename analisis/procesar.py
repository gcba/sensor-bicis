#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import sys

import csv

i = 0
    
# "ma" por moving average
alpha=100
ma=50
ma2=ma
ema = ma
vari=ma*0.3 #varianza inicial de 30% para evitar falsos detects
# para acumular valores de ma para mas tarde
mas, vars, mas2, detects, arcDetects, diferencias, arcos = [], [], [], [], [], [], []
flag=0   # si ya estamos "dentro" de un evento detectado o fuera
# cantidad de eventos
count = 0
arcCount = 0 
arcArea = 0
umb=1.23
arcLen = 0
lastPeak = 0
bicis = 0
validArc = False
while True:
    e = float(sys.stdin.readline())
    
    ma2 = (2*ma2  +e) / 3 
    delta = ma2-ma
    
    if (delta < 5*vari ):
        vari = (100*vari + abs(delta))/(100+1)
  

    
    if (delta < 5*vari ):
        ma = (ma * alpha +e) / (alpha+1)
    
     
    detect = None  
    if (delta < 5.0 * vari):       
        flag = 0
    else:
        if (flag == 0 ):
            count += 1
            detect = e 
            flag = 1

            ## Esta parte pasarla a un contador o algo así, no basarse en len de un array que ya no existe
            # if len(detects)-lastPeak< 250:
            #     bicis += 1
            # lastPeak = len(detects)
            
    
    if ((e - ma) > 1):
        arcLen += 1
        arcArea += (e-ma) 
    else:
        arcLen = 0
        if (arcArea != 0) and validArc:
            #arcos.append(arcArea)
            arcArea = 0
            validArc = False
        elif not validArc:
            arcArea = 0
    if arcLen > 30:
        validArc=True
        arcCount += 1
        arcLen = 0
        #arcDetects.append(e)
    else:
        #arcDetects.append(None)
        pass
    i += 1
    if not (i % 100):
      print "replot"
    #diferencias.append((e/ma)*10 + 10)
    print "0\t%s" % e
    print "1\t%s" % ma
    if detect:
       print "2 %s" % e
    print "3 %s" % (vari + ma) 
    


    mas.append(ma)
    vars.append(vari) # dejo la varianza anterior si es un punto extremo
    mas2.append(ma2)
    

