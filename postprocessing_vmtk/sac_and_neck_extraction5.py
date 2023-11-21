""" Sac extraction using centerlines
"""
import os
import pyvista as pv 
import numpy as np 
from pathlib import Path
import h5py
from vtk import VTK_TETRA
from vmtk import vmtkscripts

#  This script requires a vtu file of the domain labels from fenics, and the save_deg_1 results
#  Generalizing this script will be challenging, for now just edit this script to add cases. 
# Try use vmtk loop selection to define sac?
#

## Warning: DONT upgrade pyvista in desktop vmtk environment. Only v0.24.2 will work with vmtk, otherwise the objects aren't compatible for some reason....
## Strangely, on Niagara, pyvista v0.36.1 will work with vmtk

## root folder
#case_name="MCA02_4D017"
#sim_dir = "/run/user/1000/gvfs/sftp:host=niagara.scinet.utoronto.ca,user=dbruneau/scratch/s/steinman/dbruneau/7_0_Surgical/Surgical_Cases/Pulsatile"
#
## Select 3 points tofit plane (if you don't know, just choose random ones, use the 
## point selector at the end of the script and re-run with different IDs)
#if "ase9" in case_name:
#    point_ids = [3882,1102,691] # for case 9 plane
#    disp_rel_path = "Case9_m047_predeformed_finerflow/file_case9_el047/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case9_m047_predeformed_finerflow/mesh/file_case9_el047_domains000000.vtu"
#elif "ase16" in case_name:
#    point_ids = [1306,4222,2106] # for case 16 plane (neck1)
#    disp_rel_path = "Case16_m06_predeformed_finerflow/file_case16_el06/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case16_m06_predeformed_finerflow/mesh/file_case16_el06_domains000000.vtu"
#elif "ase3" in case_name:
#    point_ids = [1046,448,4090] # for case 3 plane (neck1)
#    point_ids_extracut = [1909,4445,1576] # for case 12 only 
#    point_ids_extracut2 = [2727,2618,2792] # for case 12 only 
#
#    disp_rel_path = "Case3_predeformed_finerflow/file_case3/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case3_predeformed_finerflow/mesh/file_case3_domains000000.vtu"
#elif "ase11" in case_name:
#    point_ids = [236,1998,3178] # for case 11 plane (neck1)
#    #point_ids = [2133,2694,1114] # for case 11 plane (neck1)
#    point_ids_extracut = [334,1614,1476] # for case 12 only 
#    disp_rel_path = "Case11_predeformed_finerflow/file_case11/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case11_predeformed_finerflow/mesh/file_case11_domains000000.vtu"
#elif "ase12" in case_name:
#    point_ids = [20,81,4222] # for case 12 plane (neck1)
#    point_ids_extracut = [612,1650,4770] # for case 12 only 
#    disp_rel_path = "Case12_predeformed_finerflow/file_case12/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case12_predeformed_finerflow/mesh/file_case12_domains000000.vtu"
#elif "ase8" in case_name:
#    point_ids = [3830,1896,6940] # for case 8 plane 
#    point_ids_extracut = [1930,6496,7664] # for case 8 only 
#    disp_rel_path = "Case8_m042_predeformed_finerflow/file_case8_el042/1/Visualization_sd1/displacement_save_deg_1.h5"
#    mesh_rel_path = "Case8_m042_predeformed_finerflow/mesh/file_case8_el042_domains000000.vtu"
#elif "MCA02" in case_name:
#    point_ids = [5598,4196,3468]
#    #point_ids_extracut = [1930,6496,7664] # for case 8 only 
#    mesh_rel_path = "MCA02_4D017/mesh/MCA02_4D017_domains000000.vtu"


import sys
import configparser
# Read from config file
config_file = sys.argv[1] # need to input config file for case

config = configparser.ConfigParser()
with open(config_file) as stream:
    config.read_string("[Case_Specific_Variables]\n" + stream.read()) 
# Read problem-specific variables from config file
case_path = os.path.normpath(config.get("Case_Specific_Variables","case_path_absolute").strip('\"'))
case_name = os.path.basename(case_path)

#print(os.listdir(case_path))

mesh_name = os.path.normpath(config.get("Case_Specific_Variables","mesh_path").strip('\"'))
mesh_name = mesh_name+"_domains000000.vtu"
mesh_path = os.path.join(case_path,"mesh",mesh_name)

