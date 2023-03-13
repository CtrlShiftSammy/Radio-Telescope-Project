# import numpy as np
import matplotlib.pyplot as plt

def plotter(datfile):
    # no. of data points
    nodp = 1536

    file = open(datfile,"rb")
    f = file.read()

    # t = np.linspace(tsec/nodp, tsec + tsec/nodp, nodp)
    t = [i for i in range(nodp)]
    l = len(f)/2
    r = [abs(complex(f[i],f[i+1]))**2 for i in range(int(l))]
    file.close()

    rs = {}
    for i in range(nodp):
        rs["r" + str(i)] = r[int(i*l/nodp):int((i+1)*l/nodp)]

    rss = [sum(i) for i in rs.values()]
    plt.plot(t,rss)
    plt.savefig(datfile.name.split(".")[0] + ".png")
