#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# run with source 00_postprocess_all.sh Cyl_Long.config
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt,  end time of simulation: $end_t"


str="Running spectral/other postprocessing scripts!"
echo $str

python $workflow_location/postprocessing_h5py/compute_spi.py --case=$case_path --mesh=$mesh_path --start_t=$start_t_sd2 --end_t=$end_t_sd2 --save_deg=1 --stride=$stride_sd1 --dvp=d --bands="25,1400" 
python $workflow_location/postprocessing_h5py/compute_spi.py --case=$case_path --mesh=$mesh_path --start_t=$start_t_sd2 --end_t=$end_t_sd2 --save_deg=1 --stride=1 --dvp=wss --bands="25,1400" 
python $workflow_location/postprocessing_h5py/compute_spi.py --case=$case_path --mesh=$mesh_path --start_t=$start_t_sd2 --end_t=$end_t_sd2 --save_deg=1 --stride=$stride_sd1 --bands="25,1400" 
#python $workflow_location/postprocessing_h5py/compute_spi.py --case=$case_path --mesh=$mesh_path --start_t=$start_t_sd2 --end_t=$end_t_sd2 --save_deg=1 --stride=$stride_sd1 --bands="25,1400" 
