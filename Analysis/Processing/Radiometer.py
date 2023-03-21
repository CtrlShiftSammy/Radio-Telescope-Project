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
from gnuradio import blocks
from gnuradio import filter
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
import radiometer



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
        self.T_hot = T_hot = 300
        self.T_cold = T_cold = 10
        self.P_hot = P_hot = 287
        self.P_cold = P_cold = 110
        self.timenow = timenow = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        self.prefix = prefix = "/run/media/sammy/Projects/Radio-Telescope-Project/Analysis/"
        self.gain = gain = (P_hot-P_cold)/(T_hot-T_cold)
        self.el = el = "0"
        self.az = az = "0"
        self.T_sys = T_sys = (T_hot - T_cold*(P_hot/P_cold))/((P_hot/P_cold) - 1)
        self.ymax = ymax = 200
        self.samp_rate = samp_rate = 10e6
        self.intermediate_rate = intermediate_rate = 1000
        self.integration_select = integration_select = 0
        self.integrationTimeShort = integrationTimeShort = 0.5
        self.integrationTimeLong = integrationTimeLong = 1
        self.gain_label = gain_label = gain
        self.freq = freq = 1420e6
        self.file_rate = file_rate = 1
        self.dc_gain = dc_gain = 10000
        self.csvfile = csvfile = prefix + timenow +"_AZ"+az+"_EL"+el +".csv"
        self.calibration_select = calibration_select = 0
        self.Tsys_label = Tsys_label = T_sys
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
        # Create the options list
        self._integration_select_options = [0, 1]
        # Create the labels list
        self._integration_select_labels = ['Short Integration', 'Long Integration']
        # Create the combo box
        # Create the radio buttons
        self._integration_select_group_box = Qt.QGroupBox("Integration Time" + ": ")
        self._integration_select_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._integration_select_button_group = variable_chooser_button_group()
        self._integration_select_group_box.setLayout(self._integration_select_box)
        for i, _label in enumerate(self._integration_select_labels):
            radio_button = Qt.QRadioButton(_label)
            self._integration_select_box.addWidget(radio_button)
            self._integration_select_button_group.addButton(radio_button, i)
        self._integration_select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._integration_select_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._integration_select_options.index(i)))
        self._integration_select_callback(self.integration_select)
        self._integration_select_button_group.buttonClicked[int].connect(
            lambda i: self.set_integration_select(self._integration_select_options[i]))
        self.top_grid_layout.addWidget(self._integration_select_group_box, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self._calibration_select_options = [0, 1]
        # Create the labels list
        self._calibration_select_labels = ['Without Calibration', 'With Calibration']
        # Create the combo box
        # Create the radio buttons
        self._calibration_select_group_box = Qt.QGroupBox("Select Calibration" + ": ")
        self._calibration_select_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._calibration_select_button_group = variable_chooser_button_group()
        self._calibration_select_group_box.setLayout(self._calibration_select_box)
        for i, _label in enumerate(self._calibration_select_labels):
            radio_button = Qt.QRadioButton(_label)
            self._calibration_select_box.addWidget(radio_button)
            self._calibration_select_button_group.addButton(radio_button, i)
        self._calibration_select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._calibration_select_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._calibration_select_options.index(i)))
        self._calibration_select_callback(self.calibration_select)
        self._calibration_select_button_group.buttonClicked[int].connect(
            lambda i: self.set_calibration_select(self._calibration_select_options[i]))
        self.top_grid_layout.addWidget(self._calibration_select_group_box, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._Save_CSV_File_options = [0, 1]
        # Create the labels list
        self._Save_CSV_File_labels = ['Stop Save To File', 'Start Save To File']
        # Create the combo box
        # Create the radio buttons
        self._Save_CSV_File_group_box = Qt.QGroupBox("Save To CSV File" + ": ")
        self._Save_CSV_File_box = Qt.QVBoxLayout()
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
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_ff((1/(samp_rate*integrationTimeLong)), 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff((1/(samp_rate*integrationTimeShort)), 1)
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
        self.radiometer_csv_file_writer_0 = radiometer.csv_file_writer(prefix, az, el)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            intermediate_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0.set_y_axis(-1, ymax)

        self.qtgui_time_sink_x_0.set_y_label('Total Power', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2, 0, 3, 4)
        for r in range(2, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
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
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 2, 4, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            1024,
            100,
            (-1),
            1,
            "System Hearbeat",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['Histogram', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_win, 0, 4, 2, 2)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._gain_label_formatter = None
        else:
            self._gain_label_formatter = lambda x: eng_notation.num_to_str(x)

        self._gain_label_tool_bar.addWidget(Qt.QLabel("Gain"))
        self._gain_label_label = Qt.QLabel(str(self._gain_label_formatter(self.gain_label)))
        self._gain_label_tool_bar.addWidget(self._gain_label_label)
        self.top_grid_layout.addWidget(self._gain_label_tool_bar, 2, 5, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_selector_0_0_0 = blocks.selector(gr.sizeof_float*1,0,Save_CSV_File)
        self.blocks_selector_0_0_0.set_enabled(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,calibration_select,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,integration_select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((1/gain))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(dc_gain)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, (1/1000), 1000, 1)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(samp_rate/intermediate_rate)))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, (int(intermediate_rate/file_rate)))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-T_sys))
        self._Tsys_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._Tsys_label_formatter = None
        else:
            self._Tsys_label_formatter = lambda x: eng_notation.num_to_str(x)

        self._Tsys_label_tool_bar.addWidget(Qt.QLabel("Tsys"))
        self._Tsys_label_label = Qt.QLabel(str(self._Tsys_label_formatter(self.Tsys_label)))
        self._Tsys_label_tool_bar.addWidget(self._Tsys_label_label)
        self.top_grid_layout.addWidget(self._Tsys_label_tool_bar, 3, 5, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._P_hot_tool_bar = Qt.QToolBar(self)
        self._P_hot_tool_bar.addWidget(Qt.QLabel("Hot Pw" + ": "))
        self._P_hot_line_edit = Qt.QLineEdit(str(self.P_hot))
        self._P_hot_tool_bar.addWidget(self._P_hot_line_edit)
        self._P_hot_line_edit.returnPressed.connect(
            lambda: self.set_P_hot(eng_notation.str_to_num(str(self._P_hot_line_edit.text()))))
        self.top_grid_layout.addWidget(self._P_hot_tool_bar, 1, 3, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._P_cold_tool_bar = Qt.QToolBar(self)
        self._P_cold_tool_bar.addWidget(Qt.QLabel("Cold Pw" + ": "))
        self._P_cold_line_edit = Qt.QLineEdit(str(self.P_cold))
        self._P_cold_tool_bar.addWidget(self._P_cold_line_edit)
        self._P_cold_line_edit.returnPressed.connect(
            lambda: self.set_P_cold(eng_notation.str_to_num(str(self._P_cold_line_edit.text()))))
        self.top_grid_layout.addWidget(self._P_cold_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_selector_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_selector_0_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0_0_0, 1), (self.radiometer_csv_file_writer_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_selector_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Radiometer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_T_hot(self):
        return self.T_hot

    def set_T_hot(self, T_hot):
        self.T_hot = T_hot
        self.set_T_sys((self.T_hot - self.T_cold*(self.P_hot/self.P_cold))/((self.P_hot/self.P_cold) - 1))
        self.set_gain((self.P_hot-self.P_cold)/(self.T_hot-self.T_cold))

    def get_T_cold(self):
        return self.T_cold

    def set_T_cold(self, T_cold):
        self.T_cold = T_cold
        self.set_T_sys((self.T_hot - self.T_cold*(self.P_hot/self.P_cold))/((self.P_hot/self.P_cold) - 1))
        self.set_gain((self.P_hot-self.P_cold)/(self.T_hot-self.T_cold))

    def get_P_hot(self):
        return self.P_hot

    def set_P_hot(self, P_hot):
        self.P_hot = P_hot
        Qt.QMetaObject.invokeMethod(self._P_hot_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.P_hot)))
        self.set_T_sys((self.T_hot - self.T_cold*(self.P_hot/self.P_cold))/((self.P_hot/self.P_cold) - 1))
        self.set_gain((self.P_hot-self.P_cold)/(self.T_hot-self.T_cold))

    def get_P_cold(self):
        return self.P_cold

    def set_P_cold(self, P_cold):
        self.P_cold = P_cold
        Qt.QMetaObject.invokeMethod(self._P_cold_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.P_cold)))
        self.set_T_sys((self.T_hot - self.T_cold*(self.P_hot/self.P_cold))/((self.P_hot/self.P_cold) - 1))
        self.set_gain((self.P_hot-self.P_cold)/(self.T_hot-self.T_cold))

    def get_timenow(self):
        return self.timenow

    def set_timenow(self, timenow):
        self.timenow = timenow
        self.set_csvfile(self.prefix + self.timenow +"_AZ"+self.az+"_EL"+self.el +".csv")

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix
        self.set_csvfile(self.prefix + self.timenow +"_AZ"+self.az+"_EL"+self.el +".csv")

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.set_gain_label(self.gain)
        self.blocks_multiply_const_vxx_0_0.set_k((1/self.gain))

    def get_el(self):
        return self.el

    def set_el(self, el):
        self.el = el
        self.set_csvfile(self.prefix + self.timenow +"_AZ"+self.az+"_EL"+self.el +".csv")

    def get_az(self):
        return self.az

    def set_az(self, az):
        self.az = az
        self.set_csvfile(self.prefix + self.timenow +"_AZ"+self.az+"_EL"+self.el +".csv")

    def get_T_sys(self):
        return self.T_sys

    def set_T_sys(self, T_sys):
        self.T_sys = T_sys
        self.set_Tsys_label(self.T_sys)
        self.blocks_add_const_vxx_0.set_k((-self.T_sys))

    def get_ymax(self):
        return self.ymax

    def set_ymax(self, ymax):
        self.ymax = ymax
        self.qtgui_time_sink_x_0.set_y_axis(-1, self.ymax)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_keep_one_in_n_1.set_n((int(self.samp_rate/self.intermediate_rate)))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.single_pole_iir_filter_xx_0.set_taps((1/(self.samp_rate*self.integrationTimeShort)))
        self.single_pole_iir_filter_xx_0_0.set_taps((1/(self.samp_rate*self.integrationTimeLong)))

    def get_intermediate_rate(self):
        return self.intermediate_rate

    def set_intermediate_rate(self, intermediate_rate):
        self.intermediate_rate = intermediate_rate
        self.blocks_keep_one_in_n_0.set_n((int(self.intermediate_rate/self.file_rate)))
        self.blocks_keep_one_in_n_1.set_n((int(self.samp_rate/self.intermediate_rate)))
        self.qtgui_time_sink_x_0.set_samp_rate(self.intermediate_rate)

    def get_integration_select(self):
        return self.integration_select

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select
        self._integration_select_callback(self.integration_select)
        self.blocks_selector_0.set_input_index(self.integration_select)

    def get_integrationTimeShort(self):
        return self.integrationTimeShort

    def set_integrationTimeShort(self, integrationTimeShort):
        self.integrationTimeShort = integrationTimeShort
        self.single_pole_iir_filter_xx_0.set_taps((1/(self.samp_rate*self.integrationTimeShort)))

    def get_integrationTimeLong(self):
        return self.integrationTimeLong

    def set_integrationTimeLong(self, integrationTimeLong):
        self.integrationTimeLong = integrationTimeLong
        self.single_pole_iir_filter_xx_0_0.set_taps((1/(self.samp_rate*self.integrationTimeLong)))

    def get_gain_label(self):
        return self.gain_label

    def set_gain_label(self, gain_label):
        self.gain_label = gain_label
        Qt.QMetaObject.invokeMethod(self._gain_label_label, "setText", Qt.Q_ARG("QString", str(self._gain_label_formatter(self.gain_label))))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_file_rate(self):
        return self.file_rate

    def set_file_rate(self, file_rate):
        self.file_rate = file_rate
        self.blocks_keep_one_in_n_0.set_n((int(self.intermediate_rate/self.file_rate)))

    def get_dc_gain(self):
        return self.dc_gain

    def set_dc_gain(self, dc_gain):
        self.dc_gain = dc_gain
        Qt.QMetaObject.invokeMethod(self._dc_gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.dc_gain)))
        self.blocks_multiply_const_vxx_0.set_k(self.dc_gain)

    def get_csvfile(self):
        return self.csvfile

    def set_csvfile(self, csvfile):
        self.csvfile = csvfile

    def get_calibration_select(self):
        return self.calibration_select

    def set_calibration_select(self, calibration_select):
        self.calibration_select = calibration_select
        self._calibration_select_callback(self.calibration_select)
        self.blocks_selector_0_0.set_input_index(self.calibration_select)

    def get_Tsys_label(self):
        return self.Tsys_label

    def set_Tsys_label(self, Tsys_label):
        self.Tsys_label = Tsys_label
        Qt.QMetaObject.invokeMethod(self._Tsys_label_label, "setText", Qt.Q_ARG("QString", str(self._Tsys_label_formatter(self.Tsys_label))))

    def get_Save_CSV_File(self):
        return self.Save_CSV_File

    def set_Save_CSV_File(self, Save_CSV_File):
        self.Save_CSV_File = Save_CSV_File
        self._Save_CSV_File_callback(self.Save_CSV_File)
        self.blocks_selector_0_0_0.set_output_index(self.Save_CSV_File)




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
