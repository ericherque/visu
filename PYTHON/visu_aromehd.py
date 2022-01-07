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
tailleLongitudeAromeHD = 2801 # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
tailleLatitudeAromeHD = 1791
renderView1.ViewSize = [(int) (tailleLongitudeAromeHD*MonEchelle),(int) (tailleLatitudeAromeHD*MonEchelle)]

#---------------------------------------

minLatitude = 37.5  # A ADAPTER A LA GRILLE DE DONNEES (Arome, AromeHD, Arpege, ArpegeHD)
maxLatitude = 55.4
minLongitude = -12.
maxLongitude = 16.

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
aromenc = NetCDFReader(registrationName=sys.argv[1], FileName=[sys.argv[1]])
# aromenc = NetCDFReader(registrationName='aromehd.nc', FileName=['/Users/erichrq/Cours/5A/projet_meteo/METEO_VISUALISATION/DATA/aromehd.nc'])
aromenc.Dimensions = '(latitude, longitude)'
aromenc.SphericalCoordinates = 0
aromenc.ReplaceFillValueWithNan = 1

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=aromenc)
threshold1.Scalars = ['POINTS', 'TMP_2maboveground']
threshold1.ThresholdRange = [246.971435546875, 294.422607421875]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from threshold1
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'TMP_2maboveground'
tMP_2mabovegroundLUT = GetColorTransferFunction('TMP_2maboveground')
tMP_2mabovegroundLUT.RGBPoints = [246.971435546875, 0.231373, 0.298039, 0.752941, 270.697021484375, 0.865003, 0.865003, 0.865003, 294.422607421875, 0.705882, 0.0156863, 0.14902]
tMP_2mabovegroundLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'TMP_2maboveground'
tMP_2mabovegroundPWF = GetOpacityTransferFunction('TMP_2maboveground')
tMP_2mabovegroundPWF.Points = [246.971435546875, 0.0, 0.5, 0.0, 294.422607421875, 1.0, 0.5, 0.0]
tMP_2mabovegroundPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
threshold1Display.Representation = 'Surface'
threshold1Display.ColorArrayName = ['POINTS', 'TMP_2maboveground']
threshold1Display.LookupTable = tMP_2mabovegroundLUT
threshold1Display.SelectTCoordArray = 'None'
threshold1Display.SelectNormalArray = 'None'
threshold1Display.SelectTangentArray = 'None'
threshold1Display.OSPRayScaleArray = 'TMP_2maboveground'
threshold1Display.OSPRayScaleFunction = 'PiecewiseFunction'
threshold1Display.SelectOrientationVectors = 'None'
threshold1Display.ScaleFactor = 2.8000000000000003
threshold1Display.SelectScaleArray = 'None'
threshold1Display.GlyphType = 'Arrow'
threshold1Display.GlyphTableIndexArray = 'None'
threshold1Display.GaussianRadius = 0.14
threshold1Display.SetScaleArray = ['POINTS', 'TMP_2maboveground']
threshold1Display.ScaleTransferFunction = 'PiecewiseFunction'
threshold1Display.OpacityArray = ['POINTS', 'TMP_2maboveground']
threshold1Display.OpacityTransferFunction = 'PiecewiseFunction'
threshold1Display.DataAxesGrid = 'GridAxesRepresentation'
threshold1Display.PolarAxes = 'PolarAxesRepresentation'
threshold1Display.ScalarOpacityFunction = tMP_2mabovegroundPWF
threshold1Display.ScalarOpacityUnitDistance = 0.2066683415028735
threshold1Display.OpacityArrayName = ['POINTS', 'TMP_2maboveground']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
threshold1Display.ScaleTransferFunction.Points = [246.971435546875, 0.0, 0.5, 0.0, 294.422607421875, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
threshold1Display.OpacityTransferFunction.Points = [246.971435546875, 0.0, 0.5, 0.0, 294.422607421875, 1.0, 0.5, 0.0]

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# restore active source
SetActiveSource(threshold1)
# ----------------------------------------------------------------


if __name__ == '__main__':
    # generate extracts
    SaveExtracts(ExtractsOutputDirectory='extracts')
    # SAUVE UNE COPIE D ECRAN DANS UN FICHIER PNG
    #WriteImage(sys.argv[1]+".png")
    SaveScreenshot(sys.argv[1]+".png", viewOrLayout=renderView1, TransparentBackground=1) 