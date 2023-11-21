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

simDirSurgCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile_CFD"
simDirPulsCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC_CFD_undeformed"


#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Rerun_Steady_New_Solver"
#ylim_v = 0.4
#ylim_d = 4.0
#end_t= 3.65 #3.804

#
#simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation"
#ylim_v = 0.1
#ylim_d = 10e-6

# find all logfiles in simulaation folder (file name must contain the word "logfile")

vel_csv_files_cfd = glob.glob(simDirPulsCFD + "/**/region_flow_metrics.csv", recursive = True)
vel_csv_files_cfd_Surg = glob.glob(simDirSurgCFD + "/**/region_flow_metrics.csv", recursive = True)


vel_csv_files_cfd.sort(key=natural_keys)

vel_csv_files_cfd_Surg.sort(key=natural_keys)

vel_csv_files_cfd.extend(vel_csv_files_cfd_Surg)



max_amp_vel_cfd = []
max_amp_vel = []
max_amp_disp = []


t_avg_max_amp_vel_cfd = []
t_avg_max_amp_vel = []
t_avg_max_amp_disp = []


filename_amp_vel_cfd = []
filename_amp_vel = []
filename_amp_disp = []

max_amp_pres_cfd = []
max_amp_pres = []

t_avg_max_amp_pres_cfd = []
t_avg_max_amp_pres = []

filename_amp_pres_cfd = []
filename_amp_pres = []

for i,file in enumerate(vel_csv_files_cfd):
    if i == 0:
        df = pd.read_csv(file)
    else:
        df_new = pd.read_csv(file)
        #df_new.rename(index={16: "x", 17: "y", 18: "z", 19: "x1", 20: "y1", 21: "z2"})
        df = pd.concat([df, df_new],ignore_index=True)

print(df)

    
          


csv_out_file=simDir+'/all_case_data_wss_region.csv' # file name for SBIs
print(df.head())
df.to_csv(csv_out_file)
