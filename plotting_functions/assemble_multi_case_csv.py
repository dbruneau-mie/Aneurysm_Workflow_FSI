import matplotlib as mpl
mpl.use('Agg')
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import re
#import postprocessing_common_h5py
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

start_t= 2.853 #0.951

#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/AllCases"
ylim_v = 0.5
ylim_d = 5
ylim_p = 300
end_t= 3.8 #3.804

simDirSurgCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile_CFD"
simDirSurgFSI = "/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile"
simDirSurgModal="/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Modal"
simDirPulsCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC_CFD_undeformed"
simDirPulsFSI = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
simDirPulsModal = "/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation_All_Cases"


#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.4
#ylim_d = 4.0
#end_t= 3.65 #3.804

#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")
disp_csv_files = glob.glob(simDirPulsFSI + "/**/displacement_amplitude_25_to_1400.csv", recursive = True)
vel_csv_files = glob.glob(simDirPulsFSI + "/**/velocity_amplitude_25_to_1400.csv", recursive = True)
pressure_csv_files = glob.glob(simDirPulsFSI + "/**/pressure_amplitude_25_to_1400.csv", recursive = True)
vel_csv_files_cfd = glob.glob(simDirPulsCFD + "/**/velocity_amplitude_25_to_1400.csv", recursive = True)
pressure_csv_files_cfd = glob.glob(simDirPulsCFD + "/**/pressure_amplitude_25_to_1400.csv", recursive = True)

disp_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/displacement_amplitude_25_to_1400.csv", recursive = True)
vel_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/velocity_amplitude_25_to_1400.csv", recursive = True)
pressure_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/pressure_amplitude_25_to_1400.csv", recursive = True)
vel_csv_files_cfd_Surg = glob.glob(simDirSurgCFD + "/**/velocity_amplitude_25_to_1400.csv", recursive = True)
pressure_csv_files_cfd_Surg = glob.glob(simDirSurgCFD + "/**/pressure_amplitude_25_to_1400.csv", recursive = True)

csv_modal_freqs = glob.glob(simDirPulsModal + "/**/modal_freqencies.csv", recursive = True)
csv_modal_freqs_Surg = glob.glob(simDirSurgModal + "/**/modal_freqencies.csv", recursive = True)

neck_csv_files_Puls = glob.glob(simDirPulsCFD + "/**/*neck_area_and_volume.csv", recursive = True)
neck_csv_files_Surg = glob.glob(simDirSurgCFD + "/**/*neck_area_and_volume.csv", recursive = True)


#del_index=-1
#for i in range(len(vel_csv_files)):
#    if "remesh" in vel_csv_files[i]:
#        del_index=i
#if del_index>-1:
#    del vel_csv_files[del_index]
#    del disp_csv_files[del_index]
#    del pressure_csv_files[del_index]
neck_csv_files_Puls.sort(key=natural_keys)
neck_csv_files_Surg.sort(key=natural_keys)

csv_modal_freqs.sort(key=natural_keys)
csv_modal_freqs_Surg.sort(key=natural_keys)

disp_csv_files.sort(key=natural_keys)
vel_csv_files.sort(key=natural_keys)
pressure_csv_files.sort(key=natural_keys)
vel_csv_files_cfd.sort(key=natural_keys)
pressure_csv_files_cfd.sort(key=natural_keys)

disp_csv_files_Surg.sort(key=natural_keys)
vel_csv_files_Surg.sort(key=natural_keys)
pressure_csv_files_Surg.sort(key=natural_keys)
vel_csv_files_cfd_Surg.sort(key=natural_keys)
pressure_csv_files_cfd_Surg.sort(key=natural_keys)

disp_csv_files.extend(disp_csv_files_Surg)
vel_csv_files.extend(vel_csv_files_Surg)
pressure_csv_files.extend(pressure_csv_files_Surg)
vel_csv_files_cfd.extend(vel_csv_files_cfd_Surg)
pressure_csv_files_cfd.extend(pressure_csv_files_cfd_Surg)

csv_modal_freqs.extend(csv_modal_freqs_Surg)

df_neck = []
for idx, neck_csv_file in enumerate(neck_csv_files_Puls):
    print(idx)
    if idx == 0:
        df_neck = pd.read_csv(neck_csv_file)
    else:
        df = pd.read_csv(neck_csv_file)
        df_neck = pd.concat([df_neck,df], ignore_index=True)

for idx, neck_csv_file in enumerate(neck_csv_files_Surg):
    df = pd.read_csv(neck_csv_file)
    df_neck = pd.concat([df_neck,df], ignore_index=True)

modal_freqs = []
for idx, modal_csv_file in enumerate(csv_modal_freqs):
    modal_freqs.append(np.loadtxt(modal_csv_file))

modal_freqs=np.array(modal_freqs)
print(modal_freqs)
#print(modal_freqs[0])
print(modal_freqs.shape)
print(modal_freqs[:,0])
print(modal_freqs[0,:])

