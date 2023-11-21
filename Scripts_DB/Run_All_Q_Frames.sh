#!/bin/bash

######SBATCH --nodes=1
######SBATCH --ntasks=40
######SBATCH --time=23:55:00
######SBATCH --job-name run_all_Q
######SBATCH --output=outlog_post/Q_Run_All_%j.txt
######SBATCH --error=outlog_post/Q_Run_All_err_%j.txt

cd $SLURM_SUBMIT_DIR

module --force purge
#source $HOME/sourceme.conf

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=1

#scriptName=$1


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

simDir=$SCRATCH/7_0_Surgical/Pulsatile_Ramp_Cases_FC

for case in $simDir/*/; do
    cp "Scripts/t_pyvista_modes_multi_Q_1.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_2.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_3.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_4.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_5.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_6.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_7.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_8.sh" $case
    cp "Scripts/t_pyvista_modes_multi_Q_9.sh" $case

done

#for case in $simDir/*/; do
#    #if [[ "$case" == *"ase9"* ]] || [[ "$case" == *"ase12"* ]]
#    #then
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_1.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_2.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_3.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_4.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_5.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_6.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_7.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_8.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #(echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_9.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#    #fi
#done
#wait
#
#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_2.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait
#
#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_3.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait
##
#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_4.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait

#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_5.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait
#
#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_6.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait
#
for case in $simDir/*/; do
    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_7.sh" ) $(basename -- $case)".config" && echo "$case finished") &
done
wait

#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_8.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait

#for case in $simDir/*/; do
#    (echo "Postprocessing $case" && cd $case && bash $(basename -- "Scripts/t_pyvista_modes_multi_Q_9.sh" ) $(basename -- $case)".config" && echo "$case finished") &
#done
#wait