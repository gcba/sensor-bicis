#!/bin/bash
mawk -W interactive '{if (NF==3){print $1; fflush()}}' | ./procesar.py | feedgnuplot --stream  0 --lines --dataid --autolegend -xlen 350000 --ymin 15 --ymax 70
#--extracmds "unset logscale; set logscale y" 


