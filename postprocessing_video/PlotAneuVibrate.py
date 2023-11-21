import pyvista as pv
from pyvista import examples
import numpy as np
import vtk



q_hi = pv.read("c9_surf/isosurface_Q_hi.vtp")
q_lo = pv.read("c9_surf/isosurface_Q_lo.vtp")
outer_surf = pv.read("c9_surf/OuterSurfNeutral.vtp")
outer_surf_fwd = pv.read("c9_surf/OuterSurfForwards.vtp")
outer_surf_bwd = pv.read("c9_surf/OuterSurfBackwards.vtp")

q_hi.points =  q_hi.points*1000 # NEED to scale to mm for some vmtk scripts to work.
q_lo.points =  q_lo.points*1000 # NEED to scale to mm for some vmtk scripts to work.
outer_surf.points =  outer_surf.points*1000 # NEED to scale to mm for some vmtk scripts to work.
outer_surf_bwd.points =  outer_surf_bwd.points*1000 # NEED to scale to mm for some vmtk scripts to work.
outer_surf_fwd.points =  outer_surf_fwd.points*1000 # NEED to scale to mm for some vmtk scripts to work.


surf = q_lo.extract_geometry()
q_lo_smooth = surf.smooth(n_iter=100)
surf = q_hi.extract_geometry()
q_hi_smooth = surf.smooth(n_iter=100)

#outer_surf_smooth = surf.smooth_taubin(n_iter=50, pass_band=0.05)

## Taubin smoothing
#smoother = vtk.vtkWindowedSincPolyDataFilter()
#smoother.SetInputData(surf)
#smoother.SetNumberOfIterations(100)
#smoother.SetPassBand(0.05)
#smoother.SetNormalizeCoordinates(False)
#smoother.Update()
#outer_surf_smooth= smoother.GetOutput()

silhouette = dict(
    color='black',
    line_width=2.0,
)

silhouette_outer = dict(
    color='black',
    line_width=2.0,decimate=1
)
silhouette_outer_bwd = dict(
    color="grey",
    line_width=2.0,decimate=1,feature_angle=True
)



silhouette_outer_fwd = dict(
    color="grey",
    line_width=2.0,decimate=1,feature_angle=True
)

plotter= pv.Plotter(notebook=0)
plotter.add_mesh(q_lo_smooth, color='grey', silhouette=silhouette, opacity=0.5, lighting=False)
plotter.add_mesh(q_hi_smooth, color='purple', silhouette=silhouette, lighting=False)
plotter.add_mesh(outer_surf_bwd, color='white', silhouette=silhouette_outer_bwd, opacity=0.01, lighting=False)
plotter.add_mesh(outer_surf_fwd, color='white', silhouette=silhouette_outer_fwd, opacity=0.01, lighting=False)
#plotter.add_mesh(outer_surf_bwd, color='red', silhouette=silhouette_outer_bwd, opacity=0.1)
#plotter.add_mesh(outer_surf_fwd, color='blue', silhouette=silhouette_outer_fwd, opacity=0.1)
#plotter.add_mesh(outer_surf_bwd, color='red', silhouette=silhouette_outer_bwd, opacity=0.1)
#plotter.add_mesh(outer_surf_fwd, color='blue', silhouette=silhouette_outer_fwd, opacity=0.1)
plotter.add_mesh(outer_surf, color='white', silhouette=silhouette_outer, opacity=0.25, lighting=False)

plotter.set_background('white')

plotter.show(auto_close=False)  

plotter.show(screenshot='c9_surf/render_iso_vibrate.png')  