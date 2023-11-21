#!/bin/bash

# run with source 00_postprocess_all.sh Cyl_Long.config
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path"
echo "$CameraPosition"

echo "Running pyvista postprocessing scripts!"

python /run/user/1000/gvfs/sftp\:host\=niagara.scinet.utoronto.ca\,user\=dbruneau/project/s/steinman/dbruneau/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuJet.py $case_path_absolute $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.3 $plot_time_idx

# --mesa-swr 