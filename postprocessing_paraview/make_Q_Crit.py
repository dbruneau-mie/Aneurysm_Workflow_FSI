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

timestep_plot = 180
offset_time = 20

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

# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=velocity_save_deg_2xdmf)
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'velocity_save_deg_2']
gradientOfUnstructuredDataSet1.ComputeGradient = 1
gradientOfUnstructuredDataSet1.ResultArrayName = 'Gradients'
gradientOfUnstructuredDataSet1.FasterApproximation = 0
gradientOfUnstructuredDataSet1.ComputeDivergence = 0
gradientOfUnstructuredDataSet1.DivergenceArrayName = 'Divergence'
gradientOfUnstructuredDataSet1.ComputeVorticity = 1
gradientOfUnstructuredDataSet1.VorticityArrayName = 'Vorticity'
gradientOfUnstructuredDataSet1.ComputeQCriterion = 1
gradientOfUnstructuredDataSet1.QCriterionArrayName = 'Q-criterion'
gradientOfUnstructuredDataSet1.ContributingCellOption = 'Dataset Max'
gradientOfUnstructuredDataSet1.ReplacementValueOption = 'NaN'

# show data in view
gradientOfUnstructuredDataSet1Display = Show(gradientOfUnstructuredDataSet1, renderView1)


# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
gradientOfUnstructuredDataSet1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
gradientOfUnstructuredDataSet1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
gradientOfUnstructuredDataSet1Display.GlyphType.TipResolution = 6
gradientOfUnstructuredDataSet1Display.GlyphType.TipRadius = 0.1
gradientOfUnstructuredDataSet1Display.GlyphType.TipLength = 0.35
gradientOfUnstructuredDataSet1Display.GlyphType.ShaftResolution = 6
gradientOfUnstructuredDataSet1Display.GlyphType.ShaftRadius = 0.03
gradientOfUnstructuredDataSet1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
gradientOfUnstructuredDataSet1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
gradientOfUnstructuredDataSet1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
gradientOfUnstructuredDataSet1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
gradientOfUnstructuredDataSet1Display.OpacityTransferFunction.UseLogScale = 0


