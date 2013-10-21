set title 'Bicicletas Detectadas'
set xdata time
set key box
set key bottom right
set size 1.5,1.5
set xlabel 'Tiempo'
set xtics auto 
set format x "%H:%M:%.3S"
set ylabel 'Bicis' font 'Arial,12'
set autoscale
set yrange [5:70]
set timefmt '%Y-%m-%d %H:%M:%S'
#set term png color
#set output '/tmp/plot1.png'
plot \
'0' using 1:4 title 'Presion' with lines,\
'1' using 1:4 title 'Umbral' with lines,\
'2' using 1:4 title 'Picos' with points,\
'3' using 1:4 title 'Bicis' with points 
