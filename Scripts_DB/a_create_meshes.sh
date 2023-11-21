#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "Workflow Drectory: $workflow_location"  # Need to put workflow_location in source file

echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt,  end time of simulation: $end_t"

# Run postprocessing scripts
str="Creating meshes for postprocessing!"
echo $str

python $workflow_location/postprocessing_mesh/Create_Refined_Mesh.py --case=$case_path --mesh=$mesh_path
python $workflow_location/postprocessing_mesh/Create_Solid_Only_Mesh.py --case=$case_path --mesh=$mesh_path
python $workflow_location/postprocessing_mesh/Create_Fluid_Only_Mesh.py --case=$case_path --mesh=$mesh_path
python $workflow_location/postprocessing_mesh/Create_Solid_Only_Mesh.py --case=$case_path --mesh=$refined_mesh_path
python $workflow_location/postprocessing_mesh/Create_Fluid_Only_Mesh.py --case=$case_path --mesh=$refined_mesh_path

exit