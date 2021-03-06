# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:58:33 2015

@author: greensb

NOTE: FOR ROCKSTAR CATALOGS ONLY!!!

PROCEDURE FOR VISUALIZING MICROHALOS
1. Run this script, giving it as arguments the corresponding ROCKSTAR halo file and the associated gadget snapshot blocks
2. Using the *.vis files generated, run block_combine.py to combine them all into one .txt file for visualization.
3. Use flat_visualize.py and visualize.py with the .txt file to view microhalo

to pick out a specific halo, look at top 10 largest:
data=np.loadtxt('halos.ascii')
data = data[data[:,1].argsort()]
data = data[len(data)-10:,:]

PROCEDURE FOR GENERATING DENSITY PROFILES
1. Run this script, same as above, and it will output the locations of the particles (we still need to get particle mass somehow)
2. Run command cat *.particle > all_particles.txt
3. Run density_prof.py, which takes all the particles, bins them, and outputs a density profile file, which we can plot on a personal computer

PROCEDURE FOR CALCULATING BOOST FACTORS:
1. Run this script, giving it as arguments the corresponding ROCKSTAR halo file and the associated gadget snapshot blocks
2. Run command cat *.particle > all_particles.txt
3. Run calc_boost_factor.py, with arguments of the halo particles and the halo parameters file.
"""

import numpy as np
import sys
import os

name = sys.argv[1].split('_')
paramfile = open(name[2]+"_params.txt","w")

#algorithm begins:
#first use the corresponding rockstar bgc2 halo catalogue to find largest halo
data = np.loadtxt(sys.argv[1]) #halo catalogue data
blocks = sys.argv[2:len(sys.argv)]
sim_stats = blocks[0].split("_") #this will give us our particle count and sim size to put in the data file
part_count = sim_stats[1] #STRING
sim_size = sim_stats[2] #STRING
largest_halo = np.zeros(6) #need mass, number of particles, x,y,z coordinates and virial radius (anything else?)
for i in range(0,len(data)): #scanning through all the halos
    if (data[i,2] > largest_halo[0]): #if it is the largest halo
        largest_halo[0] = data[i,2] #mass in Msun/h or Msun
        largest_halo[1] = data[i,1] #number of particles
        largest_halo[2] = data[i,3]*1000000 #radius in pc/h
        largest_halo[3] = data[i,5]*1000000 #x These in pc/h
        largest_halo[4] = data[i,6]*1000000 #y
        largest_halo[5] = data[i,7]*1000000 #z
        largest_halo_id = data[i,0]
        
#print to a parameter file the radius, particle mass, simulation particle count (ie 1024 or 512), and simulation size (in Mpc/h)
particlemass = largest_halo[0] / largest_halo[1] #total mass divided by number of particles, in Msun/h or Msun (figure it out)
paramfile.write(str(particlemass)+"\n")
paramfile.write(str(largest_halo[2])+"\n")
paramfile.write(part_count+"\n")
paramfile.write(sim_size+"\n")
paramfile.write(largest_halo_id+"\n")


#now we have the location of the largest halo, so we can call our gadget block to lattice code to generate the .vis files
for i in blocks:
    print i
    command = "bsub -o "+i+".txt python readblock.py "+i+" " + str(largest_halo[3]) + " " + str(largest_halo[4]) + " " + str(largest_halo[5]) + " " + str(largest_halo[2])
    os.system(command)   
