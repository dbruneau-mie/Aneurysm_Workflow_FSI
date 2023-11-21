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
cycles=10
period=0.951
time_steps=100000
FC = "FC_MCA"
t_values, Q_values = flow_waveform(Qmean, cycles, period, time_steps, FC)
FC = "FC_MCA_10"
t_values_10, Q_values_10 = flow_waveform(Qmean, cycles, period, time_steps, FC)
FC = "FC_ICA"
t_values_ICA, Q_values_ICA = flow_waveform(Qmean, cycles, period, time_steps, FC)
Q_norm="data/ICA_flow_rates"
t_values_ICA_Q, Q_values_ICA_Q = flow_rate(Qmean, Q_norm)

pmax=110*133.322
pmin=70*133.322

Qmin = np.min(Q_values_10)
Qmax = np.max(Q_values_10)

p_t_10 = (Q_values_10 - Qmin)*(pmax-pmin)/(Qmax-Qmin)   + pmin

Qmin = np.min(Q_values)
Qmax = np.max(Q_values)
p_t_30 = (Q_values - Qmin)*(pmax-pmin)/(Qmax-Qmin)   + pmin

#print(t_values_10[:-1])
#
#print(np.append(t_values_10[:-1],t_values_10+period))
np.savetxt("p_t.csv",np.transpose([t_values_10[:-1],p_t_10[:-1]]),delimiter=',',header='T (s),P (Pa)')
np.savetxt("Q_MCA_10",np.transpose([t_values_10[:-1],Q_values_10[:-1]]))
np.savetxt("Q_ICA",np.transpose([t_values_ICA[:-1],Q_values_ICA[:-1]]))

import matplotlib.pyplot as plt
plt.plot(t_values,p_t_30)
plt.plot(t_values_10, p_t_10) 
plt.legend(["FC_MCA","FC_MCA_10"])
plt.xlabel('t')
#plt.xlim(0, 2.85)
plt.ylabel('p (Pa)')
plt.savefig("p.png")

plt.clf()
plt.plot(t_values,Q_values)
plt.plot(t_values_10, Q_values_10) 
plt.plot(t_values_ICA,Q_values_ICA)
plt.plot(t_values_ICA_Q, Q_values_ICA_Q)
plt.legend(["FC_MCA","FC_MCA_10","FC_ICA","Q_ICA (KVS)"])
plt.xlabel('t')
#plt.xlim(0, 2.85)
plt.ylabel('Q (m^3/s')
plt.savefig("Q.png")

#print(t_values,Q_values)