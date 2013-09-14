#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Auxiliary functions and classes."""


def print_list(l, header=""):
    print header
    for e in l:
        print e

def print_dict(d, header=""):
    print header
    for k,v in d.iteritems():
        print k," : ",v

def print_dict_of_lists(d, header="", cols=5):
    print header
    for k,v in d.iteritems():
        print k," [",len(v),"]: ",v[:cols],"..."
