import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Readings/ASRT/07-04-2023/power_17:08:13.csv', header=None, names=['time', 'power'])

# Convert time to datetime format
df['time'] = pd.to_datetime(df['time'], unit='s')

df['time'] += pd.Timedelta(hours=17, minutes=8)

# Calculate the rolling mean with a window size of 5
rolling_mean = df['power'].rolling(window=30).mean()

# Plot the rolling mean with respect to time
plt.plot(df['time'], rolling_mean)
plt.xlabel('Time (hours:min)')
plt.ylabel('Relative Power (dB)')
plt.title('Half Solar Transit')
plt.show()
