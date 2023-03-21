#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 PhysicsOpenLab.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy
from gnuradio import gr
from datetime import datetime

class csv_file_writer(gr.sync_block):
    """
    docstring for block csv_file_writer
    """
    def __init__(self, prefix,az,el):
        gr.sync_block.__init__(self,
            name="csv_file_writer",
            in_sig=[numpy.float32],
            out_sig=None)
        self.prefix = prefix
        self.az = az
        self.el = el


    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        self.power = float(in0)
        self.timenow = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.textfilename = self.prefix + self.today + "_" + self.az + "_" + self.el + "_power.csv"
        self.stringToWrite = str(self.power) + ";" + self.timenow + "\n"
        
        self.f = open(self.textfilename, "a")
        self.f.write(self.stringToWrite)
        self.f.close()         
        print("File Written")

        return len(input_items[0])


