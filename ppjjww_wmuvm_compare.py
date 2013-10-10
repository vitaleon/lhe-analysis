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

##############################################################################


def derive_Rab_fields(storage):
    """Updates DataStorage with R_ab fields."""
    numevents = len(storage.d.itervalues().next())
    for i in xrange(numevents):               
        Rj1j2 = math.sqrt( storage.d["delta_phi_j1j2"][i]**2 + (storage.d["etaj1"][i]-storage.d["etaj2"][i])**2 )
        Rj1l1 = math.sqrt( storage.d["delta_phi_j1l1"][i]**2 + (storage.d["etaj1"][i]-storage.d["etal1"][i])**2 )
        Rj1l2 = math.sqrt( storage.d["delta_phi_j1l2"][i]**2 + (storage.d["etaj1"][i]-storage.d["etal2"][i])**2 )
        Rj2l1 = math.sqrt( storage.d["delta_phi_j2l1"][i]**2 + (storage.d["etaj2"][i]-storage.d["etal1"][i])**2 )
        Rj2l2 = math.sqrt( storage.d["delta_phi_j2l2"][i]**2 + (storage.d["etaj2"][i]-storage.d["etal2"][i])**2 )

        storage.d.setdefault("Rj1j2", list()).append(Rj1j2)            
        storage.d.setdefault("Rj1l1", list()).append(Rj1l1)
        storage.d.setdefault("Rj1l2", list()).append(Rj1l2)    
        storage.d.setdefault("Rj2l1", list()).append(Rj2l1)    
        storage.d.setdefault("Rj2l2", list()).append(Rj2l2)        
    return storage    

def derive_additional_fields(storage):
    """Updates DataStorage with additional fields."""
    storage.d["ptl1_ptl2"] = analysis.multiply(storage.d["ptl1"], storage.d["ptl2"])
    storage.d["ptj1_ptj2"] = analysis.multiply(storage.d["ptj1"], storage.d["ptj2"])
    derive_Rab_fields(storage)
    return storage

##############################################################################



def setI_criteria(v):
    """Should the event be kept or not?"""
    return  v["M_j1l2"]>200 and v["M_j2l1"]>200 and \
            v["M_j1j2"]>400 and \
            v["Rj1l1"]>0.4 and v["Rj1l2"]>0.4 and v["Rj2l1"]>0.4 and v["Rj2l2"]>0.4 and \
            v["ptl1"]>40 and v["ptl2"]>40 and \
            abs(v["etal1"])<1.5 and abs(v["etal2"])<1.5 and \
            v["delta_phi_l1l2"]>2.5 and \
            v["M_l1l2"]>200



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





##############################################################################



def _calc_max_val_(values):
    maxvalue = ufraction(values, 0.99)
    if maxvalue < 100:  maxvalue = max(values)
    if maxvalue>100000: maxvalue = math.ceil(maxvalue/100000.0)*100000.0
    if maxvalue>10000:  maxvalue = math.ceil(maxvalue/10000.0)*10000.0
    elif maxvalue>1000: maxvalue = math.ceil(maxvalue/1000.0)*1000.0 
    elif maxvalue>100:  maxvalue = math.ceil(maxvalue/100.0)*100.0 
    else: maxvalue = math.ceil(maxvalue) 
    return maxvalue


