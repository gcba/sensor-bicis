#!/bin/bash
mawk -W interactive '{if (NF==3){print $1,"\t",$2; fflush()}}' | ./procesar.py | feedgnuplot --stream  0 --lines --domain --dataid --autolegend --timefmt '%m-%d %H:%M:%S' --ymin 15 --ymax 70
#--extracmds "unset logscale; set logscale y" 

set timefmt '
#set term png color
#set output '/tmp/plot1.png'
plot \
'detecciones.dat' using 1:2 title 'Data 1' with linespoints

