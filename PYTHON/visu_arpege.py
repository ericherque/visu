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
tailleLongitudeAromeHD = 721 # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
tailleLatitudeAromeHD = 361
renderView1.ViewSize = [(int) (tailleLongitudeAromeHD*MonEchelle),(int) (tailleLatitudeAromeHD*MonEchelle)]

#---------------------------------------

minLatitude = -90  # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
maxLatitude = 90
minLongitude = 0.
maxLongitude = 360.

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

# ----------------------------------------------------------------
# setup view layouts
# ----------------------------------------------------------------

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.AssignView(0, renderView1)
layout1.SetSize(2152, 1078)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'NetCDF Reader'
arpegenc = NetCDFReader(registrationName='arpege.nc', FileName=[sys.argv[1]])
arpegenc.Dimensions = '(latitude, longitude)'
arpegenc.SphericalCoordinates = 0
arpegenc.ReplaceFillValueWithNan = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from arpegenc
arpegencDisplay = Show(arpegenc, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'TMP_2maboveground'
tMP_2mabovegroundLUT = GetColorTransferFunction('TMP_2maboveground')
tMP_2mabovegroundLUT.RGBPoints = [221.6695098876953, 0.231373, 0.298039, 0.752941, 269.5445022583008, 0.865003, 0.865003, 0.865003, 317.41949462890625, 0.705882, 0.0156863, 0.14902]
tMP_2mabovegroundLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'TMP_2maboveground'
tMP_2mabovegroundPWF = GetOpacityTransferFunction('TMP_2maboveground')
tMP_2mabovegroundPWF.Points = [221.6695098876953, 0.0, 0.5, 0.0, 317.41949462890625, 1.0, 0.5, 0.0]
tMP_2mabovegroundPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
arpegencDisplay.Representation = 'Slice'
arpegencDisplay.ColorArrayName = ['POINTS', 'TMP_2maboveground']
arpegencDisplay.LookupTable = tMP_2mabovegroundLUT
arpegencDisplay.SelectTCoordArray = 'None'
arpegencDisplay.SelectNormalArray = 'None'
arpegencDisplay.SelectTangentArray = 'None'
arpegencDisplay.OSPRayScaleArray = 'TMP_2maboveground'
arpegencDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
arpegencDisplay.SelectOrientationVectors = 'None'
arpegencDisplay.ScaleFactor = 35.95
arpegencDisplay.SelectScaleArray = 'None'
arpegencDisplay.GlyphType = 'Arrow'
arpegencDisplay.GlyphTableIndexArray = 'None'
arpegencDisplay.GaussianRadius = 1.7975
arpegencDisplay.SetScaleArray = ['POINTS', 'TMP_2maboveground']
arpegencDisplay.ScaleTransferFunction = 'PiecewiseFunction'
arpegencDisplay.OpacityArray = ['POINTS', 'TMP_2maboveground']
arpegencDisplay.OpacityTransferFunction = 'PiecewiseFunction'
arpegencDisplay.DataAxesGrid = 'GridAxesRepresentation'
arpegencDisplay.PolarAxes = 'PolarAxesRepresentation'
arpegencDisplay.ScalarOpacityUnitDistance = 6.308570484063421
arpegencDisplay.ScalarOpacityFunction = tMP_2mabovegroundPWF
arpegencDisplay.OpacityArrayName = ['POINTS', 'TMP_2maboveground']
arpegencDisplay.SliceFunction = 'Plane'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
arpegencDisplay.ScaleTransferFunction.Points = [221.6695098876953, 0.0, 0.5, 0.0, 317.41949462890625, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
arpegencDisplay.OpacityTransferFunction.Points = [221.6695098876953, 0.0, 0.5, 0.0, 317.41949462890625, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
arpegencDisplay.SliceFunction.Origin = [179.75, 0.0, 0.0]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# restore active source
SetActiveSource(arpegenc)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
    # SAUVE UNE COPIE D ECRAN DANS UN FICHIER PNG
    #WriteImage(sys.argv[1]+".png")
    SaveScreenshot(sys.argv[1]+".png", viewOrLayout=renderView1, TransparentBackground=1) 