set datafile separator ","
set title "Signal versus time"
set xlabel "Time"
set ylabel "Signal"
set xtics time format "%tM:%.3tS"
p 'Readings/ASRT/10-05-2023/17:59:59_Raw_2023-05-10_0_0_power.csv' u 1 w l lw 2 title "Raw data", \
'Readings/ASRT/10-05-2023/17:59:59_Integrated_2023-05-10_0_0_power.csv' u 1 w l lw 2 title "Integrated data", \
'Readings/ASRT/10-05-2023/17:59:59_Decimated_2023-05-10_0_0_power.csv' u 1 w l lw 2 title "Decimated data", \
'Readings/ASRT/10-05-2023/17:59:59_Processed_2023-05-10_0_0_power.csv' u 1 w l lw 2 title "Processed data"