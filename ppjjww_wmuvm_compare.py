#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Loads two CSV files with (p p > j j w+ w+ , w+ > mu+ vm) events and does several plots and analysis."""

import sys
import os
from csv_loader import load_float
import log as logging
from util import *

import random
import numpy as np
from matplotlib import pyplot
import math

import analysis  


def derive_additional_fields(storage):
    """Updates DataStorage with additional fields."""
    storage.d["ptl1_ptl2"] = analysis.multiply(storage.d["ptl1"], storage.d["ptl2"])
    storage.d["ptj1_ptj2"] = analysis.multiply(storage.d["ptj1"], storage.d["ptj2"])
    return storage

def setII_criteria(v):
    """Should the event be kept or not?"""
    return v["M_j1j2"]>500 and \
           v["M_j1l2"]>200 and v["M_j2l1"]>200 and \
           v["delta_phi_l1l2"]>2.5 and \
           v["R_pT"]>3.5  #and \
    #       2<abs(v["etaj1"]) and abs(v["etaj1"])<5 and \
    #       2<abs(v["etaj2"]) and abs(v["etaj2"])<5 and \
    #       abs(v["etaj1"]-v["etaj2"]) > 4 and \
    #       v["etaj1"]*v["etaj2"] < 0 #and \


def setI_criteria(v):
    """Should the event be kept or not?"""
    #TODO: czy v["delta_phi_j1l1"] jest ok??
    Rj1l1 = math.sqrt( v["delta_phi_j1l1"]**2 + (v["etaj1"]-v["etal1"])**2 )
    Rj1l2 = math.sqrt( v["delta_phi_j1l2"]**2 + (v["etaj1"]-v["etal2"])**2 )
    Rj2l1 = math.sqrt( v["delta_phi_j2l1"]**2 + (v["etaj2"]-v["etal1"])**2 )
    Rj2l2 = math.sqrt( v["delta_phi_j2l2"]**2 + (v["etaj2"]-v["etal2"])**2 )

    return  v["M_j1l2"]>200 and v["M_j2l1"]>200 and \
            v["M_j1j2"]>400 and \
            Rj1l1>0.4 and Rj1l2>0.4 and Rj2l1>0.4 and Rj2l2>0.4 and \
            v["ptl1"]>40 and v["ptl2"]>40 and \
            abs(v["etal1"])<1.5 and abs(v["etal2"])<1.5 and \
            v["delta_phi_l1l2"]>2.5 and \
            v["M_l1l2"]>200

#if __name__=="__main__":


if len(sys.argv) > 1 and sys.argv[1] == "test":
    pathbg = '/media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c10_genok.csv'
    crossxbg = 0.4233
    labelbg = "$M_H=126 GeV$, $\\alpha=1.0MS$"
    pathfg = '/media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h1e10_genok.csv'
    crossxfg = 0.5604
    labelfg = "$M_H=10^{10} GeV$, $\\alpha=1.0MS$"
else:
#python ppjjww_wmuvm_compare.py 
# /media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c10_genok.csv 0.4233 "$M_H=126 GeV$, $\alpha=1.0MS$" 
# /media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c07_genok.csv 0.5133 "$M_H=126 GeV$, $\alpha=0.7MS$"

    try: pathbg = sys.argv[1]
    except: logging.err("First bg CSV file path expected!"); sys.exit(-1)

    try: crossxbg = float(sys.argv[2])
    except: logging.err("Give bg dataset crosssection [fb] !"); sys.exit(-1)

    try: labelbg = sys.argv[3]
    except: logging.err("Give bg label !"); sys.exit(-1)

    try: pathfg = sys.argv[4]
    except: logging.err("Second fg CSV file path expected!"); sys.exit(-1)

    try: crossxfg = float(sys.argv[5])
    except: logging.err("Give fg dataset crosssection [fb] !"); sys.exit(-1)

    try: labelfg = sys.argv[6]
    except: logging.err("Give fg label !"); sys.exit(-1)

logging.set_output_level(1)

##############################################################################

bg = analysis.DataStorage(open(pathbg), crossxbg)
fg = analysis.DataStorage(open(pathfg), crossxfg)

#print_dict_of_lists(bg.d, header="Bg CSV content:")
#print_dict_of_lists(fg.d, header="Fg CSV content:")


