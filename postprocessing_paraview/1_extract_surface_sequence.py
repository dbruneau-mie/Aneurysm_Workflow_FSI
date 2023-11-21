# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
boundary_file_path = '/media/db_ubuntu/T7/Meshing/FSI/Balasso/meshes/case_balassosmooth_first_bds.pvd'
disp_file_path = '/media/db_ubuntu/T7/Simulations/7_1_Balasso_Validation/pv_solid_only/_results/Faster_Inflation_E2_Visc/Balasso_Solid/1/Visualization/displacement.xdmf'
output_path = '/media/db_ubuntu/T7/Simulations/7_1_Balasso_Validation/pv_solid_only/_results/Faster_Inflation_E2_Visc/Balasso_Solid/1/Surfaces/'
import os
if os.path.exists(output_path)==False:
	os.mkdir(output_path)
#start_t = 0.001
#dt = 0.001
#number_of_ts = 1000
#save_increment = 100
#
start_t = 0.001
dt = 0.001
number_of_ts = 100
save_increment = 10

paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
displacementxdmf = Xdmf3ReaderS(FileName=[disp_file_path])
displacementxdmf.PointArrays = ['Displacement']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1475, 799]

# show data in view
displacementxdmfDisplay = Show(displacementxdmf, renderView1)

# trace defaults for the display properties.
displacementxdmfDisplay.Representation = 'Surface'
displacementxdmfDisplay.ColorArrayName = [None, '']
displacementxdmfDisplay.OSPRayScaleArray = 'Displacement'
displacementxdmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
displacementxdmfDisplay.SelectOrientationVectors = 'Displacement'
displacementxdmfDisplay.ScaleFactor = 0.006175819784402847
displacementxdmfDisplay.SelectScaleArray = 'Displacement'
displacementxdmfDisplay.GlyphType = 'Arrow'
displacementxdmfDisplay.GlyphTableIndexArray = 'Displacement'
displacementxdmfDisplay.GaussianRadius = 0.00030879098922014235
displacementxdmfDisplay.SetScaleArray = ['POINTS', 'Displacement']
displacementxdmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
displacementxdmfDisplay.OpacityArray = ['POINTS', 'Displacement']
displacementxdmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
displacementxdmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
displacementxdmfDisplay.SelectionCellLabelFontFile = ''
displacementxdmfDisplay.SelectionPointLabelFontFile = ''
displacementxdmfDisplay.PolarAxes = 'PolarAxesRepresentation'
displacementxdmfDisplay.ScalarOpacityUnitDistance = 0.002474637418981569

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
displacementxdmfDisplay.DataAxesGrid.XTitleFontFile = ''
displacementxdmfDisplay.DataAxesGrid.YTitleFontFile = ''
displacementxdmfDisplay.DataAxesGrid.ZTitleFontFile = ''
displacementxdmfDisplay.DataAxesGrid.XLabelFontFile = ''
displacementxdmfDisplay.DataAxesGrid.YLabelFontFile = ''
displacementxdmfDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
displacementxdmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
displacementxdmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
displacementxdmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
displacementxdmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# reset view to fit data
renderView1.ResetCamera()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# create a new 'PVD Reader'
case_balassosmooth_first_bdspvd = PVDReader(FileName=boundary_file_path)
case_balassosmooth_first_bdspvd.CellArrays = ['f']

# show data in view
case_balassosmooth_first_bdspvdDisplay = Show(case_balassosmooth_first_bdspvd, renderView1)

# get color transfer function/color map for 'f'
fLUT = GetColorTransferFunction('f')

# get opacity transfer function/opacity map for 'f'
fPWF = GetOpacityTransferFunction('f')

