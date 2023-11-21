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
glyph_length=float(sys.argv[10])
glyph_density=float(sys.argv[11])

print("Glyph dens: {}".format(glyph_density))
num_frames=200


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

silhouette_outer = dict(
    color='black',
    line_width=6.0,decimate=0.0
)
# Make a geometric object to use as the glyph
geom = pv.Arrow()  # This could be any dataset
geom = pv.Arrow(tip_length=0.35,tip_radius=0.13)  # This could be any dataset
geom = pv.Arrow(tip_length=0.4,tip_radius=0.17,shaft_radius=0.1)  # This could be any dataset

# Define necessary folders
visualization_path = postprocessing_common_pv.get_visualization_path(case_path)
visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")
visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")
visualization_sd1_folder = os.path.join(visualization_path,"../Visualization_sd1")
image_folder =  os.path.join(visualization_path,"../Images/Mode_Shape_Line_Point_Trace")


if not os.path.exists(image_folder):
    os.makedirs(image_folder)

for low_freq,high_freq,mode_color in zip(lower_freq,higher_freq,color_list):

    if high_freq - low_freq < 100 and "green" not in mode_color and "red" not in mode_color:

        band_name_str = str(int(np.rint(low_freq)))+"_to_"+str(int(np.rint(high_freq)))
        res_file = "displacement_"+band_name_str+".h5"
        res_path = os.path.join(visualization_hi_pass_folder,res_file)
        
        u_max_pos = 0
        i_max_pos = 0
        u_max_vec = np.array([0,0,0])
        u_max_neg = 0
        i_max_neg = 0
        node_max = 0
        for i in range(num_frames):
            ts=i+time_step_idx
            u_vec = postprocessing_common_pv.get_data_at_idx(res_path, ts)
            u_mag = np.linalg.norm(u_vec, axis=1)*1000000
            max_mag_vector_ts = u_vec[np.argmax(u_mag)]
        
        
            if np.max(u_mag) > u_max_pos and i < num_frames/2:# and np.argmax(u_vec[np.argmax(u_mag)]):
            #print(np.percentile(u_mag,99))
            #if np.percentile(u_mag,99) > u_max:
                u_max_pos = np.max(u_mag)
                i_max_pos = i
                u_max_vec = max_mag_vector_ts
                node_max = np.argmax(u_mag)
        
            direction_change = np.sign(u_max_vec[0]) != np.sign(max_mag_vector_ts[0]) or np.sign(u_max_vec[1]) != np.sign(max_mag_vector_ts[1]) or np.sign(u_max_vec[2]) != np.sign(max_mag_vector_ts[2])
            print(direction_change)
            print(u_max_vec)
            print(max_mag_vector_ts)
        
            if np.max(u_mag) > u_max_neg and i >= num_frames/2 and direction_change:  # and np.argmax(u_vec[np.argmax(u_mag)]):
                u_max_neg = np.max(u_mag)
                i_max_neg = i                

        
        # We scale the mode shapes based on the size of the surrounding sphere for the sac and normalize to the max disp
        warp_factor = (r_sphere*1000000/5)/u_max_pos
        print("Warp Factor is {}".format(warp_factor))
        print("Warp Factor is {}".format(warp_factor))
        original_point_location = mesh_undeformed.points[node_max]

        for i in range(num_frames):
            ts=i+time_step_idx
        
            image_path = os.path.join(image_folder, 'pyvista_mode_shape_dark_aneu_edge_color_arrows'+band_name_str+'_timestep_'+str(ts)+"_warp_"+str(warp_factor)+'.png')
    
            u_vec = postprocessing_common_pv.get_data_at_idx(res_path, ts)
            current_point_location = original_point_location + u_vec[node_max]*warp_factor
            if i == 0:
                u_vec_node_max =  u_vec[node_max]
                points_array = current_point_location
            else:
                u_vec_node_max = np.append(u_vec_node_max,u_vec[node_max])
                points_array = np.append(points_array, current_point_location)
            if i==1:
                lines_array = [2,0,1]
        
            elif i > 1:
                lines_array = np.append(lines_array,[2, i, i+1])
            print(u_vec_node_max)
            print(points_array)
        
            points_plot = pv.PolyData(points_array)
            currentPoint = pv.PolyData(current_point_location)

 



            cmap='jet'
            scalar_array_name = 'Band_Disp_Mag_'+band_name_str
            vector_array_name = 'Band_Disp_Vec_'+band_name_str
            #surf.compute_normals(inplace=True)
            u_mag = np.linalg.norm(u_vec, axis=1)*1000000
            
    
            
            mesh.point_arrays[scalar_array_name] = u_mag
            mesh.point_arrays[vector_array_name] = u_vec
            
            mesh.points = mesh_undeformed.points + u_vec*warp_factor
            surf_plot = mesh.extract_surface()
            surf_plot.compute_normals(inplace=True)
            

           
            # Perform the glyph
            #glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=glyph_length*0.0015*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=glyph_density*1.5)
            #glyphs = mesh.glyph(orient=vector_array_name, scale=scalar_array_name, factor=0.001*r_sphere/0.003*warp_factor/1000, geom=geom, tolerance=0.05)
            
            

            
            
            plotter= pv.Plotter(off_screen=True)
            plotter.set_background(color="#DEDFE4")
        
            plotter.add_mesh(surf_plot, 
                            silhouette=silhouette_outer, 
                            opacity=0.3, 
                            color="#ADAEB3",
                            lighting=True, 
                            smooth_shading=True, 
                            specular=0.00, 
                            diffuse=0.9,
                            ambient=0.5)                
                            #specular=0.0, 
                            #diffuse=0.5,
                            #ambient=0.5,)
            #plotter.add_mesh(glyphs, show_scalar_bar=False, lighting=True, specular=0.00, diffuse=0.9,ambient=0.5, color=mode_color,show_edges=True)
            #plotter.add_mesh(glyph,show_scalar_bar=False, lighting=True, specular=0.00, diffuse=0.9,ambient=0.5, color="orange",show_edges=True)
        
            if i>=1:
                points_plot.lines = lines_array
        
            #plotter.add_points(points_plot,point_size=1,render_points_as_spheres=True,color="orange")
            plotter.add_mesh(points_plot,line_width=5.0,color=mode_color)#,point_size=1,render_points_as_spheres=True,color="orange")
            plotter.add_points(currentPoint,point_size=5,render_points_as_spheres=True,color=mode_color)

     
            #plotter.show(auto_close=False)  
            
            plotter.camera_position = cpos
            plotter.show(screenshot=image_path) 
            plotter.clear()    
            plotter.close()    

            #del(mesh)
            del(points_plot)
            del(surf_plot)
    