#!/usr/bin/env python

"""Read in data and plot important variables for DNS runs

# NOTE: should be run from '~/Dropbox/DNS\ Solver/PIETRO'"""
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
import scipy.integrate as si





# Parse arguments form command line
parser = argparse.ArgumentParser()


parser.add_argument("-f", type=str, nargs=1, \
                    help="folder",required=True, default='XY')
parser.add_argument("-n", type=str, nargs=2, \
                    help="nptsX, nptsY",required=True, default='135 109')
parser.add_argument("-p", type=str, nargs=1, \
                    help="folder",required=False, default='n')


args = parser.parse_args()
folder = args.f[0] # folder
plotting = args.p[0] # whether to plot or not
nptsX = int(args.n[0])
nptsY = int(args.n[1])


var_list = ['u','v','rho']
ALL_DATA = []


#folder = 'uvrho/scaled/'+folder


# read in data

for variable in var_list:
	temp_data = np.transpose(np.loadtxt('%s/dns-%sOutput-%s-%s.txt'%(folder,variable, nptsX, nptsY)))
	ALL_DATA.append(temp_data)


uvals = ALL_DATA[0]
vvals = ALL_DATA[1]
rhovals = ALL_DATA[2]







# initial data values

uvals_avg = np.average(uvals, axis=0)
rhovals_avg_L = np.average(rhovals, axis=0)
rhovals_avg_H = np.average(rhovals, axis=1)
uvals_centre = np.array(uvals)[nptsY-1,:]
rhovals_centre = np.array(rhovals)[nptsY-1,:]



rhovals_start = rhovals[2]
rhovals_end = rhovals[nptsY-2]


# define X and Y grid

yvals = np.arange(rhovals.shape[0])
xvals = np.arange(rhovals.shape[1])


X,Y = np.meshgrid(xvals, yvals)


def HP(yvals,delta_P,L,D):
	u = (delta_P)/(2*L)*(D**2-yvals**2)
	return u
	


#----------------------------integrate rho*u over y--------------------------
 
## Maybe do using scipy at some point

def mass_flow(U, RHO):
	MF = []
	for i in range(U.shape[1]):
		URHO = []
		for j in range(U.shape[0]):
			URHO.append(U[j][i]*RHO[j][i])
		intURHO = si.simps(URHO)
		MF.append(intURHO)
	return MF 


mdot = mass_flow(uvals,rhovals)

#----------------------------------------------#

matplotlib.rcParams.update({'font.size': 19})
rc('text', usetex=True)