# trace defaults for the display properties.
case_balassosmooth_first_bdspvdDisplay.Representation = 'Surface'
case_balassosmooth_first_bdspvdDisplay.ColorArrayName = ['CELLS', 'f']
case_balassosmooth_first_bdspvdDisplay.LookupTable = fLUT
case_balassosmooth_first_bdspvdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
case_balassosmooth_first_bdspvdDisplay.SelectOrientationVectors = 'None'
case_balassosmooth_first_bdspvdDisplay.ScaleFactor = 0.00617582
case_balassosmooth_first_bdspvdDisplay.SelectScaleArray = 'f'
case_balassosmooth_first_bdspvdDisplay.GlyphType = 'Arrow'
case_balassosmooth_first_bdspvdDisplay.GlyphTableIndexArray = 'f'
case_balassosmooth_first_bdspvdDisplay.GaussianRadius = 0.000308791
case_balassosmooth_first_bdspvdDisplay.SetScaleArray = [None, '']
case_balassosmooth_first_bdspvdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
case_balassosmooth_first_bdspvdDisplay.OpacityArray = [None, '']
case_balassosmooth_first_bdspvdDisplay.OpacityTransferFunction = 'PiecewiseFunction'
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid = 'GridAxesRepresentation'
case_balassosmooth_first_bdspvdDisplay.SelectionCellLabelFontFile = ''
case_balassosmooth_first_bdspvdDisplay.SelectionPointLabelFontFile = ''
case_balassosmooth_first_bdspvdDisplay.PolarAxes = 'PolarAxesRepresentation'
case_balassosmooth_first_bdspvdDisplay.ScalarOpacityFunction = fPWF
case_balassosmooth_first_bdspvdDisplay.ScalarOpacityUnitDistance = 0.0019118759741285983

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.XTitleFontFile = ''
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.YTitleFontFile = ''
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.ZTitleFontFile = ''
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.XLabelFontFile = ''
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.YLabelFontFile = ''
case_balassosmooth_first_bdspvdDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
case_balassosmooth_first_bdspvdDisplay.PolarAxes.PolarAxisTitleFontFile = ''
case_balassosmooth_first_bdspvdDisplay.PolarAxes.PolarAxisLabelFontFile = ''
case_balassosmooth_first_bdspvdDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
case_balassosmooth_first_bdspvdDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# show color bar/color legend
case_balassosmooth_first_bdspvdDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(displacementxdmf)

# create a new 'Append Attributes'
appendAttributes1 = AppendAttributes(Input=[case_balassosmooth_first_bdspvd, displacementxdmf])

# show data in view
appendAttributes1Display = Show(appendAttributes1, renderView1)

# trace defaults for the display properties.
appendAttributes1Display.Representation = 'Surface'
appendAttributes1Display.ColorArrayName = ['CELLS', 'f']
appendAttributes1Display.LookupTable = fLUT
appendAttributes1Display.OSPRayScaleArray = 'Displacement'
appendAttributes1Display.OSPRayScaleFunction = 'PiecewiseFunction'
appendAttributes1Display.SelectOrientationVectors = 'Displacement'
appendAttributes1Display.ScaleFactor = 0.00617582
appendAttributes1Display.SelectScaleArray = 'f'
appendAttributes1Display.GlyphType = 'Arrow'
appendAttributes1Display.GlyphTableIndexArray = 'f'
appendAttributes1Display.GaussianRadius = 0.000308791
appendAttributes1Display.SetScaleArray = ['POINTS', 'Displacement']
appendAttributes1Display.ScaleTransferFunction = 'PiecewiseFunction'
appendAttributes1Display.OpacityArray = ['POINTS', 'Displacement']
appendAttributes1Display.OpacityTransferFunction = 'PiecewiseFunction'
appendAttributes1Display.DataAxesGrid = 'GridAxesRepresentation'
appendAttributes1Display.SelectionCellLabelFontFile = ''
appendAttributes1Display.SelectionPointLabelFontFile = ''
appendAttributes1Display.PolarAxes = 'PolarAxesRepresentation'
appendAttributes1Display.ScalarOpacityFunction = fPWF
appendAttributes1Display.ScalarOpacityUnitDistance = 0.0019118759741285983

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
appendAttributes1Display.DataAxesGrid.XTitleFontFile = ''
appendAttributes1Display.DataAxesGrid.YTitleFontFile = ''
appendAttributes1Display.DataAxesGrid.ZTitleFontFile = ''
appendAttributes1Display.DataAxesGrid.XLabelFontFile = ''
appendAttributes1Display.DataAxesGrid.YLabelFontFile = ''
appendAttributes1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
appendAttributes1Display.PolarAxes.PolarAxisTitleFontFile = ''
appendAttributes1Display.PolarAxes.PolarAxisLabelFontFile = ''
appendAttributes1Display.PolarAxes.LastRadialAxisTextFontFile = ''
appendAttributes1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(case_balassosmooth_first_bdspvd, renderView1)

