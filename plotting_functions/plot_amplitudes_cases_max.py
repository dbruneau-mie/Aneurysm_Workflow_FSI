import matplotlib as mpl
mpl.use('Agg')
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
import postprocessing_common_h5py

"""
This script plots the compute time of the simulation graphically, from the logfiles generated on Scinet.

Args:
    case_path (Path): Path to results from simulation

"""

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#simDir="/$PROJECT/Pulsatile_Cases/Case16_m06_predeformed_finerflow"
#simDir="/project/s/steinman/dbruneau/Pulsatile_Cases/Case16_m06_predeformed_finerflow"
#simDir="/project/s/steinman/dbruneau/Pulsatile_Cases"

start_t=0.0 #2.853
end_t=3.65 #5.55#3.804

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
ylim_v = 0.4
ylim_d = 2
start_t=2.853
end_t=3.804

#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.75
#ylim_d = 5.0
#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
disp_csv_files = glob.glob(simDir + "/**/displacement_amplitude_25_to_1400.csv", recursive = True)
vel_csv_files = glob.glob(simDir + "/**/velocity_amplitude_25_to_1400.csv", recursive = True)
pressure_csv_files = glob.glob(simDir + "/**/pressure_amplitude_25_to_1400.csv", recursive = True)

print(vel_csv_files)

del_index=-1
for i in range(len(vel_csv_files)):
    if "remesh" in vel_csv_files[i]:
        del_index=i
if del_index>-1:
    del vel_csv_files[del_index]
    del disp_csv_files[del_index]
    del pressure_csv_files[del_index]

vel_csv_files.sort(key=natural_keys)
disp_csv_files.sort(key=natural_keys)
pressure_csv_files.sort(key=natural_keys)

print(vel_csv_files)
#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)

dvp_list=["v","d","p"]


fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(7,5.4)

for i in range(len(vel_csv_files)):

    for dvp in dvp_list:
        if "v" in dvp:
            viz_type = 'velocity'
            title = "RMS Velocity Amplitude, Spatial Max Value"
            label = "Amplitude (m/s)"
            convert_factor = 1
            amp_file = vel_csv_files[i] # file name for amplitudes
            ylim = ylim_v

            index = 1
        elif "d" in dvp:
            viz_type = 'displacement'
            title = "RMS Displacement Amplitude, Max Value"
            convert_factor = 1000000
            label = "Amplitude (\u03bcm)"
            amp_file = disp_csv_files[i] # file name for amplitudes
            ylim = ylim_d


            index = 0
        elif "p" in dvp:
            viz_type = 'pressure'
            index = 2 
            amp_file = pressure_csv_files[i] # file name for amplitudes

        else:
            print("Input d, v or p for dvp")

        ax[index].set_title(title)
        

        case_name = re.findall(r'case\d+', amp_file)[0]
        #amp_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
        try:
            print(amp_file)
            output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
        except:
            print("file not found!")
            break
    
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]<=end_t]
        ax[index].plot(output_amplitudes[:,0],output_amplitudes[:,3]*convert_factor,label=case_name)
        ax[index].set_ylabel(label)
        ax[index].set_ylim(0,ylim)

        ax[index].legend()

        print("point with max amplitude during this timeframe : {}".format(int(output_amplitudes[np.argmax(output_amplitudes[:,3]),12])))
        print("max value: {}".format(np.max(output_amplitudes[:,3])))
        print("99th Percentile value: {}".format(np.max(output_amplitudes[:,10])))

        print("Time of max value: {}".format(output_amplitudes[np.argmax(output_amplitudes[:,3]),0]))
