#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Export (p p > j j w+ w+ , w+ > mu+ vm) kinematic variables."""

import sys
import log as logging
import util
from parsing import eventlines_to_particlesdict
from loading import LHELoader
from csv_writer import CSVWriter
from ppjjww_wmuvm_process import *


if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: logging.err("Input LHE file path expected!"); sys.exit(-1)

    try: outpath = sys.argv[2]
    except: logging.err("Output CSV file path expected!"); sys.exit(-1)


    lhe = LHELoader(open(inpath))
    csv = CSVWriter(open(outpath, "w"))

    logging.info("Loading and parsing events...")
    for i,eventlines in enumerate(lhe.yield_events()):
        if i%10000==0: logging.dbg("%i events read..." % i)

        particles = eventlines_to_particlesdict(eventlines, \
                        particles_naming_function = name_particles)
        variables = calculate_dependent_variables(particles)
        csv.write_dict(variables)
      
    logging.info("events_counter = %i" % lhe.events_counter)




