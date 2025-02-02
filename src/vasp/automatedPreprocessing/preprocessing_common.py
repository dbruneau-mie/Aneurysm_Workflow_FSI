# Copyright (c) 2023 Simula Research Laboratory
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Union

import numpy as np
import meshio
from dolfin import Mesh, MeshFunction, File, HDF5File, FunctionSpace, Function, XDMFFile, cells, Edge
from vmtk import vmtkdistancetospheres, vmtkdijkstradistancetopoints
from morphman import vmtkscripts, write_polydata

from vasp.automatedPreprocessing.vmtkmeshgeneratorfsi import vmtkMeshGeneratorFsi

from vtk import vtkPolyData

# Global array names
distanceToSpheresArrayName = "DistanceToSpheres"
distanceToSpheresArrayNameSolid = "Thickness"
dijkstraArrayName = "DijkstraDistanceToPoints"


def distance_to_spheres_solid_thickness(surface: vtkPolyData, save_path: Union[str, Path],
                                        distance_offset: float = 0, distance_scale: float = 0.1,
                                        min_distance: float = 0.25, max_distance: float = 0.3) -> vtkPolyData:
    """
    Determines the solid thickness using vmtkdistancetospheres.
    Write the distance data to `save_path`.

    Args:
        surface (vtkPolyData): Input surface model
        save_path (Union[str, Path]): Location to store processed surface
        distance_offset (float): Offset added to the distances
        distance_scale (float): Scale applied to the distances
        min_distance (float): Minimum value for the distances
        max_distance (float): Maximum value for the distances

    Returns:
        surface (vtkPolyData): Processed surface model with info on solid thickness

    """
    distanceToSpheres = vmtkdistancetospheres.vmtkDistanceToSpheres()
    distanceToSpheres.Surface = surface
    distanceToSpheres.DistanceOffset = distance_offset
    distanceToSpheres.DistanceScale = distance_scale
    distanceToSpheres.MinDistance = min_distance
    distanceToSpheres.MaxDistance = max_distance
    distanceToSpheres.DistanceToSpheresArrayName = distanceToSpheresArrayNameSolid
    distanceToSpheres.Execute()
    distance_to_sphere = distanceToSpheres.Surface

    write_polydata(distance_to_sphere, str(save_path))

    return distance_to_sphere


def dist_sphere_spheres(surface: vtkPolyData, save_path: Union[str, Path],
                        distance_offset: float, distance_scale: float,
                        min_distance: float, max_distance: float,
                        distance_method: str = 'geodesic') -> vtkPolyData:
    """
    Determines the target edge length for each cell on the surface, including
    potential refinement or coarsening of certain user specified areas.
    Level of refinement/coarseness is determined based on the distance to the spheres.
    The distance computation can be either 'euclidean' or 'geodesic' (default).

    Args:
        surface (vtkPolyData): Input surface model
        save_path (Union[str, Path]): Location to store processed surface
        distance_offset (float): Offset added to the distances
        distance_scale (float): Scale applied to the distances
        min_distance (float): Minimum value for the distances
        max_distance (float): Maximum value for the distances
        distance_method (str): Method to compute distances ('euclidean' or 'geodesic')

    Returns:
        surface (vtkPolyData): Processed surface model with info on cell specific target edge length
    """
    if distance_method == 'euclidean':
        distanceToSpheres = vmtkdistancetospheres.vmtkDistanceToSpheres()
        distance_array_name = distanceToSpheresArrayName
    elif distance_method == 'geodesic':
        distanceToSpheres = vmtkdijkstradistancetopoints.vmtkDijkstraDistanceToPoints()
        distance_array_name = dijkstraArrayName
    else:
        raise ValueError("Invalid distance computation method. Choose 'euclidean' or 'geodesic'.")

    distanceToSpheres.Surface = surface
    distanceToSpheres.DistanceOffset = distance_offset
    distanceToSpheres.DistanceScale = distance_scale
    distanceToSpheres.MinDistance = min_distance
    distanceToSpheres.MaxDistance = max_distance
    distanceToSpheres.Execute()
    distance_to_sphere = distanceToSpheres.Surface

    surfaceCurvature = vmtkscripts.vmtkSurfaceCurvature()
    surfaceCurvature.AbsoluteCurvature = 1
    surfaceCurvature.MedianFiltering = 1
    surfaceCurvature.CurvatureType = "gaussian"
    surfaceCurvature.Offset = 0.15
    surfaceCurvature.BoundedReciprocal = 1
    surfaceCurvature.Surface = distance_to_sphere
    surfaceCurvature.Execute()
    distance_to_sphere = surfaceCurvature.Surface

    surfaceArrayOperation = vmtkscripts.vmtkSurfaceArrayOperation()
    surfaceArrayOperation.Surface = distance_to_sphere
    surfaceArrayOperation.InputArrayName = "Curvature"
    surfaceArrayOperation.Input2ArrayName = distance_array_name
    surfaceArrayOperation.ResultArrayName = "Size"
    surfaceArrayOperation.Operation = "multiply"
    surfaceArrayOperation.Execute()
    distance_to_sphere = surfaceArrayOperation.Surface

    write_polydata(distance_to_sphere, str(save_path))

    return distance_to_sphere


