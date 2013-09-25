#!/usr/bin/python
# -*- coding: utf-8 -*-

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



#if __name__=="__main__":

#pathbg = '/media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h126c10_genok.csv'
#crossxbg = 0.4233
#pathfg = '/media/Dane/PROJEKTY/lic/data/ppjjww_muvm_h1e10_genok.csv'
#crossxfg = 0.5604

try: pathbg = sys.argv[1]
except: logging.err("First bg CSV file path expected!"); sys.exit(-1)

try: crossxbg = float(sys.argv[2])
except: logging.err("Give bg dataset crosssection [fb] !"); sys.exit(-1)

try: pathfg = sys.argv[3]
except: logging.err("Second fg CSV file path expected!"); sys.exit(-1)

try: crossxfg = float(sys.argv[4])
except: logging.err("Give fg dataset crosssection [fb] !"); sys.exit(-1)

bg = analysis.DataStorage(open(pathbg), crossxbg)
fg = analysis.DataStorage(open(pathfg), crossxfg)

bg = analysis.derive_additional_fields(bg)
fg = analysis.derive_additional_fields(fg)

##############################################################################

print_dict_of_lists(bg.d, header="Bg CSV content:")
print_dict_of_lists(fg.d, header="Fg CSV content:")

#analysis.plot_comparison2(x=bg.d["ptl1_ptl2"], wx=bg.w, \
#                          y=bg.d["ptj1_ptj2"], wy=bg.w, \
#                          numbins=100, xmax=20000)    

numbins = 30
im1, H1, xedges1, yedges1 = analysis.plot_hist2d(x=bg.d["ptl1_ptl2"], y=bg.d["ptj1_ptj2"], w1=bg.w, \
                                                 xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                 ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                 title="Background ($M_H=126 GeV$) [pb/bin]", 
                                                 numbins=numbins)

im2, H2, xedges2, yedges2 = analysis.plot_hist2d(x=fg.d["ptl1_ptl2"], y=fg.d["ptj1_ptj2"], w1=fg.w, \
                                                 xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", xmax=50000, \
                                                 ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", ymax=20000, \
                                                 title="Foreground ($M_H=1e10 GeV$) [pb/bin]", 
                                                 numbins=numbins)

analysis.plot_given_hist2d(xedges1, yedges1, H2-H1, xlab="$p_T^{\mu1}$ $p_T^{\mu2}$ $[GeV^2]$", \
                            ylab="$p_T^{j1}$ $p_T^{j2}$ $[GeV^2]$", title="Signal [pb/bin]")

bgII = analysis.data_filter(bg, critera = analysis.setII_criteria)
fgII = analysis.data_filter(fg, critera = analysis.setII_criteria)

analysis.plot_comparison3(x=bgII.d["M_l1l2"], wx=bgII.w, \
                          y=fgII.d["M_l1l2"], wy=fgII.w, \
                          numbins=100, xmax=2000, variable="$M_{l_1l_2}$")    



