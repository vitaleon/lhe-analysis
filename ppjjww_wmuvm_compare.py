#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from csv_loader import load_float
import log as logging
from util import *

import random
import numpy
from matplotlib import pyplot
import math

def p99(values):
    return sorted(values)[int(math.floor(len(values)*0.99))]
    
def plot_comparison(v1, v2):
    pyplot.hist(v1, histtype="step", bins=100)
    pyplot.hist(v2, histtype="step", bins=100, range=[0,p99(v1)])
    pyplot.show()



if __name__=="__main__":

    try: inpath1 = sys.argv[1]
    except: logging.err("First input CSV file path expected!"); sys.exit(-1)

    try: scale1 = float(sys.argv[2])
    except: logging.err("Give first dataset crosssection !"); sys.exit(-1)

    try: inpath2 = sys.argv[3]
    except: logging.err("Second input CSV file path expected!"); sys.exit(-1)

    try: scale2 = float(sys.argv[4])
    except: logging.err("Give second dataset crosssection !"); sys.exit(-1)

    logging.info("Loading %s..." % inpath1)
    d1 = load_float(open(inpath1))
    logging.info("Loading %s..." % inpath2)
    d2 = load_float(open(inpath2))

    print_dict_of_lists(d1, header="CSV 1 content:")
    print_dict_of_lists(d2, header="CSV 2 content:")


