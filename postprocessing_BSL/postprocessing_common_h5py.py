import sys
import os
import numpy as np
from glob import glob
import h5py
import re
import shutil
from numpy import linalg as LA
from tempfile import mkdtemp
import pandas as pd 
import spectrograms as spec
from argparse import ArgumentParser
from numpy.fft import fftfreq, fft, ifft

"""
This script contains a number of helper functions to create visualizations outsside of fenics.
"""

def read_command_line():
    """Read arguments from commandline"""
    parser = ArgumentParser()

    parser.add_argument('--case', type=str, default="cyl_test", help="Path to simulation results",
                        metavar="PATH")
    parser.add_argument('--mesh', type=str, default="artery_coarse_rescaled", help="Mesh File Name",
                        metavar="PATH")
    parser.add_argument('--save_deg', type=int, default=2, help="Input save_deg of simulation, i.e whether the intermediate P2 nodes were saved. Entering save_deg = 1 when the simulation was run with save_deg = 2 will result in only the corner nodes being used in postprocessing")
    parser.add_argument('--stride', type=int, default=1, help="Desired frequency of output data (i.e to output every second step, stride = 2)")    

    parser.add_argument('--dt', type=float, default=0.001, help="Time step of simulation (s)")

    parser.add_argument('--start_t', type=float, default=0.0, help="Start time of simulation (s)")
    parser.add_argument('--end_t', type=float, default=0.05, help="End time of simulation (s)")
    parser.add_argument('--dvp', type=str, default="v", help="Quantity to postprocess, input v for velocity, d for sisplacement, p for pressure, or wss for wall shear stress")

    args = parser.parse_args()

    return args.case, args.mesh, args.save_deg, args.stride, args.dt, args.start_t, args.end_t, args.dvp

def read_command_line_spi():
    """Read arguments from commandline"""
    parser = ArgumentParser()

    parser.add_argument('--case', type=str, default="cyl_test", help="Path to simulation results",
                        metavar="PATH")
    parser.add_argument('--mesh', type=str, default="artery_coarse_rescaled", help="Mesh File Name",
                        metavar="PATH")
    parser.add_argument('--save_deg', type=int, default=2, help="Input save_deg of simulation, i.e whether the intermediate P2 nodes were saved. Entering save_deg = 1 when the simulation was run with save_deg = 2 will result in only the corner nodes being used in postprocessing")
    parser.add_argument('--stride', type=int, default=1, help="Desired frequency of output data (i.e to output every second step, stride = 2)")    
    parser.add_argument('--start_t', type=float, default=0.0, help="Start time of simulation (s)")
    parser.add_argument('--end_t', type=float, default=0.05, help="End time of simulation (s)")
    parser.add_argument('--cut', type=str, default="low", help="Choose 'low' or 'high', low cuts frequencies below 'thresh', high cuts frequencies above 'thresh'.")
    parser.add_argument('--thresh', type=float, default=25, help="SPI frequency threshold in Hz")
    parser.add_argument('--dvp', type=str, default="v", help="Quantity to postprocess, input v for velocity, d for sisplacement, p for pressure, or wss for wall shear stress")

    args = parser.parse_args()

    return args.case, args.mesh, args.save_deg, args.stride, args.start_t, args.end_t, args.cut, args.thresh, args.dvp

