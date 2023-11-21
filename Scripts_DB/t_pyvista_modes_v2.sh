#!/bin/bash

export MPLCONFIGDIR=/scratch/s/steinman/dbruneau/.config/matplotlib


#bash Scripts/t_pyvista_modes.sh $SCRATCH/7_0_Surgical/Rerun_Pulsatile_New_Solver/Case12_predeformed_finerflow/Case12_predeformed_finerflow.config 

module --force purge
#module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/8.2.0 python/3.7.7 # vtk 8.2.0 needed because vtk 9.0.1 has an issue with the plotter not closing
#source $HOME/../macdo708/.virtualenvs/vtk9/bin/activate

module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/9.0.1 python/3.7.7 # vtk 8.2.0 needed because vtk 9.0.1 has an issue with the plotter not closing
#module load CCEnv StdEnv/2020 gcc/9.3.0 
#module load NiaEnv/2019b python/3.8 
#module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/9.0.1 python/3.7.7
source $HOME/.virtualenvs/vtk_fix/bin/activate
# Currently only works for Case 3
# run with source 00_postprocess_all.sh Cyl_Long.config
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path"
echo "$CameraPosition"

echo "Running pyvista postprocessing scripts!"

python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuModeShapeBands_v2.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale $bands $r_sphere 1045 $glyph_length $glyph_density  # 1045 is from 2.753s, the start of the mode shape file
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuModeShapeRandomVib_v2.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale $bands $r_sphere 1045 $glyph_length $glyph_density  # 1045 is from 2.753s, the start of the mode shape file

#python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuModeShape.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale $bands $r_sphere 489 5000

# --mesa-swr 