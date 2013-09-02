#!/usr/bin/python
# -*- coding: utf-8 -*-

import inspect
import sys

output_level = 0

def dbg(txt):
    if output_level <= 0:
        print "[DBG][",inspect.stack()[1][3],"]",txt

def info(txt):
    if output_level <= 1:
        print "[INF][",inspect.stack()[1][3],"]",txt

def warn(txt):
    if output_level <= 2:
        sys.stderr.write( "[WRN]["+str( inspect.stack()[1][3] )+"] "+str(txt)+"\n" )

def err(txt):
    if output_level <= 3:
        sys.stderr.write( "[ERR]["+str( inspect.stack()[1][3] )+"] "+str(txt)+"\n" )

def set_output_level(new_output_level):
    global output_level        
    output_level = new_output_level