# hide data in view
Hide(displacementxdmf, renderView1)

# show color bar/color legend
appendAttributes1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(Input=appendAttributes1)
warpByVector1.Vectors = ['POINTS', 'Displacement']

# show data in view
warpByVector1Display = Show(warpByVector1, renderView1)

# trace defaults for the display properties.
warpByVector1Display.Representation = 'Surface'
warpByVector1Display.ColorArrayName = ['CELLS', 'f']
warpByVector1Display.LookupTable = fLUT
warpByVector1Display.OSPRayScaleArray = 'Displacement'
warpByVector1Display.OSPRayScaleFunction = 'PiecewiseFunction'
warpByVector1Display.SelectOrientationVectors = 'Displacement'
warpByVector1Display.ScaleFactor = 0.00617582
warpByVector1Display.SelectScaleArray = 'f'
warpByVector1Display.GlyphType = 'Arrow'
warpByVector1Display.GlyphTableIndexArray = 'f'
warpByVector1Display.GaussianRadius = 0.000308791
warpByVector1Display.SetScaleArray = ['POINTS', 'Displacement']
warpByVector1Display.ScaleTransferFunction = 'PiecewiseFunction'
warpByVector1Display.OpacityArray = ['POINTS', 'Displacement']
warpByVector1Display.OpacityTransferFunction = 'PiecewiseFunction'
warpByVector1Display.DataAxesGrid = 'GridAxesRepresentation'
warpByVector1Display.SelectionCellLabelFontFile = ''
warpByVector1Display.SelectionPointLabelFontFile = ''
warpByVector1Display.PolarAxes = 'PolarAxesRepresentation'
warpByVector1Display.ScalarOpacityFunction = fPWF
warpByVector1Display.ScalarOpacityUnitDistance = 0.0019119259305449266

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
warpByVector1Display.DataAxesGrid.XTitleFontFile = ''
warpByVector1Display.DataAxesGrid.YTitleFontFile = ''
warpByVector1Display.DataAxesGrid.ZTitleFontFile = ''
warpByVector1Display.DataAxesGrid.XLabelFontFile = ''
warpByVector1Display.DataAxesGrid.YLabelFontFile = ''
warpByVector1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
warpByVector1Display.PolarAxes.PolarAxisTitleFontFile = ''
warpByVector1Display.PolarAxes.PolarAxisLabelFontFile = ''
warpByVector1Display.PolarAxes.LastRadialAxisTextFontFile = ''
warpByVector1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(appendAttributes1, renderView1)

# show color bar/color legend
warpByVector1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Threshold'
threshold1 = Threshold(Input=warpByVector1)
threshold1.Scalars = ['CELLS', 'f']
threshold1.ThresholdRange = [0.0, 33.0]

# Properties modified on threshold1
threshold1.ThresholdRange = [22.0, 22.0]

# show data in view
threshold1Display = Show(threshold1, renderView1)

