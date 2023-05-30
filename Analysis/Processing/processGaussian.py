import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import numpy as np
from scipy.optimize import curve_fit

# Define the Gaussian function
def gaussian(x, baseline, amplitude, mean, std_dev):
    return baseline + amplitude * np.exp(-(x - mean)**2 / (2 * std_dev**2))

# Open the file for reading
with open('Readings/ASRT/17-05-2023/05:43:15_Processed_2023-05-17_0_0_power.csv', 'r') as f:
    times = []
    powers = []
    for line in f:
        values = line.split(';')
        time = datetime.datetime.strptime(values[1].strip(), '%d/%m/%Y %H:%M:%S')
        times.append(time)
        powers.append(float(values[0]))

# Convert time to numeric values
x = np.array([(t - times[0]).total_seconds() for t in times])

start_time = datetime.datetime(2023, 5, 17, 16, 0, 0)
end_time = datetime.datetime(2023, 5, 17, 18, 0, 0)

# Define the x-axis limits
x_min = (start_time - times[0]).total_seconds()
x_max = (end_time - times[0]).total_seconds()

# Get the indices within the specified x-axis limits
indices = np.where((x >= x_min) & (x <= x_max))

# Select the corresponding x and y values
x_selected = x[indices]
y_selected = np.array(powers)[indices]

# Find the index of the maximum value in y_selected
max_index = np.argmax(y_selected)

# Get the central x value of the largest peak
x_peak = x_selected[max_index]

# Perform curve fitting
p0 = [69, 15, x_peak, 100]  # Initial guess for the parameters
params, _ = curve_fit(gaussian, x_selected, y_selected, p0=p0)
print(params)

# Calculate half power
half_power = params[0] + params[1] / 2

# Find the indices where power crosses the half power level
crossing_indices = np.where(y_selected >= half_power)[0]
half_power_indices = [crossing_indices[0], crossing_indices[-1]]

# Get the corresponding time values
time_crossing = [times[indices[0][index]] for index in half_power_indices]

# Calculate the time difference between the two crossings
time_diff = (time_crossing[1] - time_crossing[0]).total_seconds()
print("Time taken between half power points:", time_diff, "seconds")

# Generate the best-fit Gaussian curve
y_fit = gaussian(x_selected, *params)

# Plot the power values against time
plt.plot(times, powers, label='Signal')
plt.plot([times[i] for i in indices[0]], y_fit, 'r', label='Best Fit')
plt.xlabel('Time')
plt.ylabel('Uncalibrated Power (Linear)')
plt.legend()

# Display vertical lines at half power points
plt.axvline(x=time_crossing[0], color='g', linestyle='--')
plt.axvline(x=time_crossing[1], color='g', linestyle='--')

# Adjust the time axis
plt.xlim([start_time, end_time])
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.ylim(40, 100)
plt.show()
