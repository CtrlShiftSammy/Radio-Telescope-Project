import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ephem

# Set the observer's location
observer = ephem.Observer()
observer.lon = '-77.8880'  # West longitude in degrees
observer.lat = '29.8543'   # North latitude in degrees
observer.elevation = 7   # Elevation in meters

# Set the date range
start_date = ephem.Date('2023/4/1 00:00:00') # yyyy/mm/dd hh:mm:ss
end_date = ephem.Date('2023/4/2 00:00:00') # yyyy/mm/dd hh:mm:ss

# Set the frequency for calculations (in days)
step_size = 0.1

# Create lists to store the azimuth and altitude data
azimuths = []
altitudes = []

# Create lists to store the moon's azimuth and altitude data
moon_azimuths = []
moon_altitudes = []

# Calculate the azimuth and altitude for each time step
while observer.date < end_date:
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    
    sun.compute(observer)
    moon.compute(observer)
    
    azimuths.append(sun.az * 180 / ephem.pi)
    altitudes.append(sun.alt * 180 / ephem.pi)
    
    moon_azimuths.append(moon.az * 180 / ephem.pi)
    moon_altitudes.append(moon.alt * 180 / ephem.pi)
    
    observer.date += step_size

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the sun's path
ax.plot(azimuths, altitudes, zs=0, label='Sun')

# Plot the moon's path
ax.plot(moon_azimuths, moon_altitudes, zs=0, label='Moon')

# Set the labels for the axes
ax.set_xlabel('Azimuth (degrees)')
ax.set_ylabel('Altitude (degrees)')
ax.set_zlabel('Time')

# Add a colorbar
m = plt.cm.ScalarMappable(cmap=plt.cm.cool)
m.set_array(altitudes)
cbar = plt.colorbar(m)
cbar.set_label('Altitude (degrees)')

# Add a legend
ax.legend()

# Show the plot
plt.show()
