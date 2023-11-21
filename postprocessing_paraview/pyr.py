# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Xdmf3ReaderS'
velocity_25_to_100000xdmf = Xdmf3ReaderS(FileName=['/run/user/1000/gvfs/sftp:host=niagara.scinet.utoronto.ca,user=dbruneau/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases/Case3_predeformed_finerflow/file_case3/1/visualization_hi_pass/velocity_25_to_100000.xdmf'])
velocity_25_to_100000xdmf.PointArrays = ['velocity_25_to_100000']

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
velocity_0_to_25xdmf = Xdmf3ReaderS(FileName=['/run/user/1000/gvfs/sftp:host=niagara.scinet.utoronto.ca,user=dbruneau/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases/Case3_predeformed_finerflow/file_case3/1/visualization_hi_pass/velocity_0_to_25.xdmf'])
velocity_0_to_25xdmf.PointArrays = ['velocity_0_to_25']

# show data in view
velocity_0_to_25xdmfDisplay = Show(velocity_0_to_25xdmf, renderView1)

# trace defaults for the display properties.
velocity_0_to_25xdmfDisplay.Representation = 'Surface'
velocity_0_to_25xdmfDisplay.AmbientColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.ColorArrayName = [None, '']
velocity_0_to_25xdmfDisplay.OSPRayScaleArray = 'velocity_0_to_25'
velocity_0_to_25xdmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
velocity_0_to_25xdmfDisplay.SelectOrientationVectors = 'velocity_0_to_25'
velocity_0_to_25xdmfDisplay.ScaleFactor = 0.0018633201718330384
velocity_0_to_25xdmfDisplay.SelectScaleArray = 'None'
velocity_0_to_25xdmfDisplay.GlyphType = 'Arrow'
velocity_0_to_25xdmfDisplay.GlyphTableIndexArray = 'None'
velocity_0_to_25xdmfDisplay.GaussianRadius = 9.316600859165192e-05
velocity_0_to_25xdmfDisplay.SetScaleArray = ['POINTS', 'velocity_0_to_25']
velocity_0_to_25xdmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
velocity_0_to_25xdmfDisplay.OpacityArray = ['POINTS', 'velocity_0_to_25']
velocity_0_to_25xdmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
velocity_0_to_25xdmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
velocity_0_to_25xdmfDisplay.SelectionCellLabelFontFile = ''
velocity_0_to_25xdmfDisplay.SelectionPointLabelFontFile = ''
velocity_0_to_25xdmfDisplay.PolarAxes = 'PolarAxesRepresentation'
velocity_0_to_25xdmfDisplay.ScalarOpacityUnitDistance = 0.0005540626889628097

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
velocity_0_to_25xdmfDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.XTitleFontFile = ''
velocity_0_to_25xdmfDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.YTitleFontFile = ''
velocity_0_to_25xdmfDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.ZTitleFontFile = ''
velocity_0_to_25xdmfDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.XLabelFontFile = ''
velocity_0_to_25xdmfDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.YLabelFontFile = ''
velocity_0_to_25xdmfDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
velocity_0_to_25xdmfDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
velocity_0_to_25xdmfDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
velocity_0_to_25xdmfDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
velocity_0_to_25xdmfDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
velocity_0_to_25xdmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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

