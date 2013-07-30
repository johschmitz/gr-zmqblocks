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
import pmt
import threading


class rpc_manager():
    def __init__(self):
        self.zmq_context = zmq.Context()
        self.poller = zmq.Poller()
        self.interfaces = dict()

    def set_reply_socket(self, address):
        self.rep_socket = self.zmq_context.socket(zmq.REP)
        self.rep_socket.bind(address)
        print "[RPC] reply socket bound to: ", address
        self.poller.register(self.rep_socket, zmq.POLLIN)

    def set_request_socket(self, address):
        self.req_socket = self.zmq_context.socket(zmq.REQ)
        self.req_socket.connect(address)
        print "[RPC] request socket connected to: ", address
        #self.poller.register(self.req_socket, zmq.POLLOUT)

    def add_interface(self, id_str, callback_func):
        if not self.interfaces.has_key(id_str):
            self.interfaces[id_str] = callback_func
            print "[RPC] added reply interface:", id_str
        else:
            print "ERROR: duplicate id_str"

    def watcher(self):
        while True:
            # poll for calls
            socks = dict(self.poller.poll())
            if socks.get(self.rep_socket) == zmq.POLLIN:
                # receive call
                msg = self.rep_socket.recv()
                (id_str, args) = pmt.to_python(pmt.deserialize_str(msg))
                print "[RPC] request:", id_str, ", args:", args
                reply = self.callback(id_str, args)
                self.rep_socket.send(pmt.serialize_str(pmt.to_pmt(reply)))

    def start_watcher(self):
        t = threading.Thread(target=self.watcher,args=())
        t.daemon = True
        t.start()

    def request(self, id_str, args=None):
        # FIXME: need to poll?
        self.req_socket.send(pmt.serialize_str(pmt.to_pmt((id_str,args))))
        reply = pmt.to_python(pmt.deserialize_str(self.req_socket.recv()))
        print "[RPC] reply:", reply
        return reply

    def callback(self, id_str, args):
        if self.interfaces.has_key(id_str):
            callback_func = self.interfaces.get(id_str)
            if args:
                return(callback_func(args))
            else:
                return(callback_func())
        else:
            print "[RPC] ERROR: id_str not found"
            return 0