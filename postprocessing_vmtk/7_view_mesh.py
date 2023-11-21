from dolfin import *  
import sys
import configparser
# Read from config file
mesh_path = sys.argv[1] # need to input config file for case



## Read fixed mesh
mesh = Mesh()
hdf = HDF5File(mesh.mpi_comm(), mesh_path, "r")
hdf.read(mesh, "/mesh", False)

boundaries = MeshFunction("size_t", mesh, 2)
hdf.read(boundaries, "/boundaries")

ff = File(mesh_path.replace(".h5","_boundaries.pvd"))
ff << boundaries

domains = MeshFunction("size_t", mesh, 3)
hdf.read(domains, "/domains")

ff = File(mesh_path.replace(".h5","_domains.pvd"))
ff << domains