import numpy as np
from os import path, makedirs, getcwd


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

Qmean=1.0 # normalized
cycles=2
period=0.951
time_steps=3000

Qsimscale=Qmean/6.0E-06

Tsim=0.951
FC = "FC_fit_1_cycle_rev"
t_values, Q_values = flow_waveform(Qsimscale, cycles, Tsim, time_steps, FC)
FC = "FC_MCA_10"
t_values2, Q_values2 = flow_waveform(Qmean, cycles, Tsim, time_steps, FC)

Qmin = np.min(Q_values)
Qmax = np.max(Q_values)
print(Qmin)
print(Qmax)

FC = "FC_MCA_10_pressure"
p_mean=84.8
t_values3, p_values = flow_waveform(p_mean, cycles, Tsim, time_steps, FC)

pmin = np.min(p_values)
pmax = np.max(p_values)
pavg_check=np.mean(p_values)
print(pmin)
print(pmax)
print(pavg_check)


import matplotlib.pyplot as plt

plt.plot(t_values3, p_values) 
plt.legend(["FC_MCA_10_pressure"])
plt.xlabel('t')
#plt.xlim(0, 2.85)
plt.ylabel('p (Pa)')
plt.savefig("p_FC2.png")

plt.clf()

plt.plot(t_values,Q_values)
plt.plot(t_values2,Q_values2)
plt.legend(["FC_fit_1_cycle","FC_MCA_10"])
plt.xlabel('t')
#plt.xlim(0, 2.85)
plt.ylabel('Q (m^3/s')
plt.savefig("Qcompare.png")


#print(t_values,Q_values)