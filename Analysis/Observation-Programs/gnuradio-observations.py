import matplotlib.pyplot as plt
from datetime import datetime

# Read data from file
data = []
with open('Readings/ASRT/17-05-2023/05:43:15_Processed_2023-05-17_0_0_power.csv', 'r') as file:
    for line in file:
        line = line.strip()
        signal, timestamp = line.split(';')
        signal = float(signal)
        timestamp = datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
        time_data = timestamp.strftime('%H:%M:%S')
        data.append((signal, time_data))

# Extract signal and time values
signals = [entry[0] for entry in data]
timestamps = [entry[1] for entry in data]

# Plotting
plt.plot(timestamps, signals)
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Signal vs Time')
plt.xticks(rotation=45)
plt.show()
