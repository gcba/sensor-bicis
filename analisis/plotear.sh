#!/bin/bash
# recibe como entrada el feed de datos crudos, los procesa en varios archivos distintos y lo plotea con gnuplot

# escribe los renglones de la serie 0,1,2,3 y 4 en archivos con ese mismo nombre
./procesar.py | awk '$3 ~ /[0-9]/ {print > $3}'

#los plotea
gnuplot -p plot-series.gnu
