import os
from glob import glob
import numpy as np
import postprocessing_common_h5py # copy the newest version into the current folder!
import postprocessing_common_BSL
#import spectrograms as spec
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd 


"""
This script takes the visualization files from BSL Solver and outputs velocity and pressure reformatted in the same way as for turtleFSI, 
i.e the units are converted and the data is stored in one h5 file. This way the simualtion can be postprocessed the same was as a simulation 
from TurtleFSI. A "Transformed Matrix" is created as well, which stores the output data in a format that can be opened quickly when we want to create spectrograms.

Args:
    mesh_name: Name of the non-refined input mesh for the simulation. This function will find the refined mesh based on this name
    case_path (Path): Path to results from simulation
    stride: reduce output frequncy by this factor
    save_deg (int): element degree saved from P2-P1 simulation (save_deg = 1 is corner nodes only). If we input save_deg = 1 for a simulation 
       that was run in TurtleFSI with save_deg = 2, the output from this script will be save_deg = 1, i.e only the corner nodes will be output
    dt (float): Actual time step of simulation
    start_t: Desired start time of the output files 
    end_t:  Desired end time of the output files 


Example:
python postprocessing_h5py/compute_domain_specific_viz_BSL.py --case /media/db_ubuntu/T7/Simulations/5_4_Verify_WSS/BSL_solver/_results/case16_m06 --save_deg 1 --dt 0.000679285714286 --mesh file_case16_el06 --end_t 0.951
python postprocessing_h5py/compute_domain_specific_viz_BSL.py --case /media/db_ubuntu/T7/Simulations/5_4_Verify_WSS/BSL_solver/_results/case16_m06 --save_deg 1 --dt 0.000339642857143 --mesh file_case16_el06 --end_t 0.951


"""


# Get Command Line Arguments and Input File Paths
#dvp_list = ["v","p"] # Components to postprocess
case_path, mesh_name, save_deg, stride, ts, start_t, end_t, dvp = postprocessing_common_h5py.read_command_line()
case_name = os.path.basename(os.path.normpath(case_path)) # obtains only last folder in case_path
results_path = os.path.join(case_path, "results")
mesh_path = os.path.join(case_path,"data",mesh_name+".h5")

# Get Output File Paths
visualization_path = os.path.join(results_path,os.listdir(results_path)[0])
formatted_data_folder = "res_"+case_name+'_stride_'+str(stride)+"t"+str(start_t)+"_to_"+str(end_t)+"save_deg_"+str(save_deg)
visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")

lowcut=25 # low cut frequency in Hz, for hi-pass displacement and velocity

# For pressure or velocity

# Create output folder and filenames
output_file_name = case_name+"_"+ dvp+"_mag.npz" 
formatted_data_path = formatted_data_folder+"/"+output_file_name

# If the output file exists, don't re-make it
if os.path.exists(formatted_data_path):
    print('path found!')
else: 
	# Make the output h5 files with dvp magnitudes
    time_between_input_files = postprocessing_common_BSL.create_transformed_matrix_BSL(visualization_path, formatted_data_folder, case_name, start_t,end_t,dvp,stride)

    time_between_output_files = time_between_input_files*stride # Need to give the correct interval between files
    postprocessing_common_h5py.create_domain_specific_viz(formatted_data_folder, visualization_separate_domain_folder, mesh_path, time_between_output_files,dvp)
#if dvp == "v" or dvp == "d":
#    postprocessing_common_h5py.create_hi_pass_viz(formatted_data_folder, visualization_hi_pass_folder, mesh_path,time_between_output_files,dvp,lowcut,True)

#if dvp == "d":
#    postprocessing_common_h5py.create_hi_pass_viz(formatted_data_folder, visualization_hi_pass_folder, mesh_path,time_between_output_files,dvp,lowcut)
#

