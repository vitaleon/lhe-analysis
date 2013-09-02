#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Process (p p > j j w+ w+ , w+ > mu+ vm) specific functions."""
import sys
import log as logging
import util
from parsing import eventlines_to_particlesdict
from loading import LHELoader
from math import *

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

    #################################################################
    j1 = particles["j_1"]
    j2 = particles["j_2"]
    w1 = particles["w_1"]
    w2 = particles["w_2"]
    l1 = particles["l_1"]
    l2 = particles["l_2"]
    #################################################################

    #TRANSVERSAL MOMENTUM ###########################################
    #ptj1=sqrt(p(1,i)**2+p(2,i)**2)
    ptj1 = sqrt( j1["p1"]**2 + j1["p2"]**2 )
    ptj2 = sqrt( j2["p1"]**2 + j2["p2"]**2 )

    ptw1 = sqrt( w1["p1"]**2 + w1["p2"]**2 )
    ptw2 = sqrt( w2["p1"]**2 + w2["p2"]**2 )

    ptl1 = sqrt( l1["p1"]**2 + l1["p2"]**2 )
    ptl2 = sqrt( l2["p1"]**2 + l2["p2"]**2 )

    #TOTAL MOMENTUM #################################################
    #pj1=sqrt(p(1,i)**2+p(2,i)**2+p(3,i)**2)
    pj1 = sqrt( j1["p1"]**2 + j1["p2"]**2 + j1["p3"]**2  )
    pj2 = sqrt( j2["p1"]**2 + j2["p2"]**2 + j2["p3"]**2  )
    pl1 = sqrt( l1["p1"]**2 + l1["p2"]**2 + l1["p3"]**2  )
    pl2 = sqrt( l2["p1"]**2 + l2["p2"]**2 + l2["p3"]**2  )

    #ANGLE: PHI #####################################################
    phi_l1 = atan2(l1["p2"], l1["p1"])
    phi_l2 = atan2(l2["p2"], l2["p1"])    
    delta_phi_ll = min(abs(phi_l1-phi_l2), 2*pi - abs(phi_l2-phi_l1))

    #INVARIANT MASES ################################################ 
    M_jj   = sqrt( -(j1["p1"]+j2["p1"])**2 -(j1["p2"]+j2["p2"])**2 -(j1["p3"]+j2["p3"])**2 +(j1["p4"]+j2["p4"])**2 )
    M_j1l1 = sqrt( -(j1["p1"]+l1["p1"])**2 -(j1["p2"]+l1["p2"])**2 -(j1["p3"]+l1["p3"])**2 +(j1["p4"]+l1["p4"])**2 ) 
    M_j2l2 = sqrt( -(j2["p1"]+l2["p1"])**2 -(j2["p2"]+l2["p2"])**2 -(j2["p3"]+l2["p3"])**2 +(j2["p4"]+l2["p4"])**2 ) 
    M_j1l2 = sqrt( -(j1["p1"]+l2["p1"])**2 -(j1["p2"]+l2["p2"])**2 -(j1["p3"]+l2["p3"])**2 +(j1["p4"]+l2["p4"])**2 ) 
    M_j2l1 = sqrt( -(l1["p1"]+j2["p1"])**2 -(l1["p2"]+j2["p2"])**2 -(l1["p3"]+j2["p3"])**2 +(l1["p4"]+j2["p4"])**2 )  

    #FUNCTIONS ######################################################
    #R_pT = (pT_l1 pT_l2) / (pT_j1 pT_j2). ?
    R_pT = float(ptl1 * ptl2) / float(ptj1 * ptj2)


    #################################################################

    #cosa=p(3,i)/pj1
    #sina=ptj1/pj1
    #etaj1 = -log((1.-cosaj1)/sinaj1) 
    cosaj1 = (j1["p3"])/pj1 #abs() for MadAnalysis compatibility
    sinaj1 = ptj1/pj1
    etaj1 = -log( (1.0-cosaj1) / sinaj1 )
    #etaj1 = 0.5 * log( float(pj1+j1["p3"])/float(pj1-j1["p3"]) ) 

       
    cosaj2 = (j2["p3"])/pj2 #abs() for MadAnalysis compatibility
    sinaj2 = ptj2/pj2
    etaj2 = -log((1.0-cosaj2)/sinaj2)
    #etaj2 = 0.5 * log( float(pj2+j2["p3"])/float(pj2-j2["p3"]) ) 

    cosal1 = (l1["p3"])/pl1 #abs() for MadAnalysis compatibility
    sinal1 = ptl1/pl1
    etal1 = -log( (1.0-cosal1) / sinal1 )

    cosal2 = (l2["p3"])/pl2 #abs() for MadAnalysis compatibility
    sinal2 = ptl2/pl2
    etal2 = -log( (1.0-cosal2) / sinal2 )


    #################################################################
    variables = {"ptl1":ptl1, "ptl2":ptl2, "M_j1l1":M_j1l1, "M_j2l2":M_j2l2,
                 "ptj1":ptj1, "ptj2":ptj2, "pj1":pj1, "pj2":pj2, 
                 "cosaj1":cosaj1, "cosaj2":cosaj2,
                 "sinaj1":sinaj1, "sinaj2":sinaj2, 
                 "etaj1":etaj1, "etaj2":etaj2, "etal1":etal1, "etal2":etal2,  
                 "R_pT": R_pT, "delta_phi_ll":delta_phi_ll,
                 "M_jj":M_jj, "M_j1l2":M_j1l2, "M_j2l1":M_j2l1 }    
    return variables



