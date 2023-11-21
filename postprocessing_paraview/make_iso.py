# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
import sys
import os
import postprocessing_common_paraview


CameraPosition = map(float, sys.argv[2].strip('[]').split(',')) 
CameraFocalPoint = map(float, sys.argv[3].strip('[]').split(',')) 
CameraViewUp = map(float, sys.argv[4].strip('[]').split(',')) 
CameraParallelScale = float(sys.argv[5])


case_path = sys.argv[1]
#with open("/gpfs/fs0/scratch/s/steinman/dbruneau/Aneurysm_Workflow_FSI/Scripts_Nia/pulsatile_ramp_config/Case9_m047_predeformed_finerflow.config") as file:
#with open(sys.argv[1]) as file:
#    for item in file:
#        print(item)
#import postprocessing_common_paraview
#
#case_path, mesh_name = postprocessing_common_paraview.read_command_line()
visualization_path = postprocessing_common_paraview.get_visualization_path(case_path)
visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")
image_folder =  os.path.join(visualization_path,"../Images")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
velocity_save_deg_2xdmf = Xdmf3ReaderS(FileName=[visualization_separate_domain_folder + '/velocity_save_deg_2.xdmf'])
velocity_save_deg_2xdmf.PointArrays = ['velocity_save_deg_2']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [1037, 799]

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()
# Properties modified on animationScene1
animationScene1.PlayMode = 'Sequence'


# create a new 'Calculator'
calculator1 = Calculator(Input=velocity_save_deg_2xdmf)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = ''

# show data in view
calculator1Display = Show(calculator1, renderView1)

# hide data in view
Hide(velocity_save_deg_2xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on calculator1
calculator1.Function = 'mag(velocity_save_deg_2)'

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Contour'
contour1 = Contour(Input=calculator1)
contour1.ContourBy = ['POINTS', 'Result']
contour1.Isosurfaces = [0.3916158917040857]
contour1.PointMergeMethod = 'Uniform Binning'

# show data in view
contour1Display = Show(contour1, renderView1)

# hide data in view
Hide(calculator1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on contour1
contour1.Isosurfaces = [0.75]

# set active source
SetActiveSource(velocity_save_deg_2xdmf)

# show data in view
velocity_save_deg_2xdmfDisplay = Show(velocity_save_deg_2xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on velocity_save_deg_2xdmfDisplay
velocity_save_deg_2xdmfDisplay.Opacity = 0.5

# set active source
SetActiveSource(velocity_save_deg_2xdmf)

# set active source
SetActiveSource(contour1)

# change solid color
contour1Display.DiffuseColor = [1.0, 0.0, 0.0]


## current camera placement for renderView1
#renderView1.CameraPosition = [0.09785459516700948, 0.13504100094349036, 0.04409815605715928]
#renderView1.CameraFocalPoint = [0.11979091114082246, 0.135267328293353, 0.06325466680745545]
#renderView1.CameraViewUp = [0.6500431936464535, -0.1618604928920621, -0.7424587714039469]
#renderView1.CameraParallelScale = 0.019551435004847722

# current camera placement for renderView1
#renderView1.CameraPosition = CameraPosition [0.08320748537665072, 0.11236411248695452, 0.0386984510441699]
#renderView1.CameraFocalPoint = CameraFocalPoint [0.10727798630215984, 0.10279259549134778, 0.061345755569347446]
#renderView1.CameraViewUp = CameraViewUp [0.67892472034913, 0.5460438438364111, -0.49081294268510584]
#renderView1.CameraParallelScale = CameraParallelScale 0.01303842390724087

# get the time-keeper
tk = GetTimeKeeper()
timesteps = tk.TimestepValues
animationScene1.AnimationTime = timesteps[160]

renderView1.CameraPosition = CameraPosition 
renderView1.CameraFocalPoint = CameraFocalPoint 
renderView1.CameraViewUp = CameraViewUp 
renderView1.CameraParallelScale = CameraParallelScale 

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# update the view to ensure updated data information
renderView1.Update()

# get layout
layout1 = GetLayout()
contour0p75_file = os.path.join(image_folder, 'Peak_Sys_0p75_Vel_Iso.png')
# save screenshot
SaveScreenshot(contour0p75_file, layout1, ImageResolution=[1037, 799])


# Properties modified on contour1
contour1.Isosurfaces = [0.5]

# update the view to ensure updated data information
renderView1.Update()

# get layout
layout1 = GetLayout()
contour0p5_file = os.path.join(image_folder, 'Peak_Sys_0p5_Vel_Iso.png')
# save screenshot
SaveScreenshot(contour0p5_file, layout1, ImageResolution=[1037, 799])


#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).