# hide data in view
Hide(velocity_save_deg_2xdmf, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Contour'
contour1 = Contour(Input=gradientOfUnstructuredDataSet1)
contour1.ContourBy = ['POINTS', 'Q-criterion']
contour1.ComputeNormals = 1
contour1.ComputeGradients = 0
contour1.ComputeScalars = 0
contour1.OutputPointsPrecision = 'Same as input'
contour1.GenerateTriangles = 1
contour1.Isosurfaces = [-473693.5]
contour1.PointMergeMethod = 'Uniform Binning'

# init the 'Uniform Binning' selected for 'PointMergeMethod'
contour1.PointMergeMethod.Divisions = [50, 50, 50]
contour1.PointMergeMethod.Numberofpointsperbucket = 8

# show data in view
contour1Display = Show(contour1, renderView1)

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
contour1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
contour1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
contour1Display.GlyphType.TipResolution = 6
contour1Display.GlyphType.TipRadius = 0.1
contour1Display.GlyphType.TipLength = 0.35
contour1Display.GlyphType.ShaftResolution = 6
contour1Display.GlyphType.ShaftRadius = 0.03
contour1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
contour1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
contour1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
contour1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
contour1Display.OpacityTransferFunction.UseLogScale = 0

# hide data in view
Hide(gradientOfUnstructuredDataSet1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on contour1
contour1.Isosurfaces = [100000.0]

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Extract Time Steps'
extractTimeSteps1 = ExtractTimeSteps(Input=contour1)
extractTimeSteps1.SelectionMode = 'Select Time Steps'
extractTimeSteps1.TimeStepIndices = [0]
extractTimeSteps1.TimeStepRange = [0, 1397]
extractTimeSteps1.TimeStepInterval = 1
extractTimeSteps1.ApproximationMode = 'Nearest Time Step'

# show data in view
extractTimeSteps1Display = Show(extractTimeSteps1, renderView1)

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
extractTimeSteps1Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps1Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
extractTimeSteps1Display.GlyphType.TipResolution = 6
extractTimeSteps1Display.GlyphType.TipRadius = 0.1
extractTimeSteps1Display.GlyphType.TipLength = 0.35
extractTimeSteps1Display.GlyphType.ShaftResolution = 6
extractTimeSteps1Display.GlyphType.ShaftRadius = 0.03
extractTimeSteps1Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
extractTimeSteps1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps1Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
extractTimeSteps1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps1Display.OpacityTransferFunction.UseLogScale = 0

# hide data in view
Hide(contour1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractTimeSteps1
extractTimeSteps1.TimeStepIndices = [timestep_plot]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(contour1)

# create a new 'Extract Time Steps'
extractTimeSteps2 = ExtractTimeSteps(Input=contour1)
extractTimeSteps2.SelectionMode = 'Select Time Steps'
extractTimeSteps2.TimeStepIndices = [0]
extractTimeSteps2.TimeStepRange = [0, 1397]
extractTimeSteps2.TimeStepInterval = 1
extractTimeSteps2.ApproximationMode = 'Nearest Time Step'

# show data in view
extractTimeSteps2Display = Show(extractTimeSteps2, renderView1)

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
extractTimeSteps2Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps2Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
extractTimeSteps2Display.GlyphType.TipResolution = 6
extractTimeSteps2Display.GlyphType.TipRadius = 0.1
extractTimeSteps2Display.GlyphType.TipLength = 0.35
extractTimeSteps2Display.GlyphType.ShaftResolution = 6
extractTimeSteps2Display.GlyphType.ShaftRadius = 0.03
extractTimeSteps2Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
extractTimeSteps2Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps2Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
extractTimeSteps2Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps2Display.OpacityTransferFunction.UseLogScale = 0

# hide data in view
Hide(contour1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractTimeSteps2
extractTimeSteps2.TimeStepIndices = [timestep_plot-offset_time]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(contour1)

# create a new 'Extract Time Steps'
extractTimeSteps3 = ExtractTimeSteps(Input=contour1)
extractTimeSteps3.SelectionMode = 'Select Time Steps'
extractTimeSteps3.TimeStepIndices = [0]
extractTimeSteps3.TimeStepRange = [0, 1397]
extractTimeSteps3.TimeStepInterval = 1
extractTimeSteps3.ApproximationMode = 'Nearest Time Step'

# show data in view
extractTimeSteps3Display = Show(extractTimeSteps3, renderView1)


# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
extractTimeSteps3Display.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps3Display.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
extractTimeSteps3Display.GlyphType.TipResolution = 6
extractTimeSteps3Display.GlyphType.TipRadius = 0.1
extractTimeSteps3Display.GlyphType.TipLength = 0.35
extractTimeSteps3Display.GlyphType.ShaftResolution = 6
extractTimeSteps3Display.GlyphType.ShaftRadius = 0.03
extractTimeSteps3Display.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
extractTimeSteps3Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps3Display.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
extractTimeSteps3Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
extractTimeSteps3Display.OpacityTransferFunction.UseLogScale = 0


# hide data in view
Hide(contour1, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on extractTimeSteps3
extractTimeSteps3.TimeStepIndices = [timestep_plot+offset_time]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(velocity_save_deg_2xdmf)

# show data in view
velocity_save_deg_2xdmfDisplay = Show(velocity_save_deg_2xdmf, renderView1)

# init the 'PiecewiseFunction' selected for 'OSPRayScaleFunction'
velocity_save_deg_2xdmfDisplay.OSPRayScaleFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
velocity_save_deg_2xdmfDisplay.OSPRayScaleFunction.UseLogScale = 0

# init the 'Arrow' selected for 'GlyphType'
velocity_save_deg_2xdmfDisplay.GlyphType.TipResolution = 6
velocity_save_deg_2xdmfDisplay.GlyphType.TipRadius = 0.1
velocity_save_deg_2xdmfDisplay.GlyphType.TipLength = 0.35
velocity_save_deg_2xdmfDisplay.GlyphType.ShaftResolution = 6
velocity_save_deg_2xdmfDisplay.GlyphType.ShaftRadius = 0.03
velocity_save_deg_2xdmfDisplay.GlyphType.Invert = 0

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
velocity_save_deg_2xdmfDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
velocity_save_deg_2xdmfDisplay.ScaleTransferFunction.UseLogScale = 0

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
velocity_save_deg_2xdmfDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]
velocity_save_deg_2xdmfDisplay.OpacityTransferFunction.UseLogScale = 0


# update the view to ensure updated data information
renderView1.Update()

# Properties modified on velocity_save_deg_2xdmfDisplay
velocity_save_deg_2xdmfDisplay.Opacity = 0.25

# set active source
SetActiveSource(extractTimeSteps1)

# change solid color
extractTimeSteps1Display.DiffuseColor = [0.0, 0.0, 1.0]

# set active source
SetActiveSource(extractTimeSteps2)

# set active source
SetActiveSource(extractTimeSteps3)

# change solid color
extractTimeSteps3Display.DiffuseColor = [1.0, 1.0, 0.0]

# set active source
SetActiveSource(extractTimeSteps2)

# change solid color
extractTimeSteps2Display.DiffuseColor = [1.0, 0.0, 0.0]

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

renderView1.CameraPosition = CameraPosition 
renderView1.CameraFocalPoint = CameraFocalPoint 
renderView1.CameraViewUp = CameraViewUp 
renderView1.CameraParallelScale = CameraParallelScale 

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# update the view to ensure updated data information
renderView1.Update()

Q_Contours = [5000, 20000, 50000, 100000, 200000]

for Q_Contour in Q_Contours:

    # Properties modified on contour1
    contour1.Isosurfaces = [Q_Contour]
    
    # update the view to ensure updated data information
    renderView1.Update()
    # get layout
    layout1 = GetLayout()
    QCrit_file = os.path.join(image_folder, 'QCrit_'+str(int(Q_Contour))+'_Peak_Sys_Offset_plus_minus_'+str(offset_time)+'frames_center_'+str(timestep_plot)+'.png')
    # save screenshot
    SaveScreenshot(QCrit_file, layout1, ImageResolution=[1037, 799])


#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).