import sys
import os

# state file generated using paraview version 5.1.2

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
#renderView1.UseOffscreenRendering = True
#renderView1.UseOffscreenRenderingForScreenshots = True
MonEchelle = 0.5 # REGLAGE DE LA TAILLE DE L IMAGE FINALE
tailleLongitudeAromeHD = 801 # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
tailleLatitudeAromeHD = 601
renderView1.ViewSize = [(int) (tailleLongitudeAromeHD*MonEchelle),(int) (tailleLatitudeAromeHD*MonEchelle)]

#---------------------------------------

minLatitude = 38 # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
maxLatitude = 53
minLongitude = -8.
maxLongitude = 12.

#---------------------------------------

centreLongitude=(minLongitude + maxLongitude) / 2.
centreLatitude=(minLatitude + maxLatitude) / 2.

renderView1.InteractionMode = '2D'
renderView1.OrientationAxesVisibility = 0

#renderView1.CenterOfRotation = [2., 46.45, 0.0]
#renderView1.CameraPosition = [2., 46.45, 60.]
#renderView1.CameraFocalPoint = [2., 46.45, 0.0]

renderView1.CenterOfRotation = [centreLongitude, centreLatitude, 0.0]
renderView1.CameraPosition   = [centreLongitude, centreLatitude, 60.]
renderView1.CameraFocalPoint = [centreLongitude, centreLatitude, 0.0]

#renderView1.CameraParallelScale = 9.
renderView1.CameraParallelScale =  centreLatitude - minLatitude

renderView1.CameraParallelProjection = 1
renderView1.Background = [1.0, 1.0, 1.0]

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# get the material library
materialLibrary1 = GetMaterialLibrary()

SetActiveView(None)

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
#layout1.SetSize(2152, 1078)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'NetCDF Reader'
aromenc = NetCDFReader(registrationName='arome.nc', FileName=[sys.argv[1]])
aromenc.Dimensions = '(latitude, longitude)'
aromenc.SphericalCoordinates = 0
aromenc.ReplaceFillValueWithNan = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from aromenc
aromencDisplay = Show(aromenc, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'TMP_2maboveground'
tMP_2mabovegroundLUT = GetColorTransferFunction('TMP_2maboveground')
tMP_2mabovegroundLUT.RGBPoints = [250.29733276367188, 0.231373, 0.298039, 0.752941, 269.9838562011719, 0.865003, 0.865003, 0.865003, 289.6703796386719, 0.705882, 0.0156863, 0.14902]
tMP_2mabovegroundLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'TMP_2maboveground'
tMP_2mabovegroundPWF = GetOpacityTransferFunction('TMP_2maboveground')
tMP_2mabovegroundPWF.Points = [250.29733276367188, 0.0, 0.5, 0.0, 289.6703796386719, 1.0, 0.5, 0.0]
tMP_2mabovegroundPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
aromencDisplay.Representation = 'Slice'
aromencDisplay.ColorArrayName = ['POINTS', 'TMP_2maboveground']
aromencDisplay.LookupTable = tMP_2mabovegroundLUT
aromencDisplay.SelectTCoordArray = 'None'
aromencDisplay.SelectNormalArray = 'None'
aromencDisplay.SelectTangentArray = 'None'
aromencDisplay.OSPRayScaleArray = 'TMP_2maboveground'
aromencDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
aromencDisplay.SelectOrientationVectors = 'None'
aromencDisplay.ScaleFactor = 1.999999999998181
aromencDisplay.SelectScaleArray = 'None'
aromencDisplay.GlyphType = 'Arrow'
aromencDisplay.GlyphTableIndexArray = 'None'
aromencDisplay.GaussianRadius = 0.09999999999990905
aromencDisplay.SetScaleArray = ['POINTS', 'TMP_2maboveground']
aromencDisplay.ScaleTransferFunction = 'PiecewiseFunction'
aromencDisplay.OpacityArray = ['POINTS', 'TMP_2maboveground']
aromencDisplay.OpacityTransferFunction = 'PiecewiseFunction'
aromencDisplay.DataAxesGrid = 'GridAxesRepresentation'
aromencDisplay.PolarAxes = 'PolarAxesRepresentation'
aromencDisplay.ScalarOpacityUnitDistance = 0.31929559683046127
aromencDisplay.ScalarOpacityFunction = tMP_2mabovegroundPWF
aromencDisplay.OpacityArrayName = ['POINTS', 'TMP_2maboveground']
aromencDisplay.SliceFunction = 'Plane'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
aromencDisplay.ScaleTransferFunction.Points = [250.29733276367188, 0.0, 0.5, 0.0, 289.6703796386719, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
aromencDisplay.OpacityTransferFunction.Points = [250.29733276367188, 0.0, 0.5, 0.0, 289.6703796386719, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
aromencDisplay.SliceFunction.Origin = [1.999999999990905, 45.5, 0.0]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# restore active source
SetActiveSource(aromenc)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
    # SAUVE UNE COPIE D ECRAN DANS UN FICHIER PNG
    #WriteImage(sys.argv[1]+".png")
    SaveScreenshot(sys.argv[1]+".png", viewOrLayout=renderView1, TransparentBackground=1) 