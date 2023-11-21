#!/bin/bash

module purge
source $HOME/sourceme.conf

# Turn off implicit threading in Python, R
export OMP_NUM_THREADS=1

scriptName1="Scripts_DB/b_domain_band_sd1_dp.sh"
scriptName2="Scripts_DB/b_domain_band_sd1_v.sh"


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

#simDir=$SCRATCH/7_0_Surgical/Rerun_Pulsatile_New_Solver
#simDir=$SCRATCH/7_0_Surgical/Modal_Excitation_All_Cases
#simDir=$SCRATCH/7_0_Surgical/Pulsatile_Ramp_Cases_FC
#simDir=$SCRATCH/7_0_Surgical/Surgical_Cases/Pulsatile
#simDir=$SCRATCH/7_0_Surgical/Pulsatile_Ramp_Cases_FC_CFD_undeformed
#simDir=$SCRATCH/7_0_Surgical/Surgical_Cases/Pulsatile_Refine
#simDir=$SCRATCH/7_0_Surgical/Surgical_Cases/Modal
simDir=$SCRATCH/7_0_Surgical/Surgical_Cases/Pulsatile_CFD
simDir2=$SCRATCH/7_0_Surgical/Surgical_Cases/Pulsatile
simDir3=$SCRATCH/7_0_Surgical/Surgical_Cases/Modal


for case in $simDir/*/; do
    cp $scriptName1 $case
done

for case in $simDir2/*/; do
    cp $scriptName2 $case
done
#
#for case in $simDir3/*/; do
#    cp $scriptName $case
#done


for case in $simDir/*/; do
    if [[ "$case" == *"MCA04"* ]]
    then
        (echo "Postprocessing $case" && cd $case && bash $(basename -- $scriptName1) $(basename -- $case)".config" && echo "$case finished") &
        #echo "Postprocessing $case"
    fi
done

for case in $simDir2/*/; do
    if [[ "$case" == *"MCA05"* ]] || [[ "$case" == *"MCA06"* ]] || [[ "$case" == *"MCA07"* ]] || [[ "$case" == *"MCA08"* ]]
    then
        (echo "Postprocessing $case" && cd $case && bash $(basename -- $scriptName2) $(basename -- $case)".config" && echo "$case finished") &
    fi
done
#
#
#for case in $simDir3/*/; do
#    if [[ "$case" != *"ppp"* ]]
#    then
#        (echo "Postprocessing $case" && cd $case && bash $(basename -- $scriptName) $(basename -- $case)".config" && echo "$case finished") &
#    fi
#done

wait

