#!/usr/bin/python

"""Read in data and plot important variables for DNS runs

# NOTE: should be run from '~/Dropbox/DNS\ Solver/PIETRO'"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import ast
import sys
from matplotlib import cm
import pylab as p
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
import argparse
import re
from matplotlib import rc
sys.path.insert(0,'/home/fred/SCRIPTS/Python')
from plotting_params import *




# Parse arguments form command line
parser = argparse.ArgumentParser()


parser.add_argument("-f", type=str, nargs=2, \
                    help="folder",required=True, default='XY')
parser.add_argument("-n", type=int, nargs=2, \
                    help="points for L, H",required=True)
parser.add_argument("-p", type=str, nargs=1, \
                    help="folder",required=False, default='n')
#parser.add_argument("-xy", type=int, nargs=2, \
 #                   help="X (length), y (height)",required=True)

args = parser.parse_args()
folder = args.f[0] # folder
ftype = args.f[1] # type
nptsX = args.n[0] #100
nptsY = args.n[1] #60 
plotting = args.p[0] # whether to plot or not
#domainLength = args.xy[0] #115
#domainHeight = args.xy[1] #1

domainLength = int(re.search('x(.*)y',ftype).group(1))
domainHeight = float(re.search('y(.*)',ftype).group(1))

if 'GRAD' in folder:
	delta_P = float(re.search('P(.*)x',ftype).group(1))-1
else:
	delta_P = 0.05



var_list = ['u','v','rho']
ALL_DATA = []


folder = 'uvrho/scaled/'+folder


# read in data

for variable in var_list:
	filename = "{}/{}/dns-{}Output-{}-{}.txt".format(folder, ftype, variable, nptsX, nptsY)
	f = open(filename,'r')
	data = f.read()

	# only from data split [2] to [2]
	temp_data = data.split('\n')[2:-2]

	for i in range(len(temp_data)):
		temp_data[i] = map(float, temp_data[i].split())
	#print temp_data[-1], len(temp_data)
	ALL_DATA.append(temp_data)


uvals = ALL_DATA[0]
vvals = ALL_DATA[1]
rhovals = ALL_DATA[2]







# initial data values

uvals_avg = np.average(uvals, axis=0)
rhovals_avg_L = np.average(rhovals, axis=0)
rhovals_avg_H = np.average(rhovals, axis=1)
uvals_centre = np.array(uvals)[:,nptsY-1]
rhovals_centre = np.array(rhovals)[:,nptsY-1]

#print uvals[0][59], uvals[1][59], np.array(uvals)[:,59], len(np.array(uvals)[:,59])


rhovals_start = rhovals[2]
rhovals_end = rhovals[nptsY-2]


# define L and H grid


# think X,Y may be the wrong way around
Lvals = np.linspace(0, domainLength, nptsX)
Hvals = np.linspace(0, domainHeight, nptsY)[::-1]

H, L = np.meshgrid(Hvals, Lvals)


def HP(yvals,delta_P,L,D):
	u = (delta_P)/(2*L)*(D**2-yvals**2)
	return u
	


#----------------------------integrate rho*u over y--------------------------
'''

def integrate(xval, rho,u):
	ba = domainLength
	N = 2*nptsY-1

	# wall terms
	sum_rhou = 2*rhovals[xval][0]*uvals[xval][0]
	for i in range(1,nptsY):
		sum_rhou += 4*rhovals[xval][i]*uvals[xval][i]
	# centre term
	#sum_rhou += 2*rhovals[xval][nptsY-1]*uvals[xval][nptsY-1]
	final = ba/(2*N)*sum_rhou
	return final
'''

def integrate(xval, rho, u):
	''' Find mass flow'''
	N = 2*nptsY-1
	h = domainLength/N	
	rhoval = np.array(rho)[xval,:]
	rhoval = np.concatenate((rhoval, rhoval[::-1]))#,axis=1)
	u = np.array(u)[xval,:]
	u = np.concatenate((u, u[::-1]))#,axis=1)
	sum_rhou = 0
	for i in range(1, int(N/2)):
		sum_rhou += rhoval[2*i-2]*u[2*i-2]
    	sum_rhou += 4*rhoval[2*i-1]*u[2*i-1]
    	sum_rhou += rhoval[2*i]*u[2*i]
	final = (h/3)*sum_rhou
	return final

print integrate(57, rhovals,uvals), integrate(40, rhovals,uvals)

print 'L', domainLength, 'H', domainHeight

#----------------------------------------------#

#matplotlib.rcParams.update({'font.size': 19})
#rc('text', usetex=True)


if plotting == 'y':
	# plotting


	# u
	fig = plt.figure()
	ctest=plt.contourf(L, H, uvals, cmap=cm.hot, levels=np.linspace(np.amin(uvals),np.amax(uvals),500))
	plt.colorbar()
	plt.xlabel('L')
	plt.ylabel('H')
	plt.savefig('{}/{}/uvals_{}_{}_{}.png'.format(folder,ftype, nptsX,nptsY,ftype))
	plt.show()


	# v
	fig = plt.figure()
	ctest=plt.contourf(L, H, vvals, cmap=cm.hot, levels=np.linspace(-5.7e-6,3e-5,500))
	plt.colorbar()
	plt.xlabel('$\mathrm{L}$')
	plt.ylabel('$\mathrm{H}$')
	#plt.zlim(-5.7e-6,3e-5)
	plt.savefig('{}/{}/vvals_{}_{}_{}.png'.format(folder,ftype, nptsX,nptsY,ftype))
	plt.show()

	# rho

	f, axarr = plt.subplots(2, sharex=True)#, figsize=(6,7))

	ax1 = axarr[0]

	ctest=ax1.contourf(L, H, rhovals, cmap=cm.hot, levels=np.linspace(np.amin(rhovals),np.amax(rhovals),500))
	#f.colorbar(ctest)
	#ax1.set_xlabel('L')
	ax1.set_ylabel('$\mathrm{H}$')
	


	ax2 = axarr[1]
	ax2.plot(Lvals, rhovals_centre, label='final')
	ax2.set_xlabel('$\mathrm{L}$')
	ax2.set_ylabel('$\\rho_{\mathrm{centre}}$')
	ax2.set_xlim(0,domainLength)

	plt.savefig('{}/{}/comb_rhovals_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
	plt.show()


	# u selection
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	for i in np.arange(0,nptsX,20):
		yplot = np.empty(len(Hvals))

		yplot.fill(Lvals[i])
		ax.plot(Hvals, yplot, zs=np.array(uvals)[i,:])
	ax.axes.xaxis.set_ticklabels([])
	ax.axes.yaxis.set_ticklabels([])
	ax.axes.zaxis.set_ticklabels([])
	#ax.tick_params(axis='z', which='major', pad=12)
	ax.xaxis.set_pane_color((1,1,1, 0.1))
	#ax.set_xlabel('z')
	#ax.set_ylabel('x')
	#ax.set_zlabel('$u_x$')
	plt.savefig('{}/{}/uvals_sel_{}_{}_{}.pdf'.format(folder,ftype,nptsX,nptsY,ftype),bbox_inches='tight')	
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
	plt.plot(Hvals, np.array(uvals)[0,:], label='initial')
	plt.plot(Hvals, np.array(uvals)[-1,:], label='final')
	plt.plot(Hvals, np.array(uvals)[5,:], label='5')
	plt.plot(Hvals, HP(Hvals, 	delta_P,domainLength,domainHeight),linestyle='dashed',label='HP')
	plt.xlabel('H')
	plt.ylabel('u init')
	#plt.ylim(0,0.012)
	plt.legend()
	plt.savefig('{}/{}/uvals_init_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
	plt.show()


	# rho init
	fig = plt.figure()
	plt.plot(Hvals, np.array(rhovals)[0,:], label='initial')
	#plt.plot(Hvals, np.array(uvals)[-1,:], label='final')
	#plt.plot(Hvals, np.array(rhovals)[30,:], label='n=30')
	#plt.plot(Hvals, np.array(rhovals)[59,:], label='n=59/final')
	plt.legend()
	plt.xlabel('H')
	plt.ylabel('$\\rho$ init')
	plt.savefig('{}/{}/rhovals_init_{}_{}_{}.png'.format(folder,ftype,nptsX,nptsY,ftype))
	plt.show()



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