if plotting == 'y':
	# plotting


	# u
	fig = plt.figure()
	ctest=plt.contourf(xvals, yvals, uvals, cmap=cm.hot, levels=np.linspace(np.amin(uvals),np.amax(uvals),500))
	plt.colorbar()
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.savefig('{}/uvals_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))
	plt.show()


#	# v
#	fig = plt.figure()
#	ctest=plt.contourf(xvals, yvals, vvals, cmap=cm.hot, levels=np.linspace(-5.7e-6,3e-5,500))
#	plt.colorbar()
#	plt.xlabel('$\mathrm{X}$')
#	plt.ylabel('$\mathrm{Y}$')
#	plt.zlim(-5.7e-6,3e-5)
#	plt.savefig('{}/vvals_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))
#	plt.show()

	# rho

	f, axarr = plt.subplots(2, sharex=True)#, figsize=(6,7))

	ax1 = axarr[0]

	ctest=ax1.contourf(xvals, yvals, rhovals, cmap=cm.hot, levels=np.linspace(np.amin(rhovals),np.amax(rhovals),500))
	#f.colorbar(ctest)
	#ax1.set_xlabel('L')
	ax1.set_ylabel('$\mathrm{Y}$')
	


	ax2 = axarr[1]
	ax2.plot(xvals, rhovals_centre, label='final')
	ax2.set_xlabel('$\mathrm{L}$')
	ax2.set_ylabel('$\\rho_{\mathrm{centre}}$')
	#ax2.set_xlim(0,domainLength)

	plt.savefig('{}/comb_rhovals_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))
	plt.show()


	# u selection
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	for i in np.arange(0,nptsX,10):
		yplot = np.empty(len(yvals))

		yplot.fill(xvals[i])
		ax.plot(yvals, yplot, zs=np.array(uvals)[:,i])
	plt.savefig('{}/uvals_sel_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))	
	plt.show()

#	# rho selection
#	fig = plt.figure()
#	ax = fig.gca(projection='3d')
#	for i in np.arange(0,nptsX,10):
#		yplot = np.empty(len(Hvals))

#		yplot.fill(Lvals[i])
#		ax.plot(Hvals, yplot, zs=np.array(rhovals)[i,:])
#	plt.savefig('{}/{}/rhovals_sel_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))	
#	plt.show()

#	# u centre
#	fig = plt.figure()
#	plt.plot(Lvals, uvals_centre, label='final')
#	plt.xlabel('L')
#	plt.ylabel('u centre')
#	plt.savefig('{}/{}/uvals_centre_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
#	plt.show()

#	# rho centre
#	fig = plt.figure()
#	plt.plot(Lvals, rhovals_centre, label='final')
#	plt.xlabel('L')
#	plt.ylabel('$\\rho$ centre')
#	plt.savefig('{}/{}/rhovals_centre_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
#	plt.show()



	# u init
	fig = plt.figure()
	plt.plot(yvals, np.array(uvals)[:,0], label='initial')
	plt.plot(yvals, np.array(uvals)[:,-1], label='final')
	plt.plot(yvals, np.array(uvals)[:,5], label='5')
	#plt.plot(xvals, HP(Hvals, 	delta_P,domainLength,domainHeight),linestyle='dashed',label='HP')
	plt.xlabel('Y')
	plt.ylabel('u init')
	#plt.ylim(0,0.012)
	plt.legend()
	plt.savefig('{}/uvals_sample_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))
	plt.show()

	# massflow
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ind = np.arange(1,uvals.shape[1]+1)
	width = 0.2
	mdot_bar = ax.bar(ind+width/2, mdot, width, color = 'b')
	plt.ylabel('$\mathrm{Mass}$ $\mathrm{flow}$')
	plt.savefig('{}/massflow_{}_{}_{}.png'.format(folder,nptsX,nptsY,folder))
	plt.show()

#	# rho init
#	fig = plt.figure()
#	plt.plot(Hvals, np.array(rhovals)[0,:], label='initial')
#	#plt.plot(Hvals, np.array(uvals)[-1,:], label='final')
#	#plt.plot(Hvals, np.array(rhovals)[30,:], label='n=30')
#	#plt.plot(Hvals, np.array(rhovals)[59,:], label='n=59/final')
#	plt.legend()
#	plt.xlabel('H')
#	plt.ylabel('$\\rho$ init')
#	plt.savefig('{}/{}/rhovals_init_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
#	plt.show()



#	'''
#	# u average
#	fig = plt.figure()

#	plt.plot(Hvals, uvals_avg, label='final')
#	plt.legend(loc='lower left')
#	plt.xlabel('H')
#	plt.ylabel('u')
#	plt.savefig('{}/uvals_avg_{}_{}.pdf'.format(folder,nptsX,nptsY,folder))
#	plt.show()

#	# rho average over L
#	fig = plt.figure()

#	plt.plot(Hvals, rhovals_avg_L, label='final')
#	plt.xlabel('H')
#	plt.ylabel('$\\rho$')
#	plt.savefig('{}/rhovals_avg_L_{}_{}_{}.pdf'.format(folder,nptsX,nptsY,folder))
#	plt.show()

#	# rho average over H
#	fig = plt.figure()
#	plt.plot(Lvals, rhovals_avg_H)
#	plt.xlabel('L')
#	plt.ylabel('$\\rho$')
#	plt.savefig('{}/rhovals_avg_H_{}_{}_{}.pdf'.format(folder,nptsX,nptsY,folder))
#	plt.show()

#	#rhovals start and end
#	fig = plt.figure()
#	plt.plot(Hvals, rhovals_start)
#	plt.plot(Hvals, rhovals_end)
#	plt.xlabel('H')
#	plt.ylabel('$\\rho$')
#	plt.savefig('rhovals_s_e.pdf')
#	plt.show()'''


