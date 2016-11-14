# Volume rendering of Liver data

isovalue=160.0

from vtk import *

reader = vtkStructuredPointsReader()
reader.SetFileName("liver.vtk")

# Color
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(20.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(120.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(180.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 1.0, 1.0)

volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)


volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

isoFunction = vtkVolumeRayCastIsosurfaceFunction()
isoFunction.SetIsoValue(isovalue)

volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(isoFunction )
volumeMapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
volume.VisibilityOn()

textActor = vtkTextActor()
tp = vtkTextProperty()
tp.SetColor(1.0,0.2,0.3)
tp.SetFontSize(30)
textActor.SetTextProperty(tp)
textActor.SetInput(str(isovalue))

# Bounding box.
outlineData = vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineData.GetOutputPort())
outline = vtkActor()
outline.SetMapper(outlineMapper)
outline.GetProperty().SetColor(0.9, 0.9, 0.9)

# Set a better camera position
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(-2, -2, -2)

# Create the Renderer, Window and Interator
ren = vtkRenderer()
ren.AddActor(outline)
ren.AddActor(textActor)
ren.AddVolume(volume)
ren.SetBackground(0.1, 0.1, 0.2)
ren.SetActiveCamera(camera)
ren.ResetCamera()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Volume rendering of Liver data");
renWin.SetSize(500, 500)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


def Keypress(obj, event):
    global isovalue, renWin
    key = obj.GetKeySym()
    if key == "i":
        isovalue = isovalue + 5.0
        isoFunction.SetIsoValue(isovalue)
        textActor.SetInput(str(isovalue))
        renWin.Render()
    elif key == "o":
        isovalue = isovalue - 5.0
        isoFunction.SetIsoValue(isovalue)
        textActor.SetInput(str(isovalue))
        renWin.Render()
  

iren.AddObserver("KeyPressEvent", Keypress)

iren.Initialize()


renWin.Render()
iren.Start()
