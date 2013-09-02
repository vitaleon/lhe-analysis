#!/usr/bin/python
# -*- coding: utf-8 -*-
"""LHE events parsing."""
import log
import sys
import util
from loading import LHELoader
from math import *

def parse_event_header(line):
    """Returns dictionary with information of event's header."""
    #read(5,*)npart,icrap,crap1,crap2,crap3,crap4
    parts = line.strip().split()
    header = {}

    header["npart"] = int(parts[0])
    if header["npart"] > 20: 
        log.warn('Warning: npart = %s!' % str(header["npart"]) )
    #   if(npart.gt.20)then
    #    print*,'Warning: npart =',npart,', stop execution'
    #    stop
    #   endif
    
    return header


def parse_particle_line(line):
    """Extracts information about single particle."""
    #particle fields:    
    #IDUP(I) ISTUP(I) MOTHUP(1,I) MOTHUP(2,I) ICOLUP(1,I)
    #ICOLUP(2,I) PUP(1,I) PUP(2,I) PUP(3,I) PUP(4,I) PUP(5,I)
    #VTIMUP(I) SPINUP(I)
    #
    #fortran code:
    # read(5,'(4x,6i5,5e19.11,f3.0,f4.0)')id(i),istatus(i),
    # &  imother1(i),imother2(i),icrap1(i),icrap2(i),
    # &  (p(j,i),j=1,5),crap5(i),hel(i)
    #
    #fields' descriptions:
    # (IDUP, using the standard PDG numbering [2]), status
    #(ISTUP), mother(s) (MOTHUP), colours(s) (ICOLUP), four-momentum and mass
    #(PUP), proper lifetime (VTIMUP) and spin (SPINUP). In addition the event 
    #as a whole is characterized by the an event weight (XWGTUP), 
    #a scale (SCALUP), and the (AQEDUP) and αs (AQCDUP) values used.
    #
    #sample row:
    #2 -1  0  0  502  0  0.0E+00  0.0E+00  0.31E+04  0.31E+04  0.00E+00 0. -1.

    parts = line.strip().split()
    particle = {}

    particle["id"]        = int(parts[0])
    particle["istatus"]   = int(parts[1])
    particle["imother1"]  = int(parts[2])  
    particle["imother2"]  = int(parts[3])  
    particle["icolup1"]   = int(parts[4])
    particle["icolup2"]   = int(parts[5])
    particle["p1"]        = float(parts[6])
    particle["p2"]        = float(parts[7])
    particle["p3"]        = float(parts[8])
    particle["p4"]        = float(parts[9])
    particle["p5"]        = float(parts[10])
    particle["vtimup"]    = float(parts[11])
    particle["spinup"]    = float(parts[12])

    return particle


def sort_particles_with_decreasing_pt(particles):
    """Returns list of particles sorted according to pT (transversional momentum)."""
    for particle in particles:
        particle["pt"] = sqrt( particle["p1"]**2 + particle["p2"]**2 )

    particles = sorted(particles, key = lambda p: p["pt"], reverse = True)

    return particles


def parse_event(lines):
    """Takes event lines from LHE file and returns list of particles."""
    header = parse_event_header(lines[1])   
    if header["npart"] != len(lines)-3: 
        log.warn("Warning: Number of particles=%i and \
                  number of lines=%i don't agree!" %
                   (header["npart"], len(lines)) )

    return list( parse_particle_line(line) for line in lines[2:-1] )


def particles_pdg_naming(particles):
    """Adds to each of particles from list field 'name' 
        that is constructed as PDG_orderno. """
    particleid2count = {}      
    for particle in particles:
        particleid = particle["id"]
        particlestatus = particle["istatus"]    

        #update name and counter
        particle["name"]  = str(particleid)+"_"+str(particleid2count.get(particleid, 1))
        particleid2count[particleid] = particleid2count.get(particleid, 1) + 1
        
    return particles   


def particles_list_to_dictionary(particles_list, \
        particles_naming_function = particles_pdg_naming):
    """Converts list of particles to dictionary {particle_name: particle}."""
    particles_list  = sort_particles_with_decreasing_pt(particles_list)
    return dict( (particle["name"],particle) for particle in particles_naming_function(particles_list) )


def eventlines_to_particlesdict(lines, \
        particles_naming_function = particles_pdg_naming):
    """Takes event lines from LHE file and returns dictionary
        of particles {particle_name: particle}.
    """
    particles_list = parse_event(lines)    
    particles_dict = particles_list_to_dictionary(particles_list,\
                         particles_naming_function)
    return particles_dict


if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: print "Input file path expected!"; sys.exit(-1)

    lhe = LHELoader(open(inpath))
    for eventlines in lhe.yield_events():
        particles = eventlines_to_particlesdict(eventlines)
        util.print_list(eventlines, "LINES:")
        util.print_dict(particles, "PARTICLES:")
        print "--------------------------------------"
    print "header =", lhe.header
    print "footer =", lhe.footer
    print "events_counter =", lhe.events_counter
    print "len(events) =", len(events)
    print "events = ", events[:2], "...", events[-1]

    
