#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Loads CSV files with (p p > j j w+ w+ , w+ > mu+ vm) events and does several plots and analysis."""

import sys
import os
from csv_loader import load_float
import log as logging
from util import *

import random
import numpy as np
import matplotlib
from matplotlib import pyplot
import math
import analysis  
from ppjjww_wmuvm_compare import derive_additional_fields, setII_criteria, _calc_max_val_

import pickle



def _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,\
          pathfg, labelfg, varname, varlabel, maxvalue=None, minvalue=None, nbins=100, ymax1=None, ymax2=None, ylab=""):

    
    if maxvalue is None:
        maxvalue = max([ _calc_max_val_(bg.d[varname]), _calc_max_val_(fg.d[varname]),
                         _calc_max_val_(bgI.d[varname]), _calc_max_val_(fgI.d[varname]),
                         _calc_max_val_(bgII.d[varname]), _calc_max_val_(fgII.d[varname]) ])
        logging.info("plotting for %s with label=%s maxval=%f" % (varname,varlabel,maxvalue) )


    #M_ll ANALYSIS:
    analysis.plot_signal_background(x=bg.d[varname], wx=bg.w, \
                                    y=fg.d[varname], wy=fg.w, \
                                    numbins=nbins, xmax=maxvalue, xmin=minvalue, ymax=ymax1, variable=varlabel,
                                    title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                            "]\nBackground = $\sigma$["+labelbg+"]",
                                    ylabel  = ylab) 
    pyplot.savefig(pathfg+"_"+varname+"_SIGNAL.png")   


    #M_ll set II ANALYSIS:
    analysis.plot_signal_background(x=bgII.d[varname], wx=bgII.w, \
                                    y=fgII.d[varname], wy=fgII.w, \
                                    numbins=nbins, xmax=maxvalue, xmin=minvalue, ymax=ymax2, variable=varlabel,
                                    title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+
                                            "]\nBackground = $\sigma$["+labelbg+"] (set II cuts)",
                                    ylabel  = ylab) 
    #pyplot.ylim(ylim1) 
    pyplot.savefig(pathfg+"_setII_"+varname+"_SIGNAL.png")   


#setup
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams.update({'figure.autolayout': True})
logging.set_output_level(1)

#backgorund
pathbg = '/media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c10_genok_2merge.csv'
crossxbg = 0.429258 * 300 #normalization to 300 fb^-1
labelbg = "$g=g_{MS}$" 

#foregrounds:
srcs = ['ppjjww_muvm_h126c07_genok_2merge.csv', 'ppjjww_muvm_h1e10_genok.csv','ppjjww_muvm_h126c05_genok.csv','ppjjww_muvm_h126c09_genok.csv','ppjjww_muvm_h126c08_genok.csv','ppjjww_muvm_h126c06_genok.csv']
cxs = [0.496492, 0.5604, 0.4956, 0.444,0.4573,0.4559]
labels = ["$g=0.7g_{MS}$", "$g=0$", "$g=0.5g_{MS}$", "$g=0.9g_{MS}$", "$g=0.8g_{MS}$", "$g=0.6g_{MS}$", ]
#srcs = ['ppjjww_muvm_h126c07_genok_2merge.csv']
#cxs = [0.496492]
#labels = ["$g=0.7g_{MS}$"]

#load background
bg = analysis.DataStorage(open(pathbg), crossxbg)
bg = derive_additional_fields(bg)

