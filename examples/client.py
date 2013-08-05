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

        # socket addresses
        rpc_adr_server = "tcp://"+self.options.servername+":6666"
        rpc_adr_client = "tcp://localhost:6667"
        rpc_adr_reply = "tcp://*:6667"
        probe_adr_gui = "tcp://localhost:5557"
        probe_adr_fg = "tcp://*:5557"
        source_adr = "tcp://"+self.options.servername+":5555"

        # create the main window
        self.ui = gui.gui("Client",rpc_adr_client,rpc_adr_server,probe_adr_gui)
        self.ui.show()

        # blocks
        #self.zmq_source = zmqblocks.source_reqrep_nopoll(gr.sizeof_float,source_adr)
        self.zmq_source = zmqblocks.source_reqrep(gr.sizeof_float,source_adr)
        #self.zmq_source = zmqblocks.source_pushpull(gr.sizeof_float,source_adr)
        #self.zmq_probe = zmqblocks.sink_pushpull(gr.sizeof_float,probe_adr_fg)
        self.zmq_probe = zmqblocks.sink_pubsub(gr.sizeof_float,probe_adr_fg)

        # connects
        self.connect(self.zmq_source, self.zmq_probe)

        # ZeroMQ
        self.rpc_manager = zmqblocks.rpc_manager()
        self.rpc_manager.set_reply_socket(rpc_adr_reply)
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
    parser.add_option("-s", "--servername", type="string", default="localhost",
                      help="Server hostname")
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
