""" Sac extraction using centerlines
"""
import pyvista as pv 
import numpy as np 
from pathlib import Path
import h5py
from vtk import VTK_TETRA
from vmtk import vmtkscripts
import vtk
import os
import numpy as np

#  This script requires you to export a surface (stl) from paraview of only the interface between solid and fluid. 
# To do this, append a vtu of the boundaries file from meshing in paraview and use threshold on the interface (ID 22)
# Extract the surface and export multiple timesteps, then point to them using "folder"
#

## Warning: DONT upgrade pyvista in vmtk environment. Only v0.24.2 will work with vmtk, otherwise the objects aren't compatible for some reason....

# Define case name

folder ='/media/db_ubuntu/T7/Simulations/7_1_Balasso_Validation/pv_solid_only/_results/Faster_Inflation_E2_Visc/Balasso_Solid/1/Surfaces/'
out_file = "volume_t.csv"
vol_array = []
time_array = []
for file in os.listdir(folder):
    if file.endswith(".stl"):

        reader = vmtkscripts.vmtkSurfaceReader()
        reader.InputFileName = folder+"/"+file
        reader.Execute()
        surface = reader.Surface
        
        capper = vmtkscripts.vmtkSurfaceCapper()
        capper.Surface = surface
        capper.Interactive = 0
        capper.Execute()
        surface = capper.Surface
        
        # Calculate volume of original mesh
        vol = vmtkscripts.vmtkSurfaceMassProperties()
        vol.Surface=surface
        vol.Execute()
        print(file + ": mesh volume is {} (in mm^3)\n".format(vol.Volume))
        vol_array.append(vol.Volume)
        print(file)
        time_float = float(file.split('.stl')[0])
        time_array.append(time_float)

print(vol_array)
xarray = np.array(time_array)
yarray = np.array(vol_array)
# here is your data, in two numpy arrays

data = np.column_stack([xarray, yarray])
datafile_path = folder + out_file
np.savetxt(datafile_path , data, delimiter=",")


#case_name = "meshes/open_surface"
#TargetEdgeLength_f = 0.42*3  # more or less minimum edge length of the fluid mesh (0.42*2 is best so far)
#Thick_solid = 0.5  # constant tickness of the solid wall
#nb_boundarylayers = 2  # number of sub-boundary layers is the solid and fluid mesh
#BoundaryLayerThicknessFactor = Thick_solid / TargetEdgeLength_f  # Wall Thickness == TargetEdgeLength*BoundaryLayerThicknessFactor
#
#reader = vmtkscripts.vmtkSurfaceReader()
#reader.InputFileName = case_name+'.stl'
#reader.Execute()
#surface = reader.Surface
#
#
#meshGenerator = vmtkscripts.vmtkMeshGenerator()
#meshGenerator.Surface = surface
## for remeshing
##meshGenerator.SkipRemeshing = 1
#meshGenerator.ElementSizeMode = 'edgelength'
#meshGenerator.TargetEdgeLength = TargetEdgeLength_f
##meshGenerator.MaxEdgeLength = 20*meshGenerator.TargetEdgeLength
##meshGenerator.MinEdgeLength = 0.4*meshGenerator.TargetEdgeLength
## for boundary layer (used for both fluid boundary layer and solid domain)
#meshGenerator.BoundaryLayer = 1
#meshGenerator.NumberOfSubLayers = nb_boundarylayers
#meshGenerator.BoundaryLayerOnCaps = 0
#meshGenerator.SubLayerRatio = 1
#meshGenerator.BoundaryLayerThicknessFactor = BoundaryLayerThicknessFactor
## mesh
#meshGenerator.Tetrahedralize = 1
#
#meshGenerator.Execute()
#mesh = meshGenerator.Mesh
#
## Calculate volume of original mesh
#vol = vmtkscripts.vmtkMeshVolume()
#vol.Mesh=mesh
#vol.Execute()
#txt_out.append("Mesh volume is {} (in mm^3)\n".format(vol.Volume))
#print(vol.Volume)
#
## Write mesh in VTU format #####################################################
#writer = vtk.vtkXMLUnstructuredGridWriter()
#writer.SetFileName("case_name_cfd.vtu")
#writer.SetInputData(mesh)
#writer.Update()
#writer.Write()
