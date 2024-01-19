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
refined_mesh_path = os.path.join(case_path,"mesh",mesh_name + "_refined.h5")

mesh, surf = postprocessing_common_pv.assemble_mesh(mesh_path)
edges = mesh.extract_all_edges()
mesh_refined, surf_refined = postprocessing_common_pv.assemble_mesh(refined_mesh_path)


# This option will only work with onscreen rendering (needs to be run locally)
det_cam_position=0


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

image_path = os.path.join(image_folder, 'pyvista_mesh_ruler'+mesh_name+'.png')

# Compute normals (smooths the surface)
surf.compute_normals(inplace=True)


silhouette = dict(
    color='black',
    line_width=24.0,decimate=None
)

silhouette_outer = dict(
    color='black',
    line_width=3.0,decimate=None
)

if det_cam_position == 1:
    plotter= pv.Plotter(notebook=0)
else:
    plotter= pv.Plotter(off_screen=True)


                #style='wireframe')
plotter.window_size = 4000, 3000
plotter.add_mesh(surf, 
                color='snow', 
                silhouette=silhouette, 
                show_scalar_bar=False,
                opacity=1.0,
                lighting=True, 
                smooth_shading=True, 
                specular=0.00, 
                diffuse=0.9,
                ambient=0.5, 
                name='surf',
                culling='front')

plotter.add_mesh(edges, line_width=16.0, color='black')

plotter.add_points(mesh_refined.points,point_size=20,render_points_as_spheres=True,color='red')
#plotter.add_mesh(surf_refined, 
#                color='snow', 
#                silhouette=silhouette_outer, 
#                show_scalar_bar=False,
#                opacity=0.35,
#                lighting=True, 
#                smooth_shading=True, 
#                specular=0.00, 
#                diffuse=0.9,
#                ambient=0.5, 
#                name='surf',
#                culling='front'
#                )

#plotter.add_ruler(pointa=[surf.bounds[0], surf.bounds[2] - 0.0001, 0.0], pointb=[surf.bounds[1], surf.bounds[2] - 0.0001, 0.0], title="X Distance")
plotter.show_bounds(grid='front',  all_edges=True)
#plotter.camera.zoom(0.3)
plotter.set_background('white')

plotter.show(auto_close=False)  

if det_cam_position == 1:
    plotter.show(auto_close=False) 
    print(plotter.camera_position)
    plotter.show(screenshot=image_path)  
else:
    plotter.camera_position = cpos
    plotter.show(screenshot=image_path)  