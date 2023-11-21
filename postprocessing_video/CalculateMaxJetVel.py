import pyvista as pv
from pyvista import examples
import numpy as np
import vtk
import postprocessing_common_pv
import sys
import os

pv.set_plot_theme("document")

CameraPosition = np.array(list(map(float, sys.argv[3].strip('[]').split(','))))
CameraFocalPoint = np.array(list(map(float, sys.argv[4].strip('[]').split(','))))
CameraViewUp = np.array(list(map(float, sys.argv[5].strip('[]').split(',')) ))
CameraParallelScale = float(sys.argv[6])

case_path = sys.argv[1]
mesh_name = sys.argv[2]
mesh_path = os.path.join(case_path,"mesh",mesh_name + ".h5")
neck_path = mesh_path.replace(".h5","_neck_flat.vtk")
sac_path = mesh_path.replace(".h5","_sac_flat.vtk")

mesh, surf = postprocessing_common_pv.assemble_mesh(mesh_path)

neck_plane = pv.read(neck_path)
sac = pv.read(sac_path)
sac.points = sac.points/1000
neck_plane.points = neck_plane.points/1000

# This option will only work with onscreen rendering (needs to be run locally)
det_cam_position=0
contour_val=float(sys.argv[7])
time_step_idx=int(sys.argv[8])


cpos = [CameraPosition,
        CameraFocalPoint,
        CameraViewUp]

# Define necessary folders
visualization_path = postprocessing_common_pv.get_visualization_path(case_path)
visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")
visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")
visualization_sd1_folder = os.path.join(visualization_path,"../Visualization_sd1")
image_folder =  os.path.join(visualization_path,"../Images")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

image_path = os.path.join(image_folder, 'pyvista_neck_plane_'+str(contour_val)+'.png')
res_path = os.path.join(visualization_sd1_folder, "velocity_save_deg_1.h5")

# Read in vector at specific timestep
u_vec = postprocessing_common_pv.get_data_at_idx(res_path, time_step_idx)

# Compute normals (smooths the surface)
surf.compute_normals(inplace=True)
u_mag = np.linalg.norm(u_vec, axis=1) # take magnitude

mesh.point_arrays['u_mag'] = u_mag # Assign scalar to mesh
mesh.point_arrays["u_vec"] = u_vec

# Project data onto neck plane
interpolated = neck_plane.sample(mesh)

# Now we compute the normal of the neck plane and determine which flow is goinf in or out of the sac.
interpolated.compute_normals(inplace=True)
#print(interpolated["Normals"])

# center id of neck plane (we want the normal at the center)
center_id = interpolated.find_closest_point(interpolated.center)
center_normal = interpolated["Normals"][center_id,:]

# Center of sac
sac_center = np.array(sac.center)
sac_vector = sac_center - np.array(interpolated.center)
sac_vector_mag = np.linalg.norm(sac_vector) # take magnitude
sac_unit_vector = sac_vector/sac_vector_mag

# We need to invert the normal if the normals point in the outflow direction
if np.dot(sac_unit_vector,center_normal) < 0.0:
    center_normal=-center_normal

# this cosine value will tell us which flow is pointing in or out of the sac (thresholding above zero for inflow, below for outflow)
cosine = np.dot(interpolated["u_vec"],center_normal)/interpolated["u_mag"]
interpolated.point_arrays["cosine"]=cosine
#interpolated.plot_normals(mag=0.001, show_edges=True)

inflow = interpolated.threshold(value=0.0,scalars="cosine")
outflow = interpolated.threshold(value=0.0,scalars="cosine",invert=True)


# Determine maximum velocity in outflow region

inflow_vel = []
outflow_vel = []
for i, cos in enumerate(interpolated["cosine"]):
    if cos >= 0.0:
        inflow_vel.append(interpolated["u_mag"][i])
    else:
        outflow_vel.append(interpolated["u_mag"][i])

max_inflow_vel = np.max(inflow_vel) # Do 99th percentile instead of maximum
max_outflow_vel = np.max(outflow_vel)
perc_99th_inflow_vel = np.percentile(inflow_vel,99) # Do 99th percentile instead of maximum



max_inflow_point = np.argmax(inflow["u_mag"]) # Do 99th percentile instead of maximum
max_point = np.argmax(interpolated["u_mag"]) # Do 99th percentile instead of maximum
max_vel_neck = np.max(interpolated["u_mag"]) # Do 99th percentile instead of maximum
max_vel_overall = np.max(mesh["u_mag"]) # Do 99th percentile instead of maximum
perc_99th_vel_overall = np.percentile(mesh["u_mag"],99) # Do 99th percentile instead of maximum

print(" t = {}, node with highest vel: {}".format(time_step_idx,max_point))
print("max inflow (into the sac) vel: {}".format(max_inflow_vel))
print("99th Percentile inflow vel: {}".format(perc_99th_inflow_vel))
print("max outflow vel: {}".format(max_outflow_vel))
print("max overall vel: {}".format(max_vel_overall))
print("99th Percentile overall vel: {}".format(perc_99th_vel_overall))