df_neck["Mode 0 frequency"] = modal_freqs[:,0]
df_neck["Mode 1 frequency"] = modal_freqs[:,1]
df_neck["Mode 2 frequency"] = modal_freqs[:,2]
df_neck["Mode 3 frequency"] = modal_freqs[:,3]
sac_volume = df_neck["sac_volume"]

#                                # MASS            *  Frequency ^  2
df_neck["Mode 1 stiffness"] = (sac_volume*1e3/1e9)*(df_neck["Mode 1 frequency"]*2*3.14159)**2 
df_neck["Mode 2 stiffness"] = (sac_volume*1e3/1e9)*(df_neck["Mode 2 frequency"]*2*3.14159)**2  
df_neck["Mode 3 stiffness"] = (sac_volume*1e3/1e9)*(df_neck["Mode 3 frequency"]*2*3.14159)**2 


print(df_neck)

print(pressure_csv_files)
print(vel_csv_files)
print(vel_csv_files_cfd)

#amplitude_files=[file for file in os.listdir(visualization_hi_pass_folder) if '.csv' in file and 'magnitude' in file]


#n_outfiles = len(amplitude_files)
#print(n_outfiles)
#print(amplitude_files)

dvp_list=["v_fsi","d_fsi","v_cfd","p_fsi","p_cfd"]


fig, ax = plt.subplots(len(dvp_list),1)
fig.set_size_inches(8,8)


max_amp_vel_cfd = []
max_amp_vel = []
max_amp_disp = []
p99th_amp_vel_cfd = []
p99th_amp_vel = []
p99th_amp_disp = []

t_avg_max_amp_vel_cfd = []
t_avg_max_amp_vel = []
t_avg_max_amp_disp = []
t_avg_p99th_amp_vel_cfd = []
t_avg_p99th_amp_vel = []
t_avg_p99th_amp_disp = []

filename_amp_vel_cfd = []
filename_amp_vel = []
filename_amp_disp = []

max_amp_pres_cfd = []
max_amp_pres = []
p99th_amp_pres_cfd = []
p99th_amp_pres = []

t_avg_max_amp_pres_cfd = []
t_avg_max_amp_pres = []
t_avg_p99th_amp_pres_cfd = []
t_avg_p99th_amp_pres = []

filename_amp_pres_cfd = []
filename_amp_pres = []

for i in range(len(vel_csv_files)):

    for dvp in dvp_list:
        if "v_fsi" in dvp:
            viz_type = 'velocity'
            #title = "RMS Velocity Amplitude, Spatial 99th Percentile"
            title = "Flow Instability Amplitude"
            label = "Amplitude (m/s)"
            convert_factor = 1
            amp_file = vel_csv_files[i] # file name for amplitudes
            ylim = ylim_v

            index = 1
        elif "d_fsi" in dvp:
            viz_type = 'displacement'
            #title = "RMS Displacement Amplitude, Spatial 99th Percentile"
            title = "Vibration Amplitude"

            convert_factor = 1000000
            label = "Amplitude (\u03bcm)"
            amp_file = disp_csv_files[i] # file name for amplitudes
            ylim = ylim_d


            index = 0

        if "v_cfd" in dvp:
            viz_type = 'velocity_cfd'
            #title = "RMS Velocity Amplitude, Spatial 99th Percentile"
            title = "Flow Instability Amplitude CFD"
            label = "Amplitude (m/s)"
            convert_factor = 1
            amp_file = vel_csv_files_cfd[i] # file name for amplitudes
            ylim = ylim_v

            index = 2

        elif "p_fsi" in dvp:
            viz_type = 'pressure'
            title = "Pressure Instability Amplitude"
            label = "Amplitude (Pa)"
            index = 3
            amp_file = pressure_csv_files[i] # file name for amplitudes
            ylim = ylim_p
        elif "p_cfd" in dvp:
            viz_type = 'pressure'
            title = "Pressure Instability Amplitude CFD"
            label = "Amplitude (Pa)"
            index = 4 
            amp_file = pressure_csv_files_cfd[i] # file name for amplitudes
            ylim = ylim_p

        else:
            print("Input d, v or p for dvp")

        ax[index].set_title(title)
        
        print(amp_file)

        try:
            case_name = re.findall(r'case\d+', amp_file)[0]
        except:
            case_name = re.findall(r'MCA\d+', amp_file)[0]

        #case_name = case_name.replace("case", "Case ")
        #amp_file = visualization_hi_pass_folder+'/'+amplitude_files[i]
        try:
            print(amp_file)
            output_amplitudes = np.genfromtxt(amp_file, delimiter=',')
        except:
            print("file not found!")
            break

        #if "Pulsatile_Ramp_Cases_FC_CFD_undeformed" in amp_file:
        #    output_amplitudes[:,0] = output_amplitudes[:,0]+0.951
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]<=end_t]

        ax[index].plot(output_amplitudes[:,0],output_amplitudes[:,10]*convert_factor,label=case_name)
        ax[index].set_ylabel(label)
        ax[index].set_ylim(-0.01,ylim)
        if index == 4:
            ax[index].legend()

        print("point with max amplitude during this timeframe : {}".format(int(output_amplitudes[np.argmax(output_amplitudes[:,3]),12])))
        p99th_amp = np.max(output_amplitudes[:,10])
        t_avg_p99th_amp = np.mean(output_amplitudes[:,10])

        print("99th percentile value: {}".format(p99th_amp))
        max_amp = np.max(output_amplitudes[:,3])
        t_avg_max_amp = np.mean(output_amplitudes[:,3])
        print("max value: {}".format(max_amp))

        print("Time of max value: {}".format(output_amplitudes[np.argmax(output_amplitudes[:,3]),0]))


        if "v_fsi" in dvp:
            max_amp_vel.append(max_amp)
            p99th_amp_vel.append(p99th_amp)
            t_avg_max_amp_vel.append(t_avg_max_amp)
            t_avg_p99th_amp_vel.append(t_avg_p99th_amp)
            filename_amp_vel.append(case_name)
        elif "d_fsi" in dvp:
            max_amp_disp.append(max_amp)
            p99th_amp_disp.append(p99th_amp)
            t_avg_max_amp_disp.append(t_avg_max_amp)
            t_avg_p99th_amp_disp.append(t_avg_p99th_amp)
            filename_amp_disp.append(case_name)
        elif "v_cfd" in dvp:
            max_amp_vel_cfd.append(max_amp)
            p99th_amp_vel_cfd.append(p99th_amp)
            t_avg_max_amp_vel_cfd.append(t_avg_max_amp)
            t_avg_p99th_amp_vel_cfd.append(t_avg_p99th_amp)
            filename_amp_vel_cfd.append(case_name)
        elif "p_fsi" in dvp:
            max_amp_pres.append(max_amp)
            p99th_amp_pres.append(p99th_amp)
            t_avg_max_amp_pres.append(t_avg_max_amp)
            t_avg_p99th_amp_pres.append(t_avg_p99th_amp)
            filename_amp_pres.append(case_name)
        elif "p_cfd" in dvp:
            max_amp_pres_cfd.append(max_amp)
            p99th_amp_pres_cfd.append(p99th_amp)
            t_avg_max_amp_pres_cfd.append(t_avg_max_amp)
            t_avg_p99th_amp_pres_cfd.append(t_avg_p99th_amp)
            filename_amp_pres_cfd.append(case_name)
          
