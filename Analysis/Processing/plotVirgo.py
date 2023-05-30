import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Readings/ASRT/10-05-2023/power_12:38:49.csv', header=None, names=['time', 'power'])

# Convert time to datetime format
df['time'] = pd.to_datetime(df['time'], unit='s')

df['time'] += pd.Timedelta(hours=16, minutes=46)

# Calculate the rolling mean with a window size of 5
rolling_mean = df['power'].rolling(window=30).mean()

# Plot the rolling mean with respect to time
plt.plot(df['time'], rolling_mean)
plt.xlabel('Time (hours:min)')
plt.ylabel('Relative Power (dB)')
plt.title('Half Solar Transit')

# Add a label saying "Sun"
#plt.text(df['time'][900], 14.7, 'Sun', fontsize=12, color='Black', horizontalalignment='left')
#plt.text(df['time'][2250], 14.0, 'Human', fontsize=12, color='Black', horizontalalignment='left')
#plt.text(df['time'][1900], 10.5, 'Sky', fontsize=12, color='Black', horizontalalignment='left')
#plt.text(df['time'][3000], 14.83, 'Ground', fontsize=12, color='Black', horizontalalignment='left')
#
plt.show()
