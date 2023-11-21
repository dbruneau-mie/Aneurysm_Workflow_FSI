import pyvista as pv
from pyvista import examples
import numpy as np
import vtk
import postprocessing_common_pv
import sys
import os

# Currently this is hard-coded to only work with Case 3... 

pv.set_plot_theme("document")
CameraPosition = np.array(list(map(float, sys.argv[3].strip('[]').split(','))))
CameraFocalPoint = np.array(list(map(float, sys.argv[4].strip('[]').split(','))))
CameraViewUp = np.array(list(map(float, sys.argv[5].strip('[]').split(',')) ))
CameraParallelScale = float(sys.argv[6])

case_path = sys.argv[1]
mesh_name = sys.argv[2]
mesh_path = os.path.join(case_path,"mesh",mesh_name + ".h5")
mesh, surf = postprocessing_common_pv.assemble_mesh(mesh_path)
mesh_undeformed = mesh.copy()

bands=sys.argv[7]
bands_list = bands.split(",")
num_bands = int(len(bands_list)/2)
lower_freq = np.zeros(num_bands)
higher_freq = np.zeros(num_bands)
pass_stop_list = []  # for multi-band filter, 
for i in range(num_bands):
    lower_freq[i] = float(bands_list[2*i])
    higher_freq[i] = float(bands_list[2*i+1])
    if higher_freq[i] - lower_freq[i] > 1000: 
        pass_stop_list.append("pass")  # let all high frequencies pass initially for multiband
    else:
        pass_stop_list.append("stop")  # stop the specified narrowbands
print(pass_stop_list)

r_sphere=float(sys.argv[8])
time_step_idx=int(sys.argv[9])
glyph_length=float(sys.argv[10])
glyph_density=float(sys.argv[11])

print("Glyph dens: {}".format(glyph_density))
num_frames=100


# We will automatically choose the mode glyph color from this series, in the order that bands are listed in "bands" input
color_list = ["orange","green","red","purple","blue","pink"]
  
print(glyph_length)

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
image_folder =  os.path.join(visualization_path,"../Images/Mode_Shapes_bold")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Find files here
viz_type = "displacement"
for lowfreq, highfreq, pass_stop in zip(lower_freq,higher_freq,pass_stop_list):
    viz_type = viz_type+"_"+pass_stop+"_"+str(int(np.rint(lowfreq)))+"_to_"+str(int(np.rint(highfreq)))
res_file = viz_type+".h5"
res_path = os.path.join(visualization_hi_pass_folder,res_file)

print(res_file)

u_max=0
for i in range(num_frames):
    ts=i+time_step_idx
    u_vec = postprocessing_common_pv.get_data_at_idx(res_path, ts)
    u_mag = np.linalg.norm(u_vec, axis=1)*1000000
    
    if np.max(u_mag) > u_max:
        u_max = np.max(u_mag)

# We scale the mode shapes based on the size of the surrounding sphere for the sac and normalize to the max disp
warp_factor = (r_sphere*1000000/5)/u_max
print("Warp Factor is {}".format(warp_factor))
print("Warp Factor is {}".format(warp_factor))

for i in range(num_frames):
    ts=i+time_step_idx

    image_path = os.path.join(image_folder, 'pyvista_mode_shape_light_bigger_color_arrows'+viz_type+'_timestep_'+str(ts)+"_warp_"+str(warp_factor)+'.png')

    u_vec = postprocessing_common_pv.get_data_at_idx(res_path, ts)
    cmap='jet'
    scalar_array_name = 'Band_Disp_Mag_'+viz_type
    vector_array_name = 'Band_Disp_Vec_'+viz_type
    #surf.compute_normals(inplace=True)
    u_mag = np.linalg.norm(u_vec, axis=1)*1000000
    

    
    mesh.point_arrays[scalar_array_name] = u_mag
    mesh.point_arrays[vector_array_name] = u_vec
    print(np.max(u_mag))
    #mesh.point_data.set_vectors(u_vec, vector_array_name)
    surf_plotold = mesh.copy().extract_surface()
    
    mesh.points = mesh_undeformed.points + u_vec*warp_factor
    surf_plot = mesh.extract_surface()
    surf_plot.compute_normals(inplace=True)
    
    # Make a geometric object to use as the glyph
    geom = pv.Arrow(tip_length=0.5,tip_radius=0.2,shaft_radius=0.1)  # This could be any dataset
    geom = pv.Arrow(tip_length=0.35,tip_radius=0.13)  # This could be any dataset

    geom = pv.Arrow(tip_length=0.5,tip_radius=0.2,shaft_radius=0.1)  # This could be any dataset
    geom = pv.Arrow(tip_length=0.4,tip_radius=0.17,shaft_radius=0.1)  # This could be any dataset





    # Perform the glyph
    #glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=glyph_length*0.003*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=glyph_density*1.5)
    glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=glyph_length*0.0015*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=glyph_density*1.5) # old recipe...
    
    print(glyph_density)
    #glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=0.001*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=0.05)
    
    
    silhouette_outer = dict(
        color='black',
        line_width=6.0,decimate=0.0
    )
    
    
    plotter= pv.Plotter(off_screen=True)
    #plotter.set_background(color="gray")
    plotter.add_mesh(surf_plot, 
                    silhouette=silhouette_outer, 
                    opacity=0.3, 
                    color="orange",
                    lighting=True, 
                    smooth_shading=True, 
                    specular=0.00, 
                    diffuse=0.9,
                    ambient=0.5)                
                    #specular=0.0, 
                    #diffuse=0.5,
                    #ambient=0.5,)
    plotter.add_mesh(glyphs,show_scalar_bar=False, lighting=True, specular=0.00, diffuse=0.9,ambient=0.5, color="orange",show_edges=True)
    
    plotter.show(auto_close=False)  
    
    plotter.camera_position = cpos
    plotter.show(screenshot=image_path) 
    plotter.clear()    
    #del(mesh)
    #del(surf)
