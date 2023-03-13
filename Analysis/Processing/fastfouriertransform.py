import numpy as np
from scipy.fft import fft, fftfreq
from tqdm import tqdm
name = "1912"
file = open("Readings/ASRT/22-08-2022/" + name + ".txt","rb")
f = file.readlines()
file.close()

# Number of sample points
N = len(f)
# sample spacing
T = 1.0 / 250000000.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.linspace(0.0, N*T, N, endpoint=False)
for i in range(N):
    y[i] = (float(((f[i].split())[1].decode()))**2 + (float((f[i].split())[2].decode()))**2)**0.5
yf = fft(y)
xf = fftfreq(N, T)[:N//2]
import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()