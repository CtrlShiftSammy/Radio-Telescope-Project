import virgo
import time

def observeAndPlot(d):
    
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
        'duration': d,
        'loc': '',
        'ra_dec': '',
        'az_alt': ''
    }
    print()
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S")
    reading_location = '/run/media/sammy/Projects/Radio-Telescope-Project/Readings/ASRT/06-02-2023 (ECE Lab)/'
    reading_name = 'virgo-observation_' + current_time + '.dat'
    obs_file_name = reading_location + reading_name
    # Begin data acquisition
    virgo.observe(obs_parameters=obs, obs_file=obs_file_name)

    plot_name = 'plot_' + current_time + '.png'
    plot_file_name = reading_location + plot_name
    spectrum_name = 'spectrum_' + current_time + '.csv'
    spectrum_file_name = reading_location + spectrum_name
    power_name = 'power_' + current_time + '.csv'
    power_file_name = reading_location + power_name

    # Analyze data, mitigate RFI and export the data as a CSV file
    virgo.plot(obs_parameters=obs, n=20, m=35, f_rest=1600e6,
            vlsr=False, meta=False, avg_ylim=(-5,15), cal_ylim=(-20,260),
            obs_file=obs_file_name, rfi=[(1599.2e6, 1599.3e6), (1600.8e6, 1600.9e6)],
            dB=True, spectra_csv=spectrum_file_name, power_csv=power_file_name, plot_file= plot_file_name)

time_array = [180]
for t in time_array:
    observeAndPlot(t)