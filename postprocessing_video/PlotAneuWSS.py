import pyvista as pv
from pyvista import examples
import numpy as np
import vtk
import postprocessing_common_pv
import sys
import os
import h5py
import re

def assemble_tri_mesh_arrays(points, cells):
    n_elem = cells.shape[0]

    padding = np.ones((n_elem, 1), dtype=np.int64)*3
    cells = np.hstack((padding, cells)).ravel()
    
    cell_type = np.empty(n_elem, np.uint8)
    cell_type[:] = vtk.VTK_TRIANGLE
    
    mesh = pv.UnstructuredGrid(cells, cell_type, points)
    surf = mesh.extract_surface()

    return mesh, surf

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
    print(idx_of_time)
    return idx_of_time

pv.set_plot_theme("document")
CameraPosition = np.array(list(map(float, sys.argv[3].strip('[]').split(','))))
CameraFocalPoint = np.array(list(map(float, sys.argv[4].strip('[]').split(','))))
CameraViewUp = np.array(list(map(float, sys.argv[5].strip('[]').split(',')) ))
CameraParallelScale = float(sys.argv[6])

case_path = sys.argv[1]
mesh_name = sys.argv[2]
#mesh_path = os.path.join(case_path,"mesh",mesh_name + ".h5")


#t_peak_sys = 3.0795

if sys.argv[7] != 'auto':
    plot_lim=float(sys.argv[7])
else:
    plot_lim=sys.argv[7]

try:
    t_peak_sys=float(sys.argv[8])
    wss_file = "WSS_ts.h5"
    print("using WSS at discrete time")
except: 
    wss_file = "WSS.h5"
    print("Using TAWSS")

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

res_path = os.path.join(visualization_separate_domain_folder, wss_file)

vectorData = h5py.File(res_path) 



if "WSS_ts.h5" in res_path:
    points = np.array(vectorData["Mesh/0/mesh/geometry"])
    element_connectivity = np.array(vectorData["Mesh/0/mesh/topology"])
    xdmf_file = res_path.replace(".h5", ".xdmf")
    t_idx = get_idx_of_time(xdmf_file, t_peak_sys)
    image_path = os.path.join(image_folder, 'pyvista_WSS_t'+str(t_peak_sys)+'_lighting_lim_'+str(plot_lim)+mesh_name+'.png')


else:
    points = np.array(vectorData["Mesh/mesh/geometry"])
    element_connectivity = np.array(vectorData["Mesh/mesh/topology"])
    t_idx = 0
    image_path = os.path.join(image_folder, 'pyvista_TAWSS_lighting_lim_'+str(plot_lim)+mesh_name+'.png')

mesh, surf = assemble_tri_mesh_arrays(points,element_connectivity)




u_vec = postprocessing_common_pv.get_data_at_idx(res_path, t_idx)
cmap='jet'
array_name = 'WSS (Pa)'
surf.compute_normals(inplace=True)
u_mag = u_vec# np.linalg.norm(u_vec, axis=1)*1000000
print(u_mag.shape)
print(mesh.n_points)

mesh.point_arrays[array_name] = u_mag
print(u_mag.shape)
surf_plot = mesh.extract_surface()
surf_plot.compute_normals(inplace=True)

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
if sys.argv[7] != 'auto':
    clim=[0,plot_lim]
else:
    clim=None

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

plotter.show(auto_close=False)  

plotter.camera_position = cpos
plotter.show(screenshot=image_path) 