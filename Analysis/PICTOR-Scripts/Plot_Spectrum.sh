set datafile sep ','
p 'Readings/PICTOR/01-01-2023/17:16/spectrum.csv' u 1:4 w lp title '17:16', \
    'Readings/PICTOR/01-01-2023/17:27/spectrum.csv' u 1:($4 + 0.02) w lp title '17:27', \
    'Readings/PICTOR/01-01-2023/17:38/spectrum.csv' u 1:($4 + 0.36) w lp title '17:38', \
    'Readings/PICTOR/01-01-2023/18:11/spectrum.csv' u 1:($4 + 0.36) w lp title '18:11', \
    'Readings/PICTOR/01-01-2023/18:22/spectrum.csv' u 1:($4+0.025) w lp title '18:22'    