def read_command_line_spec():
    """Read arguments from commandline"""
    parser = ArgumentParser()

    parser.add_argument('--case', type=str, default="cyl_test", help="Path to simulation results",
                        metavar="PATH")
    parser.add_argument('--mesh', type=str, default="artery_coarse_rescaled", help="Mesh File Name",
                        metavar="PATH")
    parser.add_argument('--save_deg', type=int, default=2, help="Input save_deg of simulation, i.e whether the intermediate P2 nodes were saved. Entering save_deg = 1 when the simulation was run with save_deg = 2 will result in only the corner nodes being used in postprocessing")
    parser.add_argument('--stride', type=int, default=1, help="Desired frequency of output data (i.e to output every second step, stride = 2)")    
    parser.add_argument('--start_t', type=float, default=0.0, help="Start time of simulation (s)")
    parser.add_argument('--end_t', type=float, default=0.05, help="End time of simulation (s)")
    parser.add_argument('--lowcut', type=float, default=25, help="High pass filter cutoff frequency (Hz)")
    parser.add_argument('--ylim', type=float, default=800, help="y limit of spectrogram graph")
    parser.add_argument('--r_sphere', type=float, default=1000000, help="Sphere in which to include points for spectrogram, this is the sphere radius")
    parser.add_argument('--x_sphere', type=float, default=0.0, help="Sphere in which to include points for spectrogram, this is the x coordinate of the center of the sphere (in m)")
    parser.add_argument('--y_sphere', type=float, default=0.0, help="Sphere in which to include points for spectrogram, this is the y coordinate of the center of the sphere (in m)")
    parser.add_argument('--z_sphere', type=float, default=0.0, help="Sphere in which to include points for spectrogram, this is the z coordinate of the center of the sphere (in m)")
    parser.add_argument('--dvp', type=str, default="v", help="Quantity to postprocess, input v for velocity, d for sisplacement, p for pressure, or wss for wall shear stress")

    args = parser.parse_args()

    return args.case, args.mesh, args.save_deg, args.stride, args.start_t, args.end_t, args.lowcut, args.ylim, args.r_sphere, args.x_sphere, args.y_sphere, args.z_sphere, args.dvp


def get_visualization_path(case_path):

    if os.path.exists(os.path.join(case_path,"results")):
    	# Finds the visualization path for BSL Solver format
        file_path = os.path.join(case_path,"results")
        files = sorted(glob(file_path + '/art*'))
        print(files)
        visualization_path = files[0]

    else:
        # Finds the visualization path for TurtleFSI simulations
        for file in os.listdir(case_path):
            file_path = os.path.join(case_path, file)
            if os.path.exists(os.path.join(file_path, "1")):
                visualization_path = os.path.join(file_path, "1/Visualization")
            elif os.path.exists(os.path.join(file_path, "Visualization")):
                visualization_path = os.path.join(file_path, "Visualization")
    
    return visualization_path

def get_coords(meshFile):
    mesh = h5py.File(meshFile,"r")
    coords = mesh['mesh/coordinates'][:,:] 
    return coords

def get_surface_topology_coords(outFile):
    mesh = h5py.File(outFile,"r")
    topology = mesh["Mesh/0/mesh/topology"][:,:]
    coords = mesh["Mesh/0/mesh/geometry"][:,:]
    return topology, coords

def get_domain_topology(meshFile):
	# This function obtains the topology for the fluid, solid, and all elements of the input mesh
	vectorData = h5py.File(meshFile,"r")
	domainsLoc = 'domains/values'
	domains = vectorData[domainsLoc][:] # Open domain array
	id_wall = (domains>1).nonzero() # domain = 2 is the solid
	id_fluid = (domains==1).nonzero() # domain = 1 is the fluid

	topologyLoc = 'domains/topology'
	allTopology = vectorData[topologyLoc][:,:] 
	wallTopology=allTopology[id_wall,:] 
	fluidTopology=allTopology[id_fluid,:]

	return fluidTopology, wallTopology, allTopology

def get_domain_ids(meshFile):
	# This function obtains a list of the node IDs for the fluid, solid, and all elements of the input mesh

	# Get topology of fluid, solid and whole mesh
	fluidTopology, wallTopology, allTopology = get_domain_topology(meshFile)
	wallIDs = np.unique(wallTopology) # find the unique node ids in the wall topology, sorted in ascending order
	fluidIDs = np.unique(fluidTopology) # find the unique node ids in the fluid topology, sorted in ascending order
	allIDs = np.unique(allTopology) 
	return fluidIDs, wallIDs, allIDs

