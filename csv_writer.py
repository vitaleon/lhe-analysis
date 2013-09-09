#!/usr/bin/python
# -*- coding: utf-8 -*-

class CSVWriter:

    def __init__(self, f, sep = "\t,\t"):
        self.f = f
        self.sep = sep
        self.header = None

    def write_dict(self, d):
        if self.header is None:
            self.header = list(d) 
            self.f.write(self.sep.join(d))
            self.f.write("\n")
        self.f.write(self.sep.join(str(d[col]) for col in self.header))
        self.f.write("\n")
