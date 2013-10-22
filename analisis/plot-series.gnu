set title 'Bicicletas Detectadas'
set xdata time
set key box
#set size 1.5,1.5
#set pointsize 2
set xlabel 'Tiempo'
set xtics auto 
set format x "%H:%M:%S"
set ylabel 'Bicis' font 'Arial,12'
#set autoscale
set yrange [5:140]
set timefmt '%Y-%m-%d %H:%M:%S'
#set term png color
#set output '/tmp/plot1.png'
set key top right
set style line 1 lc rgb '#8b1a0e' pt 1 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2 # --- green
set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11

set tics nomirror
set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12


plot \
'0' using 1:4 title 'Presion' with lines ,\
'1' using 1:4 title 'Umbral' with lines,\
'4' using 1:4 title 'maLP' with lines,\
'2' using 1:4 title 'Picos' with points pt 2,\
'3' using 1:4 title 'Bicis' with points ls 2 pt 6,\
'5' using 1:4 title 'ma' with lines  ls 4 
