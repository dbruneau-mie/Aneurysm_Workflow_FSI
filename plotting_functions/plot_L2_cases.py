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

start_t=0.0

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
ylim_v = 0.2
ylim_d = 0.002

#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Ramp_Cases_Steady"
#ylim_v = 0.25
#ylim_d = 2.5e-6
#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
disp_csv_files = glob.glob(simDir + "/**/d_L2_norm_compare_to_prev_cycle_log_normalized.csv", recursive = True)
vel_csv_files = glob.glob(simDir + "/**/v_L2_norm_compare_to_prev_cycle_log_normalized.csv", recursive = True)

print(vel_csv_files)

del_index=-1
for i in range(len(vel_csv_files)):
    if "remesh" in vel_csv_files[i]:
        del_index=i
if del_index>-1:
    del vel_csv_files[del_index]
    del disp_csv_files[del_index]

vel_csv_files.sort(key=natural_keys)
disp_csv_files.sort(key=natural_keys)
#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)

dvp_list=["v","d"]


fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(7,5.4)

for i in range(len(vel_csv_files)):

    for dvp in dvp_list:
        if "v" in dvp:
            viz_type = 'velocity'
            title = "Velocity"
            label = "L2 Norm - Normalized"
            data_file = vel_csv_files[i] # file name for amplitudes
            ylim = ylim_v

            index = 1
        elif "d" in dvp:
            viz_type = 'displacement'
            title = "Displacement"
            label = "L2 Norm - Normalized"
            data_file = disp_csv_files[i] # file name for amplitudes
            ylim = ylim_d


            index = 0
        else:
            print("Input d, v or p for dvp")

        ax[index].set_title(title)
        

        case_name = re.findall(r'case\d+', data_file)[0]
        case_name = case_name.replace("case", "Case ")

        #data_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
        try:
            print(data_file)
            output_L2 = np.genfromtxt(data_file, delimiter=',')
        except:
            print("file not found!")
            break
    
        output_L2=output_L2[output_L2[:,0]>=start_t]
        ax[index].plot(output_L2[:,0],output_L2[:,1],label=case_name,linewidth=0.5)
        ax[index].set_ylabel(label)
        #ax[index].set_ylim(0,ylim)
        ax[index].set_yscale("log")


        ax[index].legend()


          
ax[1].set_xlabel('Physiological Time (s)')
amp_graph_file=simDir+'/L2_Norm_all_cases_log.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file)  
plt.close()
