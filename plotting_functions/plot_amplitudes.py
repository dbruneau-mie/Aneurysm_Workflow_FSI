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

# Get input path
case_path = postprocessing_common_h5py.read_command_line()[0] 
case_name = os.path.basename(os.path.normpath(case_path)) # obtains only last folder in case_path
visualization_path = postprocessing_common_h5py.get_visualization_path(case_path)
visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")

# Get output path
imageFolder = os.path.join(visualization_path,'..',"Images")
if not os.path.exists(imageFolder):
    os.makedirs(imageFolder)

visualization_hi_pass_folder = "/media/db_ubuntu/Backup Plus/Results_Ramp/Case16_predeformed/New/visualization_hi_pass"
# find all logfiles in simulaation folder (file name must contain the word "logfile")
amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]

n_outfiles = len(amplitude_files)
print(n_outfiles)
print(amplitude_files)

dvp="v"
bands="25,100000,25,120,120,150,150,180,180,205"
start_t=2.4679
bands_list = bands.split(",")
num_bands = int(len(bands_list)/2)
lower_freq = np.zeros(num_bands)
higher_freq = np.zeros(num_bands)
for i in range(num_bands):
    lower_freq[i] = float(bands_list[2*i])
    higher_freq[i] = float(bands_list[2*i+1])

    if "v" in dvp:
        viz_type = 'velocity'
    elif "d" in dvp:
        viz_type = 'displacement'
    elif "p" in dvp:
        viz_type = 'pressure'
    else:
        print("Input d, v or p for dvp")
    viz_type = viz_type+"_amplitude_"+str(lower_freq[i])+"_to_"+str(higher_freq[i])
    amp_file = visualization_hi_pass_folder+'/'+viz_type+'.csv' # file name for amplitudes
    #amp_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
    print(amp_file)

    try:
        print(amp_file)
        output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
    except:
        print("file not found!")
        break
    output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
    plt.plot(output_amplitudes[:,0],output_amplitudes[:,10],label="99th percentile amplitude")
    plt.plot(output_amplitudes[:,0],output_amplitudes[:,11],label="1st percentile amplitude")
    plt.title('Amplitude Percentiles')
    plt.ylabel('Amplitude (units depend on d, v or p)')
    plt.xlabel('Simulation Time (s)')
    plt.legend()
    amp_graph_file=amp_file.replace(".csv",".png")
    plt.savefig(amp_graph_file)  
    plt.close()