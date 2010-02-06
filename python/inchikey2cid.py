#!/usr/bin/env python2
"""CID from InchiKey flat file

Get ChemspiderIDentifiers (CID) from InchiKeys in a flat file.

Usage: python inchikey2cid.py [options] [source]

Options:
  -h, --help              show this help

Examples:
  inchikey2cid.py filename.tab.txt
"""

__author__ = "Joerg Kurt Wegner (http://miningdrugs.blogspot.com/)"
__copyright__ = "Copyright (c) 2009 Joerg Kurt Wegner"
__license__ = "Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)"

import httplib
import urlparse
import urllib
import urllib2
import base64
import re
import sys
import getopt
import socket

def usage():
    print __doc__

def getcid_from_inchikey(inchikey):
    timeout=5
    socket.setdefaulttimeout(timeout)
    cid='NA'
    for i in range(3):
        request = urllib2.Request('http://www.chemspider.com/InChIKey/'+inchikey)
        try: 
            response = urllib2.urlopen(request)
            the_page = response.read()
            cid_pattern = re.compile('Chemical-Structure\.(\d*)\.html')
            pattern_search=cid_pattern.search(the_page)
            if str(pattern_search)!='None':
                pattern_search.groups()
                if len(pattern_search.groups())==1:
                          cid=pattern_search.groups()[0]
                break
        except urllib2.URLError, e:
            # just do another round
            cid='TimeOut'
    return cid

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
    
    try:
        ifile = open(args[0], "r") 
    except IOError, e:
        print e
        sys.exit(2)
    
    while 1:
        lines = ifile.readlines(100000) #buffer lines for speeding things up
        if not lines:
            break
        for line in lines:
            lsplit = line.strip().split('\t')
            inchikey='NA'
            for lentry in lsplit:
                if len(lentry)==25 and lentry[14]:  # quick inchikey check
                    inchikey=lentry
            if inchikey=='NA':
                lsplit.append('NA')
            else:
                lsplit.append(getcid_from_inchikey(inchikey)) # slow, slow, slow ! TimeOut or NA ?
            new_line=''
            for index in range(len(lsplit)-1):
                new_line+=lsplit[index]+'\t'
            new_line+=lsplit[len(lsplit)-1]
            print new_line
                
if __name__ == "__main__":
    main(sys.argv[1:])