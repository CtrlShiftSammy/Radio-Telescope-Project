#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Radiometer
# GNU Radio version: 3.10.5.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from datetime import datetime
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import numpy as np
import osmosdr
import time



from gnuradio import qtgui

class Radiometer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Radiometer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radiometer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Radiometer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.date = date = datetime.now().strftime("%d-%m-%Y")
        self.reading = reading = "Readings/ASRT/" + date + "/"
        self.directory = directory = "/run/media/sammy/Projects/Radio-Telescope-Project/"
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.time0 = time0 = datetime.now().strftime("%H:%M:%S")
        self.prefix = prefix = directory + reading
        self.ymax = ymax = 200
        self.samp_rate = samp_rate = 2e6
        self.intermediate_rate = intermediate_rate = 10000
        self.integration_time = integration_time = 5
        self.freq = freq = 1440e6
        self.file_rate = file_rate = 10
        self.el = el = "0"
        self.display_time = display_time = 60
        self.dc_gain = dc_gain = 10000
        self.csvfile = csvfile = prefix + timenow +".csv"
        self.csv_prefix = csv_prefix = directory + reading + time0+"_"
        self.az = az = "0"
        self.Save_CSV_File = Save_CSV_File = 0

        ##################################################
        # Blocks
        ##################################################
        self._ymax_range = Range(0, 10000, 10, 200, 5)
        self._ymax_win = RangeWidget(self._ymax_range, self.set_ymax, "y-axis max", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._ymax_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(100e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            32768, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            2.5e9, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            1450000000, #fc
            2.4e6, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self._integration_time_range = Range(0, 10, 0.1, 5, 200)
        self._integration_time_win = RangeWidget(self._integration_time_range, self.set_integration_time, "'integration_time'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._integration_time_win)
        self._dc_gain_tool_bar = Qt.QToolBar(self)
        self._dc_gain_tool_bar.addWidget(Qt.QLabel("DC Gain" + ": "))
        self._dc_gain_line_edit = Qt.QLineEdit(str(self.dc_gain))
        self._dc_gain_tool_bar.addWidget(self._dc_gain_line_edit)
        self._dc_gain_line_edit.returnPressed.connect(
            lambda: self.set_dc_gain(int(str(self._dc_gain_line_edit.text()))))
        self.top_grid_layout.addWidget(self._dc_gain_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._Save_CSV_File_options = [0, 1]
        # Create the labels list
        self._Save_CSV_File_labels = ['Stop', 'Start']
        # Create the combo box
        # Create the radio buttons
        self._Save_CSV_File_group_box = Qt.QGroupBox("Save To CSV File" + ": ")
        self._Save_CSV_File_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._Save_CSV_File_button_group = variable_chooser_button_group()
        self._Save_CSV_File_group_box.setLayout(self._Save_CSV_File_box)
        for i, _label in enumerate(self._Save_CSV_File_labels):
            radio_button = Qt.QRadioButton(_label)
            self._Save_CSV_File_box.addWidget(radio_button)
            self._Save_CSV_File_button_group.addButton(radio_button, i)
        self._Save_CSV_File_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Save_CSV_File_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._Save_CSV_File_options.index(i)))
        self._Save_CSV_File_callback(self.Save_CSV_File)
        self._Save_CSV_File_button_group.buttonClicked[int].connect(
            lambda i: self.set_Save_CSV_File(self._Save_CSV_File_options[i]))
        self.top_grid_layout.addWidget(self._Save_CSV_File_group_box, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Radiometer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date
        self.set_reading("Readings/ASRT/" + self.date + "/")

    def get_reading(self):
        return self.reading

    def set_reading(self, reading):
        self.reading = reading
        self.set_csv_prefix(self.directory + self.reading + self.time0+"_")
        self.set_prefix(self.directory + self.reading)

    def get_directory(self):
        return self.directory

    def set_directory(self, directory):
        self.directory = directory
        self.set_csv_prefix(self.directory + self.reading + self.time0+"_")
        self.set_prefix(self.directory + self.reading)

    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow
        self.set_csvfile(self.prefix + self.timenow +".csv")

    def get_time0(self):
        return self.time0

    def set_time0(self, time0):
        self.time0 = time0
        self.set_csv_prefix(self.directory + self.reading + self.time0+"_")

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_csvfile(self.prefix + self.timenow +".csv")

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_intermediate_rate(self):
        return self.intermediate_rate

    def set_intermediate_rate(self, intermediate_rate):
        self.intermediate_rate = intermediate_rate

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, 2.5e9)

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate

    def get_el(self):
        return self.el

    def set_el(self, el):
        self.el = el

    def get_display_time(self):
        return self.display_time

    def set_display_time(self, display_time):
        self.display_time = display_time

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        Qt.QMetaObject.invokeMethod(self._dc_gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.dc_gain)))

    def get_csvfile(self):
        return self.csvfile

    def set_csvfile(self, csvfile):
        self.csvfile = csvfile

    def get_csv_prefix(self):
        return self.csv_prefix

    def set_csv_prefix(self, csv_prefix):
        self.csv_prefix = csv_prefix

    def get_az(self):
        return self.az

    def set_az(self, az):
        self.az = az

    def get_Save_CSV_File(self):
        return self.Save_CSV_File

    def set_Save_CSV_File(self, Save_CSV_File):
        self.Save_CSV_File = Save_CSV_File
        self._Save_CSV_File_callback(self.Save_CSV_File)




def main(top_block_cls=Radiometer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
