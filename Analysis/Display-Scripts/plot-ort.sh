set datafile separator " "
set title "Signal versus time"
set xlabel "Time"
set ylabel "Signal"
set xtics time format "%H:%tM:%.3tS"
p 'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($5) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($6) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($7) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($8) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($9) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($10) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($11) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($12) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($13) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($14) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($15) notitle, \
'Readings/ORT/sun_slw26novS1_clean.txt' u (($1 * 3600) + ($2 * 60) + ($3) + ($4 * 0.001)):($16) notitle