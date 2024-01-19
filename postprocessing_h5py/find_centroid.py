import os
import h5py
from glob import glob
import numpy as np
import postprocessing_common_h5py
import postprocessing_common_pv

#import spectrograms as spec
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd 
import glob as glob
import re
import pyvista as pv

"""
This script takes the visualization files from TurtleFSI and outputs: 
(1) Domain-specific visualizations (wall displacement for the wall only, and velocity and pressure for the fluid only).
    This way the simualtion can be postprocessed as a CFD simulation and a Solid Mechanics Element simulation separately. 
(2) Reduced save-deg visualization if save_deg = 2 (Creates a lightweight file for faster postprocessing)
(3) Band-Pass filtered visualizations for d, v, p and strain

A "Transformed Matrix" is created as well, which stores the output data in a format that can be opened quickly when we want to create spectrograms.

Args:
    mesh_name: Name of the non-refined input mesh for the simulation. This function will find the refined mesh based on this name
    case_path (Path): Path to results from simulation
    stride: reduce output frequncy by this factor
    save_deg (int): element degree saved from P2-P1 simulation (save_deg = 1 is corner nodes only). If we input save_deg = 1 for a simulation 
       that was run in TurtleFSI with save_deg = 2, the output from this script will be save_deg = 1, i.e only the corner nodes will be output
    dt (float): Actual time step of simulation
    start_t: Desired start time of the output files 
    end_t:  Desired end time of the output files 
    dvp: postprocess d, v, or p (displacement velocity or pressure)
    bands: list of bands for band-pass filtering displacement. 

Example: --dt 0.000679285714286 --mesh file_case16_el06 --end_t 0.951

"""
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def get_idx_of_time(xdmf_file, t):
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

    idx_of_time = index_ts[np.argmin(np.abs(np.array(time_ts)-t))] # here is your result
    #print(idx_of_time)
    return idx_of_time

def create_visualizations(case_path, mesh_name, save_deg, start_t, end_t, sampling_region, fluid_sampling_domain_ID, solid_sampling_domain_ID, r_sphere, x_sphere, y_sphere, z_sphere):

    case_name = os.path.basename(os.path.normpath(case_path)) # obtains only last folder in case_path
    visualization_path = postprocessing_common_h5py.get_visualization_path(case_path)
    
    #t_peak_sys = 3.0795
    # Get Mesh
    if save_deg == 1:
        mesh_path = case_path + "/mesh/" + mesh_name +".h5" # Mesh path. Points to the corner-node input mesh
    else: 
        mesh_path = case_path + "/mesh/" + mesh_name +"_refined.h5" # Mesh path. Points to the visualization mesh with intermediate nodes 
    mesh_path_sd1 = case_path + "/mesh/" + mesh_name +".h5" # Mesh path. Points to the corner-node input mesh
    mesh_path_sac = mesh_path_sd1.replace(".h5","_sac_flat.vtk") # needed for mps
    
    visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")
    visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")


    # Get centroid of sac
    sac_mesh = pv.read(mesh_path_sac)
    sac_points = sac_mesh.points/1000
    centroid = np.mean(sac_points, axis=0)
    sac_volume = sac_mesh.volume
    sac_diameter = (6*sac_volume/3.14159)**(1/3)
    sac_radius = sac_diameter/2000
    #print(centroid)

    # Open amplitude file
    for Amp_filename in ["velocity_amplitude_25_to_1400.h5"]:#,"pressure_amplitude_25_to_1400.h5"]:
        
        Amp_file = os.path.join(visualization_hi_pass_folder, Amp_filename)
        Amp_csv = Amp_file.replace(".h5",".csv")
         
        # Find time index of maximum amplitude
        output_amplitudes = np.genfromtxt(Amp_csv, delimiter=',')
        output_amplitudes[:,1] = range(len(output_amplitudes[:,1])) # Set indices as one column of array
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]>=start_t]
        output_amplitudes=output_amplitudes[output_amplitudes[:,0]<=end_t]
        index_max = int(output_amplitudes[np.argmax(output_amplitudes[:,3]),1])

        # Get original amplitude data and build mesh
        Amp_data = postprocessing_common_pv.get_data_at_idx(Amp_file,index_max)
        vectorData = h5py.File(Amp_file) 
        points_arr = np.array(vectorData["Mesh/0/mesh/geometry"])
        element_connectivity = np.array(vectorData["Mesh/0/mesh/topology"])
        mesh, surf = postprocessing_common_pv.assemble_mesh_arrays(points_arr,element_connectivity)
        
        # For pressure, take only value. For vector, take magnitude
        if Amp_data.shape[1] ==1:
            #mesh.point_arrays['Amp_quantity'] = Amp_data # Assign scalar to mesh
            Amplitude_Magnitude = np.abs(Amp_data).flatten() # Assign scalar to mesh
            dvp="p"

        else:
            #mesh.point_arrays['Amp_quantity'] = (Amp_data[:,0]**2 + Amp_data[:,1]**2 + Amp_data[:,2]**2)**0.5
            Amplitude_Magnitude = (Amp_data[:,0]**2 + Amp_data[:,1]**2 + Amp_data[:,2]**2)**0.5
            dvp="v"

        # Get average value in desired time frame for each point.
        # Get nodal coordinates of each node in amplitude file
        # Calculate distance to centroid for each point
        # Calculate maximum distance to centroid
        dist_to_centroid = ( (points_arr[:,0]-centroid[0])**2 + (points_arr[:,1]-centroid[1])**2 + (points_arr[:,2]-centroid[2])**2)**0.5
        dist_to_diam = dist_to_centroid - sac_radius

        dist_to_diam = np.array([0.0 if x < 0.0 else x for x in dist_to_diam])
        #print(points)
        #print(dist_to_centroid)
        #print("-----------------max dist to centroid------------------")
        max_distance = np.max(dist_to_diam)
        # Calculate maximum amplitude
        max_amplitude = np.max(Amplitude_Magnitude)

        # Apply formula at every node

        #distance_function = ((max_distance - dist_to_diam)/(max_distance))**2
        n_radii = 10 # assume 8 radii away has no influence
        no_effect_distance = 0.01 #sac_radius*n_radii
        
        distance_function = ((no_effect_distance - dist_to_diam)/(no_effect_distance))
        distance_function = np.array([0.0 if x < 0.0 else x for x in distance_function])
        #distance_function = distance_function**(1/2)

        instability_proximity_index = np.abs(Amplitude_Magnitude/max_amplitude)*distance_function
        #instability_proximity_index = 
        #print(instability_proximity_index)
        #print(np.max(instability_proximity_index))
        #print(np.percentile(instability_proximity_index,99))
        #print(max_amplitude)
        normalized_amplitude = (Amplitude_Magnitude/max_amplitude)
        #print("--------------------ARRAY_LENGTHS-------------------")
        #print(len(normalized_amplitude))
        #print(len(distance_function))
        #print(len(instability_proximity_index))
        print("--------------------ARRAY_MEAN-------------------")
        print(np.mean(normalized_amplitude))
        print(np.mean(distance_function))
        print(np.mean(instability_proximity_index))
        print("--------------------ARRAY_99th-------------------")
        print(np.percentile(instability_proximity_index,99))
        print("--------------------ARRAY_MAX-------------------")
        print(np.max(instability_proximity_index))
        print(Amplitude_Magnitude.shape)
        print(instability_proximity_index.shape)

        print(len(mesh.points))
        #print(np.max(mesh.point_arrays['proximity_index']))
        # Plot in pyvista to verify?
        # print maximum value
