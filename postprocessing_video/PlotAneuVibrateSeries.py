import pyvista as pv
from pyvista import examples
import numpy as np
import vtk

# This script generates a series of cartoon-like images of Hi_pass and Lo-pass q criterion. 
# Can automate this more to point to folders, extract paraview stuff automatically, etc

start_frame = 2975
end_frame = 3013
n_ts = end_frame-start_frame
idx=0
det_cam_position=0   # Set to 1 so you can determine the camera position (position the aneurysm, exit and then the camera position will print to terminal)
trace=1  # This adds outlines of previous steps to the image. 

silhouette_outer = dict(
    color='black',
    line_width=3.0,decimate=1
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
    line_width=2.0,decimate=1
)
silhouette_outer_echo2 = dict(
    color='black',opacity=0.3,
    line_width=2.0,decimate=1
)
silhouette_outer_echo3 = dict(
    color='black',opacity=0.2,
    line_width=2.0,decimate=1
)
silhouette_outer_echo4 = dict(
    color='black',opacity=0.1,
    line_width=2.0,decimate=1
)
silhouette = dict(
    color='black',
    line_width=2.0,decimate=1
)   
silhouette_lo = dict(
    color='grey',
    line_width=2.0,decimate=1
)   
for idx in range(n_ts+1):
    outer_surf = pv.read("SurfaceSeries/C9_Q/C9_Surf_Vibrate_"+str(start_frame+idx)+".vtp")
    q_hi = pv.read("SurfaceSeries/C9_Q/C9_Qcrit_hi_"+str(start_frame+idx)+".vtp")
    q_lo = pv.read("SurfaceSeries/C9_Q/C9_Qcrit_lo_"+str(start_frame+idx)+".vtp")



    surf = q_lo.extract_geometry()
    q_lo_smooth = surf.smooth(n_iter=100)
    surf = q_hi.extract_geometry()
    q_hi_smooth = surf.smooth(n_iter=100)
    
    if det_cam_position == 1:
        plotter= pv.Plotter()
    else:
        plotter= pv.Plotter(off_screen=True)

    plotter.add_mesh(q_lo_smooth, color='grey', silhouette=silhouette_lo, opacity=0.3, lighting=False)
    plotter.add_mesh(q_hi_smooth, color='purple', silhouette=silhouette, lighting=False)
    #plotter.add_mesh(outer_surf, color='white', silhouette=silhouette_outer, opacity=0.125)

    if trace == 1:
        if idx >= 4:
            plotter.add_mesh(outer_surf_prev4, color='white', silhouette=silhouette_outer_echo4, opacity=0.0, lighting=False)
        if idx >= 3:
            plotter.add_mesh(outer_surf_prev3, color='white', silhouette=silhouette_outer_echo3, opacity=0.0, lighting=False)
        if idx >= 2:
            plotter.add_mesh(outer_surf_prev2, color='white', silhouette=silhouette_outer_echo2, opacity=0.0, lighting=False)
        if idx >= 1:
            plotter.add_mesh(outer_surf_prev, color='white', silhouette=silhouette_outer_echo, opacity=0.0, lighting=False)

    plotter.add_mesh(outer_surf, color='white', silhouette=silhouette_outer, opacity=0.125,lighting=False)



    plotter.set_background('white')
    plotter.camera_position =[(0.11058973743501245, 0.13903481799231496, 0.0541019180517798),
                              (0.12077634890773657, 0.13550843395407347, 0.06270945219459416),
                              (0.5652183791097327, -0.2699743307073844, -0.7795139797820603)]
    
    if det_cam_position == 1:
        plotter.show(auto_close=False) 
        print(plotter.camera_position)
        break
 
    #
    plotter.show(screenshot="Video/videoFrameTraceGrey_"+str(start_frame+idx)+".png")     
    plotter.close()  
    if idx >=3:
        outer_surf_prev4 = outer_surf_prev3 
    if idx >=2:
        outer_surf_prev3 = outer_surf_prev2 
    if idx >=1:
        outer_surf_prev2 = outer_surf_prev
    outer_surf_prev = outer_surf
