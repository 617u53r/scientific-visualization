from vtk import *
from array import *
import math
import time

class kbrdInteraction(object):
    def __init__(self):
        self.secs = None
        self.minT = 0.0
        self.maxT = None
        self.currT = 0.0
        self.thresholdfltr = None
        self.renWin = None
        self.wndw2imgfltr = None
        self.pngwrtr = None
    def keypress(self, obj, event):
        key = obj.GetKeySym()
        if key == "a":
            self.currT = self.minT
        while self.currT < self.maxT:
            self.thresholdfltr.ThresholdBetween(self.minT, self.currT)
            self.currT += 1500
            if self.currT > self.maxT:
                break
            self.renWin.Render()
            self.wndw2imgfltr.Update()

def span(lat1, lon1, lat2, lon2):
    a = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    b = math.sin(dLat / 2.0) * math.sin(dLat / 2.0) + math.sin(dLon / 2.0) * math.sin(dLon / 2.0) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(b), math.sqrt(1 - b))
    d = a * c
    return d

#Reading and parsing the data downloaded from the website
data = list()
f = open('events3.csv')
for line in f:
    if line[0] == '#':
        continue
    line = line.strip()[0:-1].split(';')
    timestmp = int(time.mktime(time.strptime(line[0], '%Y-%m-%d %H:%M:%S.%f')))
    Xlat, Ylong, Zdep = ([float(x) for x in line[1:4]])
    magn = float(line[4].split('--')[0])
    src = line[5]
    data.append([timestmp, Xlat, Ylong, Zdep, magn, src])
f.close()

#Creating VTK objects from the parsed data for rendering
points = vtk.vtkPoints()
magn = vtk.vtkFloatArray()
secs = vtk.vtkFloatArray()
maxLat = 0
maxLong = 0
minLat = 360
minLong = 360
for point in data:
    t, x, y, z, r = (point[:-1])
    if x > maxLat:
        maxLat = x
    if x < minLat:
        minLat = x
    if y > maxLong:
        maxLong = y
    if y < minLong:
        minLong = y
    minFltrdStrngth = 2.5
    if r > minFltrdStrngth:
        points.InsertNextPoint(x, y, z)
        magn.InsertNextValue(r)
        secs.InsertNextValue(t / 1000.)
x1 = span(minLat, minLong, maxLat, minLong)
x2 = span(minLat, maxLong, maxLat, maxLong)
y1 = span(minLat, minLong, minLat, maxLong)
y2 = span(maxLat, minLong, maxLat, maxLong)
n = points.GetNumberOfPoints()
i = 0
while i < n:
    x, y, z = points.GetPoint(i)
    x4=(x-minLat)/(maxLat-minLat)
    x=(x-minLat)/(maxLat-minLat)*x1
    yy=(1-x4)*y1+x4*y2
    y=(y-minLong)/(maxLong-minLong)*yy
    points.SetPoint(i, x, y, z)
    i=i+1
minX, maxX, minY, maxY, minZ, maxZ = points.GetBounds()
minT, maxT = secs.GetRange()

picture = vtk.vtkPNGReader()
picture.SetFileName("staticmap.png")
texture = vtk.vtkTexture()
texture.SetInputConnection(picture.GetOutputPort())
mapItaly = vtk.vtkPlaneSource()
mapItaly.SetOrigin(minX, minY, minZ)
mapItaly.SetPoint1(minX, maxY, minZ)
mapItaly.SetPoint2(maxX, minY, minZ)
mapItaly.SetXResolution(3)
mapItaly.SetYResolution(3)
mapItalyMapper = vtk.vtkPolyDataMapper()
mapItalyMapper.SetInputConnection(mapItaly.GetOutputPort())
mapItalyActor = vtk.vtkActor()
mapItalyActor.SetMapper(mapItalyMapper)
mapItalyActor.SetTexture(texture)
mapItalyActor.SetPosition(1, 1, -50)
mapItalyActor.GetProperty().SetOpacity(0.4)

transform = vtk.vtkTransform()
axes = vtk.vtkAxesActor()
axes.SetUserTransform(transform)
axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(1.0, 0.0, 0.0)
axes.GetXAxisShaftProperty().SetColor(1.0, 0.0, 0.0)
axes.GetXAxisTipProperty().SetColor(1.0, 0.0, 0.0)
axes.SetXAxisLabelText("X")
axes.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.5)
axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(10)
axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0, 1.0, 0.0)
axes.GetYAxisShaftProperty().SetColor(0.0, 1.0, 0.0)
axes.GetYAxisTipProperty().SetColor(0.0, 1.0, 0.0)
axes.SetYAxisLabelText("Y")
axes.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.5)
axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(10)
axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetColor(0.0, 0.0, 1.0)
axes.GetZAxisShaftProperty().SetColor(0.0, 0.0, 1.0)
axes.GetXAxisTipProperty().SetColor(0.0, 0.0, 1.0)
axes.SetZAxisLabelText("Z")
axes.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleMode(0.5)
axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().SetFontSize(10)
axes.SetNormalizedShaftLength(150.0, 150.0, 150.0)

