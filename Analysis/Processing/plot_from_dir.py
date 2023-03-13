import os
import sys
from iqread import plotter

for file in os.scandir():
    if file.name == sys.argv[1]:
        plotter(file)
