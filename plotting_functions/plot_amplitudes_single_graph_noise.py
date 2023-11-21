import matplotlib as mpl
mpl.use('Agg')
import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import postprocessing_common_h5py

"""
This script plots the compute time of the simulation graphically, from the logfiles generated on Scinet.

Args:
    case_path (Path): Path to results from simulation

"""


visualization_hi_pass_folder = "/media/db_ubuntu/Backup Plus/Results_Ramp/InletNoise/Fine/Case9_m047_predeformed_noise_lateral/Visualization_hi_pass"
#visualization_hi_pass_folder = "/media/db_ubuntu/Backup Plus/Results_Ramp/InletNoise/Fine/Case16_m06_predeformed_noise_lateral/Visualization_hi_pass"

# find all logfiles in simulaation folder (file name must contain the word "logfile")
amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]

n_outfiles = len(amplitude_files)
print(n_outfiles)
print(amplitude_files)

dvp_list=["v","d"]
bands="25,100000,95,140,345,375"
#bands="25,100000,25,120,120,150,150,180,180,210"

convert_name = "Avg. Inlet Velocity (m/s)" # 'Simulation Time (s)'
convert_a = 0.239880/2 # 1.0
convert_b = 2.4679*convert_a

start_t=0.0
bands_list = bands.split(",")
num_bands = int(len(bands_list)/2)
lower_freq = np.zeros(num_bands)
higher_freq = np.zeros(num_bands)
fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(8,6)

for i in range(num_bands):
    lower_freq[i] = float(bands_list[2*i])
    higher_freq[i] = float(bands_list[2*i+1])
    for dvp in dvp_list:
        if "v" in dvp:
            viz_type = 'velocity'
            title = "RMS Velocity Amplitude, Spatial 99th Percentile"
            label = "Amplitude (m/s)"

            index = 0
        elif "d" in dvp:
            viz_type = 'displacement'
            title = "RMS Displacement Amplitude, Spatial 99th Percentile"
            label = "Amplitude (m)"
            index = 1
        elif "p" in dvp:
            viz_type = 'pressure'
            index = 2
        else:
            print("Input d, v or p for dvp")

        ax[index].set_title(title)

        viz_type = viz_type+"_amplitude_"+str(lower_freq[i])+"_to_"+str(higher_freq[i])
        amp_file = visualization_hi_pass_folder+'/'+viz_type+'.csv' # file name for amplitudes
        #amp_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
        try:
            print(amp_file)
            output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
        except:
            print("file not found!")
            break
    
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]

        x_plot = output_amplitudes[:,0]*convert_a + convert_b # Convert units of x axis
        ax[index].plot(x_plot,output_amplitudes[:,10],label="{} Hz to {} Hz".format(lower_freq[i],higher_freq[i]))
        ax[index].set_ylabel(label)
        ax[index].legend()

          
ax[index].set_xlabel(convert_name)
amp_graph_file=visualization_hi_pass_folder+'/99th_percentile_amplitudes_all_bands_3.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file)  
plt.close()