def get_sampling_constants(df,start_t,end_t):
	'''
	T = period, in seconds, 
	nsamples = samples per cycle
	fs = sample rate
	'''
	T = end_t - start_t
	nsamples = df.shape[1]
	fs = nsamples/T 
	return T, nsamples, fs 

def read_npz_files(filepath):

	data = np.load(filepath)['component']
	print('making df...')
	df = pd.DataFrame(data,copy=False)
	df.index.names = ['Ids']
	print('ready')
	return df

def filter_SPI(U, W_low_cut, tag):
    if tag=="withmean":
        U_fft = fft(U)
    else:
        U_fft = fft(U-np.mean(U))
    # filter any amplitude corresponding frequency equal to 0Hz
    U_fft[W_low_cut[0]] = 0
    # filter any amplitude corresponding frequency lower to 25Hz
    U_fft_25Hz = U_fft.copy()
    #print(U_fft_25Hz)

    U_fft_25Hz[W_low_cut[1]] = 0 # This line won't work if W is not the right shape/size!!!
    # compute the absolute values

    Power_25Hz = np.sum ( np.power( np.absolute(U_fft_25Hz),2))
    Power_0Hz  = np.sum ( np.power( np.absolute(U_fft     ),2))


    if Power_0Hz < 1e-8:
        return 0
    return Power_25Hz/Power_0Hz

def calculate_spi(case_name, df, output_folder, meshFile,start_t,end_t,cut,thresh, dvp):
    # Get wall and fluid ids
    fluidIDs, wallIDs, allIDs = get_domain_ids(meshFile)
    fluidElements, wallElements, allElements = get_domain_topology(meshFile)

    # For displacement spectrogram, we need to take only the wall IDs, filter the data and scale it. 
    if dvp == "wss":
        outFile = os.path.join(output_folder,"WSS_ts.h5")
        surfaceElements, coord = get_surface_topology_coords(outFile)
        elems=np.squeeze(surfaceElements)
        IDs = list(range(len(coord)))

    elif dvp == "d":
        IDs = wallIDs
        elems=np.squeeze(wallElements)
        Coords = get_coords(meshFile)
        coord = Coords[IDs,:]
    else:
        IDs = fluidIDs
        elems=np.squeeze(fluidElements)
        Coords = get_coords(meshFile)
        coord = Coords[IDs,:]    

    df_spec = df.iloc[IDs]          


    T, num_ts, fs = spec.get_sampling_constants(df_spec,start_t,end_t)
    time_between_files = 1/fs
    W = fftfreq(num_ts, d=time_between_files)

    # Cut low or high frequencies
    if cut =="high":
        W_cut = np.where( np.abs(W) == 0 ) + np.where( np.abs(W) > thresh )
    elif cut =="low":
        W_cut = np.where( np.abs(W) == 0 ) + np.where( np.abs(W) < thresh )
    else:
        print("invalid option entered for 'cut' ")


    number_of_points = len(IDs)
    SPI = np.zeros([number_of_points])
    
    for i in range(len(IDs)):
        SPI[i] = filter_SPI(df_spec.iloc[i],W_cut,"withoutmean")

    output_filename = output_folder+'/'+case_name+'_spi_'+cut+'_cut_'+str(thresh)+"_"+dvp+'.tec'



 
    for j in range(len(IDs)):
        elems[elems == IDs[j]] = j

    print(elems)

    outfile = open(output_filename, 'w')
    if dvp == "wss":
        outfile.write('VARIABLES = X,Y,Z,SPI\nZONE N=%d,E=%d,F=FEPOINT,ET=TRIANGLE\n'%(coord.shape[0], elems.shape[0]))
    else:
        outfile.write('VARIABLES = X,Y,Z,SPI\nZONE N=%d,E=%d,F=FEPOINT,ET=TETRAHEDRON\n'%(coord.shape[0], elems.shape[0])) # Make sure to change to Triangle for WSS!!!
    for i in range(coord.shape[0]):
        outfile.write('% 16.12f % 16.12f % 16.12f % 16.12f\n'%
                        (coord[i,0],coord[i,1],coord[i,2],SPI[i]))
    for i in range(elems.shape[0]):
        c = elems[i]
        if dvp == "wss":
            outfile.write('\n%d %d %d'%(c[0]+1,c[1]+1,c[2]+1))
        else:
            outfile.write('\n%d %d %d %d'%(c[0]+1,c[1]+1,c[2]+1,c[3]+1)) # Need to add 1 because tecplot starts node numbering at 1
    outfile.close()   

