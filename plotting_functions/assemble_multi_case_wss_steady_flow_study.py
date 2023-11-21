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

simDirSteadyMax = "/scratch/s/steinman/dbruneau/7_0_Surgical/Steady_Ramp_Cases_FC_Qmax"
simDirSteadyAvg = "/scratch/s/steinman/dbruneau/7_0_Surgical/Steady_Ramp_Cases_FC_Qavg"
simDirPuls = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"


#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.4
#ylim_d = 4.0
#end_t= 3.65 #3.804

#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")

vel_csv_files = glob.glob(simDirPuls + "/**/region_flow_metrics.csv", recursive = True)
vel_csv_files_steady_max = glob.glob(simDirSteadyMax + "/**/region_flow_metrics.csv", recursive = True)
vel_csv_files_steady_avg = glob.glob(simDirSteadyAvg + "/**/region_flow_metrics.csv", recursive = True)


vel_csv_files.sort(key=natural_keys)
vel_csv_files_steady_max.sort(key=natural_keys)
vel_csv_files_steady_avg.sort(key=natural_keys)

vel_csv_files.extend(vel_csv_files_steady_avg)
vel_csv_files.extend(vel_csv_files_steady_max)

file_names = []

for i,file in enumerate(vel_csv_files):
    if i == 0:
        df = pd.read_csv(file)
    else:
        df_new = pd.read_csv(file)
        #df_new.rename(index={16: "x", 17: "y", 18: "z", 19: "x1", 20: "y1", 21: "z2"})
        df = pd.concat([df, df_new],ignore_index=True)
    file_names.append(file)

df["file_name"]=file_names 


comp_time_csv_files = glob.glob(simDirPuls + "/**/compute_time**.csv", recursive = True)
comp_time_csv_files_steady_max = glob.glob(simDirSteadyMax + "/**/compute_time**.csv", recursive = True)
comp_time_csv_files_steady_avg = glob.glob(simDirSteadyAvg + "/**/compute_time**.csv", recursive = True)


comp_time_csv_files.sort(key=natural_keys)
comp_time_csv_files_steady_max.sort(key=natural_keys)
comp_time_csv_files_steady_avg.sort(key=natural_keys)

comp_time_csv_files.extend(comp_time_csv_files_steady_avg)
comp_time_csv_files.extend(comp_time_csv_files_steady_max)

file_names = []
sim_times = []
compute_times = []

for i,file in enumerate(comp_time_csv_files):

    csv_data = np.genfromtxt(file, delimiter=",")
    sim_times.append(csv_data[11199,0])
    compute_times.append(csv_data[11199,3])
    file_names.append(file)

df["compute_time"]=compute_times 
df["sim_time"]=sim_times 
df["file_name_time"]=file_names 


csv_out_file=simDir+'/steady_flow_study_case_data_wss_region.csv' # file name for SBIs
print(df.head())
df.to_csv(csv_out_file)
