#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Filter:
    """Filtro al que se le pasan valores del sensor de presión y detecta cambios importantes (bicis)

    Va aculumando varios valores:

    self.ma Promedio movil de presión
    self.vari Varianza promedio 
    self.count Cantidad de detecciones de presión acumuladas
    self.bicis Cantidad de bicis

    Pasarle datos usando el método Procesar(e)

    """

    def __init__(self):
      
        # contador para saber cuantas lineas se procesaron hasta ahora
        self.umbral= 5  # por cuantas veces debe superar la medicion a la desviacion actual para tomar como detectada
        self.datalen = 0
            
        self.alpha=0.9
        # "ma" por moving average
        self.ma=50
        self.ma2=self.ma
        self.maLP=0  # promedio de los deltas de larguisimo plazo para detectar cambios muy grandes en el sensor (desconexiones, reinicios, etc)
        self.ema = self.ma
        self.vari=0.01 
        self.flag=0   # si ya estamos "dentro" de un evento detectado o fuera
        # cantidad de eventos
        self.count = 0
        self.bicis = 0
        self.bicis1 = 0
        self.bicis2 = 0
        self.bicis3 = 0
        self.bicis4 = 0
        self.bicis5 = 0
        prev_len=4
        self.prevDetects=[ 0 for i in range(prev_len)]
        self.prevDetect = 0 

    def Procesar(self,e, t):
        """Toma un float que es una medición de presión del sensor y devuelve 0 si no detectó nada, o el mismo valor si detectó una bici
        (por ahora detecta cada pico o rueda, ojo con eso)
        """
        
        t1=0.65 #corto plazo
        t2=0.995 #largo plazo

        self.ma2 = (t1*self.ma2  +(1-t1)*e)  
        # delta = self.ma2-self.ma
        
        #if (delta < 10*self.vari ):
        self.vari = t2*self.vari + (1-t2)*e
      

        
        #if (delta < 15*self.vari ):
        self.ma = t2*self.ma + (1-t2) *e 

       # si el promedio de largo plazo es muy distinto al ma actual, hacer un salto 
        # self.maLP= float(30*self.maLP + delta) / 31
        # if ( abs(self.maLP) > 2  ):
        #   self.ma =  e 
        #   self.maLP = 0
        #   self.vari = 5 # es arbitrario, para que se ajuste solo en un par de iteraciones

        detect = None  
        biciPosta = None  
        bici = None
        delta = (self.ma2 - self.vari)/self.vari 
        if (delta > 0.15): 
            if (self.flag == 0 ):
                self.flag = 1
                self.count += 1
                detect = True
                # voy llenando los ultimos prev_len picos detectados para ver a que distancia estaban
                # si e esta a menos de N=80 mediciones que alguno de los ultimos picos, es una bici
                # basado en que tenemos entre 50 y 80 muestras por segundo
                if any([ (self.datalen - e) < 80 for e in self.prevDetects ]) :
                    self.bicis += 1
                    biciPosta = True
                self.prevDetects[self.count % 4] = self.datalen
                if (t - self.prevDetect > 800):
                    self.prevDetect = t
                    self.bicis1 += 1
                    bici = True
        else:
            if (delta < 0.1):       
                self.flag = 0
        
        self.datalen += 1

        return detect, biciPosta, bici

     
