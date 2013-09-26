#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Analysis and visualisation of different kinematic variables."""

import sys
import os
from csv_loader import load_float
import log as logging
from util import *


import random
import numpy as np
from matplotlib import pyplot
import pylab 
import math

##############################################################################

class DataStorage:
    """Stores events from CSV-data file."""

    def __init__(self, infile=None, crossx=None):
        """infile = source CSV file with events
           crossx - initial cross section [fb]"""
        if infile is None:
            self.d = {}
            self.w = 0.0
            return
        logging.info("Loading data from = %s..." % str(infile))
        self.d = load_float(infile)
        n1 = len(self.d.itervalues().next())
        self.w = crossx / n1 * 1000.0 #calculate weight in pb
        logging.info(" %i elements of weight %f pb (total=%f fb), %i columns loaded" 
                     % (n1,self.w,crossx,len(self.d)) )


def data_filter(storage, critera = lambda dictionary_of_variables: True):
    """Returns DataStorage that contains only these events that are accepted by critera.

    critera - function that takes dict{kinematic-variable-name: value} and returns True/False
    """
    out = DataStorage()
    out.w = storage.w
    numevents = len(storage.d.itervalues().next())
    for i in xrange(numevents):
        v = dict( (k, v[i]) for k,v in storage.d.iteritems() )
        if critera(v):
            for k,v in storage.d.iteritems():
                out.d.setdefault(k, list()).append(v[i])
    kept = len(out.d.itervalues().next())
    logging.info("%i events kept out of %i (crossx=%f fb)..." 
                 % (kept, numevents, kept*out.w/1000.0))
    return out



##############################################################################

def reset_pyplot():
    pyplot.cla()
    pyplot.clf()
    pyplot.close()

def plot_signal_background(x, wx, y, wy, fraction=None, xmax=None, numbins=100, variable="x", title=""):
    """Plots signal & background (signal=foreground-background) on single plot.

    x - background variable
    wx - background events weight [pb]
    y - foreground variable
    wy - foreground events weight [pb]
    """
    weights1, weights2 = list(wx for e in x), list(wy for e in y)

    #ranges:
    if xmax is None:
        if fraction is None: fraction = 1.0
        minv, maxv = min(x+y), ufraction(x+y, fraction)  
    else:
        minv, maxv = 0, xmax
    bins = np.linspace(minv, maxv, numbins)


    #plotting
    reset_pyplot()
    h1,edges1 = np.histogram(x, bins, weights=weights1, normed=False)
    p1 = pyplot.step(edges1[:-1], h1, color="blue", label="background (%.2fpb)" % (wx*len(x)) )
    h2,edges2 = np.histogram(y, bins, weights=weights2, normed=False)
    p2 = pyplot.step(edges2[:-1], h2-h1, color="red", label="signal (%.2fpb)" % (sum(h2-h1)))
    pyplot.legend()

    pyplot.ylabel("$\sigma/bin$ [pb]")
    pyplot.xlabel(variable)
    pyplot.title(title)
    pyplot.grid(True)
    #pyplot.show()

def plot_compare2(x, wx, y, wy, fraction=None, xmax=None, numbins=100, variable="x", title=""):
    """Plots two variables on single plot.

    x - first variable
    wx - first variable events weight [pb]
    y - second variable
    wy - second variable events weight [pb]
    """
    weights1, weights2 = list(wx for e in x), list(wy for e in y)

    #ranges:
    if xmax is None:
        if fraction is None: fraction = 1.0
        minv, maxv = min(x+y), ufraction(x+y, fraction)  
    else:
        minv, maxv = 0, xmax
    bins = np.linspace(minv, maxv, numbins)

    #plotting
    reset_pyplot()
    pyplot.hist(x, bins, weights=weights1, histtype="step", \
                normed=False, label="background (%.2fpb)" % (wx*len(x)), color="blue")
    pyplot.hist(y, bins, weights=weights2, histtype="step", \
                normed=False, label="foreground (%.2fpb)" % (wy*len(y)), color="red") 
    pyplot.legend()

    pyplot.ylabel("$\sigma/bin$ [pb]")
    pyplot.xlabel(variable)
    pyplot.title(title)
    pyplot.grid(True)
    #pyplot.show()


def plot_comparison(bg, fg, variable, numbins=100, title="", variable_name=None, fraction=None, xmax=None):
    """Plots two variables on single plot.

    bg, fg = DataStorage
    variable = column name
    """
    v1, v2 = bg.d[variable], fg.d[variable] 
    w1, w2 = bg.w, fg.w
    if variable_name is not None: variable = variable_name
    return plot_compare2(v1, w1, v2, w2, fraction, xmax, numbins, variable)

##############################################################################

def plot_given_hist2d(xedges, yedges, H, xlab="x", ylab="y", title="", clim=None):
    """Draws given 2D histogram H."""
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
                
    reset_pyplot()
    pyplot.figure(num=None, figsize=(9, 3.75), dpi=80, facecolor='w', edgecolor='k')
    im = pyplot.imshow(H, extent=extent, interpolation='nearest')
    if clim is not None: im.set_clim(clim)
    pyplot.gca().invert_yaxis()
    pyplot.colorbar(shrink=0.75)
    pyplot.xlabel(xlab)
    pyplot.ylabel(ylab)
    pyplot.title(title)
    pyplot.grid(True)
    #pyplot.show()

    return im


def plot_hist2d(x, y, w1, numbins=100, xlab="x", ylab="y", title="", xmax=None, ymax=None, clim=None):
    """Calculates 2D histogram and plots it using plot_given_hist2d."""
    if xmax is None: xmax = max(x)
    if ymax is None: ymax = max(y)

    H, xedges, yedges = np.histogram2d(y, x, bins=numbins, normed=False, \
                                          weights=list(w1 for e in x), \
                                          range = [[0, ymax], [0, xmax]])
    return plot_given_hist2d(xedges, yedges, H, xlab, ylab, title, clim), H, xedges, yedges

##############################################################################
##############################################################################
##############################################################################

def calc_cut_count(v, cut):
    return sum(1 for e in v if e > cut)

def find_max_cut(v1, w1, v2, w2, numtests=100, xlab="Variable", title=""):
    minv = lfraction(v1+v2, fraction=0.00)  
    maxv = ufraction(v1+v2, fraction=0.9)  
    logging.info("minv=%f maxv=%f" % (minv,maxv))

    cuts = np.linspace(minv, maxv, numtests)
    sb_list, signal_list = [],[]
    for cut in cuts: 
        count1 = calc_cut_count(v1, cut)
        kept1  = w1*count1
        count2 = calc_cut_count(v2, cut)
        kept2  = w2*count2
        signal = kept2-kept1
        sb     = signal/kept1

        signal_list.append(signal)
        sb_list.append(sb)

    pyplot.plot(cuts, sb_list, 'go-', label='S/B', linewidth=2)
    pyplot.ylabel("S/B")
    pyplot.xlabel(xlab)
    pyplot.title(title)
    pyplot.grid(True)
    pyplot.show()

    pyplot.plot(cuts, signal_list, 'b-', label='signal [fb]', linewidth=2)
    pyplot.ylabel("signal [fb]")
    pyplot.xlabel(xlab)
    pyplot.title(title)
    pyplot.grid(True)
    pyplot.show()
