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
for i in range(num_bands):
    lower_freq[i] = float(bands_list[2*i])
    higher_freq[i] = float(bands_list[2*i+1])

r_sphere=float(sys.argv[8])
time_step_idx=int(sys.argv[9])
warp_factor=float(sys.argv[10])
num_frames=6


color_list = ["orange","green","red","purple","blue","pink"]
outline_echo=True
geom_color = "white"

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
image_folder =  os.path.join(visualization_path,"../Images/Mode_Shapes")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

silhouette_outer = dict(
    color='black',
    line_width=5.0,decimate=0
)
#silhouette_outer_echo = dict(
#    color=[0.5, 0.5, 0.5],default_opacity=0.5,
#    line_width=2.0,decimate=1
#)
#silhouette_outer_echo2 = dict(
#    color=[0.7, 0.7, 0.7],default_opacity=0.7,
#    line_width=2.0,decimate=1
#)
#silhouette_outer_echo3 = dict(
#    color=[0.8, 0.8, 0.8],default_opacity=0.8,
#    line_width=2.0,decimate=1
#)
#silhouette_outer_echo4 = dict(
#    color=[0.9, 0.9, 0.9],default_opacity=0.9,
#    line_width=2.0,decimate=1
#)
silhouette_outer_echo = dict(
    color='black',opacity=0.5,
    line_width=2.0,decimate=0
)
silhouette_outer_echo2 = dict(
    color='black',opacity=0.3,
    line_width=2.0,decimate=0
)
silhouette_outer_echo3 = dict(
    color='black',opacity=0.2,
    line_width=2.0,decimate=0
)
silhouette_outer_echo4 = dict(
    color='black',opacity=0.1,
    line_width=2.0,decimate=0
)


for low_freq,high_freq,mode_color in zip(lower_freq,higher_freq,color_list):

    band_name_str = str(int(np.rint(low_freq)))+"_to_"+str(int(np.rint(high_freq)))
    res_file = "displacement_"+band_name_str+".h5"
    res_path = os.path.join(visualization_hi_pass_folder,res_file)
    
    for i in range(num_frames):
        ts=i+time_step_idx
    
        image_path = os.path.join(image_folder, 'pyvista_mode_shape_multiframe_nooutline_'+band_name_str+'_timestep_'+str(ts)+"_warp_"+str(warp_factor)+'.png')

        u_vec = postprocessing_common_pv.get_data_at_idx(res_path, ts)
        cmap='jet'
        scalar_array_name = 'Band_Disp_Mag_'+band_name_str
        vector_array_name = 'Band_Disp_Vec_'+band_name_str
        #surf.compute_normals(inplace=True)
        u_mag = np.linalg.norm(u_vec, axis=1)*1000000
        
        
        mesh.point_arrays[scalar_array_name] = u_mag
        mesh.point_arrays[vector_array_name] = u_vec
        print(np.max(u_mag))
        #mesh.point_data.set_vectors(u_vec, vector_array_name)

        mesh.points = mesh_undeformed.points + u_vec*warp_factor
        outer_surf = mesh.extract_surface()
        outer_surf = outer_surf.smooth(n_iter=50)
        outer_surf.compute_normals(inplace=True)
        
        # Make a geometric object to use as the glyph
        #geom = pv.Arrow()  # This could be any dataset
        
        # Perform the glyph
        #glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=0.001*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=0.05)
        
        

        plotter= pv.Plotter(off_screen=True)
           
        #plotter.add_mesh(glyphs, show_scalar_bar=False, lighting=True, specular=0.00, diffuse=0.9,ambient=0.5, color=mode_color)
        if outline_echo:
            if i >= 4:
                plotter.add_mesh(outer_surf_prev4, color=geom_color, silhouette=silhouette_outer_echo4, opacity=0.1, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 3:
                plotter.add_mesh(outer_surf_prev3, color=geom_color, silhouette=silhouette_outer_echo3, opacity=0.2, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 2:
                plotter.add_mesh(outer_surf_prev2, color=geom_color, silhouette=silhouette_outer_echo2, opacity=0.32, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 1:
                plotter.add_mesh(outer_surf_prev, color=geom_color, silhouette=silhouette_outer_echo, opacity=0.5, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
        else:
            if i >= 4:
                plotter.add_mesh(outer_surf_prev4, color=geom_color, opacity=0.1, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 3:
                plotter.add_mesh(outer_surf_prev3, color=geom_color, opacity=0.2, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 2:
                plotter.add_mesh(outer_surf_prev2, color=geom_color, opacity=0.32, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
            if i >= 1:
                plotter.add_mesh(outer_surf_prev, color=geom_color, opacity=0.5, lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)
        plotter.add_mesh(outer_surf, color=geom_color, silhouette=silhouette_outer,lighting=True,smooth_shading=True, specular=0.00, diffuse=0.9, ambient=0.5)


        
        plotter.show(auto_close=False)  
        
        plotter.camera_position = cpos
        plotter.show(screenshot=image_path) 
        plotter.close()

        if i >=3:
            outer_surf_prev4 = outer_surf_prev3.copy()
        if i >=2:
            outer_surf_prev3 = outer_surf_prev2.copy() 
        if i >=1:
            outer_surf_prev2 = outer_surf_prev.copy()
        outer_surf_prev = outer_surf.copy()

        #del(mesh)
        #del(surf)
