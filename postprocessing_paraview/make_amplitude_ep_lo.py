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
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmf = Xdmf3ReaderS(FileName=[visualization_hi_pass_folder + '/MaxPrincipalHiPassStrain_amplitude_0_to_25.xdmf'])
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmf.PointArrays = ['MaxPrincipalHiPassStrain_amplitude_0_to_25']
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmf.CellArrays = []
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmf.Sets = []

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
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmfDisplay = GetDisplayProperties(MaxPrincipalHiPassStrain_amplitude_0_to_25xdmf, view=renderView1)

# show color bar/color legend
MaxPrincipalHiPassStrain_amplitude_0_to_25xdmfDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'MaxPrincipalHiPassStrain_amplitude_0_to_25'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT = GetColorTransferFunction('MaxPrincipalHiPassStrain_amplitude_0_to_25')
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.AutomaticRescaleRangeMode = 'Never'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.InterpretValuesAsCategories = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.AnnotationsInitialized = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.ShowCategoricalColorsinDataRangeOnly = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.RescaleOnVisibilityChange = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.EnableOpacityMapping = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.RGBPoints = [0.0, 0.0, 0.0, 0.5625, 5.5555500000000004e-08, 0.0, 0.0, 1.0, 1.8253974999999999e-07, 0.0, 1.0, 1.0, 2.4603174999999993e-07, 0.5, 1.0, 0.5, 3.0952375e-07, 1.0, 1.0, 0.0, 4.36508e-07, 1.0, 0.0, 0.0, 5e-07, 0.5, 0.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.UseLogScale = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.ColorSpace = 'RGB'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.UseBelowRangeColor = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.BelowRangeColor = [0.0, 0.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.UseAboveRangeColor = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.AboveRangeColor = [0.5, 0.5, 0.5]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.NanColor = [1.0, 1.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.NanOpacity = 1.0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.Discretize = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.NumberOfTableValues = 256
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.ScalarRangeInitialized = 1.0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.HSVWrap = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.VectorComponent = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.VectorMode = 'Magnitude'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.AllowDuplicateScalars = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.Annotations = []
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.ActiveAnnotatedValues = []
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.IndexedColors = []
MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.IndexedOpacities = []

# get opacity transfer function/opacity map for 'MaxPrincipalHiPassStrain_amplitude_0_to_25'
MaxPrincipalHiPassStrain_amplitude_0_to_25PWF = GetOpacityTransferFunction('MaxPrincipalHiPassStrain_amplitude_0_to_25')
MaxPrincipalHiPassStrain_amplitude_0_to_25PWF.Points = [0.0, 0.0, 0.5, 0.0, 5e-07, 1.0, 0.5, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25PWF.AllowDuplicateScalars = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25PWF.UseLogScale = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25PWF.ScalarRangeInitialized = 1

# Properties modified on renderView1
renderView1.Background = [1.0, 1.0, 1.0]

# ------------------------------------------------------------

# get color legend/bar for MaxPrincipalHiPassStrain_amplitude_0_to_25LUT in view renderView1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar = GetScalarBar(MaxPrincipalHiPassStrain_amplitude_0_to_25LUT, renderView1)
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.AutoOrient = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.Orientation = 'Vertical'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.WindowLocation = 'LowerRightCorner'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.Position = [0.89, 0.02]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.Title = 'MaxPrincipalHiPassStrain_amplitude_0_to_25'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.ComponentTitle = 'Magnitude'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleJustification = 'Centered'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.HorizontalTitle = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleOpacity = 1.0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleFontFamily = 'Arial'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleFontFile = ''
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleBold = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleItalic = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleShadow = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleFontSize = 16
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelColor = [0.0, 0.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelOpacity = 1.0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelFontFamily = 'Arial'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelFontFile = ''
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelBold = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelItalic = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelShadow = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelFontSize = 16
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.AutomaticLabelFormat = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelFormat = '%-#6.3g'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.DrawTickMarks = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.DrawTickLabels = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.UseCustomLabels = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.CustomLabels = []
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.AddRangeLabels = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.RangeLabelFormat = '%-#6.1e'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.DrawAnnotations = 1
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.AddRangeAnnotations = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.AutomaticAnnotations = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.DrawNanAnnotation = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.NanAnnotation = 'NaN'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TextPosition = 'Ticks right/top, annotations left/bottom'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.ReverseLegend = 0
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.ScalarBarThickness = 16
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.ScalarBarLength = 0.33

# change scalar bar placement
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.WindowLocation = 'AnyLocation'
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.Position = [0.884281581485053, 0.08698372966207758]

# Properties modified on MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.TitleColor = [0.0, 0.0, 0.0]
MaxPrincipalHiPassStrain_amplitude_0_to_25LUTColorBar.LabelColor = [0.0, 0.0, 0.0]

#--------------------------------------------------------------




# update the view to ensure updated data information
renderView1.Update()

# get the time-keeper
tk = GetTimeKeeper()
timesteps = tk.TimestepValues
animationScene1.AnimationTime = timesteps[160]

# Get camera position from command line
renderView1.CameraPosition = CameraPosition 
renderView1.CameraFocalPoint = CameraFocalPoint 
renderView1.CameraViewUp = CameraViewUp 
renderView1.CameraParallelScale = CameraParallelScale 

scales_amp = [1e-03, 2e-03, 5e-03, 1e-02, 2e-02, 5e-02, 1e-01, 2e-01, 5e-01, 1.0]
for scale_amp in scales_amp:
# Rescale transfer function
    # Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
    MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.ApplyPreset('jet', True)
    colorMap = GetColorTransferFunction('Temp')
    # Rescale transfer function
    MaxPrincipalHiPassStrain_amplitude_0_to_25LUT.RescaleTransferFunction(0.0, scale_amp)

    renderView1.Update()
    
    # get layout
    layout1 = GetLayout()
    amplitude_file = os.path.join(image_folder, 'MPS_amplitude_lo_peak_sys_'+str(scale_amp)+'.png')
    # save screenshot
    SaveScreenshot(amplitude_file, layout1, ImageResolution=[1037, 799])

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).