import os
import glob
import numpy as np
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


#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/AllCases"
start_t=0.951 #2.853
end_t= 3.8 #3.804

start_t_sys = 3.0
end_t_sys = 3.2

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
disp_csv_files = glob.glob(simDirPulsFSI + "/**/d_mag**SBI.csv", recursive = True)
vel_csv_files = glob.glob(simDirPulsFSI + "/**/v_mag**SBI.csv", recursive = True)
pressure_csv_files = glob.glob(simDirPulsFSI + "/**/p**SBI.csv", recursive = True)
vel_csv_files_cfd = glob.glob(simDirPulsCFD + "/**/v_mag**SBI.csv", recursive = True)
pressure_csv_files_cfd = glob.glob(simDirPulsCFD + "/**/p**SBI.csv", recursive = True)

disp_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/d_mag**SBI.csv", recursive = True)
vel_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/v_mag**SBI.csv", recursive = True)
pressure_csv_files_Surg = glob.glob(simDirSurgFSI + "/**/p**SBI.csv", recursive = True)
vel_csv_files_cfd_Surg = glob.glob(simDirSurgCFD + "/**/v_mag**SBI.csv", recursive = True)
pressure_csv_files_cfd_Surg = glob.glob(simDirSurgCFD + "/**/p**SBI.csv", recursive = True)



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


print(pressure_csv_files)
print(vel_csv_files)
print(vel_csv_files_cfd)

print(len(disp_csv_files ))
print(len(vel_csv_files ))
print(len(pressure_csv_files ))
print(len(vel_csv_files_cfd ))
print(len(pressure_csv_files_cfd ))

dvp_list=["v_fsi","d_fsi","v_cfd","p_fsi","p_cfd"]

SBI_Max_vel_cfd = []
SBI_Max_vel = []
SBI_Max_disp = []
SBI_Max_pres_cfd = []
SBI_Max_pres = []


SBI_Avg_vel_cfd = []
SBI_Avg_vel = []
SBI_Avg_disp = []
SBI_Avg_pres_cfd = []
SBI_Avg_pres = []

SBI_Sys_vel_cfd = []
SBI_Sys_vel = []
SBI_Sys_disp = []
SBI_Sys_pres_cfd = []
SBI_Sys_pres = []

filename_amp_vel_cfd = []
filename_amp_vel = []
filename_amp_disp = []
filename_amp_pres_cfd = []
filename_amp_pres = []


for i in range(len(vel_csv_files)):

    for dvp in dvp_list:
        if "v_fsi" in dvp:
            SBI_file = vel_csv_files[i] # file name for SBIs
        elif "d_fsi" in dvp:
            SBI_file = disp_csv_files[i] # file name for SBIs
        elif "v_cfd" in dvp:
            SBI_file = vel_csv_files_cfd[i] # file name for SBIs
        elif "p_fsi" in dvp:
            SBI_file = pressure_csv_files[i] # file name for SBIs
        elif "p_cfd" in dvp:
            SBI_file = pressure_csv_files_cfd[i] # file name for SBIs

        else:
            print(dvp)
            print("Input d, v or p for dvp")
    
        #print(SBI_file)

        try:
            case_name = re.findall(r'case\d+', SBI_file)[0]
        except:
            case_name = re.findall(r'MCA\d+', SBI_file)[0]

        #case_name = case_name.replace("case", "Case ")
        #SBI_file = visualization_hi_pass_folder+'/'+SBI_files[i]
        try:
            output_SBIs = np.genfromtxt(SBI_file, delimiter=',')
        except:
            print("file not found!")
            break
        
        if "A17" in case_name and dvp == "p_cfd":
            print(case_name)
            print(SBI_file)
            print(output_SBIs)

        output_SBIs_Sys=output_SBIs[output_SBIs[:,0]>=start_t_sys]
        output_SBIs_Sys=output_SBIs_Sys[output_SBIs_Sys[:,0]<=end_t_sys]

        output_SBIs=output_SBIs[output_SBIs[:,0]>=start_t]
        output_SBIs=output_SBIs[output_SBIs[:,0]<=end_t]

        SBI_Max = np.max(output_SBIs[:,1])
        SBI_Avg = np.mean(output_SBIs[:,1])
        SBI_Sys = np.mean(output_SBIs_Sys[:,1])

        if "v_fsi" in dvp:
            SBI_Max_vel.append(SBI_Max)
            SBI_Avg_vel.append(SBI_Avg)
            SBI_Sys_vel.append(SBI_Sys)
            filename_amp_vel.append(case_name)
        elif "d_fsi" in dvp:
            SBI_Max_disp.append(SBI_Max)
            SBI_Avg_disp.append(SBI_Avg)
            SBI_Sys_disp.append(SBI_Sys)
            filename_amp_disp.append(case_name)
        elif "v_cfd" in dvp:
            SBI_Max_vel_cfd.append(SBI_Max)
            SBI_Avg_vel_cfd.append(SBI_Avg)
            SBI_Sys_vel_cfd.append(SBI_Sys)
            filename_amp_vel_cfd.append(case_name)
        elif "p_fsi" in dvp:
            SBI_Max_pres.append(SBI_Max)
            SBI_Avg_pres.append(SBI_Avg)
            SBI_Sys_pres.append(SBI_Sys)
            filename_amp_pres.append(case_name)
        elif "p_cfd" in dvp:
            SBI_Max_pres_cfd.append(SBI_Max)
            SBI_Avg_pres_cfd.append(SBI_Avg)
            SBI_Sys_pres_cfd.append(SBI_Sys)
            filename_amp_pres_cfd.append(case_name)
          
columns = ["max velocity SBI","temporal average velocity SBI","systolic velocity SBI","case name vel",
           "max velocity SBI CFD","temporal average velocity SBI CFD","systolic velocity SBI CFD","case name vel CFD",
           "max displacement SBI","temporal average displacement SBI","systolic displacement SBI","case name disp",
           "max pressure SBI","temporal average pressure SBI","systolic pressure SBI","case name pres",
           "max pressure SBI CFD","temporal average pressure SBI CFD","systolic pressure SBI CFD","case name pres CFD"]
data = list(zip(SBI_Max_vel,SBI_Avg_vel,SBI_Sys_vel,filename_amp_vel,
        SBI_Max_vel_cfd,SBI_Avg_vel_cfd,SBI_Sys_vel_cfd,filename_amp_vel_cfd,
        SBI_Max_disp,SBI_Avg_disp,SBI_Sys_disp,filename_amp_disp,
        SBI_Max_pres,SBI_Avg_pres,SBI_Sys_pres,filename_amp_pres,
        SBI_Max_pres_cfd,SBI_Avg_pres_cfd,SBI_Sys_pres_cfd,filename_amp_pres_cfd))



df = pd.DataFrame(data,columns=columns)

csv_out_file=simDir+'/all_case_data_SBI.csv' # file name for SBIs
print(df.head())
df.to_csv(csv_out_file)
