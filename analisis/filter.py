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
      self.datalen = 0
          
      self.alpha=100
      # "ma" por moving average
      self.ma=50
      self.ma2=self.ma
      self.maLP=0  # promedio de los deltas de larguisimo plazo para detectar cambios muy grandes en el sensor (desconexiones, reinicios, etc)
      self.ema = self.ma
      self.vari=self.ma #varianza inicial de 30% para evitar falsos detects
      # para acumular valores de ma para mas tarde
      self.mas, vars, mas2, detects, arcDetects, diferencias, arcos = [], [], [], [], [], [], []
      self.flag=0   # si ya estamos "dentro" de un evento detectado o fuera
      # cantidad de eventos
      self.count = 0
      self.arcCount = 0 
      self.arcArea = 0
      self.arcLen = 0
      self.lastPeak = 0
      self.bicis = 0
      self.validArc = False
      prev_len=4
      self.prevDetects=[ 0 for i in range(prev_len)]

  def Procesar(self,e):
    """Toma un float que es una medición de presión del sensor y devuelve 0 si no detectó nada, o el mismo valor si detectó una bici
    (por ahora detecta cada pico o rueda, ojo con eso)
    """
    

    self.ma2 = (2*self.ma2  +e) / 3 
    delta = self.ma2-self.ma
    
    if (delta < 5*self.vari ):
        self.vari = (100*self.vari + abs(delta))/(100+1)
  

    
    if (delta < 5*self.vari ):
        self.ma = (self.ma * self.alpha +e) / (self.alpha+1)

   # si el promedio de largo plazo es muy distinto al ma actual, hacer un salto 
    self.maLP= (5000*self.maLP + delta) / 5001
    if ( abs(self.maLP) > 10 ):
      self.maLP = 0
      self.ma = self.ma + self.maLP 
      self.vari = 50

 
     
    detect = None  
    if (delta < 5.0 * self.vari):       
        self.flag = 0
    else:
        if (self.flag == 0 ):
            self.flag = 1
            self.count += 1
            # voy llenando los ultimos prev_len picos detectados para ver a que distancia estaban
# revisar esto, creo que no está bien
            if any([ (self.datalen - e) < 25 for e in self.prevDetects ]) :
               self.bicis += 1
               detect = e 
            self.prevDetects[self.count % 4] = self.datalen

            ## Esta parte pasarla a un contador o algo así, no basarse en len de un array que ya no existe
            # if len(detects)-lastPeak< 250:
            #     bicis += 1
            # lastPeak = len(detects)
            
    
    self.datalen += 1

    return detect
 
     