# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
import sys
import os
import postprocessing_common_paraview

print("Modules Loaded!")

CameraPosition = map(float, sys.argv[2].strip('[]').split(',')) 
CameraFocalPoint = map(float, sys.argv[3].strip('[]').split(',')) 
CameraViewUp = map(float, sys.argv[4].strip('[]').split(',')) 
CameraParallelScale = float(sys.argv[5])

timestep_plot = 2960

case_path = sys.argv[1]
#with open("/gpfs/fs0/scratch/s/steinman/dbruneau/Aneurysm_Workflow_FSI/Scripts_Nia/pulsatile_ramp_config/Case9_m047_predeformed_finerflow.config") as file:
#with open(sys.argv[1]) as file:
#    for item in file:
#        print(item)
#import postprocessing_common_paraview
#
#case_path, mesh_name = postprocessing_common_paraview.read_command_line()
visualization_path = postprocessing_common_paraview.get_visualization_path(case_path)
visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")
image_folder =  os.path.join(visualization_path,"../Images")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
velocity_25_to_100000xdmf = Xdmf3ReaderS(FileName=[visualization_hi_pass_folder + '/velocity_25_to_100000.xdmf'])
velocity_25_to_100000xdmf.PointArrays = ['velocity_25_to_100000']

print("Data Loaded!")

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [957, 799]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# create a new 'Xdmf3ReaderS'
velocity_0_to_25xdmf = Xdmf3ReaderS(FileName=[visualization_hi_pass_folder + '/velocity_0_to_25.xdmf'])
velocity_0_to_25xdmf.PointArrays = ['velocity_0_to_25']

# show data in view
velocity_0_to_25xdmfDisplay = Show(velocity_0_to_25xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(velocity_25_to_100000xdmf)

# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=velocity_25_to_100000xdmf)
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'velocity_25_to_100000']
gradientOfUnstructuredDataSet1.ComputeVorticity = 1
gradientOfUnstructuredDataSet1.ComputeQCriterion = 1

# show data in view
gradientOfUnstructuredDataSet1Display = Show(gradientOfUnstructuredDataSet1, renderView1)

# hide data in view
Hide(velocity_25_to_100000xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(velocity_0_to_25xdmf)

# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet2 = GradientOfUnstructuredDataSet(Input=velocity_0_to_25xdmf)
gradientOfUnstructuredDataSet2.ScalarArray = ['POINTS', 'velocity_0_to_25']
gradientOfUnstructuredDataSet2.ComputeVorticity = 1
gradientOfUnstructuredDataSet2.ComputeQCriterion = 1

# show data in view
gradientOfUnstructuredDataSet2Display = Show(gradientOfUnstructuredDataSet2, renderView1)

print("Running!")

# hide data in view
Hide(velocity_0_to_25xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(gradientOfUnstructuredDataSet1)

# create a new 'Contour'
contour1 = Contour(Input=gradientOfUnstructuredDataSet1)
contour1.ContourBy = ['POINTS', 'Q-criterion']
contour1.Isosurfaces = [0.023889437317848206]
contour1.PointMergeMethod = 'Uniform Binning'

# show data in view
contour1Display = Show(contour1, renderView1)

# hide data in view
Hide(gradientOfUnstructuredDataSet1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(gradientOfUnstructuredDataSet1)

# set active source
SetActiveSource(contour1)

# Properties modified on contour1
contour1.Isosurfaces = [5000.0]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(gradientOfUnstructuredDataSet2)

# create a new 'Contour'
contour2 = Contour(Input=gradientOfUnstructuredDataSet2)
contour2.ContourBy = ['POINTS', 'Q-criterion']
contour2.Isosurfaces = [807797.0]
contour2.PointMergeMethod = 'Uniform Binning'

# show data in view
contour2Display = Show(contour2, renderView1)

# hide data in view
Hide(gradientOfUnstructuredDataSet2, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on contour2
contour2.Isosurfaces = [50000.0]

# update the view to ensure updated data information
renderView1.Update()

# change solid color
contour2Display.DiffuseColor = [0.7372549019607844, 0.7372549019607844, 0.7372549019607844]

# Properties modified on contour2Display
contour2Display.Opacity = 0.4

# set active source
SetActiveSource(contour1)

# change solid color
contour1Display.DiffuseColor = [0.6666666666666666, 0.6666666666666666, 1.0]

# Properties modified on contour1
contour1.Isosurfaces = [500.0]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on contour1
contour1.Isosurfaces = [100.0]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(velocity_25_to_100000xdmf)

# show data in view
velocity_25_to_100000xdmfDisplay = Show(velocity_25_to_100000xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on velocity_25_to_100000xdmfDisplay
velocity_25_to_100000xdmfDisplay.Opacity = 0.25


renderView1.CameraPosition = CameraPosition 
renderView1.CameraFocalPoint = CameraFocalPoint 
renderView1.CameraViewUp = CameraViewUp 
renderView1.CameraParallelScale = CameraParallelScale 

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# get the time-keeper
tk = GetTimeKeeper()
timesteps = tk.TimestepValues
animationScene1.AnimationTime = timesteps[timestep_plot]

print("Saving Images....")

# update the view to ensure updated data information
renderView1.Update()

Q_Contours = [5000, 20000, 50000, 100000, 200000]
Q_Contours_Hi = [100, 250, 1000, 5000, 20000]

for Q_Contour,Q_Contour_Hi in zip(Q_Contours,Q_Contours_Hi):

    # Properties modified on contour1
    contour1.Isosurfaces = [Q_Contour]
    contour2.Isosurfaces = [Q_Contour_Hi]
    
    # update the view to ensure updated data information
    renderView1.Update()
    # get layout
    layout1 = GetLayout()
    print("Saving Image")
    QCrit_file = os.path.join(image_folder, 'QCritLo_'+str(int(Q_Contour))+'QCritHi_'+str(int(Q_Contour_Hi))+'_Peak_Sys_'+str(timestep_plot)+'.png')
    # save screenshot
    SaveScreenshot(QCrit_file, layout1, ImageResolution=[1037, 799])


#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).