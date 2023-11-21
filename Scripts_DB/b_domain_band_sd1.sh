#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.configbat
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt, end time of simulation: $end_t"

# Run postprocessing scripts
str="Running h5py postprocessing scripts!"
echo $str
python $workflow_location/postprocessing_h5py/create_visualizations.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=v --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --points=$points_v
python $workflow_location/postprocessing_h5py/create_visualizations.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=d --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --points=$points_d
python $workflow_location/postprocessing_h5py/create_visualizations.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=p --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --points=$points_p

exit