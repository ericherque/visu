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
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'NetCDF Reader'
lecteurNC = NetCDFReader(FileName=[sys.argv[1]])
lecteurNC.Dimensions = '(latitude, longitude)'
lecteurNC.SphericalCoordinates = 0
lecteurNC.OutputType = 'Image'

# create a new 'Calculator'
conversionKelvinCelsius = Calculator(Input=lecteurNC)
conversionKelvinCelsius.ResultArrayName = 'TMPC_2maboveground'
conversionKelvinCelsius.Function = 'TMP_2maboveground-273.15'

# create a new 'Threshold'
seuillage = Threshold(Input=conversionKelvinCelsius)
seuillage.Scalars = ['POINTS', 'TMPC_2maboveground']
#seuillage.ThresholdRange = [-100., 100.0]
seuillage.LowerThreshold = -100.
seuillage.UpperThreshold = +100.

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get color transfer function/color map for 'TMPC2maboveground'
tMPC2mabovegroundLUT = GetColorTransferFunction('TMPC2maboveground')
# tMPC2mabovegroundLUT.RGBPoints = [-20., 0.231373, 0.298039, 0.752941, 6., 0.865003, 0.865003, 0.865003, 30.0, 0.705882, 0.0156863, 0.14902]
# TABLE DE COULEUR DISCONTINUE. UNE COULEUR CONSTANTE PAR PLAGE DE TEMPERATURE
tMPC2mabovegroundLUT.RGBPoints = [	-100.000, 0.0, 0.0, 1.0,
					-20.000, 0.0, 0.0, 1.0,

					-20.000, 0.0, 0.2, 1.0,
					-12.000, 0.0, 0.2,1.0,

					-12.000, 0.0, 0.44313725490196076,1.0,
					-3.000, 0.0, 0.44313725490196076,1.0,

					-3.000, 0.0, 0.7686274509803922, 1.0,
					3.000, 0.0, 0.7686274509803922, 1.0,

					3.000, 0.0, 1.0, 0.8313725490196079,
					7.000, 0.0, 1.0, 0.8313725490196079,

					7.000, 0.2196078431372549, 1.0, 0.0,
					18.000, 0.2196078431372549, 1.0, 0.0,

					18.000, 0.8941176470588236, 1.0, 0.0,
					24.000, 0.8941176470588236, 1.0, 0.0,

					24.000, 1.0, 0.5215686274509804, 0.0,
					30.000, 1.0, 0.5215686274509804, 0.0,

					30.000, 1.0, 0.0, 0.0,
					100.000, 1.0, 0.0, 0.0]
tMPC2mabovegroundLUT.ColorSpace = 'HSV'
tMPC2mabovegroundLUT.NumberOfTableValues = 1000
tMPC2mabovegroundLUT.ScalarRangeInitialized = 1.0


# get opacity transfer function/opacity map for 'TMPC2maboveground'
tMPC2mabovegroundPWF = GetOpacityTransferFunction('TMPC2maboveground')
tMPC2mabovegroundPWF.Points = [-20., 0.0, 0.5, 0.0, 30.0, 1.0, 0.5, 0.0]
tMPC2mabovegroundPWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from seuillage
seuillageDisplay = Show(seuillage, renderView1)
# trace defaults for the display properties.
seuillageDisplay.AmbientColor = [0.0, 0.0, 0.0]
seuillageDisplay.ColorArrayName = ['POINTS', 'TMPC_2maboveground']
seuillageDisplay.LookupTable = tMPC2mabovegroundLUT

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(seuillage)
# ----------------------------------------------------------------


# SAUVE UNE COPIE D ECRAN DANS UN FICHIER PNG
#WriteImage(sys.argv[1]+".png")
SaveScreenshot(sys.argv[1]+".png", viewOrLayout=renderView1, TransparentBackground=1) 


# REALISE LE ROGNAGE DES PARTIES EXTERNES PAR L UTILITAIRE convert D IMAGEMAGICK, QUI DOIT ETRE INSTALLE SUR L OS
# os.system('convert -trim -define png:color-type=6' + sys.argv[1]+".png " + sys.argv[1]+".png")

