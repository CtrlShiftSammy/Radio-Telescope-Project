set datafile separator ","
set xrange[0:45]
set title "Relative power of signal versus time"
set xlabel "Time"
set ylabel "Relative Power (dB)"
set xtics time format "%tM:%.3tS"
p 'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:26:10.csv' u ($1 - 52):3 w l lw 2 notitle, \
'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:26:10.csv' u ($1 - 104):3 w l lw 2 notitle, \
'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:26:10.csv' u ($1 - 156):3 w l lw 2 notitle, \
'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:37:50.csv' u ($1 - 104):3 w l lw 2 notitle, \
'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:37:50.csv' u ($1 - 156):3 w l lw 2 notitle, \
'Readings/ASRT/06-02-2023 (ECE Lab)/power_processed_19:37:50.csv' u ($1 - 208):3 w l lw 2 notitle, \
