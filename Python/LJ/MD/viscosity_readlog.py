#!/usr/bin/env python

"""Reads in log files and extracts pressure, shear and bulk viscosity data"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import argparse
from matplotlib import rc


np.set_printoptions(precision=16)
# Parse arguments form command line
parser = argparse.ArgumentParser()


parser.add_argument("-T", type=str, nargs='+', \
                    help="Temperature",required=True)
parser.add_argument("-rhof", type=str, nargs='+', \
                    help="Fluid density",required=False, default = ['0.1', '0.15','0.2', '0.25','0.3', '0.35', '0.4', '0.45', '0.5', '0.55', '0.6', '0.65', '0.7', '0.75', '0.8', '0.85', '0.9'])#, '0.95', '0.975', '1.0'])



args = parser.parse_args()
T = args.T
dens = args.rhof

if len(T) ==1:
	T = T[0]

press = []
shear = []
bulk = []
density = []


def read_log(T, den):

    filename = "/media/fred/My Passport/LJ_relations_results/CORRECT/T%s/rhof%s/log.rel_rhof%s" % (T,den,den)

    # read in data
    f = open(filename,'r')
    data = f.read()


    data_lines = data.split('\n')
    density.append(float(den))
    print 'Density: ', den

    for i in range(0,len(data_lines)-1):

        log_data = data_lines[i].split()

	if len(log_data) >1:
			
                if log_data[1] == 'shear' and log_data[2] == 'viscosity' and log_data[3] == ':':
		        print 'Shear viscosity: ', log_data[4]
                        shear.append(float(log_data[4]))
		if log_data[1] == 'bulk' and log_data[2] == 'pt':
			print 'Bulk viscosity: ', log_data[5]
			bulk.append(float(log_data[5]))
		if log_data[0] == 'Loop':
			dat = data_lines[i-1].split()
			print 'Pressure: ', dat[5]
			press.append(float(dat[5]))
		continue
		
    return 



def save_data(D, P, SH, BU):

	data_list = [D,P,SH,BU]
	data_array = np.transpose(np.array(data_list))
	print data_array
	print type(data_array[0][0])
	np.savetxt('relations_T%s.dat'%(T), data_array,fmt="%s",header = 'Density Pressure Shear Bulk')
	return data_array

def P_135(rho):
        rho = np.array(map(float,rho))
        P = 0.1762*np.exp(-4.108*rho)+0.00509*np.exp(7.747*rho)
        return P

def P_17(rho):
	rho = np.array(map(float,rho))
	P = 0.163*np.exp(-1.078*rho)+0.02561*np.exp(6.305*rho)
	return P

def P_20(rho):
	rho = np.array(map(float,rho))
	P = 0.1346*np.exp(1.028*rho)+0.04655*np.exp(5.829*rho)
	return P

def P_25(rho):
	rho = np.array(map(float,rho))
	return 0.1155*np.exp(2.778*rho)+0.0919*np.exp(5.23*rho)

def shear_135(rho):
        rho = np.array(map(float,rho))
        return 0.1373*np.exp(1.724*rho)+0.0307*np.exp(5.153*rho)

def shear_17(rho):
	rho = np.array(map(float,rho))
	return 0.167*np.exp(1.715*rho)+0.008242*np.exp(6.292*rho)

def shear_20(rho):
	rho = np.array(map(float,rho))
	return 0.1776*np.exp(1.722*rho)+0.01142*np.exp(5.78*rho)

def shear_25(rho):
	rho = np.array(map(float,rho))
	return 0.2275*np.exp(1.378*rho)+0.01373*np.exp(5.549*rho)

def bulk_135(rho):
        rho = np.array(map(float,rho))
        return 1.116*np.exp(-((rho-0.4509)/0.1872)**2)+1.077*np.exp(-((rho-1.113)/0.4903)**2)

def bulk_17(rho):
	rho = np.array(map(float,rho))
	return 14.41*rho**2.805*np.exp(-2.936*rho)

def bulk_20(rho):
	rho = np.array(map(float,rho))
	return 13.91*rho**2.935*np.exp(-2.947*rho)

def bulk_25(rho):
	rho = np.array(map(float,rho))
	return 6.938*rho**2.645*np.exp(-2.169*rho)

def Woodcock(rho, rho_0, T):
	rho = np.array(map(float,rho))
	T = float(T)
	term1 = np.sqrt(2)*(1-(1/T)**2-(T/8))*rho
	term2 = 3.025*(1/T)**(1/3)*rho**4
	return rho_0*(1+term1+term2)

	
# PLOTTING

dens_new =[]

for d in dens:
	try:
		read_log(T,d)
		dens_new.append(d)
	except IOError: pass
rho_0 = 0.4
final_data = save_data(dens_new,press,shear,bulk)
rhovals = np.arange(0.05,0.91,0.01)

matplotlib.rcParams.update({'font.size': 19})
rc('text', usetex=True)

fig = plt.figure()
plt.plot(final_data[:,0], final_data[:,1], marker ='D' , linestyle = 'none')
if T == '1.7':
	plt.plot(rhovals, P_17(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
if T == '2.0':
	plt.plot(rhovals, P_20(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
if T == '2.5':
	plt.plot(rhovals, P_25(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
plt.ylabel('$\mathrm{P}$')
plt.xlabel('$\\rho$')
plt.xlim(0.1,0.9)
plt.savefig('PLOTS/rho_v_P_T%s.pdf'%(T))
plt.show()

fig = plt.figure()
plt.plot(final_data[:,0], final_data[:,2], marker ='D', linestyle = 'none')
#plt.plot(final_data[:,0], Woodcock(final_data[:,0], rho_0, T), lw = 2.0,linestyle = 'dashed', c='r', label = "Woodcock")
if T == '1.7':
	plt.plot(rhovals, shear_17(rhovals), lw = 2.0,linestyle = 'dashed', c='b', label= "Fit")
if T == '2.0':
	plt.plot(rhovals, shear_20(rhovals), lw = 2.0,linestyle = 'dashed', c='b')
if T == '2.5':
	plt.plot(rhovals, shear_25(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
plt.ylabel('$\eta$')
plt.xlabel('$\\rho$')
plt.xlim(0.1,0.9)
#plt.legend()
#plt.ylim(0,6)
plt.savefig('PLOTS/rho_v_shear_T%s.pdf'%(T))
plt.show()

fig = plt.figure()
plt.plot(final_data[:,0], final_data[:,3], marker ='D', linestyle = 'none')
if T == '1.7':
	plt.plot(rhovals, bulk_17(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
if T == '2.0':
	plt.plot(rhovals, bulk_20(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
if T == '2.5':
	plt.plot(rhovals, bulk_25(rhovals), lw = 2.0, linestyle = 'dashed', c='b')
plt.ylabel('$\kappa$')
plt.xlabel('$\\rho$')
plt.xlim(0.1,0.9)
#plt.ylim(-2,14)
plt.savefig('PLOTS/rho_v_bulk_T%s.pdf'%(T))
plt.show()



# COMPARE EXPRESSIONS FOR T
'''

fig = plt.figure()
plt.plot(rhovals, P_135(rhovals), label = '$T=1.35$', lw = 2.0)
plt.plot(rhovals, P_17(rhovals), label = '$T=1.7$', lw = 2.0)
plt.plot(rhovals, P_20(rhovals), label = '$T=2.0$', lw = 2.0)
plt.plot(rhovals, P_25(rhovals), label = '$T=2.5$', lw = 2.0)
plt.ylabel('$\mathrm{P}$')
plt.xlabel('$\\rho$')
plt.legend()
plt.xlim(0.1,0.9)
#plt.ylim(0,20)
plt.savefig('PLOTS/rho_v_P.pdf')
#plt.show()

fig = plt.figure()
plt.plot(rhovals, shear_135(rhovals), label = '$T=1.35$', lw = 2.0)
plt.plot(rhovals, shear_17(rhovals), label = '$T=1.7$', lw = 2.0)
plt.plot(rhovals, shear_20(rhovals), label = '$T=2.0$', lw = 2.0)
plt.plot(rhovals, shear_25(rhovals), label = '$T=2.5$', lw = 2.0)
plt.ylabel('$\eta$')
plt.xlabel('$\\rho$')
plt.legend()
plt.xlim(0.1,0.9)
#plt.ylim(0,20)
plt.savefig('PLOTS/rho_v_shear.pdf')
#plt.show()

fig = plt.figure()
plt.plot(rhovals, bulk_135(rhovals), label = '$T=1.35$', lw = 2.0)
plt.plot(rhovals, bulk_17(rhovals), label = '$T=1.7$', lw = 2.0)
plt.plot(rhovals, bulk_20(rhovals), label = '$T=2.0$', lw = 2.0)
plt.plot(rhovals, bulk_25(rhovals), label = '$T=2.5$', lw = 2.0)
plt.ylabel('$\kappa$')
plt.xlabel('$\\rho$')
plt.legend()
plt.xlim(0.1,0.9)
#plt.ylim(0,20)
plt.savefig('PLOTS/rho_v_bulk.pdf')
#plt.show()


'''