#
        #contour = mesh.contour([0.01], scalars="proximity_index")
        #if contour.n_points > 0:
        #    contour = postprocessing_common_pv.vtk_taubin_smooth(contour) # smooth the surface
        #    contour.compute_normals(inplace=True) # Compute normals        
        #plotter= pv.Plotter(notebook=0)

        #plotter.add_mesh(mesh,scalars="proximity_index", opacity=0.25)#,opacity="sigmoid",cmap='Reds',point_size=30)#,silhouette=silhouette_outer, opacity=0.0)
        #if contour.n_points > 0:
        #    plotter.add_mesh(contour,
        #                    color='red', 
        #                    clim=[0.0, 2.0], # NOTE this is for u_mag only!
        #                    lighting=True, 
        #                    smooth_shading=True, 
        #                    specular=0.00, 
        #                    diffuse=0.9,
        #                    ambient=0.5, 
        #                    name='contour')
        #plotter.show(auto_close=False)  

        #instability_proximity_index = (max_distance - dist_to_centroid)/(max_distance)
        ##instability_proximity_index = (Amplitude_Magnitude/max_amplitude)#(max_distance - dist_to_centroid)/(max_distance)
        ##print(instability_proximity_index)
        #print(np.percentile(instability_proximity_index))
        #print(np.mean(instability_proximity_index))
#
#
        # Plot in pyvista to verify?
        # print maximum value
        fnname="Proximity_Index"+dvp
        point_cloud = pv.PolyData(mesh.points)
        point_cloud[fnname] = distance_function
        plotter= pv.Plotter(notebook=0)
#
        plotter.add_mesh(point_cloud,scalars=fnname,opacity="sigmoid_5",cmap='Reds',point_size=30)#,silhouette=silhouette_outer, opacity=0.0)
#
        plotter.show(auto_close=False)  

    

if __name__ == '__main__':
    # Get Command Line Arguments and Input File Paths
    case_path, mesh_name, save_deg, _, _, start_t, end_t, _, _, sampling_region, fluid_sampling_domain_ID, solid_sampling_domain_ID, r_sphere, x_sphere, y_sphere, z_sphere = postprocessing_common_pv.read_command_line_region()
    create_visualizations(case_path, mesh_name, save_deg, start_t, end_t, sampling_region, fluid_sampling_domain_ID, solid_sampling_domain_ID, r_sphere, x_sphere, y_sphere, z_sphere)