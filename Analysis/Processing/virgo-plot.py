import virgo
import time
# Define observation parameters
obs = {
    'dev_args': '',
    'rf_gain': 30,
    'if_gain': 25,
    'bb_gain': 18,
    'frequency': 1600e6,
    'bandwidth': 2.4e6,
    'channels': 2048,
    't_sample': 1,
    'duration': 600,
    'loc': '',
    'ra_dec': '',
    'az_alt': ''
}
print()
# Analyze data, mitigate RFI and export the data as a CSV file
virgo.plot(obs_parameters=obs, n=20, m=35, f_rest=1600e6,
           vlsr=False, meta=False, avg_ylim=(-5,15), cal_ylim=(-20,260),
           obs_file='/run/media/sammy/sammy-data/Projects/Radio-Telescope-Project/Readings/ASRT/12-01-2023/virgo-observation_13:45:44.dat', rfi=[(1599.2e6, 1599.3e6), (1600.8e6, 1600.9e6)],
           dB=True, spectra_csv='/run/media/sammy/sammy-data/Projects/Radio-Telescope-Project/Readings/ASRT/12-01-2023/spectrum.csv', power_csv='/run/media/sammy/sammy-data/Projects/Radio-Telescope-Project/Readings/ASRT/12-01-2023/power.csv', plot_file='')