#loop over foregrounds:
for suffix,crossxfg,labelfg in zip(srcs,cxs,labels):

    #load foreground
    pathfg = '/media/Dane/PROJEKTY/lic/data/'+suffix
    crossxfg = crossxfg * 300 #normalization to 300 fb^-1

    fg = analysis.DataStorage(open(pathfg), crossxfg)
    fg = derive_additional_fields(fg)

    logging.info("Applying (set II) cuts ...")
    bgII = analysis.data_filter(bg, critera = setII_criteria)
    fgII = analysis.data_filter(fg, critera = setII_criteria)
     

    ##############################################################################

    bins_shape = [8,20]

    logging.info("R_pT plots")
    im1, H1, xedges1, yedges1 = analysis.plot_hist2d(x=bg.d["ptl1_ptl2"], y=bg.d["ptj1_ptj2"], w1=bg.w, \
                                                     xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                     ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                     title="Background = $\sigma$["+labelbg+"]\n[events/bin], bin=$10^3$ x $10^3$", 
                                                     numbins=bins_shape)
    #pyplot.savefig(pathbg+"_RpT_BG.png")
    pickle.dump(H1, open(pathbg+"_RpT_BG.pickle", "wb") )
    pickle.dump(xedges1, open(pathbg+"_RpT_BG.xedges.pickle", "wb") )
    pickle.dump(yedges1, open(pathbg+"_RpT_BG.yedges.pickle", "wb") )

    im2, H2, xedges2, yedges2 = analysis.plot_hist2d(x=fg.d["ptl1_ptl2"], y=fg.d["ptj1_ptj2"], w1=fg.w, \
                                                     xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                     ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                     title="Foreground = $\sigma$["+labelfg+"]\n[events/bin], bin=$10^3$ x $10^3$", 
                                                     numbins=bins_shape, clim=im1.get_clim())
    #pyplot.savefig(pathfg+".RpT.FG.png")
    #pickle.dump(H2, open(pathfg+"_RpT_FG.pickle", "wb") )

    im3 = analysis.plot_given_hist2d(xedges1, yedges1, H2-H1, \
                                     xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", \
                                     ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", \
                                     title="Signal = $\sigma$["+labelfg+"] - $\sigma$["+labelbg+"]\n[events/bin], bin=$10^3$ x $10^3$")
    #pyplot.savefig(pathfg+"_RpT_SIGNAL.png")
    pickle.dump((H2-H1), open(pathfg+"_RpT_SIGNAL.pickle", "wb") )

    ##############################################################################

    continue
    logging.info("single variables plots")
    

    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "etal1", "$\eta_{l_1}$", nbins=29, maxvalue=3, ylab="events/bin, bin=0.2", minvalue=-3)
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "etal2", "$\eta_{l_2}$", nbins=29, maxvalue=3, ylab="events/bin, bin=0.2", minvalue=-3)
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "etaj1", "$\eta_{j_1}$", nbins=29, maxvalue=6, ylab="events/bin, bin=0.2", minvalue=-6)
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "etaj2", "$\eta_{j_2}$", nbins=29, maxvalue=6, ylab="events/bin, bin=0.2", minvalue=-6)
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "ptl1", "$p_T^{l_1}$  $[GeV]$", nbins=31, maxvalue=600, ylab="events/bin, bin=20")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "ptl2", "$p_T^{l_2}$  $[GeV]$", nbins=31, maxvalue=600, ylab="events/bin, bin=20")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "Rj1j2", "$\Delta R_{j_1j_2}$", maxvalue=16, nbins=41, ylab="events/bin, bin=0.2")



    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "M_j1l2", "$M_{j_1l_2}$ $[GeV]$", maxvalue=3000, nbins=31, ylab="events/bin, bin=100")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "M_j2l1", "$M_{j_2l_1}$ $[GeV]$", maxvalue=3000, nbins=31, ylab="events/bin, bin=100")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "M_j1j2", "$M_{j_1j_2}$ $[GeV]$", maxvalue=6000, nbins=31, ylab="events/bin, bin=200")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "delta_phi_l1l2", "$\Delta\phi_{l_1l_2}$", maxvalue=4.0, nbins=41, ylab="events/bin, bin=0.1")

    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "M_l1l2", "$M_{l_1l_2}$  $[GeV]$", maxvalue=3000, nbins=31, ylab="events/bin, bin=100", ymax2=5.0)
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "Rj1l1", "$\Delta R_{j_1l_1}$", maxvalue=8, nbins=41, ylab="events/bin, bin=0.2")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "Rj1l2", "$\Delta R_{j_1l_2}$", maxvalue=8, nbins=41, ylab="events/bin, bin=0.2")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "Rj2l1", "$\Delta R_{j_2l_1}$", maxvalue=8, nbins=41, ylab="events/bin, bin=0.2")
    _store_single_variable_plots_(bg, bgII,  pathbg, labelbg, fg, fgII,  pathfg, labelfg, "Rj2l2", "$\Delta R_{j_2l_2}$", maxvalue=8, nbins=41, ylab="events/bin, bin=0.2")

    ##############################################################################

