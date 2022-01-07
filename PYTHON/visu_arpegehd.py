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
tailleLongitudeAromeHD = 741 # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
tailleLatitudeAromeHD = 521
renderView1.ViewSize = [(int) (tailleLongitudeAromeHD*MonEchelle),(int) (tailleLatitudeAromeHD*MonEchelle)]

#---------------------------------------

minLatitude = 20  # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
maxLatitude = 72
minLongitude = -32.
maxLongitude = 42.

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
arpegehdnc = NetCDFReader(registrationName=sys.argv[1], FileName=[sys.argv[1]])
arpegehdnc.Dimensions = '(latitude, longitude)'
arpegehdnc.SphericalCoordinates = 0
arpegehdnc.ReplaceFillValueWithNan = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from arpegehdnc
arpegehdncDisplay = Show(arpegehdnc, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'TMP_2maboveground'
tMP_2mabovegroundLUT = GetColorTransferFunction('TMP_2maboveground')
tMP_2mabovegroundLUT.RGBPoints = [245.30157470703125, 0.231373, 0.298039, 0.752941, 272.58282470703125, 0.865003, 0.865003, 0.865003, 299.86407470703125, 0.705882, 0.0156863, 0.14902]
tMP_2mabovegroundLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'TMP_2maboveground'
tMP_2mabovegroundPWF = GetOpacityTransferFunction('TMP_2maboveground')
tMP_2mabovegroundPWF.Points = [245.30157470703125, 0.0, 0.5, 0.0, 299.86407470703125, 1.0, 0.5, 0.0]
tMP_2mabovegroundPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
arpegehdncDisplay.Representation = 'Slice'
arpegehdncDisplay.ColorArrayName = ['POINTS', 'TMP_2maboveground']
arpegehdncDisplay.LookupTable = tMP_2mabovegroundLUT
arpegehdncDisplay.SelectTCoordArray = 'None'
arpegehdncDisplay.SelectNormalArray = 'None'
arpegehdncDisplay.SelectTangentArray = 'None'
arpegehdncDisplay.OSPRayScaleArray = 'TMP_2maboveground'
arpegehdncDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
arpegehdncDisplay.SelectOrientationVectors = 'None'
arpegehdncDisplay.ScaleFactor = 7.400000000001683
arpegehdncDisplay.SelectScaleArray = 'None'
arpegehdncDisplay.GlyphType = 'Arrow'
arpegehdncDisplay.GlyphTableIndexArray = 'None'
arpegehdncDisplay.GaussianRadius = 0.37000000000008415
arpegehdncDisplay.SetScaleArray = ['POINTS', 'TMP_2maboveground']
arpegehdncDisplay.ScaleTransferFunction = 'PiecewiseFunction'
arpegehdncDisplay.OpacityArray = ['POINTS', 'TMP_2maboveground']
arpegehdncDisplay.OpacityTransferFunction = 'PiecewiseFunction'
arpegehdncDisplay.DataAxesGrid = 'GridAxesRepresentation'
arpegehdncDisplay.PolarAxes = 'PolarAxesRepresentation'
arpegehdncDisplay.ScalarOpacityUnitDistance = 1.2434594600066942
arpegehdncDisplay.ScalarOpacityFunction = tMP_2mabovegroundPWF
arpegehdncDisplay.OpacityArrayName = ['POINTS', 'TMP_2maboveground']
arpegehdncDisplay.SliceFunction = 'Plane'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
arpegehdncDisplay.ScaleTransferFunction.Points = [245.30157470703125, 0.0, 0.5, 0.0, 299.86407470703125, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
arpegehdncDisplay.OpacityTransferFunction.Points = [245.30157470703125, 0.0, 0.5, 0.0, 299.86407470703125, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
arpegehdncDisplay.SliceFunction.Origin = [5.000000000008413, 46.0, 0.0]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# restore active source
SetActiveSource(arpegehdnc)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
    # SAUVE UNE COPIE D ECRAN DANS UN FICHIER PNG
    #WriteImage(sys.argv[1]+".png")
    SaveScreenshot(sys.argv[1]+".png", viewOrLayout=renderView1, TransparentBackground=1) 