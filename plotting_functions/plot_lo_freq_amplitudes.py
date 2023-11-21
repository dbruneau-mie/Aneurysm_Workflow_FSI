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

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
ylim_v = 0.2
ylim_d = 1.4
end_t= 5.55 #3.804


#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.4
#ylim_d = 4.0
#end_t= 3.65 #3.804

#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
vel_csv_files = glob.glob(simDir + "/**/velocity_amplitude_0_to_25.csv", recursive = True)

print(vel_csv_files)

del_index=-1
for i in range(len(vel_csv_files)):
    if "remesh" in vel_csv_files[i]:
        del_index=i
if del_index>-1:
    del vel_csv_files[del_index]

vel_csv_files.sort(key=natural_keys)

print(vel_csv_files)
#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)

dvp_list=["v"]


fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(5.5,4.5)

for i in range(len(vel_csv_files)):

    for dvp in dvp_list:
        if "v" in dvp:
            viz_type = 'velocity'
            convert_factor = 1
            amp_file = vel_csv_files[i] # file name for amplitudes

        try:
            print(amp_file)
            output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
        except:
            print("file not found!")
            break
    
        print("point with max amplitude during this timeframe : {}".format(int(output_amplitudes[np.argmax(output_amplitudes[:,3]),12])))
        print("99th percentile value: {}".format(np.max(output_amplitudes[:,10])))
        print("max value: {}".format(np.max(output_amplitudes[:,3])))

        print("Time of max value: {}".format(output_amplitudes[np.argmax(output_amplitudes[:,3]),0]))

          
ax[1].set_xlabel('Physiological Time (s)')
amp_graph_file=simDir+'/99th_percentile_amplitudes_all_cases.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file, dpi=800)  
plt.close()
