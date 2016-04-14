#!/usr/bin/python

"""Code should be run from directory containing the data"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import ast
from matplotlib import cm
import pylab as p
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
import argparse
import re
from matplotlib import rc


# Simple code to plot the input and output data. For the current setup the density shouldn't change

# Select data files (rho or u)
rhodata = np.transpose(np.loadtxt('dns-uOutput-135-109.txt'))
rhoinit = np.transpose(np.loadtxt('dns-uOutput-init-135-109.txt'))

print np.max(rhoinit)
print rhodata.shape, rhoinit.shape
yvals = np.arange(rhodata.shape[0])
xvals = np.arange(rhodata.shape[1])

xvals_i = np.arange(rhoinit.shape[0])
yvals_i = np.arange(rhoinit.shape[1])

name = 'simple'

# DENSITY 2D

# Contour plot of final data
den_max = np.max(rhodata)
den_min = np.min(rhodata)
fig = plt.figure()
fig.text(0.44, 0.025, '$x$', ha='center', va='center', fontsize=26)
#plt.ylim(l_lim-0.3,r_lim+0.3)
plt.ylabel('$y$', fontsize=26)
plt.tick_params(pad=7)
ctest=plt.contourf(xvals, yvals, rhodata, cmap=cm.RdBu, levels=np.linspace(den_min,den_max,500))
plt.colorbar()
plt.savefig('den_2d_%s.png'%name)
plt.show()

# Contour plot of initial data
den_max = np.max(rhoinit)
den_min = np.min(rhoinit)
fig = plt.figure()
fig.text(0.44, 0.025, '$x$', ha='center', va='center', fontsize=26)
#plt.ylim(l_lim-0.3,r_lim+0.3)
plt.ylabel('$y$', fontsize=26)
plt.tick_params(pad=7)
ctest=plt.contourf(yvals_i, xvals_i, rhoinit, cmap=cm.RdBu, levels=np.linspace(den_min,den_max,500))
plt.colorbar()
plt.savefig('den_2d_%s_init.png'%name)
plt.show()
