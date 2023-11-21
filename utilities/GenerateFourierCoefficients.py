import numpy as np
from os import path, makedirs, getcwd
from scipy.interpolate import UnivariateSpline
from scipy.integrate import simps, romberg

#///////////////////////////////////////////////////////////////
# Read Inflow wave form and return the flow rate at all times
def flow_waveform(Qmean, cycles, period, time_steps, FC):
    omega = (2.0 * np.pi / period) #* cycles
    an = []
    bn = []

    #Load the Fourier Coefficients
    infile_FC = open( path.join(path.dirname(path.abspath(__file__)), 'data', FC), 'r').readlines()
    for line in infile_FC:
        if line[0] != "#":
            print(line)
            abn = line.split()
            an.append(float(abn[0]))
            bn.append(float(abn[1]))

    t_values = np.linspace(0, period*cycles, num=time_steps)
    print(t_values)
    Q_values = []
    for t in t_values:
        Qn = 0 + 0j
        for i in range (len(an)):
            Qn = Qn + (an[i]-bn[i]*1j)*np.exp(1j*i*omega*t)
        Qn = abs(Qn)
        Q_values.append( Qmean * Qn )
        #print (t, Qn)
    return t_values, Q_values

#///////////////////////////////////////////////////////////////
# Read Inflow wave form and return the flow rate at all times
def flow_rate(Qmean, Q_norm):

    A = np.loadtxt(Q_norm, delimiter=' ')
    t_values=A[:,0]
    Q_values=A[:,1]
    Q_values = Qmean * Q_values

    return t_values, Q_values

#///////////////////////////////////////////////////////////////
# Read time series data into "time" and "values"
def read_from_file(data_file):
    time = []
    values = []

    #Load the Fourier Coefficients
    infile = open( path.join(path.dirname(path.abspath(__file__)), 'data', data_file), 'r').readlines()
    for line in infile:
        if "#" not in line:
            print(line)
            abn = line.split(",")
            time.append(float(abn[0]))
            values.append(float(abn[1]))
            print(line)

    return time, values


def fourier_coefficients(x, y, T, N):
    '''From x-array and y-spline and period T, calculate N complex Fourier coefficients.'''
    omega = 2*np.pi/T
    ck = []
    ck.append(1/T*simps(y(x), x))
    for n in range(1,N):
        c = 1/T*simps(y(x)*np.exp(-1j*n*omega*x), x)

        # Clamp almost zero real and imag components to zero
        if 1:
            cr = c.real
            ci = c.imag
            if abs(cr) < 1e-14: cr = 0.0
            if abs(ci) < 1e-14: ci = 0.0
            c = cr + ci*1j

        ck.append(2*c)
    ck = np.array(ck)
    return ck

# This script generates fourier coefficients from an input csv file of point data. It then reads the FCs in and plots the data.  

T=0.951
N = 10000
num_fourier_coefficients=20
cycles=1

# Read this file
time, values = read_from_file("p_t_sim.csv")
# Fit a spline to the data
transient_profile = UnivariateSpline(time, values, s=None, k=1)
# Compute fourier coefficients of transient profile
timedisc = np.linspace(0, T, N)
ck = fourier_coefficients(timedisc, transient_profile, T, num_fourier_coefficients)
average_val = ck.real[0]
# Convert from complex Fourier coefficients to standard fourier coefficinents
an, bn = ck.real/average_val, -ck.imag/average_val

# Save data
print(an, bn)
coeff_array= np.array([an,bn]).T
np.savetxt('data/FC_Pressure',coeff_array,delimiter='\t',header='Period = :{}'.format(T))

# Read in and generate point data from FC file that was just saved
mean_p_input = np.mean(values)
FC = "FC_Pressure"
t_values_FC, p_values_FC = flow_waveform(mean_p_input/1.01, cycles, T, N, FC)

pmin = np.min(p_values_FC)
pmax = np.max(p_values_FC)
pavg_check=np.mean(p_values_FC)
print(pmin/133.32)
print(pmax/133.32)
print(pavg_check/133.32)
print(mean_p_input/133.32)


import matplotlib.pyplot as plt

plt.plot(t_values_FC, p_values_FC) 
plt.plot(time, values) 

plt.legend(["FC_pressure","Input P Data"])
plt.xlabel('t')
#plt.xlim(0, 2.85)
plt.ylabel('p (Pa)')
plt.savefig("p_FC_data_k1.png")

