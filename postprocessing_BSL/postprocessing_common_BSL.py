import sys
import os
import numpy as np
from glob import glob
import h5py
import re
import shutil
from numpy import linalg as LA
import pandas as pd

"""
This script contains a number of helper functions to create visualizations outside of fenics for the BSL solver.
"""

def create_transformed_matrix_BSL(input_path, output_folder, case_name, start_t,end_t,dvp,stride=1):

    

	# Create name for case, define output path
	print('Creating matrix for case {}...'.format(case_name))
	output_folder = output_folder

	# Create output directory
	if os.path.exists(output_folder):
		print('Path exists')
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	# Get all the h5 files
	file_format = "h5"
	files = sorted(glob(input_path + '/art*curcyc*.{}'.format("h5")))
	print('There are {} files'.format(len(files)))
	files = files[::stride]
	print('Using {} files with stride {}'.format(len(files), stride))

	xdmf_files = sorted(glob(input_path + '/art*.{}'.format("xdmf")))
	xdmf_file = xdmf_files[0] # All of the output xdmf files will contain the time, choose the first one

	# This loop determines the file names from the xdmf output file
	print(xdmf_file)
	file1 = open(xdmf_file, 'r') 
	Lines = file1.readlines() 
	time_ts=[]
	
	# This loop goes through the xdmf output file and gets the time value (time_ts)
	for line in Lines: 
		if '<Time Value' in line:
			time_pattern = '<Time Value="(.+?)"'
			time_str = re.findall(time_pattern, line)
			time = float(time_str[0])
			time_ts.append(time)

	time_between_files = (time_ts[2] - time_ts[1])/1000 # Calculate the time between files from xdmf file (in s)

	# Open up the first h5 file to get the number of nodes for the output data
	vectorData = h5py.File(files[0])
	vectorArray = vectorData['Solution/u']
	#print(len(vectorArray))
	num_arrays = 1

	num_ts = len(files) # Total number of timesteps 

	# Get shape of output data
	num_rows = vectorArray.shape[0]
	num_cols = int((end_t-start_t)/(time_between_files*stride))+2 # plus 2 is a hack to make sure there is enough room, will remove these final column(s) at the end

	# Pre-allocate the arrays for the formatted data
	if dvp != "p":
		dvp_x = np.zeros((num_rows, num_cols))
		dvp_y = np.zeros((num_rows, num_cols))
		dvp_z = np.zeros((num_rows, num_cols))
	dvp_magnitude = np.zeros((num_rows, num_cols))

	# Initialize variables
	tol = 1e-8  # temporal spacing tolerance, if this tolerance is exceeded, a warning flag will indicate that the data has uneven spacing
	idx_zeroed = 0 # Output index for formatted data
	h5_file_prev = ""
	for idx, file in enumerate(files):
		#id_offset = int(start_time/ts_length)+1
		time_file= idx*time_between_files*stride
		if time_file>=start_t and time_file <= end_t:

			# Open up Vector Array from h5 file
			vectorData = h5py.File(file)
			vectorArray = vectorData['Solution/u']
			vectorArrayFull = vectorArray[:,:] # Important not to take slices of this array, slows code considerably... 
			# instead make a copy (VectorArrayFull) and slice that.
			
			# Get required data depending on whether pressure, displacement or velocity
			if dvp == "p":
				dvp_magnitude[:,idx_zeroed] = vectorArrayFull[:,0]*1000 # Slice VectorArrayFull
			else:
				vectorArray = vectorArrayFull[:,:]	
				dvp_x[:,idx_zeroed] = vectorArray[:,0]
				dvp_y[:,idx_zeroed] = vectorArray[:,1]
				dvp_z[:,idx_zeroed] = vectorArray[:,2]
				dvp_magnitude[:,idx_zeroed] = LA.norm(vectorArray, axis=1) 

			print('Transferred timestep number {} at time: '.format(time_file))
			vectorData.close()
			idx_zeroed+=1 # Move to the next index of the output h5 file
	
	# Create output h5 file

	# Remove blank columns
	formatted_dvp_magnitude = dvp_magnitude[:,~np.all(dvp_magnitude == 0, axis = 0)] # risky... maybe use something other than all zeroes
	if dvp != "p":
		formatted_dvp_x = dvp_x[:,~np.all(dvp_x == 0, axis = 0)]
		formatted_dvp_y = dvp_y[:,~np.all(dvp_y == 0, axis = 0)]
		formatted_dvp_z = dvp_z[:,~np.all(dvp_z == 0, axis = 0)]
		formatted_data = [formatted_dvp_magnitude,formatted_dvp_x,formatted_dvp_y,formatted_dvp_z]
	num_cols = formatted_dvp_magnitude.shape[1]

	# Name components
	component_names = ["mag","x","y","z"]
	for i in range(len(component_names)):

		# If "p" we only have the magnitude, so end the loop early
		if (dvp == "p" or dvp =="wss") and i>0: 
			break

		# Create output path
		component = dvp+"_"+component_names[i]
		output_file_name = case_name+"_"+ component+'.npz'  
		output_path = os.path.join(output_folder, output_file_name) 

		# Remove old file path
		if os.path.exists(output_path):
			print('File path exists; rewriting')
			os.remove(output_path)

		# Create output h5 file

		# Store output
		if dvp == "v" or dvp =="d":
			np.savez_compressed(output_path, component=formatted_data[i])
		else:
			np.savez_compressed(output_path, component=formatted_dvp_magnitude)

	return time_between_files



if __name__ == "__main__":
	print('See functions.')