# trace defaults for the display properties.
gradientOfUnstructuredDataSet1Display.Representation = 'Surface'
gradientOfUnstructuredDataSet1Display.AmbientColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.ColorArrayName = [None, '']
gradientOfUnstructuredDataSet1Display.OSPRayScaleArray = 'Gradients'
gradientOfUnstructuredDataSet1Display.OSPRayScaleFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet1Display.SelectOrientationVectors = 'velocity_25_to_100000'
gradientOfUnstructuredDataSet1Display.ScaleFactor = 0.0018633201718330384
gradientOfUnstructuredDataSet1Display.SelectScaleArray = 'Gradients'
gradientOfUnstructuredDataSet1Display.GlyphType = 'Arrow'
gradientOfUnstructuredDataSet1Display.GlyphTableIndexArray = 'Gradients'
gradientOfUnstructuredDataSet1Display.GaussianRadius = 9.316600859165192e-05
gradientOfUnstructuredDataSet1Display.SetScaleArray = ['POINTS', 'Gradients']
gradientOfUnstructuredDataSet1Display.ScaleTransferFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet1Display.OpacityArray = ['POINTS', 'Gradients']
gradientOfUnstructuredDataSet1Display.OpacityTransferFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet1Display.DataAxesGrid = 'GridAxesRepresentation'
gradientOfUnstructuredDataSet1Display.SelectionCellLabelFontFile = ''
gradientOfUnstructuredDataSet1Display.SelectionPointLabelFontFile = ''
gradientOfUnstructuredDataSet1Display.PolarAxes = 'PolarAxesRepresentation'
gradientOfUnstructuredDataSet1Display.ScalarOpacityUnitDistance = 0.0005540626889628097

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
gradientOfUnstructuredDataSet1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.XTitleFontFile = ''
gradientOfUnstructuredDataSet1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.YTitleFontFile = ''
gradientOfUnstructuredDataSet1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.ZTitleFontFile = ''
gradientOfUnstructuredDataSet1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.XLabelFontFile = ''
gradientOfUnstructuredDataSet1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.YLabelFontFile = ''
gradientOfUnstructuredDataSet1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
gradientOfUnstructuredDataSet1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.PolarAxes.PolarAxisTitleFontFile = ''
gradientOfUnstructuredDataSet1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.PolarAxes.PolarAxisLabelFontFile = ''
gradientOfUnstructuredDataSet1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.PolarAxes.LastRadialAxisTextFontFile = ''
gradientOfUnstructuredDataSet1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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

# trace defaults for the display properties.
gradientOfUnstructuredDataSet2Display.Representation = 'Surface'
gradientOfUnstructuredDataSet2Display.AmbientColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.ColorArrayName = [None, '']
gradientOfUnstructuredDataSet2Display.OSPRayScaleArray = 'Gradients'
gradientOfUnstructuredDataSet2Display.OSPRayScaleFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet2Display.SelectOrientationVectors = 'velocity_0_to_25'
gradientOfUnstructuredDataSet2Display.ScaleFactor = 0.0018633201718330384
gradientOfUnstructuredDataSet2Display.SelectScaleArray = 'Gradients'
gradientOfUnstructuredDataSet2Display.GlyphType = 'Arrow'
gradientOfUnstructuredDataSet2Display.GlyphTableIndexArray = 'Gradients'
gradientOfUnstructuredDataSet2Display.GaussianRadius = 9.316600859165192e-05
gradientOfUnstructuredDataSet2Display.SetScaleArray = ['POINTS', 'Gradients']
gradientOfUnstructuredDataSet2Display.ScaleTransferFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet2Display.OpacityArray = ['POINTS', 'Gradients']
gradientOfUnstructuredDataSet2Display.OpacityTransferFunction = 'PiecewiseFunction'
gradientOfUnstructuredDataSet2Display.DataAxesGrid = 'GridAxesRepresentation'
gradientOfUnstructuredDataSet2Display.SelectionCellLabelFontFile = ''
gradientOfUnstructuredDataSet2Display.SelectionPointLabelFontFile = ''
gradientOfUnstructuredDataSet2Display.PolarAxes = 'PolarAxesRepresentation'
gradientOfUnstructuredDataSet2Display.ScalarOpacityUnitDistance = 0.0005540626889628097

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
gradientOfUnstructuredDataSet2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.XTitleFontFile = ''
gradientOfUnstructuredDataSet2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.YTitleFontFile = ''
gradientOfUnstructuredDataSet2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.ZTitleFontFile = ''
gradientOfUnstructuredDataSet2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.XLabelFontFile = ''
gradientOfUnstructuredDataSet2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.YLabelFontFile = ''
gradientOfUnstructuredDataSet2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
gradientOfUnstructuredDataSet2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.PolarAxes.PolarAxisTitleFontFile = ''
gradientOfUnstructuredDataSet2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.PolarAxes.PolarAxisLabelFontFile = ''
gradientOfUnstructuredDataSet2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.PolarAxes.LastRadialAxisTextFontFile = ''
gradientOfUnstructuredDataSet2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
gradientOfUnstructuredDataSet2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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

# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.AmbientColor = [0.0, 0.0, 0.0]
contour1Display.ColorArrayName = [None, '']
contour1Display.OSPRayScaleArray = 'Gradients'
contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
contour1Display.SelectOrientationVectors = 'velocity_25_to_100000'
contour1Display.ScaleFactor = 0.0008954927325248718
contour1Display.SelectScaleArray = 'Gradients'
contour1Display.GlyphType = 'Arrow'
contour1Display.GlyphTableIndexArray = 'Gradients'
contour1Display.GaussianRadius = 4.477463662624359e-05
contour1Display.SetScaleArray = ['POINTS', 'Gradients']
contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
contour1Display.OpacityArray = ['POINTS', 'Gradients']
contour1Display.OpacityTransferFunction = 'PiecewiseFunction'
contour1Display.DataAxesGrid = 'GridAxesRepresentation'
contour1Display.SelectionCellLabelFontFile = ''
contour1Display.SelectionPointLabelFontFile = ''
contour1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
contour1Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.XTitleFontFile = ''
contour1Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.YTitleFontFile = ''
contour1Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.ZTitleFontFile = ''
contour1Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.XLabelFontFile = ''
contour1Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.YLabelFontFile = ''
contour1Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
contour1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
contour1Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
contour1Display.PolarAxes.PolarAxisTitleFontFile = ''
contour1Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
contour1Display.PolarAxes.PolarAxisLabelFontFile = ''
contour1Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
contour1Display.PolarAxes.LastRadialAxisTextFontFile = ''
contour1Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
contour1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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

# trace defaults for the display properties.
contour2Display.Representation = 'Surface'
contour2Display.AmbientColor = [0.0, 0.0, 0.0]
contour2Display.ColorArrayName = [None, '']
contour2Display.OSPRayScaleArray = 'Gradients'
contour2Display.OSPRayScaleFunction = 'PiecewiseFunction'
contour2Display.SelectOrientationVectors = 'velocity_0_to_25'
contour2Display.ScaleFactor = 0.0009524233639240265
contour2Display.SelectScaleArray = 'Gradients'
contour2Display.GlyphType = 'Arrow'
contour2Display.GlyphTableIndexArray = 'Gradients'
contour2Display.GaussianRadius = 4.762116819620133e-05
contour2Display.SetScaleArray = ['POINTS', 'Gradients']
contour2Display.ScaleTransferFunction = 'PiecewiseFunction'
contour2Display.OpacityArray = ['POINTS', 'Gradients']
contour2Display.OpacityTransferFunction = 'PiecewiseFunction'
contour2Display.DataAxesGrid = 'GridAxesRepresentation'
contour2Display.SelectionCellLabelFontFile = ''
contour2Display.SelectionPointLabelFontFile = ''
contour2Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
contour2Display.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.XTitleFontFile = ''
contour2Display.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.YTitleFontFile = ''
contour2Display.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.ZTitleFontFile = ''
contour2Display.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.XLabelFontFile = ''
contour2Display.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.YLabelFontFile = ''
contour2Display.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
contour2Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
contour2Display.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
contour2Display.PolarAxes.PolarAxisTitleFontFile = ''
contour2Display.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
contour2Display.PolarAxes.PolarAxisLabelFontFile = ''
contour2Display.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
contour2Display.PolarAxes.LastRadialAxisTextFontFile = ''
contour2Display.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
contour2Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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

