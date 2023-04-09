import matplotlib.pyplot as plt
import datetime

# Open the file for reading
with open('Readings/ASRT/26-03-2023/14:03:05_2023-03-26_0_0_power.csv', 'r') as f:

    # Initialize empty lists to store the time and power values
    times = []
    powers = []

    # Loop over each line in the file
    for line in f:

        # Split the line into time and power values
        values = line.split(';')

        # Convert the time string into a datetime object
        time = datetime.datetime.strptime(values[1].strip(), '%d/%m/%Y %H:%M:%S')

        # Append the time and power values to their respective lists
        times.append(time)
        powers.append(float(values[0]))

# Plot the power values against time
plt.plot(times, powers)
plt.xlabel('Time')
plt.ylabel('Power')

# Adjust the time axis
plt.xlim([datetime.datetime(2023, 3, 26, 14, 29, 0), datetime.datetime(2023, 3, 26, 14, 59, 0)])

plt.show()
