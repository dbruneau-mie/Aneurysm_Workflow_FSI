#!/bin/bash


export MPLCONFIGDIR=/scratch/s/steinman/dbruneau/.config/matplotlib

module --force purge
module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/9.0.1 python/3.7.7 # vtk 8.2.0 needed because vtk 9.0.1 has an issue with the plotter not closing
source $HOME/.virtualenvs/vtk_fix/bin/activate
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.configbat
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path, timestep: $dt, end time of simulation: $end_t"

# Run postprocessing scripts
str="Running h5py postprocessing scripts!"
echo $str

if [[ "$case_path" == *"MCA"* ]]
then
    # Solid Sampling
    python $PROJECT/Aneurysm_Workflow_FSI/postprocessing_h5py/wss_region.py --case=$case_path --mesh=$mesh_path_domain_ID --dt=$dt --start_t=$start_t_sd2 --end_t=$end_t_sd2 --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --sampling_region="domain" --fluid_sampling_domain_ID=1 --solid_sampling_domain_ID=1001
    echo "Found Surgical Cases"
else
    # Sphere
    python $PROJECT/Aneurysm_Workflow_FSI/postprocessing_h5py/wss_region.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd2 --end_t=$end_t_sd2  --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --r_sphere=$r_sphere --x_sphere=$x_sphere --y_sphere=$y_sphere --z_sphere=$z_sphere 
    echo "Found Puls Study Cases"
fi



#python $workflow_location/postprocessing_h5py/create_visualizations_region.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=v --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --sampling_region="domain" --fluid_sampling_domain_ID=1 --solid_sampling_domain_ID=1001
#python $workflow_location/postprocessing_h5py/create_visualizations.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=d --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --points=$points_d
#python $workflow_location/postprocessing_h5py/create_visualizations.py --case=$case_path --mesh=$mesh_path --dt=$dt --start_t=$start_t_sd1 --end_t=$end_t_sd1 --dvp=p --save_deg=1 --stride=$stride_sd1 --bands="25,1400" --points=$points_p

exit