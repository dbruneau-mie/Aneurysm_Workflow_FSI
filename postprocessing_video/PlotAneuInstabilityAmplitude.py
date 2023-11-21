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
mesh, surf = postprocessing_common_pv.assemble_mesh(mesh_path)

if sys.argv[7] != 'auto':
    plot_lim=float(sys.argv[7])
else:
    plot_lim=sys.argv[7]

time_step_idx=int(sys.argv[8])
colorbar_y=float(sys.argv[9])

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

image_path = os.path.join(image_folder, 'pyvista_instability_amplitude_lighting_lim_'+str(plot_lim)+mesh_name+'.png')
res_path = os.path.join(visualization_hi_pass_folder, "velocity_amplitude_25_to_1400.h5")

u_vec = postprocessing_common_pv.get_data_at_idx(res_path, time_step_idx)
cmap='jet'
array_name = 'u_mag'
surf.compute_normals(inplace=True)
u_mag = np.linalg.norm(u_vec, axis=1)
print(u_mag.shape)
print(mesh.n_points)

mesh.point_arrays[array_name] = u_mag
print(u_mag.shape)
surf_plot = mesh.extract_surface()
surf_plot.compute_normals(inplace=True)

bbox = mesh.bounds
#print(bbox)
point_cloud = pv.PolyData(mesh.points)
point_cloud["Instability Amplitude (m/s)"] = u_mag
grid = pv.UniformGrid()
#grid.dimensions = [bbox[1]-bbox[0], bbox[3]-bbox[2], bbox[5]-bbox[4]]
n_x=20
n_y=20
n_z=20
factor=1.2
#grid.origin = [(bbox[1]+bbox[0])/2, (bbox[3]+bbox[2])/2, (bbox[5]+bbox[4])/2]
grid.origin = [(bbox[0]), (bbox[2]), (bbox[4])]

grid.dimensions = [n_x,n_y,n_z]
grid.spacing = [factor*(bbox[1]-bbox[0])/n_x, factor*(bbox[3]-bbox[2])/n_y, factor*(bbox[5]-bbox[4])/n_z]
#grid['scalars'] = -grid.x
#
#result=grid
print("running interpolation")
#result = grid.interpolate(point_cloud)
print("finished interpolation")

#q_lo = pv.read("c9_surf/isosurface_Q_lo.vtp")
#outer_surf = pv.read("c9_surf/Outer_surf_normals.vtp")
#
#q_lo.points =  q_lo.points*1000 # NEED to scale to mm for some vmtk scripts to work.
#outer_surf.points =  outer_surf.points*1000 # NEED to scale to mm for some vmtk scripts to work.
#
#
#surf = q_lo.extract_geometry()
#q_lo_smooth = surf.smooth(n_iter=100)
#surf = outer_surf.extract_geometry()
#outer_surf_smooth = surf.smooth(n_iter=1, relaxation_factor=0.1, convergence=0.0, edge_angle=0.1, feature_angle=0.1, boundary_smoothing=False)
#

silhouette_outer = dict(
    color='black',
    line_width=4.0,decimate=0.0
)
sargs = dict(vertical=True,height=0.25, position_x=0.05, position_y=colorbar_y)
#mesh.plot(opacity=1.0, lighting=False)
contours = surf_plot.contour()
plotter= pv.Plotter(off_screen=True)
#plotter= pv.Plotter(notebook=0)

if sys.argv[7] != 'auto':
    clim=[0,plot_lim]
else:
    clim=None
'''
plotter.add_mesh(surf_plot, 
                scalars=array_name,
                cmap=cmap,
                scalar_bar_args=sargs, 
                silhouette=silhouette_outer, 
                opacity=1.0, 
                clim=clim,
                lighting=True, 
                smooth_shading=True, 
                specular=0.00, 
                diffuse=0.9,
                ambient=0.5)                
                #specular=0.0, 
                #diffuse=0.5,
                #ambient=0.5,)

plotter.add_mesh(contours,color="white", line_width=4,opacity=0.3)

'''

plotter.add_mesh(surf_plot,color="white",silhouette=silhouette_outer, opacity=0.0)

plotter.add_mesh(point_cloud,opacity="sigmoid_5",cmap='Reds',point_size=30,clim=clim, scalar_bar_args=sargs)#,silhouette=silhouette_outer, opacity=0.0)
#plotter.add_bounding_box(line_width=5, color='black')
#plotter.add_mesh(mesh, opacity="sigmoid",cmap="Greys")

#contour = mesh.contour([0.05], scalars="u_mag")
#if contour.n_points > 0:
#    plotter.add_mesh(contour,
#                    color='red', 
#                    silhouette=silhouette_outer, 
#                    clim=[0.0, 2.0], # NOTE this is for u_mag only!
#                    lighting=True, 
#                    smooth_shading=True, 
#                    specular=0.00, 
#                    diffuse=0.9,
#                    ambient=0.5, 
#                    name='contour')

#plotter.add_mesh(result, opacity="linear")
#plotter.add_volume(result,opacity="linear")
plotter.show(auto_close=False)  

plotter.camera_position = cpos
plotter.show(screenshot=image_path) 