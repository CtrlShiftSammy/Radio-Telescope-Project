set datafile separator ","
set xrange[44100:45900]
set title "Relative power of signal versus time"
set xlabel "Time"
set ylabel "Relative Power (dB)"
set xtics time format "%tH:%tM:%.3tS"
p 'Readings/ASRT/20-01-2023/power_23:55:03.csv' u ($1 - 297):2 w l lt rgb "#ffb3ba" title 'PaAC-RTP ASRT Reading 21-01-2023', \
'Readings/ASRT/20-01-2023/power_processed_23:55:03.csv' u ($1 - 297):3 w l lw 2 lt rgb "#ff0000" notitle, \
'Readings/ASRT/21-01-2023/power_23:55:52.csv' u ($1 - 248):2 w l lt rgb "#baffc9" title 'PaAC-RTP ASRT Reading 22-01-2023', \
'Readings/ASRT/21-01-2023/power_processed_23:55:52.csv' u ($1 - 248):3 w l lw 2 lt rgb "#00ff00" notitle, \
'Readings/ASRT/22-01-2023/power_23:56:33.csv' u ($1 - 207):2 w l lt rgb "#bae1ff" title 'PaAC-RTP ASRT Reading 23-01-2023', \
'Readings/ASRT/22-01-2023/power_processed_23:56:33.csv' u ($1 - 207):3 w l lw 2 lt rgb "#0000ff" notitle, \