#mesh_name = case_name + "_domains000000.vtu"
#mesh_path = os.path.join(case_path,"mesh",mesh_name)
#ifile_surface = case_name + "/" + config.get("Case_Specific_Variables","ifile_surface")
point_ids=np.array(list(map(int, config.get("Case_Specific_Variables","neck_plane_nodes").strip('\"').strip('[]').split(',')))) 
print(point_ids)
print(type(point_ids))

txt_out_file = mesh_path.replace("domains000000.vtu","neck_area_and_volume.txt")
neck_path = mesh_path.replace("domains000000.vtu","neck.vtk")
neck_path_flat = mesh_path.replace("domains000000.vtu","neck_flat.vtk")
sac_path = mesh_path.replace("domains000000.vtu","sac.vtk")
sac_path_flat = mesh_path.replace("domains000000.vtu","sac_flat.vtk")


txt_out = []
#txt_out_file =mesh_path+"neck_area_and_volume.txt"
txt_out.append("Case name is: "+mesh_path+"\n")

# Helper function to compute the volume of the bounding box of a pyvista object
def bounding_box_volume(mesh_name):
    points =mesh_name.outline().points
    x=[]
    y=[]
    z=[]
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    xmax = np.max(np.array(x))
    xmin = np.min(np.array(x))
    ymax = np.max(np.array(y))
    ymin = np.min(np.array(y))
    zmax = np.max(np.array(z))
    zmin = np.min(np.array(z))
    vol = (xmax-xmin)*(ymax-ymin)*(zmax-zmin)
    return vol

# Read mesh

mesh_fsi = pv.read(mesh_path)


#index_t = 2960
#
#vectorData = h5py.File(disp_path, "r") 
#ArrayName = 'VisualisationVector/' + str(index_t)   
#deformation = vectorData[ArrayName][:,:] # Important not to take slices of this array, slows code considerably... 
#
#mesh_fsi.points = mesh_fsi.points + deformation

mesh = mesh_fsi.threshold(value=[0.99,1.01], scalars='f')

#print(mesh.array_names)
#pl = pv.Plotter()
##pl = pv.Plotter(off_screen=True)
#pl.add_mesh(mesh, color='white',opacity=0.1)
#
#pl.add_mesh(fluid_only, color='pink', show_edges=True, pickable=False)
#pl.show()



# Save original mesh indices for later
mesh['orig_indices'] = np.arange(mesh.n_points, dtype=np.int32)
mesh.points =  mesh.points*1000 # NEED to scale to mm for some vmtk scripts to work.
###########################
# Get surface
###########################
surf = mesh.extract_surface()

# Calculate volume of original mesh
vol = vmtkscripts.vmtkMeshVolume()
vol.Mesh=mesh
vol.Execute()
txt_out.append("Mesh volume is {} (in mm^3)\n".format(vol.Volume))

# Tidy up this clipping algorithm....

# Plot plane through neck points
cloud = np.array([mesh.points[point_ids[0],:],mesh.points[point_ids[1],:],mesh.points[point_ids[2],:]])
print(point_ids)
plane, center, normal = pv.fit_plane_to_points(cloud, return_meta=True)





#if "ase3" in mesh_path:
#    cloud = np.array([mesh.points[point_ids_extracut2[0],:],mesh.points[point_ids_extracut2[1],:],mesh.points[point_ids_extracut2[2],:]])
#    plane_ex2, center_ex2, normal_ex2 = pv.fit_plane_to_points(cloud, return_meta=True)
#
## if the case requires an extra cut to isolate the sac
#if "ase8" in mesh_path or "ase12" in mesh_path or "ase11" in mesh_path or "ase3" in mesh_path:
#    # Plot plane through neck points
#    cloud = np.array([mesh.points[point_ids_extracut[0],:],mesh.points[point_ids_extracut[1],:],mesh.points[point_ids_extracut[2],:]])
#    plane_ex, center_ex, normal_ex = pv.fit_plane_to_points(cloud, return_meta=True)
#    extracut = mesh.clip(origin=center_ex, normal=normal_ex)#, invert=False)
#    extracut2 = mesh.clip(origin=center_ex, normal=normal_ex, invert=False)
#    if bounding_box_volume(extracut) > bounding_box_volume(extracut2):
#        mesh=extracut
#    else:
#        mesh=extracut2
#
#if "ase3" in mesh_path:
#    del cloud, plane_ex, center_ex, normal_ex, extracut, extracut2
#    # Plot plane through neck points
#
#    extracut = mesh.clip(origin=center_ex2, normal=normal_ex2)#, invert=False)
#    extracut2 = mesh.clip(origin=center_ex2, normal=normal_ex2, invert=False)
#    if bounding_box_volume(extracut) > bounding_box_volume(extracut2):
#        mesh=extracut
#        print(bounding_box_volume(extracut))
#        print(bounding_box_volume(extracut2))
#
#    else:
#        mesh=extracut2
#        print("q")

