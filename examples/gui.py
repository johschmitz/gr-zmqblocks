#!/usr/bin/env python
# 
# Copyright 2013 Institute for Theoretical Information Technology,
#                RWTH Aachen University
# 
# Authors: Johannes Schmitz <schmitz@ti.rwth-aachen.de>
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

import os
from PyQt4 import Qt, QtGui, QtCore, uic
import PyQt4.Qwt5 as Qwt
import zmqblocks

class gui(QtGui.QMainWindow):
    def __init__(self, window_name, rpc_adr_buttons, rpc_adr_waveform, probe_adr, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.gui = uic.loadUi(os.path.join(os.path.dirname(__file__),'main_window.ui'), self)

        self.update_timer = Qt.QTimer()

        # ZeroMQ
        self.probe_manager = zmqblocks.probe_manager()
        self.probe_manager.add_pull_socket(probe_adr, 'float32', self.plot_data)
        self.rpc_mgr_buttons = zmqblocks.rpc_manager()
        self.rpc_mgr_buttons.set_request_socket(rpc_adr_buttons)
        self.rpc_mgr_waveform = zmqblocks.rpc_manager()
        self.rpc_mgr_waveform.set_request_socket(rpc_adr_waveform)

        self.gui.setWindowTitle(window_name)
        self.gui.qwtPlot.setTitle("Signal Scope")
        self.gui.qwtPlot.setAxisTitle(Qwt.QwtPlot.xBottom, "Samples")
        self.gui.qwtPlot.setAxisTitle(Qwt.QwtPlot.yLeft, "Amplitude")
        self.gui.qwtPlot.setAxisScale(Qwt.QwtPlot.xBottom, 0, 100)
        self.gui.qwtPlot.setAxisScale(Qwt.QwtPlot.yLeft, -2, 2)

        #Signals
        self.connect(self.update_timer, QtCore.SIGNAL("timeout()"), self.probe_manager.watcher)
        self.connect(self.gui.pushButton_run, QtCore.SIGNAL("clicked()"), self.start_fg)
        self.connect(self.gui.pushButton_stop, QtCore.SIGNAL("clicked()"), self.stop_fg)
        self.connect(self.gui.comboBox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.set_waveform)
        self.connect(self.gui.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.set_gain)
        self.shortcut_start = QtGui.QShortcut(Qt.QKeySequence("Ctrl+S"), self.gui)
        self.shortcut_stop = QtGui.QShortcut(Qt.QKeySequence("Ctrl+C"), self.gui)
        self.shortcut_exit = QtGui.QShortcut(Qt.QKeySequence("Ctrl+D"), self.gui)
        self.connect(self.shortcut_start, QtCore.SIGNAL("activated()"), self.start_fg)
        self.connect(self.shortcut_stop, QtCore.SIGNAL("activated()"), self.stop_fg)
        self.connect(self.shortcut_exit, QtCore.SIGNAL("activated()"), self.gui.close)

        # Grid
        grid = Qwt.QwtPlotGrid()
        pen = Qt.QPen(Qt.Qt.DotLine)
        pen.setColor(Qt.Qt.black)
        pen.setWidth(0)
        grid.setPen(pen)
        grid.attach(self.gui.qwtPlot)

        # start update timer
        self.update_timer.start(30)

    def start_fg(self):
        self.rpc_mgr_buttons.request("start_fg")

    def stop_fg(self):
        self.rpc_mgr_buttons.request("stop_fg")

    # plot the data from the queues
    def plot_data(self,samples):
        self.x = range(0,len(samples),1)
        self.y = samples
        # clear the previous points from the plot
        self.gui.qwtPlot.clear()
        # draw curve with new points and plot
        curve = Qwt.QwtPlotCurve()
        curve.setPen(Qt.QPen(Qt.Qt.blue, 2))
        curve.attach(self.gui.qwtPlot)
        curve.setData(self.x, self.y)
        self.gui.qwtPlot.replot()

    def set_waveform(self, waveform_str):
        self.rpc_mgr_waveform.request("set_waveform",str(waveform_str))

    def set_gain(self, gain):
        self.rpc_set_gain(gain)

    def rpc_set_gain(self, gain):
        self.rpc_mgr_waveform.request("set_k",gain)

