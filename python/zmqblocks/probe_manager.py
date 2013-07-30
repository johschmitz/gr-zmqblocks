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

import zmq
import threading
import struct

class probe_manager():
    def __init__(self):
        self.zmq_context = zmq.Context()
        self.poller = zmq.Poller()
        self.interfaces = []

    def add_pull_socket(self, address, data_type, callback_func):
        socket = self.zmq_context.socket(zmq.PULL)
        socket.connect(address)
        # use a tuple to store interface elements
        self.interfaces.append((socket, data_type, callback_func))
        self.poller.register(socket, zmq.POLLIN)

    def watcher(self):
        poll = dict(self.poller.poll(0))
        for i in self.interfaces:
            # i = (socket, data_type, callback_func)
            if poll.get(i[0]) == zmq.POLLIN:
                # receive data
                msg_packed = i[0].recv()
                # use python struct library to unpack the data
                chars_in_msg = len(msg_packed)/struct.calcsize(i[1])
                msg_unpacked = struct.unpack(str(chars_in_msg)+i[1],msg_packed)
                # invoke callback function
                i[2](msg_unpacked)
