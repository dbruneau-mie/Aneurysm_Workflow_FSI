import h5py
from shutil import copyfile
from numpy import genfromtxt
import numpy as np

inlet_id1=2  # inlet id 
outlet_id1=3  # outlet nb
solid_dirichlet_id1=11

inlet_y = -0.00374494
outlet_y = 0.00375074

# User inputs ----------------------------
mesh_folder = '/media/db_ubuntu/T7/Simulations/5_3_FSI_Cyl_MWE/Demonstrate_Instability/4_Cyl_Ramp_Discontinuous_Flat_Outlet/mesh/'
mesh_name = "artery_coarse_rescaled.h5"   # Name of original h5 mesh file
# -----------------------------------------
mesh_path=mesh_folder+mesh_name

predeformed_mesh_path=mesh_path.replace(".h5", "_flat_outlet_solid.h5")
copyfile(mesh_path, predeformed_mesh_path)

#f = HDF5File(mpi_comm_world(),'meshes/'+mesh_name, 'r')
#mesh_file = Mesh()
#f.read(mesh, 'mesh')

vectorData = h5py.File(predeformed_mesh_path,'a')



#hdf5_store = h5py.File("meshes/deformed_"+meshname+'.h5', "w")




facet_ids = vectorData['boundaries/values']
facet_topology = vectorData['boundaries/topology']


outlet_facet_ids = [i for i, x in enumerate(facet_ids) if x == outlet_id1]
outlet_facet_topology = facet_topology[outlet_facet_ids,:]
outlet_nodes = np.unique(outlet_facet_topology.flatten())

inlet_facet_ids = [i for i, x in enumerate(facet_ids) if x == inlet_id1]
inlet_facet_topology = facet_topology[inlet_facet_ids,:]
inlet_nodes = np.unique(inlet_facet_topology.flatten())

solid_dirichlet_facet_ids = [i for i, x in enumerate(facet_ids) if x == solid_dirichlet_id1]
solid_dirichlet_facet_topology = facet_topology[solid_dirichlet_facet_ids,:]
solid_dirichlet_nodes = np.unique(solid_dirichlet_facet_topology.flatten())

ArrayNames = ['boundaries/coordinates','mesh/coordinates','domains/coordinates']

for ArrayName in ArrayNames:

	vectorArray = vectorData[ArrayName]
	for node_id in range(len(vectorArray)):
		if node_id in outlet_nodes:
			vectorArray[node_id,1] = outlet_y
		elif node_id in inlet_nodes:
			vectorArray[node_id,1] = inlet_y
		elif node_id in solid_dirichlet_nodes:
			if abs(vectorArray[node_id,1]-inlet_y)<abs(vectorArray[node_id,1]-outlet_y):
				vectorArray[node_id,1] = inlet_y
			else:
				vectorArray[node_id,1] = outlet_y	#print(vectorArray[:,:])

#ArrayNames = ['boundaries/values','mesh/coordinates','domains/coordinates']


vectorData.close() 