# trace defaults for the display properties.
velocity_25_to_100000xdmfDisplay.Representation = 'Surface'
velocity_25_to_100000xdmfDisplay.AmbientColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.ColorArrayName = [None, '']
velocity_25_to_100000xdmfDisplay.OSPRayScaleArray = 'velocity_25_to_100000'
velocity_25_to_100000xdmfDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
velocity_25_to_100000xdmfDisplay.SelectOrientationVectors = 'velocity_25_to_100000'
velocity_25_to_100000xdmfDisplay.ScaleFactor = 0.0018633201718330384
velocity_25_to_100000xdmfDisplay.SelectScaleArray = 'None'
velocity_25_to_100000xdmfDisplay.GlyphType = 'Arrow'
velocity_25_to_100000xdmfDisplay.GlyphTableIndexArray = 'None'
velocity_25_to_100000xdmfDisplay.GaussianRadius = 9.316600859165192e-05
velocity_25_to_100000xdmfDisplay.SetScaleArray = ['POINTS', 'velocity_25_to_100000']
velocity_25_to_100000xdmfDisplay.ScaleTransferFunction = 'PiecewiseFunction'
velocity_25_to_100000xdmfDisplay.OpacityArray = ['POINTS', 'velocity_25_to_100000']
velocity_25_to_100000xdmfDisplay.OpacityTransferFunction = 'PiecewiseFunction'
velocity_25_to_100000xdmfDisplay.DataAxesGrid = 'GridAxesRepresentation'
velocity_25_to_100000xdmfDisplay.SelectionCellLabelFontFile = ''
velocity_25_to_100000xdmfDisplay.SelectionPointLabelFontFile = ''
velocity_25_to_100000xdmfDisplay.PolarAxes = 'PolarAxesRepresentation'
velocity_25_to_100000xdmfDisplay.ScalarOpacityUnitDistance = 0.0005540626889628097

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
velocity_25_to_100000xdmfDisplay.DataAxesGrid.XTitleColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.XTitleFontFile = ''
velocity_25_to_100000xdmfDisplay.DataAxesGrid.YTitleColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.YTitleFontFile = ''
velocity_25_to_100000xdmfDisplay.DataAxesGrid.ZTitleColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.ZTitleFontFile = ''
velocity_25_to_100000xdmfDisplay.DataAxesGrid.GridColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.XLabelColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.XLabelFontFile = ''
velocity_25_to_100000xdmfDisplay.DataAxesGrid.YLabelColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.YLabelFontFile = ''
velocity_25_to_100000xdmfDisplay.DataAxesGrid.ZLabelColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
velocity_25_to_100000xdmfDisplay.PolarAxes.PolarAxisTitleColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.PolarAxes.PolarAxisTitleFontFile = ''
velocity_25_to_100000xdmfDisplay.PolarAxes.PolarAxisLabelColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.PolarAxes.PolarAxisLabelFontFile = ''
velocity_25_to_100000xdmfDisplay.PolarAxes.LastRadialAxisTextColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
velocity_25_to_100000xdmfDisplay.PolarAxes.SecondaryRadialAxesTextColor = [0.0, 0.0, 0.0]
velocity_25_to_100000xdmfDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on velocity_25_to_100000xdmfDisplay
velocity_25_to_100000xdmfDisplay.Opacity = 0.25

# current camera placement for renderView1
renderView1.CameraPosition = [0.09097052016472228, 0.11341196753724778, 0.040526392550608276]
renderView1.CameraFocalPoint = [0.10630261306373026, 0.1024034236935799, 0.06179516804102285]
renderView1.CameraViewUp = [0.8098148580479092, 0.48219890532327053, -0.3341917284881307]
renderView1.CameraParallelScale = 0.01303842390724087

# get layout
layout1 = GetLayout()

# save screenshot
SaveScreenshot('/run/user/1000/gvfs/sftp:host=niagara.scinet.utoronto.ca,user=dbruneau/scratch/s/steinman/dbruneau/7_0_Surgical/Pulsatile_Ramp_Cases/Case3_predeformed_finerflow/file_case3/1/Images/Case3_displacement_amplitude_hi_peak_sys_2e-..png', layout1, ImageResolution=[957, 799])

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.09097052016472228, 0.11341196753724778, 0.040526392550608276]
renderView1.CameraFocalPoint = [0.10630261306373026, 0.1024034236935799, 0.06179516804102285]
renderView1.CameraViewUp = [0.8098148580479092, 0.48219890532327053, -0.3341917284881307]
renderView1.CameraParallelScale = 0.01303842390724087

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).