#!/bin/bash

#SBATCH --time=03:40:00
#SBATCH --mail-type=NONE
#SBATCH --nodes=1
#SBATCH --job-name postproc_mesh
#SBATCH --output=outlog_post/Run_All_%j.txt
#SBATCH --error=outlog_post/Run_All_err_%j.txt

# #SBATCH --partition=debug


module purge
source $HOME/sourceme.conf

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=1

scriptName=$1


# Run this with the following command:
# bash Scripts/Run_All.sh Scripts/a_create_meshes.sh 

#for case in $listCases; do
#    cp $scriptsDir$scriptName $simDir$case
#done
#
## We are assuming that the config files are in the working directory for the case now
#
#for case in $listCases; do
#    (echo "Postprocessing $case" && cd $simDir$case && bash $scriptName $case".config" && echo "$case finished") &
#done
#wait
#$workflow_location

simDir=$SCRATCH/7_0_Surgical/Rerun_Steady_New_Solver

for case in $simDir/*/; do
    cp $scriptName $case
done

for case in $simDir/*/; do
    if [[ "$case" == *"ase"* ]]
    then
        (echo "Postprocessing $case" && cd $case && bash $(basename -- $scriptName) $(basename -- $case)".config" && echo "$case finished") &
    fi
done
wait