def create_domain_specific_viz(formatted_data_folder, output_folder, meshFile,time_between_files,dvp):

	# Get input data
	components_data = []
	component_names = ["mag","x","y","z"]
	for i in range(len(component_names)):
		if dvp == "p" and i>0:
			break
		file_str = dvp+"_"+component_names[i]+".npz"
		print(file_str)
		component_file = [file for file in os.listdir(formatted_data_folder) if file_str in file]
		component_data = np.load(formatted_data_folder+"/"+component_file[0])['component']
		components_data.append(component_data)


	# Create name for output file, define output path

	if dvp == "v":
		viz_type = 'velocity'
	elif dvp == "d":
		viz_type = 'displacement'
	elif dvp == "p":
		viz_type = 'pressure'
	else:
		print("Input d, v or p for dvp")

	output_file_name = viz_type+'.h5'  
	output_path = os.path.join(output_folder, output_file_name)  

	# Create output directory
	if os.path.exists(output_folder):
		print('Path exists!')
	if not os.path.exists(output_folder):
		print("creating output folder")
		os.makedirs(output_folder)

	#read in the fsi mesh:
	fsi_mesh = h5py.File(meshFile,'r')

	# Count fluid and total nodes
	coordArrayFSI= fsi_mesh['mesh/coordinates'][:,:]
	topoArrayFSI= fsi_mesh['mesh/topology'][:,:]
	nNodesFSI = coordArrayFSI.shape[0]
	nElementsFSI = topoArrayFSI.shape[0]

	# Get fluid only topology
	fluidTopology, wallTopology, allTopology = get_domain_topology(meshFile)
	fluidIDs, wallIDs, allIDs = get_domain_ids(meshFile)
	coordArrayFluid= fsi_mesh['mesh/coordinates'][fluidIDs,:]
	nNodesFluid = len(fluidIDs)
	nElementsFluid = fluidTopology.shape[1]

	coordArraySolid= fsi_mesh['mesh/coordinates'][wallIDs,:]
	nNodesSolid = len(wallIDs)
	nElementsSolid = wallTopology.shape[1]
	# Get number of timesteps
	num_ts = components_data[0].shape[1]    

	# Remove old file path
	if os.path.exists(output_path):
		print('File path exists; rewriting')
		os.remove(output_path)
	# Create H5 file
	vectorData = h5py.File(output_path,'a')

	# Create mesh arrays
	# 1. update so that the fluid only nodes are used
	# Easiest way is just inputting the fluid-only mesh
	# harder way is modifying the topology of the mesh.. if an element contains a node that is in the solid, then don't include it? 
	# for save_deg = 2, maybe we can use fenics to create refined mesh with the fluid and solid elements noted?
	# hopefully that approach will yield the same node numbering as turtleFSI


	if dvp == "d":
		geoArray = vectorData.create_dataset("Mesh/0/mesh/geometry", (nNodesSolid,3))
		geoArray[...] = coordArraySolid
		topoArray = vectorData.create_dataset("Mesh/0/mesh/topology", (nElementsSolid,4), dtype='i')

		# Fix Wall topology (need to renumber nodes consecutively so that dolfin can read the mesh)
		for node_id in range(nNodesSolid):
			wallTopology = np.where(wallTopology == wallIDs[node_id], node_id, wallTopology)
		topoArray[...] = wallTopology
		#print(wallTopology)

	else:
		geoArray = vectorData.create_dataset("Mesh/0/mesh/geometry", (nNodesFluid,3))
		geoArray[...] = coordArrayFluid
		topoArray = vectorData.create_dataset("Mesh/0/mesh/topology", (nElementsFluid,4), dtype='i')

		# Fix Fluid topology
		for node_id in range(len(fluidIDs)):
			fluidTopology = np.where(fluidTopology == fluidIDs[node_id], node_id, fluidTopology)
		topoArray[...] = fluidTopology

    # 2. loop through elements and load in the df
	for idx in range(num_ts):
		ArrayName = 'VisualisationVector/' + str(idx)
		if dvp == "p":
			v_array = vectorData.create_dataset(ArrayName, (nNodesFluid,1))
			v_array[:,0] = components_data[0][fluidIDs,idx]
			attType = "Scalar"

		elif dvp == "v":
			v_array = vectorData.create_dataset(ArrayName, (nNodesFluid,3))
			v_array[:,0] = components_data[1][fluidIDs,idx]
			v_array[:,1] = components_data[2][fluidIDs,idx]
			v_array[:,2] = components_data[3][fluidIDs,idx]
			attType = "Vector"

		elif dvp == "d":
			v_array = vectorData.create_dataset(ArrayName, (nNodesSolid,3))
			v_array[:,0] = components_data[1][wallIDs,idx]
			v_array[:,1] = components_data[2][wallIDs,idx]
			v_array[:,2] = components_data[3][wallIDs,idx]
			attType = "Vector"

		else:
			print("ERROR, input dvp")

	vectorData.close() 

    # 3 create xdmf so that we can visualize
	if dvp == "d":
		create_xdmf_file(num_ts,time_between_files,nElementsSolid,nNodesSolid,attType,viz_type,output_folder)

	else:
		create_xdmf_file(num_ts,time_between_files,nElementsFluid,nNodesFluid,attType,viz_type,output_folder)


