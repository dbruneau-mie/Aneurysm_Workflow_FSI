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


print("read camera position:")
print(CameraPosition)
print(CameraFocalPoint)
print(CameraViewUp)

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


#points = pv.PolyData(mesh.points)
#points['u_mag'] = u_mag

contour = mesh.contour([contour_val], scalars="u_mag")
if contour.n_points > 0:
    contour = postprocessing_common_pv.vtk_taubin_smooth(contour) # smooth the surface
    contour.compute_normals(inplace=True) # Compute normals


silhouette = dict(
    color='black',
    line_width=4.0,decimate=None
)

silhouette_outer = dict(
    color='black',
    line_width=3.0,decimate=None
)
geom = pv.Arrow(tip_length=0.4,tip_radius=0.17,shaft_radius=0.1)  # This could be any dataset

#if det_cam_position == 1:
#    plotter= pv.Plotter(notebook=0)
#else:
#    plotter= pv.Plotter(off_screen=True)
#
#
#
plotter= pv.Plotter()
#plotter.add_mesh(points,scalars="u_mag",opacity=0.35,point_size=10.0, render_points_as_spheres=True) 
plotter.add_mesh(surf, 
                color='snow', 
                silhouette=silhouette_outer, 
                show_scalar_bar=False,
                opacity=0.35,
                lighting=True, 
                smooth_shading=True, 
                specular=0.00, 
                diffuse=0.9,
                ambient=0.5, 
                name='surf',
                culling='front'
                )

#interpolated = neck_plane.interpolate(points,radius=1000,sharpness=0.1)
interpolated = neck_plane.sample(mesh)
#interpolated=interpolated.threshold(value=0.0)
#plotter.add_mesh(interpolated,scalars="u_mag",point_size=10.0, render_points_as_spheres=True)
glyphs = interpolated.glyph(orient="u_vec", scale="u_mag", factor=0.002, geom=geom, tolerance=0.08)
plotter.add_mesh(glyphs, show_scalar_bar=False, lighting=True, specular=0.00, diffuse=0.9,ambient=0.5,show_edges=True)


# Now we compute the normal of the neck plane and determine which flow is goinf in or out of the sac.
interpolated.compute_normals(inplace=True)
print(interpolated["Normals"])

# Average Normal
#avg_normal = np.mean(interpolated["Normals"],axis=0)
#print(avg_normal)

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

plotter.add_mesh(inflow,color="pink")
#plotter.add_mesh(outflow,color="grey")

# Determine maximum velocity in outflow region
#max_inflow_vel = np.max(inflow["u_mag"]) # Do 99th percentile instead of maximum
#max_outflow_vel = np.max(outflow["u_mag"])

inflow_vel = []
outflow_vel = []
for i, cos in enumerate(interpolated["cosine"]):
    if cos >= 0.0:
        inflow_vel.append(interpolated["u_mag"][i])
    else:
        outflow_vel.append(interpolated["u_mag"][i])

max_inflow_vel = np.max(inflow_vel) # Do 99th percentile instead of maximum
max_outflow_vel = np.max(outflow_vel)

max_inflow_point = np.argmax(inflow["u_mag"]) # Do 99th percentile instead of maximum
max_point = np.argmax(interpolated["u_mag"]) # Do 99th percentile instead of maximum
max_vel = np.max(interpolated["u_mag"]) # Do 99th percentile instead of maximum

print(max_vel)
print(max_point)
print(interpolated["cosine"][max_point])

print(max_inflow_vel)
print(max_outflow_vel)

#poly = pv.PolyData(interpolated.points[center_id])
#plotter.add_mesh(poly,point_size=10.0, render_points_as_spheres=True)
#
#poly2 = pv.PolyData(sac_center)
#plotter.add_mesh(poly2,point_size=10.0, render_points_as_spheres=True)

poly2 = pv.PolyData(interpolated.points[max_point])
plotter.add_mesh(poly2,point_size=20.0, render_points_as_spheres=True)

#if contour.n_points > 0:
#    plotter.add_mesh(contour,
#                    color='red', 
#                    silhouette=silhouette, 
#                    clim=[0.0, 2.0], # NOTE this is for u_mag only!
#                    lighting=True, 
#                    smooth_shading=True, 
#                    specular=0.00, 
#                    diffuse=0.9,
#                    ambient=0.5, 
#                    name='contour')

plotter.set_background('white')

plotter.show(auto_close=False)  

if det_cam_position == 1:
    plotter.show(auto_close=False) 
    print(plotter.camera_position)
else:
    plotter.camera_position = cpos
    plotter.show(screenshot=image_path)  


#interpolated.plot_normals(mag=0.001, show_edges=True)
