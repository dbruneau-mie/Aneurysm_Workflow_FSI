import matplotlib as mpl
mpl.use('Agg')
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
import postprocessing_common_h5py
import pandas as pd

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


simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Steady_Ramp_Cases_FC_Qmax"
ylim_v = 0.3
ylim_d = 1.5
end_t= 3.65 #3.804
ylim_c3 = 15.0
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

dvp_list=["v","d"]


fig, ax = plt.subplots(3,1,gridspec_kw={"height_ratios":[0.2, 1,1]})
fig.set_size_inches(5.5,5.5)

output_csv_data_d = []
header_txt_d = []
output_csv_data_v = []
header_txt_v = []
output_csv_data_p = []
header_txt_p = []
for i in range(len(vel_csv_files)):



    for dvp in dvp_list:
        if "v" in dvp:
            viz_type = 'velocity'
            #title = "RMS Velocity Amplitude, Spatial 99th Percentile"
            title = "Flow Instability Amplitude"
            label = "Amplitude (m/s)"
            convert_factor = 1
            amp_file = vel_csv_files[i] # file name for amplitudes
            ylim = ylim_v

            index = 2
        elif "d" in dvp:
            viz_type = 'displacement'
            #title = "RMS Displacement Amplitude, Spatial 99th Percentile"
            title = "Vibration Amplitude"

            convert_factor = 1000000
            label = "Amplitude (\u03bcm)"
            amp_file = disp_csv_files[i] # file name for amplitudes
            ylim = ylim_d


            index = 1

        elif "p" in dvp:
            viz_type = 'pressure'
            index = 3 
            amp_file = pressure_csv_files[i] # file name for amplitudes

        else:
            print("Input d, v or p for dvp")
        

        

        case_name = re.findall(r'case\d+', amp_file)[0]
        case_name = case_name.replace("case", "Case ")
        #amp_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
        try:
            print(amp_file)
            output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
        except:
            print("file not found!")
            break
    
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]<=end_t]

        plot_time = output_amplitudes[:,0]
        plot_amplitude = output_amplitudes[:,10]*convert_factor

        ax[index].plot(plot_time,plot_amplitude,label=case_name)
        ax[index].set_ylabel(label)
        ax[index].set_ylim(0,ylim)
        if dvp == "v":
            ax[index].set_title(title)
            #ax[index].legend()

        if "Case 3" in case_name and "d" in dvp:
            ax[0].plot(plot_time,plot_amplitude)
            #ax[0].set_ylabel(label)
            ax[0].set_ylim(ylim,ylim_c3) 
            ax[0].set_xticklabels([])
            ax[0].set_title(title)

        print("point with max amplitude during this timeframe : {}".format(int(output_amplitudes[np.argmax(output_amplitudes[:,3]),12])))
        print("99th percentile value: {}".format(np.max(output_amplitudes[:,10])))
        print("max value: {}".format(np.max(output_amplitudes[:,3])))

        print("Time of max value: {}".format(output_amplitudes[np.argmax(output_amplitudes[:,3]),0]))

        if "v" in dvp:
            if i == 0:
                header_txt_v.append("Time (s)")
                output_csv_data_v.append(plot_time)            
            header_txt_v.append(case_name + " Amplitude (m/s)")
            output_csv_data_v.append(plot_amplitude)
        elif "d" in dvp:
            if i == 0:
                header_txt_d.append("Time (s)")
                output_csv_data_d.append(plot_time)            
            header_txt_d.append(case_name + " Amplitude (\u03bcm)")
            output_csv_data_d.append(plot_amplitude)
        elif "p" in dvp:
            if i == 0:
                header_txt_p.append("Time (s)")
                output_csv_data_p.append(plot_time)            
            header_txt_p.append(case_name + " Amplitude (Pa)")
            output_csv_data_p.append(plot_amplitude)

          
ax[2].set_xlabel('Physiological Time (s)')
amp_graph_file=simDir+'/99th_percentile_amplitudes_all_cases_qmax.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file, dpi=800)  
plt.close()


for dvp in dvp_list:
    if "v" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_d).T,columns=header_txt_d)
        csv_out_file=simDir+'/disp_99th_percentile_amplitudes_bands.csv' # file name for amplitudes
        df.to_csv(csv_out_file)
    elif "d" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_v).T,columns=header_txt_v)
        csv_out_file=simDir+'/vel_99th_percentile_amplitudes_bands.csv' # file name for amplitudes
        df.to_csv(csv_out_file)
    elif "p" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_p).T,columns=header_txt_p)
        csv_out_file=simDir+'/pres_99th_percentile_amplitudes_bands.csv' # file name for amplitudes
        df.to_csv(csv_out_file)