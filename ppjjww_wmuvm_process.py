#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Process (p p > j j w+ w+ , w+ > mu+ vm) specific functions."""
import sys
import log as logging
import util
from parsing import eventlines_to_particlesdict
from loading import LHELoader
from math import *
from variables import *


def name_particles(particles):
    """Adds to particles field 'name' that is constructed as PDG_orderno. 

    For W+ names are w_orderno, for jets j_orderno, 
    for leptons l_orderno, for incoming quarks (substracts) q_orderno.
    """

    w       = {24}
    jet     = {1, -1, 2, -2, 3, -3, 4, -4, 21}
    l       = {13, -13, 11, -11}
    #mET   12 -12 14 -14 16 -16 1000022 # Missing ET class, name is reserved

    particleid2count = {}
    w2count = {}
    jet2count = {}
    l2count = {}
    q2count = {}        

    for particle in particles:
        particleid = particle["id"]
        particlestatus = particle["istatus"]
        particle2count = particleid2count #default counter

        #select special naming for selected particles
        if particlestatus in {1,2}: #products and temporary products
            if particleid in w: 
                particleid = "w"
                particle2count = w2count
            elif particleid in jet:
                particleid = "j"
                particle2count = jet2count
            elif particleid in l:
                particleid = "l"
                particle2count = l2count
        elif particlestatus in {-1} and particleid in jet: #substracts
            particleid = "q"
            particle2count = q2count
        else: print "Warning: giving default name to particle:", particle

        #update proper name and counter
        particle["name"]  = str(particleid)+"_"+str(particle2count.get(particleid, 1))
        particle2count[particleid] = particle2count.get(particleid, 1) + 1
        
    return particles   


def calculate_dependent_variables(particles):
    """Basing on parameteres of particles calculates set of kinematic variables."""
    j1 = particles["j_1"]
    j2 = particles["j_2"]
    l1 = particles["l_1"]
    l2 = particles["l_2"]
    particles = {"j1": j1, "j2": j2, "l1":l1, "l2":l2}

    variables = {}
    update_variables_by_single(variables, particles, momentum, "p")
    update_variables_by_single(variables, particles, pT, "pt")
    update_variables_by_single(variables, particles, pZ, "pz")
    update_variables_by_single(variables, particles, eta, "eta")
    update_variables_by_single(variables, particles, eta_ma, "etama")
    update_variables_by_unordered_pair(variables, particles, invariant_mass, "M_")
    update_variables_by_unordered_pair(variables, particles, delta_phi, "delta_phi_")
    variables["R_pT"] = R_pT_coeff(l1,l2,j1,j2)
    
    #print variables
    return variables

##############################################################################

def is_event_valid(particles, variables):
    """Should the event be kept or not?"""
    p, v = particles, variables #short abbreviations

    return v["M_j1j2"]>500 and \
           v["M_j1l2"]>200 and v["M_j2l1"]>200 and \
           v["delta_phi_l1l2"]>2.5 and \
           v["R_pT"]>3.5  #and \
    #       2<abs(v["etaj1"]) and abs(v["etaj1"])<5 and \
    #       2<abs(v["etaj2"]) and abs(v["etaj2"])<5 and \
    #       abs(v["etaj1"]-v["etaj2"]) > 4 and \
    #       v["etaj1"]*v["etaj2"] < 0 #and \


if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: logging.err("Input file path expected!"); sys.exit(-1)

    lhe = LHELoader(open(inpath))

    logging.info("Loading and parsing events...")
    #events = []
    kept = 0
    for i,eventlines in enumerate(lhe.yield_events()):
        if i%10000==0: logging.dbg("%i events read..." % i)

        particles = eventlines_to_particlesdict(eventlines, \
                        particles_naming_function = name_particles)
        variables = calculate_dependent_variables(particles)

        kept += is_event_valid(particles, variables)

        #events.append(particles)
        #util.print_list(eventlines, "LINES:")
        #util.print_dict(particles, "PARTICLES:")
        #util.print_dict(variables, "VARIABLES:")
        #print "--------------------------------------"

    #print "header =", lhe.header
    #print "footer =", lhe.footer
    logging.info("events_counter = %i" % lhe.events_counter)
    #logging.info("len(events) = %i" % len(events))
    logging.info("number of kept events = %i" % kept)
    #print "events = ", events[:2], "...", events[-1]