title = vtk.vtkTextMapper()
title.SetInput("SeSe Visualization Project")
tp = title.GetTextProperty()
tp.SetFontSize(50)
tp.SetColor(0.0, 0.0, 0.0)
titleActor = vtk.vtkActor2D()
titleActor.SetMapper(title)
titleActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
titleActor.GetPositionCoordinate().SetValue(0.2, 0.9)

text = vtk.vtkTextMapper()
text.SetInput("Rotate the map.\nZoom in/out with a mouse.\n Press A for animation.")
tp = text.GetTextProperty()
tp.SetFontSize(10)
tp.SetColor(0.0, 0.0, 0.0)
tp.SetJustificationToCentered()
textActor = vtk.vtkActor2D()
textActor.SetMapper(text)
textActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
textActor.GetPositionCoordinate().SetValue(0.5, 0.01)

magn.SetName("Magnitude")
secs.SetName("Time")
points_polydata = vtk.vtkPolyData()
points_polydata.SetPoints(points)
points_polydata.GetPointData().AddArray(magn)
points_polydata.GetPointData().AddArray(secs)
points_polydata.GetPointData().SetActiveScalars("Magnitude")
thresholdfltr = vtk.vtkThresholdPoints()
thresholdfltr.SetInput(points_polydata)
minFltrdStrngth = 3
maxFltrdStrngth = 6
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(minFltrdStrngth, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(minFltrdStrngth + 0.2, 255.0 / 255.0, 153.0 / 255.0, 51.0 / 255.0)
colorTransferFunction.AddRGBPoint(minFltrdStrngth + 1.0, 255.0 / 255.0, 0, 0)
colorTransferFunction.AddRGBPoint(minFltrdStrngth + 1.5, 100.0 / 255.0, 0, 100.0 / 255.0)
colorTransferFunction.AddRGBPoint(maxFltrdStrngth - 1.0, 100.0 / 255.0, 0, 200.0 / 255.0)
colorTransferFunction.AddRGBPoint(maxFltrdStrngth, 90.0 / 255.0, 0, 210.0 / 255.0)

colorBar = vtk.vtkScalarBarActor()
colorBar.SetLookupTable(colorTransferFunction)
colorBar.SetPosition(0.87, 0.17)
colorBar.SetWidth(0.09)
tp = vtk.vtkTextProperty()
tp.SetColor(0,0,0)
colorBar.SetLabelTextProperty(tp)

sphere = vtk.vtkSphereSource()
glyph = vtk.vtkGlyph3D()
glyph.SetInput(thresholdfltr.GetOutput())
glyph.SetSource(sphere.GetOutput())
glyph.ScalingOn()
glyph.SetScaleFactor(6.0)
glyph.SetScaleModeToScaleByScalar()
glyph.SetColorModeToColorByScalar()
glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputConnection(glyph.GetOutputPort())
glyphMapper.SetLookupTable(colorTransferFunction)
glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)

camera = vtk.vtkCamera()
camera.SetFocalPoint((maxX-minX)/2,(maxY-minY)/2,minZ)
camera.SetPosition((maxX-minX)/2,(maxY-minY)/2,-700)
camera.Zoom(0.3)

#Rendering the objects
ren = vtk.vtkRenderer()
ren.SetBackground(1,1,1)
ren.AddActor(titleActor)
ren.AddActor(textActor)
ren.AddActor(mapItalyActor)
ren.AddActor(axes)
ren.AddActor(colorBar)
ren.AddActor(glyphActor)
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1000, 1000)
renWin.AddRenderer(ren)
ren.SetActiveCamera(camera)
wndw2imgfltr = vtk.vtkWindowToImageFilter()
wndw2imgfltr.SetInput(renWin)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)
keyboard_interface = kbrdInteraction()
keyboard_interface.renWin = renWin
keyboard_interface.wndw2imgfltr = wndw2imgfltr
thresholdfltr.SetInputArrayToProcess(0, 0, 0, 0, "Time")
keyboard_interface.thresholdfltr = thresholdfltr
keyboard_interface.minT = minT
keyboard_interface.maxT = maxT
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)
interactor.Initialize()
interactor.Start()