def is_event_valid(particles, variables):
    """Should the event be kept?"""
    p, v = particles, variables #short abbreviations

    #print_list( lines, "lines")
    #print_list( particles_list, "particles_list" )
    #print_dict( particles, "particles" )
    #print_dict( variables, "variables" )
    #sys.exit(-1)
    #return True
    #print variables["etaj1"]
    #return variables["etaj1"]>4.0 and variables["etaj1"]<5.0 # and variables["etaj2"]>4.0 and variables["etaj2"]<5.0
    #return variables["ptj1"]>=10.0 and variables["ptj2"]>=7.0 and variables["ptl1"]>=11.0 and variables["ptl2"]>=11.0
    #return variables["M_j2l2"]>=200
    #return variables["ptl2"] >= 14.0
    return variables["etaj1"] >= 3

    #variables = {"ptl1":ptl1, "ptl2":ptl2, "M_j1l1":M_j1l1, "M_j2l2":M_j2l2,
    #            "ptj1":ptj1, "ptj2":ptj2, "pj1":pj1, "pj2":pj2, 
    #             "cosaj1":cosaj1, "cosaj2":cosaj2,
    ##             "sinaj1":sinaj1, "sinaj2":sinaj2, 
    #             "etaj1":etaj1, "etaj2":etaj2, "etal1":etal1, "etal2":etal2,  
    #             "R_pT": R_pT, "delta_phi_ll":delta_phi_ll,
    #             "M_jj":M_jj, "M_j1l2":M_j1l2, "M_j2l1":M_j2l1 } 

    #return 2<abs(v["etaj1"]) and abs(v["etaj1"])<5 and \
    #       2<abs(v["etaj2"]) and abs(v["etaj2"])<5 and \
    #       v["M_j1l2"]>200 and v["M_j2l1"]>200 and \
    #       v["M_jj"]>500 and v["R_pT"]>3.5 and v["delta_phi_ll"]>2.5 \
    #        and abs(v["etaj1"]-v["etaj2"]) > 4


if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: log.err("Input file path expected!"); sys.exit(-1)

    lhe = LHELoader(open(inpath))

    logging.info("Loading and parsing events...")
    events = []
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
    logging.info("len(events) = %i" % len(events))
    logging.info("number of kept events = %i" % kept)
    #print "events = ", events[:2], "...", events[-1]