ax[1].set_xlabel('Physiological Time (s)')
amp_graph_file=simDir+'/99th_percentile_amplitudes_all_cases_surg_puls_dvp_onecycle.png' # file name for amplitudes
fig.tight_layout()
plt.savefig(amp_graph_file, dpi=800)  
plt.close()

print(len(max_amp_pres))
print(df_neck)
print(df_neck.shape)
df_neck["max velocity amplitude"] = max_amp_vel
df_neck["99th percentile velocity amplitude"] = p99th_amp_vel
df_neck["max velocity amplitude temporal average"] = t_avg_max_amp_vel
df_neck["99th percentile velocity amplitude temporal average"] = t_avg_p99th_amp_vel
df_neck["case name vel"] = filename_amp_vel

df_neck["max velocity amplitude CFD"] = max_amp_vel_cfd
df_neck["99th percentile velocity amplitude CFD"] = p99th_amp_vel_cfd
df_neck["max velocity amplitude CFD temporal average"] = t_avg_max_amp_vel_cfd
df_neck["99th percentile velocity amplitude CFD temporal average"] = t_avg_p99th_amp_vel_cfd
df_neck["case name vel CFD"] = filename_amp_vel_cfd

df_neck["max displacement amplitude"] = max_amp_disp
df_neck["99th percentile displacement amplitude"] = p99th_amp_disp
df_neck["max displacement amplitude temporal average"] = t_avg_max_amp_disp
df_neck["99th percentile displacement amplitude temporal average"] = t_avg_p99th_amp_disp
df_neck["case name disp"] = filename_amp_disp

df_neck["max pressure amplitude"] = max_amp_pres
df_neck["99th percentile pressure amplitude"] = p99th_amp_pres
df_neck["max pressure amplitude temporal average"] = t_avg_max_amp_pres
df_neck["99th percentile pressure amplitude temporal average"] = t_avg_p99th_amp_pres
df_neck["case name pres"] = filename_amp_pres

df_neck["max pressure amplitude CFD"] = max_amp_pres_cfd
df_neck["99th percentile pressure amplitude CFD"] = p99th_amp_pres_cfd
df_neck["max pressure amplitude CFD temporal average"] = t_avg_max_amp_pres_cfd
df_neck["99th percentile pressure amplitude CFD temporal average"] = t_avg_p99th_amp_pres_cfd
df_neck["case name pres CFD"] = filename_amp_pres_cfd




csv_out_file=simDir+'/all_case_data_with_modes.csv' # file name for amplitudes
print(df_neck.head(17))
df_neck.to_csv(csv_out_file)
