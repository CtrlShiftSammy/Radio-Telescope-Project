import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from scipy.fft import fft, fftfreq

name = "gqrx_20220910_093851_104450100_1800000_fc"
scaling = 1
file = open("Readings/ASRT/10-09-2022/" + name + ".raw","rb")
f = file.read()
file.close()
# Number of sample points
N = int(len(f) / (2 * scaling)) - 1
# sample spacing
T = 1.0 / 250000000.0
outputFile = open("Readings/ASRT/10-09-2022/" + name + ".txt", "w")
print("Samples = " + str(len(f) / 2))
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.linspace(0.0, N*T, N, endpoint=False)
for i in tqdm(range(int(len(f) / (2 * scaling)) - 1)):
    outputFile.write(str(i) + " " + str(f[(2 * scaling)*i] - 127.5) + " " + str(f[(2 * scaling)*i+1] - 127.5)+ "\n")
    y[i] = ((f[(2 * scaling)*i] - 127.5)**2 + (f[(2 * scaling)*i+1] - 127.5)**2)**0.5
outputFile.close()
yf = fft(y)
xf = fftfreq(N, T)[:N//2]
import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()