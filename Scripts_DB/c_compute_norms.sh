#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt,  end time of simulation: $end_t"

# Run postprocessing scripts
str="Creating readable h5 files (must be run in serial)"
echo $str
python $workflow_location/postprocessing_fenics/compute_norms.py --case=$case_path --mesh=$mesh_path --dt=$dt --save_deg=1 --stride=2

exit