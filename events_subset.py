#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Reads LHE file and kepts some subset of events."""
import sys
import log as logging
import util
from parsing import eventlines_to_particlesdict
from loading import LHELoader
from math import *
from variables import *






if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: logging.err("Input file path expected!"); sys.exit(-1)

    try: outpath = sys.argv[2]
    except: print "Output file path expected!"; sys.exit(-1)

    try: fraction = float(sys.argv[3])
    except: print "Fraction of events to be kept expected!"; sys.exit(-1)
    

    logging.info("Opening streams...")
    lhe = LHELoader(open(inpath))
    if outpath == "stdout": outfile = sys.stdout
    else: outfile = open(outpath, "w")

    logging.info("Loading header...")
    header = lhe.load_header()
    outfile.writelines(header)

    logging.info("Loading and parsing events...")
    counter = 0
    kept = 0
    for i,eventlines in enumerate(lhe.yield_events()):
        if i%10000==0: logging.dbg("%i events read..." % i)
        counter += fraction
        if counter > 1.0:
            counter -= 1.0
            outfile.writelines(eventlines)
            kept += 1

    logging.info("Writting footer...")
    outfile.writelines(lhe.footer)

    logging.info("events_counter = %i" % lhe.events_counter)
    logging.info("number of kept events = %i" % kept)