clipped = mesh.clip(origin=center, normal=normal)#, invert=False)
clipped2 = mesh.clip(origin=center, normal=normal, invert=False)


clipped.plot()
val = input("Does this clip contain the sac (enter y or n):")
print(val)
if val == "n":
    clipped = clipped2
    print("Took the other side of the clip containing the sac")
else:
    print("Took this side of the clip that contains the sac")


#if bounding_box_volume(clipped) > bounding_box_volume(clipped2):
#    clipped=clipped2


clipped = clipped.connectivity(largest=False)
bodies = clipped.split_bodies()

for i, body in enumerate(bodies):
    print(f"Body {i} volume: {body.volume:.3f}")
    pl = pv.Plotter()
    pl.add_text('Showing Body ID#: {}'.format(i), position='upper_right',  color='blue', shadow=True, font_size=26)
    pl.add_mesh(body)
    pl.show()

    val = input("Is this the sac (enter y or n):")
    print(val)
    if val == "y":
        clipped = body
        break

clipped.save(sac_path_flat) # Save flat clipped sac

# Calculate the volume of the sac
vol = vmtkscripts.vmtkMeshVolume()
vol.Mesh=clipped
vol.Execute()
sac_volume=vol.Volume
txt_out.append("Sac volume is {} (in mm^3)\n".format(sac_volume))

# Calculate neck area
sliced = mesh.slice(origin=center, normal=normal)#, invert=False)

print(type(sliced))
sliced = sliced.connectivity(largest=False)
bodies = sliced.split_bodies()

for i, body in enumerate(bodies):
    pl = pv.Plotter()
    pl.add_text('Showing Plane ID#: {}'.format(i), position='upper_right',  color='blue', shadow=True, font_size=26)
    pl.add_mesh(body)
    pl.add_mesh(mesh,opacity=0.1)
    pl.show()

    val = input("Is this (Plane #{}) the neck (enter y or n):".format(i))
    print(val)
    if val == "y":
        sliced = body
        break


print(type(sliced))

sliced_plane = sliced.compute_cell_sizes()

neck_plane_surf_out = sliced_plane.extract_surface()
print(type(neck_plane_surf_out))
neck_plane_surf_out.save(neck_path_flat)  # save flat clipped neck

#print(dir(sliced_plane))
#print(sliced_plane.area)
neck_area = np.sum(sliced_plane["Area"])
txt_out.append("Neck area (cross-section) is {} (in mm^2)\n".format(neck_area))
# Calculate neck diameter
neck_diameter = np.sqrt(neck_area*4/3.14159)
txt_out.append("Neck diameter is {} (in mm)\n".format(neck_diameter))

# Make larger plane (if sac goes past plane boundaries, distance is not calculated correctly)
measurement_plane = pv.Plane(center=center, direction=normal, i_size=50, j_size=50, i_resolution=10, j_resolution=10)

# Calculate sac height
_ = clipped.compute_implicit_distance(measurement_plane, inplace=True)
clipped['implicit_distance'] = np.abs(clipped['implicit_distance'])

# plot to ensure algorithm works
pl = pv.Plotter()
_ = pl.add_mesh(clipped, scalars='implicit_distance', cmap='bwr')
_ = pl.add_mesh(measurement_plane, color='w', style='wireframe')
pl.show()

height = np.max(clipped['implicit_distance'])
txt_out.append("Sac height is {} (in mm)\n".format(height))

# Calculate aspect ratio
aspect_ratio = height/neck_diameter
txt_out.append("Aspect ratio is {}\n".format(aspect_ratio))

# Save neck area and sac volume to file
txt_out.append("------------------------------------------------\n")
file_object = open(txt_out_file, 'w')
for line in txt_out:
    file_object.write(line)
    print(line)
