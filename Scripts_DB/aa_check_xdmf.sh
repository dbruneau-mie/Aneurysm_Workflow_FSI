#!/bin/bash

source /home/s/steinman/dbruneau/sourceme.conf

# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt,  end time of simulation: $end_t_sd1"

# Run postprocessing scripts
DVP="d"
OUT=`python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/check_xdmf.py --case=$case_path --dt=$dt  --start_t=0.0 --end_t=$end_t_sd1 --dvp=$DVP`
echo $OUT
if [[ "$OUT" == *"WARNING"* ]]; then
    echo "In $1, found warning, fixing xdmf file for $DVP"
    python  $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/make_xdmf_from_logfile.py --case=$case_path --mesh=$mesh_path --dt=$dt --dvp=$DVP --save_deg=$save_deg_sim
fi

DVP="v"
OUT=`python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/check_xdmf.py --case=$case_path --dt=$dt  --start_t=0.0 --end_t=$end_t_sd1 --dvp=$DVP`
echo $OUT
if [[ "$OUT" == *"WARNING"* ]]; then
    echo "In $1, found warning, fixing xdmf file for $DVP"
    python  $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/make_xdmf_from_logfile.py --case=$case_path --mesh=$mesh_path --dt=$dt --dvp=$DVP --save_deg=$save_deg_sim
fi

DVP="p"
OUT=`python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/check_xdmf.py --case=$case_path --dt=$dt  --start_t=0.0 --end_t=$end_t_sd1 --dvp=$DVP`
echo $OUT
if [[ "$OUT" == *"WARNING"* ]]; then
    echo "In $1, found warning, fixing xdmf file for $DVP"
    python  $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_h5py/make_xdmf_from_logfile.py --case=$case_path --mesh=$mesh_path --dt=$dt --dvp=$DVP --save_deg=$save_deg_sim
fi