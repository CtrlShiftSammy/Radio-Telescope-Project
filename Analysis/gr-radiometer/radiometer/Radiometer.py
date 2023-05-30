#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Radiometer
# GNU Radio version: 3.10.6.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from datetime import datetime
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import numpy as np
import osmosdr
import time
import radiometer
import sip



class Radiometer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Radiometer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radiometer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.date = date = datetime.now().strftime("%d-%m-%Y")
        self.time0 = time0 = datetime.now().strftime("%H:%M:%S")
        self.reading = reading = "Readings/ASRT/" + date + "/"
        self.directory = directory = "/run/media/sammy/Projects/Radio-Telescope-Project/"
        self.ymax = ymax = 200
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.samp_rate = samp_rate = 2e6
        self.processed_csv_prefix = processed_csv_prefix = directory + reading + time0+"_Processed_"
        self.prefix = prefix = directory + reading
        self.intermediate_rate = intermediate_rate = 10000
        self.integration_time = integration_time = 0.1
        self.freq = freq = 1449e6
        self.file_rate = file_rate = 10
        self.file_name = file_name = directory + reading + time0+"_Raw.dat"
        self.el = el = "0"
        self.dc_gain = dc_gain = 10000
        self.bandwidth = bandwidth = 50e6
        self.az = az = "0"
        self.Save_CSV_File = Save_CSV_File = 0
        self.RF_Gain = RF_Gain = 5
        self.IF_Gain = IF_Gain = 20
        self.BB_Gain = BB_Gain = 25

        ##################################################
        # Blocks
        ##################################################

        self._integration_time_range = Range(0, 10, 0.1, 0.1, 200)
        self._integration_time_win = RangeWidget(self._integration_time_range, self.set_integration_time, "'integration_time'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._integration_time_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_range = Range(950e6, 1950e6, 1e6, 1449e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "'freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._bandwidth_range = Range(1e6, 100e6, 1e6, 50e6, 200)
        self._bandwidth_win = RangeWidget(self._bandwidth_range, self.set_bandwidth, "'bandwidth'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._bandwidth_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
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
        self.top_grid_layout.addWidget(self._Save_CSV_File_group_box, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._RF_Gain_range = Range(0, 30, 0.1, 5, 200)
        self._RF_Gain_win = RangeWidget(self._RF_Gain_range, self.set_RF_Gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._RF_Gain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._IF_Gain_range = Range(0, 30, 0.1, 20, 200)
        self._IF_Gain_win = RangeWidget(self._IF_Gain_range, self.set_IF_Gain, "IF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._IF_Gain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._BB_Gain_range = Range(0, 30, 0.1, 25, 200)
        self._BB_Gain_win = RangeWidget(self._BB_Gain_range, self.set_BB_Gain, "BB Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._BB_Gain_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_ff((1/(samp_rate*integration_time)), 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(RF_Gain, 0)
        self.rtlsdr_source_0.set_if_gain(IF_Gain, 0)
        self.rtlsdr_source_0.set_bb_gain(BB_Gain, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(bandwidth, 0)
        self.radiometer_csv_file_writer_0 = radiometer.csv_file_writer(processed_csv_prefix, az, el)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            bandwidth, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
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

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 8, 1, 3, 1)
        for r in range(8, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_f(
            (file_rate*20), #size
            file_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, ymax)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Processed Power', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(False)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)

        self.qtgui_time_sink_x_0_0_1.disable_legend()

        labels = ['Signal', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win, 9, 0, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            (intermediate_rate*20), #size
            intermediate_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, ymax)

        self.qtgui_time_sink_x_0_0.set_y_label('Averaged Power', "")

        self.qtgui_time_sink_x_0_0.enable_tags(False)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['Signal', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 8, 0, 1, 1)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Radiometer")

        labels = ['Value', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, 0)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 7, 0, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            (4*bandwidth), #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 1, 8, 1)
        for r in range(0, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_selector_0_0_0 = blocks.selector(gr.sizeof_float*1,0,Save_CSV_File)
        self.blocks_selector_0_0_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(dc_gain)
        self.blocks_moving_average_xx_0_1 = blocks.moving_average_ff(10000, (1/1000), 1000, 1)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, (int(samp_rate/intermediate_rate)))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(intermediate_rate/file_rate)))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_selector_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_1, 0), (self.single_pole_iir_filter_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_moving_average_xx_0_1, 0))
        self.connect((self.blocks_selector_0_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0_0_0, 1), (self.radiometer_csv_file_writer_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_keep_one_in_n_0, 0))


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

    def get_time0(self):
        return self.time0

    def set_time0(self, time0):
        self.time0 = time0
        self.set_file_name(self.directory + self.reading + self.time0+"_Raw.dat")
        self.set_processed_csv_prefix(self.directory + self.reading + self.time0+"_Processed_")

    def get_reading(self):
        return self.reading

    def set_reading(self, reading):
        self.reading = reading
        self.set_file_name(self.directory + self.reading + self.time0+"_Raw.dat")
        self.set_prefix(self.directory + self.reading)
        self.set_processed_csv_prefix(self.directory + self.reading + self.time0+"_Processed_")

    def get_directory(self):
        return self.directory

    def set_directory(self, directory):
        self.directory = directory
        self.set_file_name(self.directory + self.reading + self.time0+"_Raw.dat")
        self.set_prefix(self.directory + self.reading)
        self.set_processed_csv_prefix(self.directory + self.reading + self.time0+"_Processed_")

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, self.ymax)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, self.ymax)

    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_keep_one_in_n_1.set_n((int(self.samp_rate/self.intermediate_rate)))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.single_pole_iir_filter_xx_0_0.set_taps((1/(self.samp_rate*self.integration_time)))

    def get_processed_csv_prefix(self):
        return self.processed_csv_prefix

    def set_processed_csv_prefix(self, processed_csv_prefix):
        self.processed_csv_prefix = processed_csv_prefix

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_intermediate_rate(self):
        return self.intermediate_rate

    def set_intermediate_rate(self, intermediate_rate):
        self.intermediate_rate = intermediate_rate
        self.blocks_keep_one_in_n_0.set_n((int(self.intermediate_rate/self.file_rate)))
        self.blocks_keep_one_in_n_1.set_n((int(self.samp_rate/self.intermediate_rate)))
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.intermediate_rate)

    def get_integration_time(self):
        return self.integration_time

    def set_integration_time(self, integration_time):
        self.integration_time = integration_time
        self.single_pole_iir_filter_xx_0_0.set_taps((1/(self.samp_rate*self.integration_time)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, (4*self.bandwidth))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.bandwidth)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.blocks_keep_one_in_n_0.set_n((int(self.intermediate_rate/self.file_rate)))
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.file_rate)

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name

    def get_el(self):
        return self.el

    def set_el(self, el):
        self.el = el

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        self.blocks_multiply_const_vxx_0.set_k(self.dc_gain)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, (4*self.bandwidth))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.bandwidth)
        self.rtlsdr_source_0.set_bandwidth(self.bandwidth, 0)

    def get_az(self):
        return self.az

    def set_az(self, az):
        self.az = az

    def get_Save_CSV_File(self):
        return self.Save_CSV_File

    def set_Save_CSV_File(self, Save_CSV_File):
        self.Save_CSV_File = Save_CSV_File
        self._Save_CSV_File_callback(self.Save_CSV_File)
        self.blocks_selector_0_0_0.set_output_index(self.Save_CSV_File)

    def get_RF_Gain(self):
        return self.RF_Gain

    def set_RF_Gain(self, RF_Gain):
        self.RF_Gain = RF_Gain
        self.rtlsdr_source_0.set_gain(self.RF_Gain, 0)

    def get_IF_Gain(self):
        return self.IF_Gain

    def set_IF_Gain(self, IF_Gain):
        self.IF_Gain = IF_Gain
        self.rtlsdr_source_0.set_if_gain(self.IF_Gain, 0)

    def get_BB_Gain(self):
        return self.BB_Gain

    def set_BB_Gain(self, BB_Gain):
        self.BB_Gain = BB_Gain
        self.rtlsdr_source_0.set_bb_gain(self.BB_Gain, 0)




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
