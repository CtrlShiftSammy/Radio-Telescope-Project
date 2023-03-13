import matplotlib.pyplot as plt
from tqdm import tqdm
#name = "../../FMcapture1"
name = "1912"
scaling = 1
#file = open("Readings/ASRT/22-08-2022/" + name + ".dat","rb")
file = open("Readings/ORT/sun_slw26novS1.dat", "rb")
f = file.read()
file.close()
outputFile = open("Readings/ORT/sun_slw26novS1.txt", "w")
print("Samples = " + str(len(f) / 2))
for i in tqdm(range(int(len(f) / (2 * scaling)) - 1)):
    outputFile.write(str(i) + " " + str(f[(2 * scaling)*i] - 127.5) + " " + str(f[(2 * scaling)*i+1] - 127.5)+ "\n")
outputFile.close()