def _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, varname, varlabel):


    maxvalue = max([ _calc_max_val_(bg.d[varname]), _calc_max_val_(fg.d[varname]),
                     _calc_max_val_(bgI.d[varname]), _calc_max_val_(fgI.d[varname]),
                     _calc_max_val_(bgII.d[varname]), _calc_max_val_(fgII.d[varname]) ])
    logging.info("plotting for %s with label=%s maxval=%f" % (varname,varlabel,maxvalue) )


    #M_ll ANALYSIS:
    analysis.plot_signal_background(x=bg.d[varname], wx=bg.w, \
                                    y=fg.d[varname], wy=fg.w, \
                                    numbins=100, xmax=maxvalue, variable=varlabel,
                                    title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                            "]\nBackground = $\sigma$["+labelbg+"]") 
    pyplot.savefig(pathfg+"."+varname+".SIGNAL.png")   

    #analysis.plot_compare2(x=bg.d[varname], wx=bg.w, \
    #                       y=fg.d[varname], wy=fg.w, \
    #                       numbins=100, xmax=maxvalue, variable=varlabel,
    #                        title="Foreground = $\sigma$["+labelfg+
    #                               "]\nBackground = $\sigma$["+labelbg+"]")    
    #pyplot.savefig(pathfg+"."+varname+".FG.png")   



    #M_ll set I ANALYSIS:
    analysis.plot_signal_background(x=bgI.d[varname], wx=bgI.w, \
                                    y=fgI.d[varname], wy=fgI.w, \
                                    numbins=100, xmax=maxvalue, variable=varlabel,
                                    title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                            "]\nBackground = $\sigma$["+labelbg+"] (set I cuts)")
    ylim1 = pyplot.ylim()
    pyplot.savefig(pathfg+".setI."+varname+".SIGNAL.png")   

    #analysis.plot_compare2(x=bgI.d[varname], wx=bgI.w, \
    #                       y=fgI.d[varname], wy=fgI.w, \
    #                       numbins=100, xmax=maxvalue, variable=varlabel,
    #                        title="Foreground = $\sigma$["+labelfg+
    #                               "]\nBackground = $\sigma$["+labelbg+"] (set I cuts)")    
    #ylim2 = pyplot.ylim()
    #pyplot.savefig(pathfg+".setI."+varname+".FG.png")  



    #M_ll set II ANALYSIS:
    analysis.plot_signal_background(x=bgII.d[varname], wx=bgII.w, \
                                    y=fgII.d[varname], wy=fgII.w, \
                                    numbins=100, xmax=maxvalue, variable=varlabel,
                                    title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                            "]\nBackground = $\sigma$["+labelbg+"] (set II cuts)") 
    pyplot.ylim(ylim1) 
    pyplot.savefig(pathfg+".setII."+varname+".SIGNAL.png")   

    #analysis.plot_compare2(x=bgII.d[varname], wx=bgII.w, \
    #                       y=fgII.d[varname], wy=fgII.w, \
    #                       numbins=100, xmax=maxvalue, variable=varlabel,
    #                        title="Foreground = $\sigma$["+labelfg+
    #                               "]\nBackground = $\sigma$["+labelbg+"] (set II cuts)")    
    #pyplot.ylim(ylim2) 
    #pyplot.savefig(pathfg+".setII."+varname+".FG.png")   



if __name__=="__main__":

#sample use
#python ppjjww_wmuvm_compare.py 
# /media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c10_genok.csv 0.4233 "\$M_H=126 GeV$, $\alpha=1.0MS$" 
# /media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c07_genok.csv 0.5133 "\$M_H=126 GeV$, $\alpha=0.7MS$"

    try: pathbg = sys.argv[1]
    except: logging.err("First bg CSV file path expected!"); sys.exit(-1)
    logging.info("pathbg = %s" % pathbg)

    try: crossxbg = float(sys.argv[2])
    except: logging.err("Give bg dataset crosssection [fb] !"); sys.exit(-1)
    logging.info("crossxbg = %f" % crossxbg)

    try: labelbg = sys.argv[3]
    except: logging.err("Give bg label !"); sys.exit(-1)
    logging.info("labelbg = %s" % labelbg)

    try: pathfg = sys.argv[4]
    except: logging.err("Second fg CSV file path expected!"); sys.exit(-1)
    logging.info("pathfg = %s" % pathfg)

    try: crossxfg = float(sys.argv[5])
    except: logging.err("Give fg dataset crosssection [fb] !"); sys.exit(-1)
    logging.info("crossxfg = %f" % crossxfg)

    try: labelfg = sys.argv[6]
    except: logging.err("Give fg label !"); sys.exit(-1)
    logging.info("labelfg = %s" % labelfg)

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

    logging.info("R_pT plots")
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
    #pyplot.savefig(pathfg+".RpT.FG.png")

    im3 = analysis.plot_given_hist2d(xedges1, yedges1, H2-H1, \
                                     xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", \
                                     ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", \
                                     title="Signal [pb/bin]\n$\sigma$["+labelfg+"] - $\sigma$["+labelbg+"]")
    pyplot.savefig(pathfg+".RpT.SIGNAL.png")

    ##############################################################################

    logging.info("single variables plots")

    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "M_j1l2", "$M_{j_1l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "M_j2l1", "$M_{j_2l_1}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "M_j1j2", "$M_{j_1j_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "Rj1l1", "$d_{j_1l_1}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "Rj1l2", "$d_{j_1l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "Rj2l1", "$d_{j_2l_1}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "Rj2l2", "$d_{j_2l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "ptl1", "$p_T^{l_1}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "ptl2", "$p_T^{l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "etal1", "$\eta_{l_1}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "etal2", "$\eta_{l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "delta_phi_l1l2", "$\Delta\phi_{l_1l_2}$")
    _store_single_variable_plots_(bg, bgI, bgII,  pathbg, labelbg, fg, fgI, fgII,  pathfg, labelfg, "M_l1l2", "$M_{l_1l_2}$")

