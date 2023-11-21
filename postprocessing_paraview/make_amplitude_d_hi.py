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
displacement_amplitude_25_to_100000xdmf = Xdmf3ReaderS(FileName=[visualization_hi_pass_folder + '/displacement_amplitude_25_to_100000.xdmf'])
displacement_amplitude_25_to_100000xdmf.PointArrays = ['displacement_amplitude_25_to_100000']
displacement_amplitude_25_to_100000xdmf.CellArrays = []
displacement_amplitude_25_to_100000xdmf.Sets = []

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
displacement_amplitude_25_to_100000xdmfDisplay = GetDisplayProperties(displacement_amplitude_25_to_100000xdmf, view=renderView1)

# set scalar coloring
ColorBy(displacement_amplitude_25_to_100000xdmfDisplay, ('POINTS', 'displacement_amplitude_25_to_100000', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
displacement_amplitude_25_to_100000xdmfDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
displacement_amplitude_25_to_100000xdmfDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'displacement_amplitude_25_to_100000'
displacement_amplitude_25_to_100000LUT = GetColorTransferFunction('displacement_amplitude_25_to_100000')
displacement_amplitude_25_to_100000LUT.AutomaticRescaleRangeMode = 'Never'
displacement_amplitude_25_to_100000LUT.InterpretValuesAsCategories = 0
displacement_amplitude_25_to_100000LUT.AnnotationsInitialized = 0
displacement_amplitude_25_to_100000LUT.ShowCategoricalColorsinDataRangeOnly = 0
displacement_amplitude_25_to_100000LUT.RescaleOnVisibilityChange = 0
displacement_amplitude_25_to_100000LUT.EnableOpacityMapping = 0
displacement_amplitude_25_to_100000LUT.RGBPoints = [0.0, 0.0, 0.0, 0.5625, 5.5555500000000004e-08, 0.0, 0.0, 1.0, 1.8253974999999999e-07, 0.0, 1.0, 1.0, 2.4603174999999993e-07, 0.5, 1.0, 0.5, 3.0952375e-07, 1.0, 1.0, 0.0, 4.36508e-07, 1.0, 0.0, 0.0, 5e-07, 0.5, 0.0, 0.0]
displacement_amplitude_25_to_100000LUT.UseLogScale = 0
displacement_amplitude_25_to_100000LUT.ColorSpace = 'RGB'
displacement_amplitude_25_to_100000LUT.UseBelowRangeColor = 0
displacement_amplitude_25_to_100000LUT.BelowRangeColor = [0.0, 0.0, 0.0]
displacement_amplitude_25_to_100000LUT.UseAboveRangeColor = 0
displacement_amplitude_25_to_100000LUT.AboveRangeColor = [0.5, 0.5, 0.5]
displacement_amplitude_25_to_100000LUT.NanColor = [1.0, 1.0, 0.0]
displacement_amplitude_25_to_100000LUT.NanOpacity = 1.0
displacement_amplitude_25_to_100000LUT.Discretize = 1
displacement_amplitude_25_to_100000LUT.NumberOfTableValues = 256
displacement_amplitude_25_to_100000LUT.ScalarRangeInitialized = 1.0
displacement_amplitude_25_to_100000LUT.HSVWrap = 0
displacement_amplitude_25_to_100000LUT.VectorComponent = 0
displacement_amplitude_25_to_100000LUT.VectorMode = 'Magnitude'
displacement_amplitude_25_to_100000LUT.AllowDuplicateScalars = 1
displacement_amplitude_25_to_100000LUT.Annotations = []
displacement_amplitude_25_to_100000LUT.ActiveAnnotatedValues = []
displacement_amplitude_25_to_100000LUT.IndexedColors = []
displacement_amplitude_25_to_100000LUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'displacement_amplitude_25_to_100000'
displacement_amplitude_25_to_100000PWF = GetOpacityTransferFunction('displacement_amplitude_25_to_100000')
displacement_amplitude_25_to_100000PWF.Points = [0.0, 0.0, 0.5, 0.0, 5e-07, 1.0, 0.5, 0.0]
displacement_amplitude_25_to_100000PWF.AllowDuplicateScalars = 1
displacement_amplitude_25_to_100000PWF.UseLogScale = 0
displacement_amplitude_25_to_100000PWF.ScalarRangeInitialized = 1

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# ------------------------------------------------------------

# get color legend/bar for displacement_amplitude_25_to_100000LUT in view renderView1
displacement_amplitude_25_to_100000LUTColorBar = GetScalarBar(displacement_amplitude_25_to_100000LUT, renderView1)
displacement_amplitude_25_to_100000LUTColorBar.AutoOrient = 1
displacement_amplitude_25_to_100000LUTColorBar.Orientation = 'Vertical'
displacement_amplitude_25_to_100000LUTColorBar.WindowLocation = 'LowerRightCorner'
displacement_amplitude_25_to_100000LUTColorBar.Position = [0.89, 0.02]
displacement_amplitude_25_to_100000LUTColorBar.Title = 'displacement_amplitude_25_to_100000'
displacement_amplitude_25_to_100000LUTColorBar.ComponentTitle = 'Magnitude'
displacement_amplitude_25_to_100000LUTColorBar.TitleJustification = 'Centered'
displacement_amplitude_25_to_100000LUTColorBar.HorizontalTitle = 0
displacement_amplitude_25_to_100000LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
displacement_amplitude_25_to_100000LUTColorBar.TitleOpacity = 1.0
displacement_amplitude_25_to_100000LUTColorBar.TitleFontFamily = 'Arial'
displacement_amplitude_25_to_100000LUTColorBar.TitleFontFile = ''
displacement_amplitude_25_to_100000LUTColorBar.TitleBold = 0
displacement_amplitude_25_to_100000LUTColorBar.TitleItalic = 0
displacement_amplitude_25_to_100000LUTColorBar.TitleShadow = 0
displacement_amplitude_25_to_100000LUTColorBar.TitleFontSize = 16
displacement_amplitude_25_to_100000LUTColorBar.LabelColor = [0.0, 0.0, 0.0]
displacement_amplitude_25_to_100000LUTColorBar.LabelOpacity = 1.0
displacement_amplitude_25_to_100000LUTColorBar.LabelFontFamily = 'Arial'
displacement_amplitude_25_to_100000LUTColorBar.LabelFontFile = ''
displacement_amplitude_25_to_100000LUTColorBar.LabelBold = 0
displacement_amplitude_25_to_100000LUTColorBar.LabelItalic = 0
displacement_amplitude_25_to_100000LUTColorBar.LabelShadow = 0
displacement_amplitude_25_to_100000LUTColorBar.LabelFontSize = 16
displacement_amplitude_25_to_100000LUTColorBar.AutomaticLabelFormat = 1
displacement_amplitude_25_to_100000LUTColorBar.LabelFormat = '%-#6.3g'
displacement_amplitude_25_to_100000LUTColorBar.DrawTickMarks = 1
displacement_amplitude_25_to_100000LUTColorBar.DrawTickLabels = 1
displacement_amplitude_25_to_100000LUTColorBar.UseCustomLabels = 0
displacement_amplitude_25_to_100000LUTColorBar.CustomLabels = []
displacement_amplitude_25_to_100000LUTColorBar.AddRangeLabels = 1
displacement_amplitude_25_to_100000LUTColorBar.RangeLabelFormat = '%-#6.1e'
displacement_amplitude_25_to_100000LUTColorBar.DrawAnnotations = 1
displacement_amplitude_25_to_100000LUTColorBar.AddRangeAnnotations = 0
displacement_amplitude_25_to_100000LUTColorBar.AutomaticAnnotations = 0
displacement_amplitude_25_to_100000LUTColorBar.DrawNanAnnotation = 0
displacement_amplitude_25_to_100000LUTColorBar.NanAnnotation = 'NaN'
displacement_amplitude_25_to_100000LUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
displacement_amplitude_25_to_100000LUTColorBar.ReverseLegend = 0
displacement_amplitude_25_to_100000LUTColorBar.ScalarBarThickness = 16
displacement_amplitude_25_to_100000LUTColorBar.ScalarBarLength = 0.33

# change scalar bar placement
displacement_amplitude_25_to_100000LUTColorBar.WindowLocation = 'AnyLocation'
displacement_amplitude_25_to_100000LUTColorBar.Position = [0.884281581485053, 0.08698372966207758]

# Properties modified on displacement_amplitude_25_to_100000LUTColorBar
displacement_amplitude_25_to_100000LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
displacement_amplitude_25_to_100000LUTColorBar.LabelColor = [0.0, 0.0, 0.0]

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

scales_amp = [1e-08, 2e-08, 5e-08, 1e-07, 2e-07, 5e-07, 1e-06, 2e-06]
for scale_amp in scales_amp:
# Rescale transfer function
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    displacement_amplitude_25_to_100000LUT.ApplyPreset('jet', True)
    colorMap = GetColorTransferFunction('Temp')
    # Rescale transfer function
    displacement_amplitude_25_to_100000LUT.RescaleTransferFunction(0.0, scale_amp)

    renderView1.Update()
    
    # get layout
    layout1 = GetLayout()
    amplitude_file = os.path.join(image_folder, 'displacement_amplitude_hi_peak_sys_'+str(scale_amp)+'.png')
    # save screenshot
    SaveScreenshot(amplitude_file, layout1, ImageResolution=[1037, 799])

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).