def create_hi_pass_viz(formatted_data_folder, output_folder, meshFile,time_between_files,dvp,lowcut=0,highcut=100000,magnitude=False):

	# Get input data
	components_data = []
	component_names = ["mag","x","y","z"]
	for i in range(len(component_names)):
		if ("p" in dvp or magnitude == True) and i>0:
			break
		file_str = dvp+"_"+component_names[i]+".npz"
		print("Opened file: " + file_str)
		component_file = [file for file in os.listdir(formatted_data_folder) if file_str in file]
		component_data = np.load(formatted_data_folder+"/"+component_file[0])['component']
		components_data.append(component_data)


	# Create name for output file, define output path

	if "v" in dvp:
		viz_type = 'velocity'
	elif "d" in dvp:
		viz_type = 'displacement'
	elif "p" in dvp:
		viz_type = 'pressure'
	else:
		print("Input d, v or p for dvp")

	if magnitude == True:
		viz_type = viz_type + "_magnitude"
	viz_type = viz_type+"_"+str(lowcut)+"_to_"+str(highcut)
	output_file_name = viz_type+'.h5'  
	output_path = os.path.join(output_folder, output_file_name)  

	# Create output directory
	if os.path.exists(output_folder):
		print('Path exists!')
	if not os.path.exists(output_folder):
		print("creating output folder")
		os.makedirs(output_folder)

	#read in the fsi mesh:
	fsi_mesh = h5py.File(meshFile,'r')

	# Count fluid and total nodes
	coordArrayFSI= fsi_mesh['mesh/coordinates'][:,:]
	topoArrayFSI= fsi_mesh['mesh/topology'][:,:]
	nNodesFSI = coordArrayFSI.shape[0]
	nElementsFSI = topoArrayFSI.shape[0]

	# Get fluid only topology
	fluidTopology, wallTopology, allTopology = get_domain_topology(meshFile)
	fluidIDs, wallIDs, allIDs = get_domain_ids(meshFile)
	coordArrayFluid= fsi_mesh['mesh/coordinates'][fluidIDs,:]

	# Get number of timesteps
	num_ts = components_data[0].shape[1]    

	# Remove old file path
	if os.path.exists(output_path):
		print('File path exists; rewriting')
		os.remove(output_path)
	# Create H5 file
	vectorData = h5py.File(output_path,'a')

	# Create mesh arrays
	# 1. update so that the fluid only nodes are used
	# Easiest way is just inputting the fluid-only mesh
	# harder way is modifying the topology of the mesh.. if an element contains a node that is in the solid, then don't include it? 
	# for save_deg = 2, maybe we can use fenics to create refined mesh with the fluid and solid elements noted?
	# hopefully that approach will yield the same node numbering as turtleFSI

	geoArray = vectorData.create_dataset("Mesh/0/mesh/geometry", (nNodesFSI,3))
	geoArray[...] = coordArrayFSI
	topoArray = vectorData.create_dataset("Mesh/0/mesh/topology", (nElementsFSI,4), dtype='i')
	topoArray[...] = allTopology

    # if lowcut exists, use a hi-pass filter on the results.
	if lowcut > 0:
		print("Filtering data...")
		for idy in range(nNodesFSI):
			if idy%1000 == 0:
				print("...")
			
			f_crit = int(1/time_between_files)/2 - 1
			if highcut >=f_crit:
				highcut = f_crit
			components_data[0][idy,:] = spec.butter_bandpass_filter(components_data[0][idy,:], lowcut=lowcut, highcut=highcut, fs=int(1/time_between_files)-1)
			if dvp != "p" and magnitude == False:
				components_data[1][idy,:] = spec.butter_bandpass_filter(components_data[1][idy,:], lowcut=lowcut, highcut=highcut, fs=int(1/time_between_files)-1)
				components_data[2][idy,:] = spec.butter_bandpass_filter(components_data[2][idy,:], lowcut=lowcut, highcut=highcut, fs=int(1/time_between_files)-1)
				components_data[3][idy,:] = spec.butter_bandpass_filter(components_data[3][idy,:], lowcut=lowcut, highcut=highcut, fs=int(1/time_between_files)-1)

    # 2. loop through elements and load in the df
	for idx in range(num_ts):
		ArrayName = 'VisualisationVector/' + str(idx)
		if "p" in dvp or magnitude == True:
			v_array = vectorData.create_dataset(ArrayName, (nNodesFSI,1))
			v_array[:,0] = components_data[0][:,idx]
			attType = "Scalar"

		else:
			v_array = vectorData.create_dataset(ArrayName, (nNodesFSI,3))
			v_array[:,0] = components_data[1][:,idx]
			v_array[:,1] = components_data[2][:,idx]
			v_array[:,2] = components_data[3][:,idx]
			attType = "Vector"

	vectorData.close() 

    # 3 create xdmf so that we can visualize
	create_xdmf_file(num_ts,time_between_files,nElementsFSI,nNodesFSI,attType,viz_type,output_folder)