def generate_mesh(surface: vtkPolyData, number_of_sublayers_fluid: int, number_of_sublayers_solid: int,
                  solid_thickness: str, solid_thickness_parameters: list, centerlines: vtkPolyData,
                  solid_side_wall_id: int = 11, interface_fsi_id: int = 22, solid_outer_wall_id: int = 33,
                  fluid_volume_id: int = 0, solid_volume_id: int = 1, no_solid: bool = False,
                  extract_branch: bool = False, branch_group_ids: list = [], branch_ids_offset: int = 1000) -> tuple:
    """
    Generates a mesh suitable for FSI from an input surface model.

    Args:
        surface (vtkPolyData): Surface model to be meshed.
        number_of_sublayers_fluid (int): Number of sublayers for fluid.
        number_of_sublayers_solid (int): Number of sublayers for solid.
        solid_thickness (str): Type of solid thickness ('variable' or 'constant').
        solid_thickness_parameters (list): List of parameters for solid thickness.
        centerlines (vtkPolyData): Centerlines of input model.
        solid_side_wall_id (int, optional): ID for solid side wall. Default is 11.
        interface_fsi_id (int, optional): ID for the FSI interface. Default is 22.
        solid_outer_wall_id (int, optional): ID for solid outer wall. Default is 33.
        fluid_volume_id (int, optional): ID for the fluid volume. Default is 0.
        solid_volume_id (int, optional): ID for the solid volume. Default is 1.
        no_solid (bool, optional): Generate mesh without solid.
        extract_branch (bool, optional): Enable extraction of a specific branch, marking solid mesh IDs with an offset.
        branch_group_ids (list, optional): Specify group IDs to extract for the branch.
        branch_ids_offset (int): Set offset for marking solid mesh IDs when extracting a branch.

    Returns:
        tuple: A tuple containing the generated mesh (vtkUnstructuredGrid) and the remeshed surface (vtkPolyData).
    """
    meshGenerator = vmtkscripts.vmtkMeshGenerator() if no_solid else vmtkMeshGeneratorFsi()
    meshGenerator.Surface = surface

    # Mesh Parameters
    meshGenerator.ElementSizeMode = "edgelengtharray"  # Variable size mesh
    meshGenerator.TargetEdgeLengthArrayName = "Size"  # Variable size mesh
    meshGenerator.LogOn = 1
    meshGenerator.ExitOnError = 0
    meshGenerator.BoundaryLayer = 1
    meshGenerator.NumberOfSubLayersSolid = number_of_sublayers_solid
    meshGenerator.NumberOfSubLayersFluid = number_of_sublayers_fluid
    meshGenerator.NumberOfSubLayers = number_of_sublayers_fluid
    meshGenerator.BoundaryLayerOnCaps = 0
    meshGenerator.SubLayerRatioFluid = 0.75
    meshGenerator.SubLayerRatioSolid = 0.75
    meshGenerator.SubLayerRatio = 0.75
    meshGenerator.BoundaryLayerThicknessFactor = 0.5
    meshGenerator.Tetrahedralize = 1
    meshGenerator.VolumeElementScaleFactor = 0.8
    meshGenerator.EndcapsEdgeLengthFactor = 1.0
    meshGenerator.Centerlines = centerlines
    meshGenerator.ExtractBranch = extract_branch
    meshGenerator.BranchGroupIds = branch_group_ids
    meshGenerator.BranchIdsOffset = branch_ids_offset

    # Solid thickness handling
    if solid_thickness == 'variable':
        meshGenerator.ElementSizeModeSolid = "edgelengtharray"
        meshGenerator.TargetEdgeLengthArrayNameSolid = distanceToSpheresArrayNameSolid
    else:
        meshGenerator.ElementSizeModeSolid = "edgelength"
        meshGenerator.SolidThickness = solid_thickness_parameters[0]

    # IDs
    meshGenerator.SolidSideWallId = solid_side_wall_id
    meshGenerator.InterfaceFsiId = interface_fsi_id
    meshGenerator.SolidOuterWallId = solid_outer_wall_id
    meshGenerator.FluidVolumeId = fluid_volume_id
    meshGenerator.SolidVolumeId = solid_volume_id

    # Generate mesh
    meshGenerator.Execute()
    remeshed_surface = meshGenerator.RemeshedSurface
    generated_mesh = meshGenerator.Mesh

    return generated_mesh, remeshed_surface


