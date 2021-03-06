#!/usr/bin/python

"""Checking whether Navier-Stokes like equations are satisfied for the transient code. Slightly shorter script as there aren't as many cases considered"""
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



# Parse arguments form command line
parser = argparse.ArgumentParser()


parser.add_argument("-f", type=str, nargs=1, \
                    help="folder",required=True, default='XY')
parser.add_argument("-n", type=int, nargs=2, \
                    help="points for L, H",required=True)
parser.add_argument("-xy", type=int, nargs=2, \
                    help="X (length), y (height)",required=True)

args = parser.parse_args()
folder = args.f[0] # folder/type
nptsX = args.n[0] #100
nptsY = args.n[1] #60 
domainLength = args.xy[0] #115
domainHeight = args.xy[1] #1



var_list = ['u','v','rho']
ALL_DATA = []





# read in data

for variable in var_list:
	filename = "{}/dns-{}Output-{}-{}.txt".format(folder, variable, nptsX, nptsY)
	f = open(filename,'r')
	data = f.read()

	# only from data split [2] to [2]
	temp_data = data.split('\n')[2:-2]

	for i in range(len(temp_data)):
		temp_data[i] = map(float, temp_data[i].split())
	#print temp_data[-1], len(temp_data)
	ALL_DATA.append(temp_data)


uvals = np.array(ALL_DATA[0])
vvals = np.array(ALL_DATA[1])
rhovals = np.array(ALL_DATA[2])



#-------------------CALC P and MU--------------------



C1=8.1
C2=-17.55
C3=10.47
A1=6.22
A2=-13.86
A3=8.64

mu = np.zeros((rhovals.shape))
p = np.zeros((rhovals.shape))
rhou = np.zeros((rhovals.shape))
rhov = np.zeros((rhovals.shape))

for i in range(nptsX):
	for j in range(nptsY):
		mu[i][j]=A1*rhovals[i][j]*rhovals[i][j]+A2*rhovals[i][j]+A3
		p[i][j]=C1*rhovals[i][j]*rhovals[i][j]+C2*rhovals[i][j]+C3
		rhou[i][j] = rhovals[i][j]*uvals[i][j]
		rhov[i][j] = rhovals[i][j]*vvals[i][j]

#-------------------DERIVATIVES----------------------

dX = domainLength/nptsX
dY = domainHeight/(nptsY+0.5) #due to BCs

ux = np.zeros((nptsX,nptsY))
uy = np.zeros((nptsX,nptsY))
uxx = np.zeros((nptsX,nptsY))
uyy = np.zeros((nptsX,nptsY))
uxy = np.zeros((nptsX,nptsY))

vx = np.zeros((nptsX,nptsY))
vy = np.zeros((nptsX,nptsY))
vxx = np.zeros((nptsX,nptsY))
vyy = np.zeros((nptsX,nptsY))
vxy = np.zeros((nptsX,nptsY))

rhoux = np.zeros((nptsX,nptsY))
rhovy = np.zeros((nptsX,nptsY))

px = np.zeros((nptsX,nptsY))
py = np.zeros((nptsX,nptsY))

mux = np.zeros((nptsX,nptsY))
muy = np.zeros((nptsX,nptsY))




for i in range(1,nptsX-1):
	for j in range(1,nptsY-1):
		ux[i][j] = (uvals[i+1][j]-uvals[i-1][j])/(2.*dX)
		uy[i][j] = (uvals[i][j+1]-uvals[i][j-1])/(2.*dY)
		uxx[i][j] = (uvals[i+1][j] - 2*uvals[i][j] +uvals[i-1][j])/(dX*dX)
		uyy[i][j] = (uvals[i][j+1] - 2*uvals[i][j] +uvals[i][j-1])/(dY*dY)
		uxy[i][j] = (uvals[i+1][j+1] - uvals[i+1][j-1] - uvals[i-1][j+1] + uvals[i-1][j-1])/(4.*dX*dY)

		vx[i][j] = (vvals[i+1][j]-vvals[i-1][j])/(2.*dX)
		vy[i][j] = (vvals[i][j+1]-vvals[i][j-1])/(2.*dY)
		vxx[i][j] = (vvals[i+1][j] - 2*vvals[i][j] +vvals[i-1][j])/(dX*dX)
		vyy[i][j] = (vvals[i][j+1] - 2*vvals[i][j] +vvals[i][j-1])/(dY*dY)
		vxy[i][j] = (vvals[i+1][j+1] - vvals[i+1][j-1] - vvals[i-1][j+1] + vvals[i-1][j-1])/(4.*dX*dY)

		rhoux[i][j] = (rhou[i+1][j]-rhou[i-1][j])/(2.*dX)
		rhovy[i][j] = (rhov[i][j+1]-rhov[i][j-1])/(2.*dY)

		px[i][j] = (p[i+1][j]-p[i-1][j])/(2.*dX)
		py[i][j] = (p[i][j+1]-p[i][j-1])/(2.*dY)

		mux[i][j] = (mu[i+1][j]-mu[i-1][j])/(2.*dX)
		muy[i][j] = (mu[i][j+1]-mu[i][j-1])/(2.*dY)



#----------------------------NS -----------------------------------

RHS_x = np.zeros((nptsX,nptsY))
RHS_y = np.zeros((nptsX,nptsY))

LHS_x = np.zeros((nptsX,nptsY))
LHS_y = np.zeros((nptsX,nptsY))

cont_eqn = np.zeros((nptsX,nptsY))

for i in range(1,nptsX):
	for j in range(1,nptsY):
		RHS_x[i][j] = -px[i][j] + mu[i][j]*(uxx[i][j]+uyy[i][j]) + mux[i][j]*(ux[i][j] + vy[i][j])
		RHS_y[i][j] = -py[i][j] + mu[i][j]*(vxx[i][j]+vyy[i][j]) + muy[i][j]*(ux[i][j] + vy[i][j])

		# don't need LHS as we're ignoring these terms
		LHS_x[i][j] = rhovals[i][j] * (uvals[i][j]*ux[i][j] + vvals[i][j]*uy[i][j])
		LHS_y[i][j] = rhovals[i][j] * (uvals[i][j]*vx[i][j] + vvals[i][j]*vy[i][j])
		cont_eqn[i][j] = rhoux[i][j] + rhovy[i][j]

		print 'x: ', RHS_x[i][j],' y: ',  RHS_y[i][j],' cont: ', cont_eqn[i][j]

RHS_x_sum = np.sum(RHS_x)
LHS_x_sum = np.sum(LHS_x)
RHS_y_sum = np.sum(RHS_y)
LHS_y_sum = np.sum(LHS_y)
cont_eqn_sum = np.sum(cont_eqn)


print 'Sums'
print 'x: ', RHS_x_sum,' y: ',  RHS_y_sum,' cont: ', cont_eqn_sum





