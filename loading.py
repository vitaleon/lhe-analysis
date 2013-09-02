#!/usr/bin/python
# -*- coding: utf-8 -*-
"""LHE files loading."""
import log
import sys

class LHELoader:
    """Loads and parses LHE files."""

    def load_header(self):
        """Returns header from LHE file."""
        if len(self.header) > 0 or len(self.event) > 0 or len(self.footer) > 0:
            log.warn("You cannot read header after \
                      you started reading events!")
            return self.header 

        self.header = []
        for line in self.infile.xreadlines():
            if "<event>" in line:
                self.event.append(line)
                break
            self.header.append(line)
            
        return self.header

    def yield_events(self):
        """Yields events from LHE file."""
        if len(self.header) <= 0: 
            self.load_header()

        while len(self.footer) <= 0:

            for line in self.infile.xreadlines(): #read event
                self.event.append(line)
                if "</event>" in line: 
                    self.events_counter += 1
                    yield self.event
                    self.event = []
                    break

            for line in self.infile.xreadlines(): #read what's after event
                if "<event>" in line: 
                    self.event.append(line)
                    break
                self.footer.append(line)

        if len(self.event) > 0:
            log.warn("Last event has not ending tag!")
            self.events_counter += 1
            yield self.event
            self.event = []     
            

    def __init__(self, infile):
        """Opens for reading input file (infile=file) \
            that should be in LHE format."""
        self.infile = infile
        self.header = []
        self.footer = []
        self.event = []
        self.events_counter = 0

        

if __name__=="__main__":

    try: inpath = sys.argv[1]
    except: print "Input file path expected!"; sys.exit(-1)

    lhe = LHELoader(open(inpath))
    events = list( lhe.yield_events() )
    print "header =", lhe.header
    print "footer =", lhe.footer
    print "events_counter =", lhe.events_counter
    print "len(events) =", len(events)
    print "events = ", events[:2], "...", events[-1]