bg = derive_additional_fields(bg)
fg = derive_additional_fields(fg)

logging.info("Applying (set I) cuts ...")
bgI = analysis.data_filter(bg, critera = setI_criteria)
fgI = analysis.data_filter(fg, critera = setI_criteria)

logging.info("Applying (set II) cuts ...")
bgII = analysis.data_filter(bg, critera = setII_criteria)
fgII = analysis.data_filter(fg, critera = setII_criteria)
 
##############################################################################

#R_pT ANALYSIS:
numbins = 40
im1, H1, xedges1, yedges1 = analysis.plot_hist2d(x=bg.d["ptl1_ptl2"], y=bg.d["ptj1_ptj2"], w1=bg.w, \
                                                 xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                 ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                 title="Background [pb/bin]\n$\sigma$["+labelbg+"]", 
                                                 numbins=numbins)
pyplot.savefig(pathbg+".RpT.BG.png")

im2, H2, xedges2, yedges2 = analysis.plot_hist2d(x=fg.d["ptl1_ptl2"], y=fg.d["ptj1_ptj2"], w1=fg.w, \
                                                 xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                 ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                 title="Foreground [pb/bin]\n$\sigma$["+labelfg+"]", 
                                                 numbins=numbins, clim=im1.get_clim())
pyplot.savefig(pathfg+".RpT.FG.png")

im3 = analysis.plot_given_hist2d(xedges1, yedges1, H2-H1, \
                                 xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", \
                                 ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", \
                                 title="Signal [pb/bin]\n$\sigma$["+labelfg+"] - $\sigma$["+labelbg+"]")
pyplot.savefig(pathfg+".RpT.SIGNAL.png")

#M_ll ANALYSIS:
analysis.plot_signal_background(x=bg.d["M_l1l2"], wx=bg.w, \
                                y=fg.d["M_l1l2"], wy=fg.w, \
                                numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                                title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                        "]\nBackground = $\sigma$["+labelbg+"]") 
pyplot.savefig(pathfg+".Mll.SIGNAL.png")   

analysis.plot_compare2(x=bg.d["M_l1l2"], wx=bg.w, \
                       y=fg.d["M_l1l2"], wy=fg.w, \
                       numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                        title="Foreground = $\sigma$["+labelfg+
                               "]\nBackground = $\sigma$["+labelbg+"]")    
ylim1 = pyplot.ylim()
pyplot.savefig(pathfg+".Mll.FG.png")   



#M_ll set I ANALYSIS:
analysis.plot_signal_background(x=bgI.d["M_l1l2"], wx=bgI.w, \
                                y=fgI.d["M_l1l2"], wy=fgI.w, \
                                numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                                title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                        "]\nBackground = $\sigma$["+labelbg+"] (set I cuts)")
pyplot.savefig(pathfg+".setI.Mll.SIGNAL.png")   

analysis.plot_compare2(x=bgI.d["M_l1l2"], wx=bgI.w, \
                       y=fgI.d["M_l1l2"], wy=fgI.w, \
                       numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                        title="Foreground = $\sigma$["+labelfg+
                               "]\nBackground = $\sigma$["+labelbg+"] (set I cuts)")    
ylim2 = pyplot.ylim()
pyplot.savefig(pathfg+".setI.Mll.FG.png")  



#M_ll set II ANALYSIS:
analysis.plot_signal_background(x=bgII.d["M_l1l2"], wx=bgII.w, \
                                y=fgII.d["M_l1l2"], wy=fgII.w, \
                                numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                                title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                        "]\nBackground = $\sigma$["+labelbg+"] (set II cuts)") 
pyplot.ylim(ylim1) 
pyplot.savefig(pathfg+".setII.Mll.SIGNAL.png")   



analysis.plot_compare2(x=bgII.d["M_l1l2"], wx=bgII.w, \
                       y=fgII.d["M_l1l2"], wy=fgII.w, \
                       numbins=100, xmax=2000, variable="$M_{l_1l_2}$",
                        title="Foreground = $\sigma$["+labelfg+
                               "]\nBackground = $\sigma$["+labelbg+"] (set II cuts)")    
pyplot.ylim(ylim2) 
pyplot.savefig(pathfg+".setII.Mll.FG.png")   





