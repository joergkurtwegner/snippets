#!/usr/bin/env python2

"""Molecule similarity to GXML graph
Calculate GXML graph based on molecule similarity and nearest neighbor similarity.

Usage: python molsim2xgml.py [options] [source]

Options:
  -h, --help              show this help

Examples:
  molsim2xgml.py filename.sdf
"""

__author__ = "Joerg Kurt Wegner (http://miningdrugs.blogspot.com/)"
__copyright__ = "Copyright (c) 2009 Joerg Kurt Wegner"
__license__ = "Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)"

import sys
import getopt
import pybel as pb
import openbabel as ob

class XGML:
    def __init__(self):
        print """<?xml version="1.0" encoding="UTF-8"?>
<section name="xgml"> <!-- XGML start -->
<attribute key="Creator" type="String">Pybel similarity matrix, Joerg Kurt Wegner, http://miningdrugs.blogspot.com</attribute>
<attribute key="Version" type="String">0.1</attribute>
<section name="graph"> <!-- graph start -->
<attribute key="hierarchic" type="int">1</attribute>
<attribute key="label" type="String"></attribute>
<attribute key="directed" type="int">1</attribute>
"""

    def __del__(self):
        print """</section> <!-- graph end -->
</section> <!-- XGML end -->"""

    def addNode(self, node_id, node_label,node_type, node_color):
        print """<section name="node"> <!-- node start -->
<attribute key="id" type="int">"""+str(node_id)+"""</attribute>
<attribute key="label" type="String">"""+str(node_label)+"""</attribute>
<section name="graphics">
<attribute key="type" type="String">"""+str(node_type)+"""</attribute> <!-- ellipse, diamond, rectangle -->
<attribute key="fill" type="String">"""+node_color+"""</attribute>
<attribute key="outline" type="String">#000000</attribute>
</section>              
<section name="LabelGraphics">
<attribute key="text" type="String">"""+str(node_label)+"""</attribute>
</section>
</section> <!-- node end -->
"""
    def addEdge(self, node_id1, node_id2, edge_label):
        print """<section name="edge"> <!-- edge start -->
<attribute key="source" type="int">"""+str(node_id1)+"""</attribute>
<attribute key="target" type="int">"""+str(node_id2)+"""</attribute>
<attribute key="label" type="String">"""+str(edge_label)+"""</attribute>
<section name="LabelGraphics">
<attribute key="text" type="String">"""+str(edge_label)+"""</attribute>
</section>
</section> <!-- edge end -->
"""


def usage():
    print __doc__

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

    xgml=XGML()
    filname=args[0]
    sdfile=pb.readfile("sdf", filname)
    node_index={}
    node_fp={}
    index=0
    for mol in sdfile:
        title=mol.title.strip()
        title=title.replace('>','greater')
        title=title.replace('<','smaller')
        title=title.replace(';',',')
        node_index[title]=index
        node_fp[title]=mol.calcfp(fptype='FP2')
        node_type='ellipse'
        node_color='#FF0000'
        if title.find('Test')!=-1:
            node_type='diamond'
            node_color='#00FF00'
        elif title.find('Train')!=-1:
            node_type='rectangle'
            node_color='#0000FF'
        xgml.addNode(index,title,node_type,node_color)
        index+=1
    for molname1 in node_index.keys():
        molindex1=node_index[molname1]
        molfp1=node_fp[molname1]
        maxsim=[]
        max_molindex=[]
        knn_count=1
        for index in range(knn_count):
            maxsim.append(-1.0)
            max_molindex.append(-1)
        for molname2 in node_index.keys():
            molindex2=node_index[molname2]
            if molindex1<molindex2:
                molfp2=node_fp[molname2]
                similarity=molfp1|molfp2
                minsim=maxsim[0]
                minsim_index=0
                for index in range(len(maxsim)):
                    if maxsim[index]<minsim:
                        minsim=maxsim[index]
                        minsim_index=index
                maxsim[minsim_index]=similarity
                max_molindex[minsim_index]=molindex2
        # s=str(molindex1)+':'
        for index in range(len(maxsim)):
            shortsim=str(maxsim[index])[0:5]
            xgml.addEdge(molindex1,max_molindex[index],shortsim)
            # s+=str(max_molindex[index])+'='+shortsim+','
        # print s
     

if __name__ == "__main__":
    main(sys.argv[1:])