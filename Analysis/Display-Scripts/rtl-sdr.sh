#!/bin/bash
nos=$((2048000*$1))
rtl_sdr -f 1450000000 -g 40 -n $nos $2
#python3 -B plot_from_dir.py $2
