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

start_t=2.851
end_t=3.804

#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases"
#ylim_v = 0.2
#ylim_d = 2

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
ylim_v = 0.25
ylim_d = 2.5
#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
disp_csv_files_all = glob.glob(simDir + "/**/displacement_point_id**", recursive = True)
vel_csv_files_all = glob.glob(simDir + "/**/velocity_point_id**", recursive = True)
pressure_csv_files_all = glob.glob(simDir + "/**/pressure_point_id**", recursive = True)

#point_ids_d = [22036,19618,654,7895,1437,25077]
#point_ids_v = [16413,7814,12399,10150,11729,17190]
#point_ids_p = [160,13060,12627,336,908,11404]
point_ids_d = [22036,1872,2026,1805,2138,373]
point_ids_v = [13706,15196,16417,9592,13612,17190]
point_ids_p = [160,3605,12627,4976,811,11404]

vel_csv_files=[]
for i in range(len(vel_csv_files_all)):
    if any([str(x) in vel_csv_files_all[i] for x in point_ids_v]):
        vel_csv_files.append(vel_csv_files_all[i])

pressure_csv_files=[]
for i in range(len(pressure_csv_files_all)):
    if any([str(x) in pressure_csv_files_all[i] for x in point_ids_p]):
        pressure_csv_files.append(pressure_csv_files_all[i])

disp_csv_files=[]
for i in range(len(disp_csv_files_all)):
    if  any([str(x) in disp_csv_files_all[i] for x in point_ids_d]):
        disp_csv_files.append(disp_csv_files_all[i])

print(vel_csv_files)

vel_csv_files.sort(key=natural_keys)
disp_csv_files.sort(key=natural_keys)
pressure_csv_files.sort(key=natural_keys)
#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)

dvp_list=["v","d"]


fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(4,6)

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
            title = "Velocity of Point w. Max Amplitude"
            label = "Velocity (m/s)"
            convert_factor = 1
            amp_file = vel_csv_files[i] # file name for amplitudes
            ylim = ylim_v

            index = 1
        elif "d" in dvp:
            viz_type = 'displacement'
            title = "Displacement of Point w. Max Amplitude"
            convert_factor = 1000000
            label = "Displacement (\u03bcm)"
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

        if "d" in dvp:
            plot_amplitude = (output_amplitudes[:,1]-output_amplitudes[0,1])*convert_factor
        else:
            plot_amplitude = (output_amplitudes[:,1])*convert_factor

        ax[index].plot(plot_time,plot_amplitude,label=case_name,linewidth=0.5)
        ax[index].set_ylabel(label)
        #ax[index].set_ylim(0,ylim)
        ax[index].legend()

        if "v" in dvp:
            if i == 0:
                header_txt_v.append("Time (s)")
                output_csv_data_v.append(plot_time)            
            header_txt_v.append(case_name + " Velocity (m/s)")
            output_csv_data_v.append(plot_amplitude)
        elif "d" in dvp:
            if i == 0:
                header_txt_d.append("Time (s)")
                output_csv_data_d.append(plot_time)            
            header_txt_d.append(case_name + " Displacement (\u03bcm)")
            output_csv_data_d.append(plot_amplitude)
        elif "p" in dvp:
            if i == 0:
                header_txt_p.append("Time (s)")
                output_csv_data_p.append(plot_time)            
            header_txt_p.append(case_name + " Pressure (Pa)")
            output_csv_data_p.append(plot_amplitude)
          
ax[1].set_xlabel('Physiological Time (s)')
amp_graph_file=simDir+'/point_traces_all_cases.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file, dpi=800)  
plt.close()

for dvp in dvp_list:
    if "v" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_d).T,columns=header_txt_d)
        csv_out_file=simDir+'/disp_point_traces.csv' # file name for amplitudes
        df.to_csv(csv_out_file)
    elif "d" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_v).T,columns=header_txt_v)
        csv_out_file=simDir+'/vel_point_traces.csv' # file name for amplitudes
        df.to_csv(csv_out_file)
    elif "p" in dvp:
        df = pd.DataFrame(np.row_stack(output_csv_data_p).T,columns=header_txt_p)
        csv_out_file=simDir+'/pres_point_traces.csv' # file name for amplitudes
        df.to_csv(csv_out_file)