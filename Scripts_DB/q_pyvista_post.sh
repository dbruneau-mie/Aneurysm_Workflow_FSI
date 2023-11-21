#!/bin/bash

export MPLCONFIGDIR=/scratch/s/steinman/dbruneau/.config/matplotlib

#module --force purge
#module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/9.0.1 python/3.7.7
#source $HOME/../macdo708/.virtualenvs/vtk9/bin/activate

module --force purge
module load CCEnv StdEnv/2020 gcc/9.3.0 vtk/9.0.1 python/3.7.7 # vtk 8.2.0 needed because vtk 9.0.1 has an issue with the plotter not closing
source $HOME/.virtualenvs/vtk_fix/bin/activate

# run with source 00_postprocess_all.sh Cyl_Long.config
# point to config file on the command line, like this: sbatch d_execute.sh path/to/config.config
. $1

echo "Sourcing config file: $1"
echo "case path: $case_path, mesh path: $mesh_path"
echo "$CameraPosition"

echo "Running pyvista postprocessing scripts!"

python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale auto $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.1 $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.25 $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.5 $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.75 $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuAmplitude.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 1.0 $plot_time_idx $ColorbarY
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.3 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.4 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.5 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.6 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.7 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuContour.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 0.75 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 100 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 200 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 500 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 1000 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 2000 $plot_time_idx
python $SCRATCH/Aneurysm_Workflow_FSI/postprocessing_video/PlotAneuQ_hi_lo.py $case_path $mesh_path $CameraPosition $CameraFocalPoint $CameraViewUp $CameraParallelScale 50000 5000 $plot_time_idx

# --mesa-swr 