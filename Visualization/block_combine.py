# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:26:44 2015

@author: greensb

This file combines all of the visualization arrays generated for the different
blocks in a snapshot to form a final mesh which can be visualized.
"""

import numpy as np
import sys

#files
blocks = sys.argv[1:len(sys.argv)]
name = sys.argv[1].split('_')
latticefile = open(name[4]+"_final_mesh.txt","w")

#parameters
vis_size = 256 #the dimension of our cube for visualization
cube = np.ndarray((vis_size,vis_size,vis_size)) #goes from 0 to 255, initialized to zeros

#put all the files together
#this would be amazing to run using parallel processors
for i in blocks:
    data = open(i,"rb")
    for j in range(0,vis_size):
        for k in range(0,vis_size):
            for m in range(0,vis_size):
                cube[j][k][m] += float(data.readline())
                
#output this to a final visualization file                
for i in range(0,vis_size):
    for j in range(0,vis_size):
        for k in range(0,vis_size):
            latticefile.write(str(cube[i][j][k])+"\n")
