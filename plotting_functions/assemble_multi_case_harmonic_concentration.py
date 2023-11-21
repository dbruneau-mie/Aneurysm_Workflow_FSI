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

mode= "sigmoid"

simDir="/scratch/s/steinman/dbruneau/7_0_Surgical/AllCases"


simDirSurgCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile_CFD"
simDirSurgFSI = "/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile"
simDirSurgModal="/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Modal"
simDirPulsCFD = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC_CFD_undeformed"
simDirPulsFSI = "/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases_FC"
simDirPulsModal = "/scratch/s/steinman/dbruneau/7_0_Surgical/Modal_Excitation_All_Cases"


csv_modal_freqs = glob.glob(simDirPulsFSI + "/**/harmonic_concentration_"+mode+".csv", recursive = True)
csv_modal_freqs_Surg = glob.glob(simDirSurgFSI + "/**/harmonic_concentration_"+mode+".csv", recursive = True)

csv_modal_freqs_CFD = glob.glob(simDirPulsCFD + "/**/harmonic_concentration_"+mode+".csv", recursive = True)
csv_modal_freqs_Surg_CFD = glob.glob(simDirSurgCFD + "/**/harmonic_concentration_"+mode+".csv", recursive = True)


csv_modal_freqs.sort(key=natural_keys)
csv_modal_freqs_Surg.sort(key=natural_keys)

csv_modal_freqs_CFD.sort(key=natural_keys)
csv_modal_freqs_Surg_CFD.sort(key=natural_keys)

csv_modal_freqs.extend(csv_modal_freqs_Surg)
csv_modal_freqs_CFD.extend(csv_modal_freqs_Surg_CFD)


mode1_whole_freq = []
mode1_half_freq = []
mode1_third_freq = []
mode1_quarter_freq = []
mode2_whole_freq = []
mode2_half_freq = []
mode2_third_freq = []
mode2_quarter_freq = []
mode3_whole_freq = []
mode3_half_freq = []
mode3_third_freq = []
mode3_quarter_freq = []
case_names=[]

#for idx, modal_csv_file in enumerate(csv_modal_freqs_CFD):

for idx, modal_csv_file in enumerate(csv_modal_freqs_CFD):
    try:
        case_name = re.findall(r'case\d+', modal_csv_file)[0]
    except:
        case_name = re.findall(r'MCA\d+', modal_csv_file)[0]
    case_names.append(case_name)
    harmonic_concentration_modes = np.loadtxt(open(modal_csv_file, "rb"), delimiter=",", skiprows=1)
    mode1_whole_freq.append(harmonic_concentration_modes[0][0])
    mode1_half_freq.append(harmonic_concentration_modes[0][1])
    mode1_third_freq.append(harmonic_concentration_modes[0][2])
    mode1_quarter_freq.append(harmonic_concentration_modes[0][3])
    mode2_whole_freq.append(harmonic_concentration_modes[1][0])
    mode2_half_freq.append(harmonic_concentration_modes[1][1])
    mode2_third_freq.append(harmonic_concentration_modes[1][2])
    mode2_quarter_freq.append(harmonic_concentration_modes[1][3])
    mode3_whole_freq.append(harmonic_concentration_modes[2][0])
    mode3_half_freq.append(harmonic_concentration_modes[2][1])
    mode3_third_freq.append(harmonic_concentration_modes[2][2])
    mode3_quarter_freq.append(harmonic_concentration_modes[2][3])
    #mode1_whole_freq.append(harmonic_concentration_modes[])

columns = ["case_name",
           "mode1_whole_freq_harmonic_concentration",
           "mode1_half_freq_harmonic_concentration",
           "mode1_third_freq_harmonic_concentration",
           "mode1_quarter_freq_harmonic_concentration",
           "mode2_whole_freq_harmonic_concentration",
           "mode2_half_freq_harmonic_concentration",
           "mode2_third_freq_harmonic_concentration",
           "mode2_quarter_freq_harmonic_concentration",
           "mode3_whole_freq_harmonic_concentration",
           "mode3_half_freq_harmonic_concentration",
           "mode3_third_freq_harmonic_concentration",
           "mode3_quarter_freq_harmonic_concentration"]

data = list(zip(case_names,
                mode1_whole_freq,
                mode1_half_freq,
                mode1_third_freq,
                mode1_quarter_freq,
                mode2_whole_freq,
                mode2_half_freq,
                mode2_third_freq,
                mode2_quarter_freq,
                mode3_whole_freq,
                mode3_half_freq,
                mode3_third_freq,
                mode3_quarter_freq))



df = pd.DataFrame(data,columns=columns)

#modal_freqs=np.array(modal_freqs)

#print(modal_freqs)
#df_neck["Mode 1 Harmonic Concentration"] = modal_freqs[:,0]
#df_neck["Mode 2 Harmonic Concentration"] = modal_freqs[:,1]
#df_neck["Mode 3 Harmonic Concentration"] = modal_freqs[:,2]
#
#modal_freqs_CFD = []
#for idx, modal_csv_file in enumerate(csv_modal_freqs_CFD):
#    modal_freqs_CFD.append(np.loadtxt(modal_csv_file))
#
#modal_freqs_CFD=np.array(modal_freqs_CFD)
#print(modal_freqs_CFD)
#df_neck["Mode 1 Harmonic Concentration CFD"] = modal_freqs_CFD[:,0]
#df_neck["Mode 2 Harmonic Concentration CFD"] = modal_freqs_CFD[:,1]
#df_neck["Mode 3 Harmonic Concentration CFD"] = modal_freqs_CFD[:,2]
#
#
#
csv_out_file=simDir+'/all_case_data_harmonic_concentration_'+mode+'_CFD.csv' # file name for amplitudes
#print(df_neck.head(17))
df.to_csv(csv_out_file)
