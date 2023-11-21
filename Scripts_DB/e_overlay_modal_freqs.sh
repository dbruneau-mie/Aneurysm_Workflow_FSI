#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# run with source 00_postprocess_all.sh Cyl_Long.config
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt,  end time of region of interest: $end_t_ROI"


str="Running spectral/other postprocessing scripts!"
echo $str

python $workflow_location/postprocessing_h5py/overlay_modes_on_spectrograms.py --case=$case_path --mesh=$mesh_path --end_t=$end_t_sd2 --start_t=$start_t_sd2 --save_deg=1 --r_sphere=$r_sphere --x_sphere=$x_sphere --y_sphere=$y_sphere --z_sphere=$z_sphere --stride=$stride_sd1 --dvp=d

exit