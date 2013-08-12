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
from optparse import OptionParser
from gnuradio.eng_option import eng_option
import PyQt4.Qt as Qt
import gui
import sys


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
    qapp = Qt.QApplication(sys.argv)
    rpc_adr_server = "tcp://"+options.servername+":6666"
    probe_adr_gui = "tcp://"+options.servername+":5556"
    qapp.main_window = gui.gui("Remote Server GUI",rpc_adr_server,rpc_adr_server,probe_adr_gui)
    qapp.main_window.show()
    qapp.exec_()

