# !/usr/bin/python

import dan_utils
import pyvista as pv 

from os import path 
import vmtk #import vmtkscripts
import vtk
import numpy as np

mesh = pv.read('meshes/case16_el06_cfd.vtu')

dan_utils.generate_h5_file(mesh,"MehdiMesh")
