import pyvista as pv 
from scipy.spatial import cKDTree as KDTree 
import h5py 
import numpy as np

def assert_all_quads(mesh):
    """ Remove triangles from mesh.
    VMTK's volume mesh will have a surface of triangles.
    This function removes them and returns the quad-only mesh.
    """

    cell_types = np.zeros(mesh.n_cells)
    cells = mesh.cells

    i = 0
    idx = 0
    while i < len(mesh.cells):
        cell_types[idx] = cells[i]
        plus = cells[i]
        i = i + plus  + 1
        idx += 1
    
    quad_mask = np.array(cell_types) == 4
    mesh_quad = mesh.extract_cells(quad_mask)
    return mesh_quad


def generate_h5_file(mesh, outfile):
    """ Generate lab-specific h5 mesh file for our solver.
    File layout:
        - Mesh
            - coordinates
            - topology
            - ID_N
                - cellIds, coordinates, pointIds, topology
            - Wall
                - cellIds, coordinates, normal, pointIds, topology
    """
    case_name = outfile

    # Quads only
    mesh_quad = assert_all_quads(mesh)

    # Get surf
    surf_mask = mesh.cell_arrays['CellEntityIds'] == 1
    surf = mesh.extract_cells(surf_mask)
    surf_pt_ids = surf.point_arrays['vtkOriginalPointIds']
    surf = pv.PolyData(surf.points, surf.cells)
    surf.point_arrays['vtkOriginalPointIds'] = surf_pt_ids
    surf = surf.compute_normals()

    # Wall points
    wall_coordinates = surf.points 
    wall_pointIds = surf.point_arrays['vtkOriginalPointIds']
    wall_topology = surf.faces.reshape(-1,4)[:,1:]
    wall_cellIds = wall_pointIds[wall_topology]
    wall_normals = surf.point_arrays['Normals']
    
    # Extract caps        
    entity_ids = np.unique(mesh.cell_arrays['CellEntityIds'])
    valid_entity_ids = sorted(set(entity_ids) - set([0, 1]))
    entity_masks = [mesh.cell_arrays['CellEntityIds'] == i for i in valid_entity_ids]
    caps = [mesh.extract_cells(em) for em in entity_masks]

    # Make sure points are duplicate
    tree = KDTree(mesh_quad.points)
    inds = [tree.query(c.points, k=1)[1] == 0 for c in caps]
    dists = np.all([np.all(tree.query(c.points, k=1)[0] == 0) for c in caps])
    assert dists, 'Cap points are not in quad mesh'

    # Get relevant cap quantities
    caps_coordinates = [c.points for c in caps]
    caps_pointIds = [c.point_arrays['vtkOriginalPointIds'] for c in caps]
    caps_topology = [c.cells.reshape(-1,4)[:,1:] for c in caps]
    caps_cellIds = [c.point_arrays['vtkOriginalPointIds'][c.cells.reshape(-1,4)[:,1:]] for c in caps]

    # Now create dataset
    f = h5py.File(outfile+".h5", "w")
    
    f.create_dataset('Mesh/coordinates', 
        data=mesh_quad.points, 
        compression="gzip", 
        compression_opts=9
        )
    f.create_dataset('Mesh/topology', 
        data=mesh_quad.cells.reshape(-1,5)[:,1:], 
        compression="gzip", 
        compression_opts=9
        )
    
    f.create_dataset('Mesh/Wall/coordinates', 
        data=wall_coordinates, 
        compression="gzip", 
        compression_opts=9
        )
    f.create_dataset('Mesh/Wall/pointIds', 
        data=wall_pointIds, 
        compression="gzip", 
        compression_opts=9
        )
    f.create_dataset('Mesh/Wall/topology', 
        data=wall_topology, 
        compression="gzip", 
        compression_opts=9
        )
    f.create_dataset('Mesh/Wall/cellIds', 
        data=wall_cellIds, 
        compression="gzip", 
        compression_opts=9
        )
    f.create_dataset('Mesh/Wall/normal', 
        data=wall_normals, 
        compression="gzip", 
        compression_opts=9
        )
    
    for cdx in range(len(caps)):
        f.create_dataset('Mesh/ID_{}/coordinates'.format(cdx + 1), 
            data=caps_coordinates[cdx], 
            compression="gzip", 
            compression_opts=9
            )
        f.create_dataset('Mesh/ID_{}/pointIds'.format(cdx + 1), 
            data=caps_pointIds[cdx], 
            compression="gzip", 
            compression_opts=9
            )
        f.create_dataset('Mesh/ID_{}/topology'.format(cdx + 1), 
            data=caps_topology[cdx], 
            compression="gzip", 
            compression_opts=9
            )
        f.create_dataset('Mesh/ID_{}/cellIds'.format(cdx + 1), 
            data=caps_cellIds[cdx], 
            compression="gzip", 
            compression_opts=9
            )

    f.close()