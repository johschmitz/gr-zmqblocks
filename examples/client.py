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


###############################################################################
# Imports
###############################################################################
import zmqblocks
from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import numpy
import signal
import gui
from PyQt4 import QtGui
import sys

###############################################################################
# GNU Radio top_block
###############################################################################
class top_block(gr.top_block):
    def __init__(self, options):
        gr.top_block.__init__(self)  

        self.options = options

        # create a QT application
        self.qapp = QtGui.QApplication(sys.argv)
        # give Ctrl+C back to system
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        # create the main window
        self.ui = gui.gui("Client","tcp://localhost:6667","tcp://localhost:6666","tcp://localhost:5557")
        self.ui.show()

        # blocks
        #self.zmq_source = zmqblocks.source_reqrep_nopoll(gr.sizeof_float,"tcp://localhost:5555")
        self.zmq_source = zmqblocks.source_reqrep(gr.sizeof_float,"tcp://localhost:5555")
        #self.zmq_source = zmqblocks.source_pushpull(gr.sizeof_float,"tcp://localhost:5555")
        self.zmq_probe = zmqblocks.probe_pushpull(gr.sizeof_float,"tcp://*:5557")

        # connects
        self.connect(self.zmq_source, self.zmq_probe)

        # ZeroMQ
        self.rpc_manager = zmqblocks.rpc_manager()
        self.rpc_manager.set_reply_socket("tcp://*:6667")
        self.rpc_manager.add_interface("start_fg",self.start_fg)
        self.rpc_manager.add_interface("stop_fg",self.stop_fg)
        self.rpc_manager.start_watcher()

    def start_fg(self):
        print "Start Flowgraph"
        try:
            self.start()
        except RuntimeError:
            print "Can't start, flowgraph already running!"

    def stop_fg(self):
        print "Stop Flowgraph"
        self.stop()
        self.wait()


###############################################################################
# Options Parser
###############################################################################
def parse_options():
    """ Options parser. """
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    return options

###############################################################################
# Main
###############################################################################
if __name__ == "__main__":
    options = parse_options()
    tb = top_block(options)
    tb.qapp.exec_()
    tb.stop()
    tb = None