file_object.close()


# Algorithm to extract curved neck using vmtk
try:
    neck_plane = pv.read(neck_path)
    sac_surf=pv.read(sac_path)

except:

    ######################################################
    # Centerlines 
    # Note: When IDing outlets, also click on top of sac.
    # Click sac last.
    # ALSO, this doesnt work at FSI scale (units in meters) need to scale by x1000 (units in mm)q
    ######################################################
    centerline_filt = vmtkscripts.vmtkCenterlines()
    centerline_filt.Surface = surf
    centerline_filt.SeedSelectorName = 'pickpoint'
    centerline_filt.Resampling = 1
    centerline_filt.ResamplingStepLength = 0.05
    centerline_filt.smoothing = True
    centerline_filt.iterations = 100
    centerline_filt.factor = 0.1
    centerline_filt.Execute()
    centerlines = centerline_filt.Centerlines
    
    viewCent = vmtkscripts.vmtkCenterlineViewer()
    viewCent.Centerlines = centerlines
    viewCent.Execute()
    
    ###########################
    # ID branches on centerline
    ###########################
    brancher = vmtkscripts.vmtkBranchExtractor()
    brancher.Centerlines = centerlines
    brancher.RadiusArrayName = 'MaximumInscribedSphereRadius'
    brancher.Execute()
    centerlines_branched = brancher.Centerlines
    
    ###########################
    # ID branch groups on surf
    ###########################
    clipper = vmtkscripts.vmtkBranchClipper()
    clipper.Surface = surf
    clipper.Centerlines = centerlines_branched
    clipper.Execute()
    
    surf_clipped = pv.wrap(clipper.Surface)
    centerlines_clipped = pv.wrap(clipper.Centerlines)
   
    ###########################
    # ID sac
    ###########################
    branch_ids = np.unique(surf_clipped.point_arrays['GroupIds'])
    print(branch_ids)
    surf_clipped.plot(scalars="GroupIds")
 
    sac_idx = branch_ids[-1]
    
    mask = [0 if sac_idx != x else 1 for x in surf_clipped.point_arrays['GroupIds']]
    surf_clipped.point_arrays['SacMask'] = mask
    surf_clipped['Displacement'] = surf_clipped.point_arrays['GroupIds']
    surf_clipped.plot(scalars='SacMask')
    
    
    sac_surf = surf_clipped.threshold(1, scalars='SacMask')
    sac_surf = sac_surf.extract_surface()

   
    ###########################
    # Extract neck line 
    ###########################
    neck = sac_surf.extract_feature_edges(
    		feature_angle=60,
    		boundary_edges=True,
    		non_manifold_edges=False,
    		feature_edges=False,
    		manifold_edges=False,
    		).extract_largest()

    
    neck = neck.clean()
    neck_plane = neck.delaunay_2d()
    neck_plane = neck_plane.triangulate()

    neck_plane_edges = neck_plane.extract_feature_edges(
    		feature_angle=60,
    		boundary_edges=True,
    		non_manifold_edges=False,
    		feature_edges=False,
    		manifold_edges=False,
    		)
    
    neck_plane =  neck_plane.subdivide(2)
    neck_plane = neck_plane.smooth(5000)
    

    combined = neck_plane+sac_surf
    combined.points = combined.points/1000

    neck_plane.save(neck_path)    
    sac_surf.save(sac_path) 



#

# These last lines plot the automatically extracted sac from vmtk, with the option to pick points.
# This can be used to determine three points to fit a flat plane, close to the auomatically extracetd sac

def callback(mesh, pid):
    #print(surf.point_arrays['orig_indices'][pid])
    point = surf.points[pid]
    pl.add_point_labels(point, ["Point ID: "+str(surf.point_arrays['orig_indices'][pid])])



pl = pv.Plotter()
#pl = pv.Plotter(off_screen=True)


pl.add_mesh(clipped, color='pink', show_edges=True, pickable=False)
pl.add_mesh(sac_surf, color='blue', show_edges=True, opacity=0.5, pickable=False)
pl.add_mesh(surf, color='white',opacity=0.1)
pl.enable_point_picking(callback=callback, show_message="Click P to show the point ID for the nearest point",use_mesh=True,font_size=18,show_point=True)
pl.show()
#pl.show(screenshot='airplane.png')
