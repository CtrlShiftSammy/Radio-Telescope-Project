set datafile sep ','
set title "Figure 3. Velocity of arms of Milky Way processed from data PICTOR Radio Telescope, Athens, Greece"
set xlabel "Velocity of Hydrogen gas with respect to Earth (m/s)"
set ylabel "Relative power of observed velocity"
label1 = -2713.02
set xrange[-130000:50000]
p 'Readings/PICTOR/01-01-2023/17:16/spectrum.csv' u (((1420.4057517682 / $1) - 1) * 299792458):4 w l title '17:16', \
    'Readings/PICTOR/01-01-2023/17:27/spectrum.csv' u (((1420.4057517682 / $1) - 1) * 299792458):($4 + 0.02) w l title '17:27', \
    'Readings/PICTOR/01-01-2023/17:38/spectrum.csv' u (((1420.4057517682 / $1) - 1) * 299792458):($4 + 0.36) w l title '17:38', \
    'Readings/PICTOR/01-01-2023/18:11/spectrum.csv' u (((1420.4057517682 / $1) - 1) * 299792458):($4 + 0.36) w l title '18:11', \
    'Readings/PICTOR/01-01-2023/18:22/spectrum.csv' u (((1420.4057517682 / $1) - 1) * 299792458):($4+0.025) w l title '18:22', \
