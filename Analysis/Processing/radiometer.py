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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import radiometer



from gnuradio import qtgui

class radiometer(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "radiometer")

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
        self.samp_rate = samp_rate = 2.5E6
        self.prefix = prefix = "/run/media/sammy/Projects/Radio-Telescope-Project/Analysis/"
        self.integration_select = integration_select = 0
        self.frequency = frequency = 1.45E9

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._integration_select_options = [0, 1]
        # Create the labels list
        self._integration_select_labels = ['0.5 s', '2 s']
        # Create the combo box
        self._integration_select_tool_bar = Qt.QToolBar(self)
        self._integration_select_tool_bar.addWidget(Qt.QLabel("'integration_select'" + ": "))
        self._integration_select_combo_box = Qt.QComboBox()
        self._integration_select_tool_bar.addWidget(self._integration_select_combo_box)
        for _label in self._integration_select_labels: self._integration_select_combo_box.addItem(_label)
        self._integration_select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._integration_select_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._integration_select_options.index(i)))
        self._integration_select_callback(self.integration_select)
        self._integration_select_combo_box.currentIndexChanged.connect(
            lambda i: self.set_integration_select(self._integration_select_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._integration_select_tool_bar)
        self.single_pole_iir_filter_xx_1 = filter.single_pole_iir_filter_cc((1.0 / (samp_rate * 0.5)), 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_cc((1.0 / (samp_rate * 2)), 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(0, 0)
        self.rtlsdr_source_0.set_if_gain(10, 0)
        self.rtlsdr_source_0.set_bb_gain(10, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.radiometer_csv_file_writer_0 = radiometer.csv_file_writer('', '', '')
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
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


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
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
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_histogram_sink_x_0 = qtgui.histogram_sink_f(
            1024,
            100,
            (-1),
            1,
            "",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0.enable_grid(False)
        self.qtgui_histogram_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
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
        self.top_layout.addWidget(self._qtgui_histogram_sink_x_0_win)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,integration_select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_cc(1000, 1, 4000, 1)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.radiometer_csv_file_writer_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_histogram_sink_x_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_float_to_complex_1, 0), (self.single_pole_iir_filter_xx_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_complex_to_float_1, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.single_pole_iir_filter_xx_1, 0), (self.blocks_selector_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "radiometer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.single_pole_iir_filter_xx_0.set_taps((1.0 / (self.samp_rate * 2)))
        self.single_pole_iir_filter_xx_1.set_taps((1.0 / (self.samp_rate * 0.5)))

    def get_prefix(self):
        return self.prefix

    def set_prefix(self, prefix):
        self.prefix = prefix

    def get_integration_select(self):
        return self.integration_select

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select
        self._integration_select_callback(self.integration_select)
        self.blocks_selector_0.set_input_index(self.integration_select)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.rtlsdr_source_0.set_center_freq(self.frequency, 0)




def main(top_block_cls=radiometer, options=None):

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
