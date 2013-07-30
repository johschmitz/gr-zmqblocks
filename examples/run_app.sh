#!/bin/sh
export LD_LIBRARY_PATH="$PWD/../build/lib"
export PYTHONPATH="$PWD/../build/swig:$PWD/../python"
/usr/bin/python $1
