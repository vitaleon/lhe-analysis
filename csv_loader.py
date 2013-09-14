#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import itertools
import log as logging
from util import *

def load_float(f, sep=","):
    header = list(p.strip() for p in f.readline().split(sep))
    values = list(list() for e in header)
    for i,line in enumerate(f.xreadlines()):
        if i%10000==0: logging.dbg("%i read..." % i)
        for column,p in enumerate(line.split(sep)):
            values[column].append( float(p) )
    logging.info("%i read..." % (i+1))
    return dict( itertools.izip(header, values) )
                



if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: logging.err("Input CSV file path expected!"); sys.exit(-1)

    d1 = load_float(open(inpath))
    print_dict_of_lists(d1, header="CSV content:")