# trace defaults for the display properties.
threshold1Display.Representation = 'Surface'
threshold1Display.ColorArrayName = ['CELLS', 'f']
threshold1Display.LookupTable = fLUT
threshold1Display.OSPRayScaleArray = 'Displacement'
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.SelectOrientationVectors = 'Displacement'
threshold1Display.ScaleFactor = 0.006170159999999998
threshold1Display.SelectScaleArray = 'f'
threshold1Display.GlyphType = 'Arrow'
threshold1Display.GlyphTableIndexArray = 'f'
threshold1Display.GaussianRadius = 0.0003085079999999999
threshold1Display.SetScaleArray = ['POINTS', 'Displacement']
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityArray = ['POINTS', 'Displacement']
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1Display.SelectionCellLabelFontFile = ''
threshold1Display.SelectionPointLabelFontFile = ''
threshold1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1Display.ScalarOpacityFunction = fPWF
threshold1Display.ScalarOpacityUnitDistance = 0.004447458703783077

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
threshold1Display.DataAxesGrid.XTitleFontFile = ''
threshold1Display.DataAxesGrid.YTitleFontFile = ''
threshold1Display.DataAxesGrid.ZTitleFontFile = ''
threshold1Display.DataAxesGrid.XLabelFontFile = ''
threshold1Display.DataAxesGrid.YLabelFontFile = ''
threshold1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
threshold1Display.PolarAxes.PolarAxisTitleFontFile = ''
threshold1Display.PolarAxes.PolarAxisLabelFontFile = ''
threshold1Display.PolarAxes.LastRadialAxisTextFontFile = ''
threshold1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(warpByVector1, renderView1)

# show color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=threshold1)

# show data in view
extractSurface1Display = Show(extractSurface1, renderView1)

# trace defaults for the display properties.
extractSurface1Display.Representation = 'Surface'
extractSurface1Display.ColorArrayName = ['CELLS', 'f']
extractSurface1Display.LookupTable = fLUT
extractSurface1Display.OSPRayScaleArray = 'Displacement'
extractSurface1Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractSurface1Display.SelectOrientationVectors = 'Displacement'
extractSurface1Display.ScaleFactor = 0.006170159999999998
extractSurface1Display.SelectScaleArray = 'f'
extractSurface1Display.GlyphType = 'Arrow'
extractSurface1Display.GlyphTableIndexArray = 'f'
extractSurface1Display.GaussianRadius = 0.0003085079999999999
extractSurface1Display.SetScaleArray = ['POINTS', 'Displacement']
extractSurface1Display.ScaleTransferFunction = 'PiecewiseFunction'
extractSurface1Display.OpacityArray = ['POINTS', 'Displacement']
extractSurface1Display.OpacityTransferFunction = 'PiecewiseFunction'
extractSurface1Display.DataAxesGrid = 'GridAxesRepresentation'
extractSurface1Display.SelectionCellLabelFontFile = ''
extractSurface1Display.SelectionPointLabelFontFile = ''
extractSurface1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
extractSurface1Display.DataAxesGrid.XTitleFontFile = ''
extractSurface1Display.DataAxesGrid.YTitleFontFile = ''
extractSurface1Display.DataAxesGrid.ZTitleFontFile = ''
extractSurface1Display.DataAxesGrid.XLabelFontFile = ''
extractSurface1Display.DataAxesGrid.YLabelFontFile = ''
extractSurface1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
extractSurface1Display.PolarAxes.PolarAxisTitleFontFile = ''
extractSurface1Display.PolarAxes.PolarAxisLabelFontFile = ''
extractSurface1Display.PolarAxes.LastRadialAxisTextFontFile = ''
extractSurface1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# hide data in view
Hide(threshold1, renderView1)

# show color bar/color legend
extractSurface1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

for ts in range(number_of_ts):
    if ts % save_increment == 0:
        out_surf_name = output_path + str(dt*ts+start_t) + ".stl"
        SaveData(out_surf_name, proxy=extractSurface1)
    animationScene1.GoToNext()

animationScene1.GoToLast()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.00741411536000669, 0.08899284899234772, 0.0355273382141755]
renderView1.CameraFocalPoint = [0.00741411536000669, 0.08899284899234772, -0.108872901648283]
renderView1.CameraParallelScale = 0.03737353219377646

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).