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
end_t=5.55#3.65 #3.804

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Pulsatile_New_Solver"
ylim_v = 0.2
ylim_d = 1

#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.4
#ylim_d = 4.0
#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
disp_csv_files = glob.glob(simDir + "/**/displacement_amplitude_25_to_1402.csv", recursive = True)
#case_list = glob.glob(simDir + "/**Case**")
case_list = ["Case3","Case8","Case9","Case11","Case12","Case16"]
bands_list = [["25_to_1402","pass","195_to_245"],
              ["25_to_1402"],
              ["25_to_1402","pass","335_to_370","455_to_485","485_to_510"],
              ["25_to_1402"],
              ["25_to_1402","pass","95_to_135","160_to_190"],
              ["25_to_1402","pass","120_to_140","155_to_175","180_to_200"]]
band_plot_names = ["All Vibration > 25 Hz", "Bruit", "Mode 1", "Mode 2", "Mode 3"]

print(case_list)
print(len(case_list))

#del_index=-1
#for i in range(len(vel_csv_files)):
#    if "remesh" in vel_csv_files[i]:
#        del_index=i
#if del_index>-1:
#    del vel_csv_files[del_index]
#    del disp_csv_files[del_index]
#    del pressure_csv_files[del_index]
#
#vel_csv_files.sort(key=natural_keys)
#disp_csv_files.sort(key=natural_keys)
#pressure_csv_files.sort(key=natural_keys)
#
#print(vel_csv_files)
#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)



#fig, ax = plt.subplots(1,len(case_list))
fig, ax = plt.subplots(1,len(case_list))

fig.set_size_inches(16,3)

for idx, case_name in enumerate(case_list):
    case_dir = glob.glob(simDir + "/**"+case_name+"**")[0]
    disp_csv_files = glob.glob(case_dir + "/**/displacement_amplitude**.csv", recursive = True)
    print(disp_csv_files)
    for idy, band in enumerate(bands_list[idx]):

        amp_file = glob.glob(case_dir + "/**/displacement_amplitude_"+band+"**.csv", recursive = True)[0]


        case_name = re.findall(r'case\d+', amp_file)[0]
        viz_type = 'displacement'
        title = case_name #"RMS Displacement Amplitude, Spatial 99th Percentile"
        convert_factor = 1000000
        label = "Amplitude (\u03bcm)"
        ylim = ylim_d

        ax[idx].set_title(title)
        

        output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
    
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]<=end_t]
        ax[idx].plot(output_amplitudes[:,0],output_amplitudes[:,10]*convert_factor,label=band_plot_names[idy])
        ax[idx].set_ylabel(label)
        ax[idx].set_ylim(0,ylim)

        ax[idx].legend()

        print("point with max amplitude during this timeframe : {}".format(int(output_amplitudes[np.argmax(output_amplitudes[:,3]),12])))
        #print(np.max(output_amplitudes[:,3]))
        #print(output_amplitudes[np.argmax(output_amplitudes[:,3]),3])

          
ax[1].set_xlabel('Simulation Time (s)')
amp_graph_file=simDir+'/99th_percentile_amplitudes_separate graphs_multiband.png' # file name for amplitudes
#fig.tight_layout()
plt.savefig(amp_graph_file)  
plt.close()
