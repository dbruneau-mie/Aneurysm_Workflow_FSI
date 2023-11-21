To run workflow for BSL solver: 

1. run meshing script "reformatMeshc16.py" to obtain the correctly formatted mesh. Put this mesh in a folder called "mesh" in the main simulation directory
1.5. Need to copy postprocessing_common_h5py.py into this folder
2. run: 
python postprocessing_h5py/compute_domain_specific_viz_BSL.py --case /media/db_ubuntu/T7/Simulations/5_4_Verify_WSS/BSL_solver/_results/_SS/case16_m06_duplicate --save_deg 1 --dt 0.000339642857143 --mesh file_case16_el06 --end_t 0.951

3. run
python postprocessing_h5py/compute_domain_specific_viz_BSL.py --case /media/db_ubuntu/T7/Simulations/5_4_Verify_WSS/BSL_solver/_results/_SS/case16_m06_duplicate --save_deg 1 --dt 0.000339642857143 --mesh file_case16_el06 --end_t 0.951

4. run (stride can be any value)
python postprocessing_h5py/compute_domain_specific_viz_BSL.py --case /media/db_ubuntu/T7/Simulations/5_4_Verify_WSS/BSL_solver/_results/_SS/case16_m06_duplicate --save_deg 1 --dt 0.000339642857143 --mesh file_case16_el06 --end_t 0.951 --stride 20
