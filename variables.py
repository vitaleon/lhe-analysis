#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Particles' kinematic variables calculation."""
from math import *
import itertools

def invariant_mass(j1,j2):
    M_jj = sqrt( -(j1["p1"]+j2["p1"])**2 -(j1["p2"]+j2["p2"])**2 -(j1["p3"]+j2["p3"])**2 +(j1["p4"]+j2["p4"])**2 )
    return M_jj

def delta_phi(l1,l2):
    phi_l1 = atan2(l1["p2"], l1["p1"])
    phi_l2 = atan2(l2["p2"], l2["p1"])    
    delta_phi_ll = min(abs(phi_l1-phi_l2), 2*pi - abs(phi_l2-phi_l1))
    return delta_phi_ll

def momentum(j1):
    """Total momentum: p=sqrt(p(1,i)**2+p(2,i)**2+p(3,i)**2)."""
    return sqrt( j1["p1"]**2 + j1["p2"]**2 + j1["p3"]**2  )

def pT(j1):
    """Transversal momentum: pT=sqrt(p(1,i)**2+p(2,i)**2)."""
    ptj1 = sqrt( j1["p1"]**2 + j1["p2"]**2 )
    return ptj1

def pZ(p):
    return p["p3"]

def eta(j1):
    """etaj1 = -log((1.-cosa)/sina) where cosa=p(3,i)/pj1, sina=ptj1/pj1 """
    pj1 = momentum(j1)
    ptj1 = pT(j1)

    cosaj1 = (j1["p3"])/pj1 
    sinaj1 = ptj1/pj1
    etaj1 = -log( (1.0-cosaj1) / sinaj1 )
    return etaj1

def eta_ma(j1):
    pj1 = momentum(j1)
    ptj1 = pT(j1)

    cosaj1 = abs(j1["p3"])/pj1 #abs() for MadAnalysis compatibility
    sinaj1 = ptj1/pj1
    etaj1 = -log( (1.0-cosaj1) / sinaj1 )
    return etaj1


def R_pT_coeff(l1,l2,j1,j2):
    """R_pT = (pT_l1 pT_l2) / (pT_j1 pT_j2)"""
    R_pT = float(pT(l1) * pT(l2)) / float(pT(j1) * pT(j2))
    return R_pT


######################################################################################


def update_variables_by_single(variables, particles, variable_func, variable_prefix, sep=""):
    for particle_name, particle in particles.iteritems():
        variable_name = variable_prefix+sep+particle_name
        variables[variable_name] = variable_func(particle)

def update_variables_by_unordered_pair(variables, particles, variable_func, variable_prefix, sep=""):
    particles_list = sorted(list(particles.iteritems()))
    for (p1_name,p1), (p2_name,p2) in itertools.combinations(particles_list, 2):
        variable_name = variable_prefix+sep+p1_name+sep+p2_name
        variables[variable_name] = variable_func(p1, p2)
        