def create_xdmf_file(num_ts,time_between_files,nElements,nNodes,attType,viz_type,output_folder):

	# Create strings
	num_el = str(nElements)
	num_nodes = str(nNodes)
	nDim = '1' if attType == "Scalar" else '3'
	
	# Write lines of xdmf file
	lines = []
	lines.append('<?xml version="1.0"?>\n')
	lines.append('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
	lines.append('<Xdmf Version="3.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
	lines.append('  <Domain>\n')
	lines.append('    <Grid Name="TimeSeries_'+viz_type+'" GridType="Collection" CollectionType="Temporal">\n')
	lines.append('      <Grid Name="mesh" GridType="Uniform">\n')
	lines.append('        <Topology NumberOfElements="'+num_el+'" TopologyType="Tetrahedron" NodesPerElement="4">\n')
	lines.append('          <DataItem Dimensions="'+num_el+' 4" NumberType="UInt" Format="HDF">'+viz_type+'.h5:/Mesh/0/mesh/topology</DataItem>\n')
	lines.append('        </Topology>\n')
	lines.append('        <Geometry GeometryType="XYZ">\n')
	lines.append('          <DataItem Dimensions="'+num_nodes+' 3" Format="HDF">'+viz_type+'.h5:/Mesh/0/mesh/geometry</DataItem>\n')
	lines.append('        </Geometry>\n')

	for idx in range(num_ts):
		time_value = str(idx*time_between_files)
		lines.append('        <Time Value="'+time_value+'" />\n')
		lines.append('        <Attribute Name="'+viz_type+'" AttributeType="'+attType+'" Center="Node">\n')
		lines.append('          <DataItem Dimensions="'+num_nodes+' '+nDim+'" Format="HDF">'+viz_type+'.h5:/VisualisationVector/'+str(idx)+'</DataItem>\n')
		lines.append('        </Attribute>\n')
		lines.append('      </Grid>\n')
		if idx == num_ts-1:
			break
		lines.append('      <Grid> \n')
		if attType == "Scalar":
			#lines.append('        <ns0:include xpointer="xpointer(//Grid[@Name=&quot;TimeSeries_'+viz_type+'&quot;]/Grid[1]/*[self::Topology or self::Geometry])" />\n')
			lines.append('        <xi:include xpointer="xpointer(//Grid[@Name=&quot;TimeSeries_'+viz_type+'&quot;]/Grid[1]/*[self::Topology or self::Geometry])" />\n')
		else:
			lines.append('        <xi:include xpointer="xpointer(//Grid[@Name=&quot;TimeSeries_'+viz_type+'&quot;]/Grid[1]/*[self::Topology or self::Geometry])" />\n')

	lines.append('    </Grid>\n')
	lines.append('  </Domain>\n')
	lines.append('</Xdmf>\n')

	# writing lines to file 
	xdmf_path = output_folder+'/'+viz_type+'.xdmf'

	# Remove old file path
	if os.path.exists(xdmf_path):
		print('File path exists; rewriting')
		os.remove(xdmf_path)

	xdmf_file = open(xdmf_path, 'w') 
	xdmf_file.writelines(lines) 
	xdmf_file.close() 


def create_transformed_matrix(input_path, output_folder,meshFile, case_name, start_t,end_t,dvp,stride=1):
	# Create name for case, define output path
	print('Creating matrix for case {}...'.format(case_name))
	output_folder = output_folder

	# Create output directory
	if os.path.exists(output_folder):
		print('Path exists')
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	# Get node ids from input mesh. If save_deg = 2, you can supply the original mesh to get the data for the 
	# corner nodes, or supply a refined mesh to get the data for all nodes (very computationally intensive)
	if dvp != "wss":
	    fluidIDs, wallIDs, allIDs = get_domain_ids(meshFile)
	    ids = allIDs

	# Get name of xdmf file
	if dvp == 'd':
		xdmf_file = input_path + '/displacement.xdmf' # Change
	elif dvp == 'v':
		xdmf_file = input_path + '/velocity.xdmf' # Change
	elif dvp == 'p':
		xdmf_file = input_path + '/pressure.xdmf' # Change
	elif dvp == 'wss':
		xdmf_file = input_path + '/WSS_ts.xdmf' # Change
	else:
		print('input d, v, p or wss for dvp')

	# If the simulation has been restarted, the output is stored in multiple files and may not have even temporal spacing
	# This loop determines the file names from the xdmf output file
	file1 = open(xdmf_file, 'r') 
	Lines = file1.readlines() 
	h5_ts=[]
	time_ts=[]
	index_ts=[]
	
	# This loop goes through the xdmf output file and gets the time value (time_ts), associated 
	# .h5 file (h5_ts) and index of each timestep inthe corresponding h5 file (index_ts)
	for line in Lines: 
		if '<Time Value' in line:
			time_pattern = '<Time Value="(.+?)"'
			time_str = re.findall(time_pattern, line)
			time = float(time_str[0])
			time_ts.append(time)

		elif 'VisualisationVector' in line:
			#print(line)
			h5_pattern = '"HDF">(.+?):/'
			h5_str = re.findall(h5_pattern, line)
			h5_ts.append(h5_str[0])

			index_pattern = "VisualisationVector/(.+?)</DataItem>"
			index_str = re.findall(index_pattern, line)
			index = int(index_str[0])
			index_ts.append(index)
    
	time_between_files = time_ts[2] - time_ts[1] # Calculate the time between files from xdmf file

	# Open up the first h5 file to get the number of timesteps and nodes for the output data
	file = input_path + '/'+  h5_ts[0]
	vectorData = h5py.File(file) 
	if dvp == "wss":
		ids = list(range(len(vectorData['VisualisationVector/0'][:])))
	vectorArray = vectorData['VisualisationVector/0'][ids,:] 

	num_ts = int(len(time_ts))  # Total amount of timesteps in original file

	# Get shape of output data
	num_rows = vectorArray.shape[0]
	num_cols = int((end_t-start_t)/(time_between_files*stride)) 

	# Pre-allocate the arrays for the formatted data
	if dvp == "v" or dvp == "d":
		dvp_x = np.zeros((num_rows, num_cols))
		dvp_y = np.zeros((num_rows, num_cols))
		dvp_z = np.zeros((num_rows, num_cols))
	dvp_magnitude = np.zeros((num_rows, num_cols))

	# Initialize variables
	tol = 1e-8  # temporal spacing tolerance, if this tolerance is exceeded, a warning flag will indicate that the data has uneven spacing
	idx_zeroed = 0 # Output index for formatted data
	h5_file_prev = ""
	for i in range(0,num_ts):
		time_file=time_ts[i]
		if i>0:
			if np.abs(time_file-time_ts[i-1] - time_between_files) > tol: # if the spacing between files is not equal to the intended timestep
				print('Warning: Uenven temporal spacing detected!!')

		# Open input h5 file
		h5_file = input_path + '/'+h5_ts[i]
		if h5_file != h5_file_prev: # If the h5 file is different than for the previous timestep, open the h5 file for the current timestep
			vectorData.close()
			vectorData = h5py.File(h5_file) 
		h5_file_prev = h5_file # Record h5 file name for this step

		# If the timestep falls within the desired timeframe and has the correct stride
		if time_file>=start_t and time_file <= end_t and i%stride == 0:

			# Open up Vector Array from h5 file
			ArrayName = 'VisualisationVector/' + str((index_ts[i]))	
			vectorArrayFull = vectorData[ArrayName][:,:] # Important not to take slices of this array, slows code considerably... 
			# instead make a copy (VectorArrayFull) and slice that.
			
			try:
				# Get required data depending on whether pressure, displacement or velocity
				if dvp == "p" or dvp == "wss":
					dvp_magnitude[:,idx_zeroed] = vectorArrayFull[ids,0] # Slice VectorArrayFull
				else:
					vectorArray = vectorArrayFull[ids,:]	
					dvp_x[:,idx_zeroed] = vectorArray[:,0]
					dvp_y[:,idx_zeroed] = vectorArray[:,1]
					dvp_z[:,idx_zeroed] = vectorArray[:,2]
					dvp_magnitude[:,idx_zeroed] = LA.norm(vectorArray, axis=1) 
			except:
				print("Finished reading solutions")
				break

			print('Transferred timestep number {} at time: '.format(index_ts[i])+ str(time_ts[i]) +' from file: '+ h5_ts[i])
			idx_zeroed+=1 # Move to the next index of the output h5 file
	
	vectorData.close()

	# Create output h5 file

	# Remove blank columns
	if dvp == "d" or dvp == "v":
		formatted_data = [dvp_magnitude,dvp_x,dvp_y,dvp_z]

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
			np.savez_compressed(output_path, component=dvp_magnitude)

	return time_between_files


if __name__ == "__main__":
	print('See functions.')