def convert_xml_mesh_to_hdf5(file_name_xml_mesh: Union[str, Path], scaling_factor: float = 1) -> None:
    """Converts an XML mesh to an HDF5 mesh.

    Args:
        file_name_xml_mesh (Union[str, Path]): The name of the XML mesh file.
        scaling_factor (float, optional): A scaling factor to apply to the mesh coordinates.
                                          The default value is 1 (no scaling). Note that probes
                                          and parameters inside _info.json file will not be scaled
                                          if you only scale HDF5 file.

    Returns:
        None

    Raises:
        FileNotFoundError: If the XML mesh file does not exist.
    """

    # Check if the XML mesh file exists
    xml_mesh_path = Path(file_name_xml_mesh)
    if not xml_mesh_path.is_file():
        raise FileNotFoundError(f"The file '{xml_mesh_path}' does not exist.")

    mesh = Mesh(str(xml_mesh_path))

    # Rescale the mesh coordinates
    x = mesh.coordinates()
    x[:, :] *= scaling_factor
    mesh.bounding_box_tree().build(mesh)

    # Convert subdomains to mesh function
    boundaries = MeshFunction("size_t", mesh, 2, mesh.domains())
    boundaries.set_values(boundaries.array() + 1)  # FIXME: Explain why this is necessary

    base, first_dot, rest = xml_mesh_path.name.partition('.')
    file_name_boundaries = str(xml_mesh_path.with_name(base + "_boundaries.pvd"))
    boundary_file = File(file_name_boundaries)
    boundary_file << boundaries

    domains = MeshFunction("size_t", mesh, 3, mesh.domains())
    domains.set_values(domains.array() + 1)  # in order to have fluid==1 and solid==2

    file_name_domains = str(xml_mesh_path.with_name(base + "_domains.pvd"))
    domain_file = File(file_name_domains)
    domain_file << domains

    file_name_h5_mesh = str(xml_mesh_path.with_name(base + '.h5'))
    hdf = HDF5File(mesh.mpi_comm(), file_name_h5_mesh, "w")
    hdf.write(mesh, "/mesh")
    hdf.write(boundaries, "/boundaries")
    hdf.write(domains, "/domains")


def convert_vtu_mesh_to_xdmf(file_name_vtu_mesh: Union[str, Path], file_name_xdmf_mesh: Union[str, Path]) -> None:
    """
    Convert a VTU mesh to XDMF format using meshio. This function is intended to run in serial.

    Args:
        file_name_vtu_mesh (Union[str, Path]): Path to the input VTU mesh file.
        file_name_xdmf_mesh (Union[str, Path]): Path to the output XDMF file.
    """
    # Load the VTU mesh
    vtu_mesh = meshio.read(file_name_vtu_mesh)

    # Extract cell data
    tetra_data = vtu_mesh.cell_data_dict.get("CellEntityIds", {}).get("tetra", None)
    triangle_data = vtu_mesh.cell_data_dict.get("CellEntityIds", {}).get("triangle", None)

    # Extract cell types and data
    tetra_cells = None
    triangle_cells = None
    for cell in vtu_mesh.cells:
        if cell.type == "tetra":
            tetra_cells = cell.data
        elif cell.type == "triangle":
            triangle_cells = cell.data

    # Create mesh objects
    tetra_mesh = meshio.Mesh(points=vtu_mesh.points, cells={"tetra": tetra_cells},
                             cell_data={"CellEntityIds": [tetra_data]})
    triangle_mesh = meshio.Mesh(points=vtu_mesh.points, cells=[("triangle", triangle_cells)],
                                cell_data={"CellEntityIds": [triangle_data]})

    # Define Path objects
    tetra_xdmf_path = Path(file_name_xdmf_mesh)
    triangle_xdmf_path = tetra_xdmf_path.with_name(tetra_xdmf_path.stem + '_triangle.xdmf')

    # Write the VTU mesh to XDMF format
    meshio.write(tetra_xdmf_path, tetra_mesh)
    meshio.write(triangle_xdmf_path, triangle_mesh)

    print(f"Tetra mesh XDMF file written to: {tetra_xdmf_path}")
    print(f"Triangle mesh XDMF file written to: {triangle_xdmf_path}\n")


def edge_length_evaluator(file_name_mesh: Union[str, Path], file_name_edge_length_xdmf: Union[str, Path]) -> None:
    """
    Evaluates the edge length of a mesh.

    Args:
        file_name_mesh (Union[str, Path]): Path to the XML mesh file.
        file_name_edge_length_xdmf (Union[str, Path]): Path to the output XDMF file.
    """
    file_name_mesh = Path(file_name_mesh)

    # Check if the XML mesh file exists
    if not file_name_mesh.is_file():
        raise FileNotFoundError(f"The file '{file_name_mesh}' does not exist.")
    try:
        mesh = Mesh(str(file_name_mesh))
    except RuntimeError:
        mesh = Mesh()
        with XDMFFile(str(file_name_mesh)) as xdmf:
            xdmf.read(mesh)

    mesh.init(1)
    num_cells = mesh.num_cells()
    V = FunctionSpace(mesh, "DG", 0)
    u = Function(V)
    values = np.zeros(num_cells, dtype=np.float64)

    for cell in cells(mesh):
        edges = cell.entities(1)
        value = 0
        for edge in edges:
            value += Edge(mesh, edge).length()
        values[cell.index()] = value / len(edges)

    u.vector().set_local(values)
    u.vector().apply("local")
    u.rename("edge_length", "edge_length")

    with XDMFFile(str(file_name_edge_length_xdmf)) as xdmf:
        xdmf.write_checkpoint(u, "edge_length", 0, append=False)
