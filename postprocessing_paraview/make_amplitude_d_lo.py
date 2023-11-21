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

visualization_path = postprocessing_common_paraview.get_visualization_path(case_path)
visualization_separate_domain_folder = os.path.join(visualization_path,"../Visualization_separate_domain")
visualization_hi_pass_folder = os.path.join(visualization_path,"../visualization_hi_pass")

image_folder =  os.path.join(visualization_path,"../Images")
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
displacement_amplitude_0_to_25xdmf = Xdmf3ReaderS(FileName=[visualization_hi_pass_folder + '/displacement_amplitude_0_to_25.xdmf'])
displacement_amplitude_0_to_25xdmf.PointArrays = ['displacement_amplitude_0_to_25']
displacement_amplitude_0_to_25xdmf.CellArrays = []
displacement_amplitude_0_to_25xdmf.Sets = []

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

# get display properties
displacement_amplitude_0_to_25xdmfDisplay = GetDisplayProperties(displacement_amplitude_0_to_25xdmf, view=renderView1)

# set scalar coloring
ColorBy(displacement_amplitude_0_to_25xdmfDisplay, ('POINTS', 'displacement_amplitude_0_to_25', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
displacement_amplitude_0_to_25xdmfDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
displacement_amplitude_0_to_25xdmfDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'displacement_amplitude_0_to_25'
displacement_amplitude_0_to_25LUT = GetColorTransferFunction('displacement_amplitude_0_to_25')
displacement_amplitude_0_to_25LUT.AutomaticRescaleRangeMode = 'Never'
displacement_amplitude_0_to_25LUT.InterpretValuesAsCategories = 0
displacement_amplitude_0_to_25LUT.AnnotationsInitialized = 0
displacement_amplitude_0_to_25LUT.ShowCategoricalColorsinDataRangeOnly = 0
displacement_amplitude_0_to_25LUT.RescaleOnVisibilityChange = 0
displacement_amplitude_0_to_25LUT.EnableOpacityMapping = 0
displacement_amplitude_0_to_25LUT.RGBPoints = [0.0, 0.0, 0.0, 0.5625, 5.5555500000000004e-08, 0.0, 0.0, 1.0, 1.8253974999999999e-07, 0.0, 1.0, 1.0, 2.4603174999999993e-07, 0.5, 1.0, 0.5, 3.0952375e-07, 1.0, 1.0, 0.0, 4.36508e-07, 1.0, 0.0, 0.0, 5e-07, 0.5, 0.0, 0.0]
displacement_amplitude_0_to_25LUT.UseLogScale = 0
displacement_amplitude_0_to_25LUT.ColorSpace = 'RGB'
displacement_amplitude_0_to_25LUT.UseBelowRangeColor = 0
displacement_amplitude_0_to_25LUT.BelowRangeColor = [0.0, 0.0, 0.0]
displacement_amplitude_0_to_25LUT.UseAboveRangeColor = 0
displacement_amplitude_0_to_25LUT.AboveRangeColor = [0.5, 0.5, 0.5]
displacement_amplitude_0_to_25LUT.NanColor = [1.0, 1.0, 0.0]
displacement_amplitude_0_to_25LUT.NanOpacity = 1.0
displacement_amplitude_0_to_25LUT.Discretize = 1
displacement_amplitude_0_to_25LUT.NumberOfTableValues = 256
displacement_amplitude_0_to_25LUT.ScalarRangeInitialized = 1.0
displacement_amplitude_0_to_25LUT.HSVWrap = 0
displacement_amplitude_0_to_25LUT.VectorComponent = 0
displacement_amplitude_0_to_25LUT.VectorMode = 'Magnitude'
displacement_amplitude_0_to_25LUT.AllowDuplicateScalars = 1
displacement_amplitude_0_to_25LUT.Annotations = []
displacement_amplitude_0_to_25LUT.ActiveAnnotatedValues = []
displacement_amplitude_0_to_25LUT.IndexedColors = []
displacement_amplitude_0_to_25LUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'displacement_amplitude_0_to_25'
displacement_amplitude_0_to_25PWF = GetOpacityTransferFunction('displacement_amplitude_0_to_25')
displacement_amplitude_0_to_25PWF.Points = [0.0, 0.0, 0.5, 0.0, 5e-07, 1.0, 0.5, 0.0]
displacement_amplitude_0_to_25PWF.AllowDuplicateScalars = 1
displacement_amplitude_0_to_25PWF.UseLogScale = 0
displacement_amplitude_0_to_25PWF.ScalarRangeInitialized = 1

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# ------------------------------------------------------------

# get color legend/bar for displacement_amplitude_0_to_25LUT in view renderView1
displacement_amplitude_0_to_25LUTColorBar = GetScalarBar(displacement_amplitude_0_to_25LUT, renderView1)
displacement_amplitude_0_to_25LUTColorBar.AutoOrient = 1
displacement_amplitude_0_to_25LUTColorBar.Orientation = 'Vertical'
displacement_amplitude_0_to_25LUTColorBar.WindowLocation = 'LowerRightCorner'
displacement_amplitude_0_to_25LUTColorBar.Position = [0.89, 0.02]
displacement_amplitude_0_to_25LUTColorBar.Title = 'displacement_amplitude_0_to_25'
displacement_amplitude_0_to_25LUTColorBar.ComponentTitle = 'Magnitude'
displacement_amplitude_0_to_25LUTColorBar.TitleJustification = 'Centered'
displacement_amplitude_0_to_25LUTColorBar.HorizontalTitle = 0
displacement_amplitude_0_to_25LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
displacement_amplitude_0_to_25LUTColorBar.TitleOpacity = 1.0
displacement_amplitude_0_to_25LUTColorBar.TitleFontFamily = 'Arial'
displacement_amplitude_0_to_25LUTColorBar.TitleFontFile = ''
displacement_amplitude_0_to_25LUTColorBar.TitleBold = 0
displacement_amplitude_0_to_25LUTColorBar.TitleItalic = 0
displacement_amplitude_0_to_25LUTColorBar.TitleShadow = 0
displacement_amplitude_0_to_25LUTColorBar.TitleFontSize = 16
displacement_amplitude_0_to_25LUTColorBar.LabelColor = [0.0, 0.0, 0.0]
displacement_amplitude_0_to_25LUTColorBar.LabelOpacity = 1.0
displacement_amplitude_0_to_25LUTColorBar.LabelFontFamily = 'Arial'
displacement_amplitude_0_to_25LUTColorBar.LabelFontFile = ''
displacement_amplitude_0_to_25LUTColorBar.LabelBold = 0
displacement_amplitude_0_to_25LUTColorBar.LabelItalic = 0
displacement_amplitude_0_to_25LUTColorBar.LabelShadow = 0
displacement_amplitude_0_to_25LUTColorBar.LabelFontSize = 16
displacement_amplitude_0_to_25LUTColorBar.AutomaticLabelFormat = 1
displacement_amplitude_0_to_25LUTColorBar.LabelFormat = '%-#6.3g'
displacement_amplitude_0_to_25LUTColorBar.DrawTickMarks = 1
displacement_amplitude_0_to_25LUTColorBar.DrawTickLabels = 1
displacement_amplitude_0_to_25LUTColorBar.UseCustomLabels = 0
displacement_amplitude_0_to_25LUTColorBar.CustomLabels = []
displacement_amplitude_0_to_25LUTColorBar.AddRangeLabels = 1
displacement_amplitude_0_to_25LUTColorBar.RangeLabelFormat = '%-#6.1e'
displacement_amplitude_0_to_25LUTColorBar.DrawAnnotations = 1
displacement_amplitude_0_to_25LUTColorBar.AddRangeAnnotations = 0
displacement_amplitude_0_to_25LUTColorBar.AutomaticAnnotations = 0
displacement_amplitude_0_to_25LUTColorBar.DrawNanAnnotation = 0
displacement_amplitude_0_to_25LUTColorBar.NanAnnotation = 'NaN'
displacement_amplitude_0_to_25LUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
displacement_amplitude_0_to_25LUTColorBar.ReverseLegend = 0
displacement_amplitude_0_to_25LUTColorBar.ScalarBarThickness = 16
displacement_amplitude_0_to_25LUTColorBar.ScalarBarLength = 0.33

# change scalar bar placement
displacement_amplitude_0_to_25LUTColorBar.WindowLocation = 'AnyLocation'
displacement_amplitude_0_to_25LUTColorBar.Position = [0.884281581485053, 0.08698372966207758]

# Properties modified on displacement_amplitude_0_to_25LUTColorBar
displacement_amplitude_0_to_25LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
displacement_amplitude_0_to_25LUTColorBar.LabelColor = [0.0, 0.0, 0.0]

#--------------------------------------------------------------




# update the view to ensure updated data information
renderView1.Update()

# get the time-keeper
tk = GetTimeKeeper()
timesteps = tk.TimestepValues
animationScene1.AnimationTime = timesteps[2960]

# Get camera position from command line
renderView1.CameraPosition = CameraPosition 
renderView1.CameraFocalPoint = CameraFocalPoint 
renderView1.CameraViewUp = CameraViewUp 
renderView1.CameraParallelScale = CameraParallelScale 

scales_amp = [1e-05, 2e-05, 5e-05, 1e-04, 2e-04, 5e-04, 1e-03, 2e-03, 5e-03, 1e-2]
for scale_amp in scales_amp:
# Rescale transfer function
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    displacement_amplitude_0_to_25LUT.ApplyPreset('jet', True)
    colorMap = GetColorTransferFunction('Temp')
    # Rescale transfer function
    displacement_amplitude_0_to_25LUT.RescaleTransferFunction(0.0, scale_amp)

    renderView1.Update()
    
    # get layout
    layout1 = GetLayout()
    amplitude_file = os.path.join(image_folder, 'displacement_amplitude_lo_peak_sys_'+str(scale_amp)+'.png')
    # save screenshot
    SaveScreenshot(amplitude_file, layout1, ImageResolution=[1037, 799])

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).