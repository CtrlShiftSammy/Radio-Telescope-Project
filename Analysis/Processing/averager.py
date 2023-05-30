import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Readings/ASRT/07-04-2023/power_17:08:13.csv', header=None, names=['time', 'power'])

# Convert time to datetime format
df['time'] = pd.to_datetime(df['time'], unit='s')
df['time'] += pd.Timedelta(hours=17, minutes=8)
# Filter data between start and end times
start_time = pd.to_datetime('17:41').time()
end_time = pd.to_datetime('17:44').time()
df_filtered = df[(df['time'].dt.time >= start_time) & (df['time'].dt.time <= end_time)]

# Calculate average power
avg_power = df_filtered['power'].mean()

print(f"Average power between {start_time} and {end_time}: {avg_power:.2f} dB")
