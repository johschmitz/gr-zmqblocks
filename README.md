gr-zmqblocks GNU Radio module
-----------------------------
Provides additional blocks and Python classes to connect GNU Radio flowgraphs
over a network and to perform remote procedure calls.

Build requirements
------------------
In order to build the gr-zmqblocks module you will need to install ZeroMQ
(http://zeromq.org/) including the C++ headers.

How to build
------------
In the gr-zmqblocks folder do:

    mkdir build
    cd build
    cmake ../
    make

optional:
    make install

How to run example
------------------
In the gr-zmqblocks folder do:

If not installed

    cd examples
    ./run_app.sh server

on another terminal or machine

    ./run_app.sh client -s hostname

If installed just run

    server.py

and

    client.py -s hostname

It is not important if server or client is started first.

Copyright information
------------------
Copyright © 2013 Institute for Theoretical Information Technology,
                 RWTH Aachen University
Johannes Schmitz <schmitz@ti.rwth-aachen.de>

Unless otherwise stated, all files are distributed under GPL v3 license.
