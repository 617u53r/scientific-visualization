# Volume rendering of Liver data

from vtk import *

reader = vtkStructuredPointsReader()
reader.SetFileName("liver.vtk")

# Opacity
opacityTransferFunction = vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(10, 0.3)
opacityTransferFunction.AddPoint(190, 0.7)
opacityTransferFunction.AddPoint(255, 1.0)

# Color
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(20.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(120.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(180.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 1.0, 1.0)

volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)

MIP = vtkVolumeRayCastMIPFunction()
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(MIP)
volumeMapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)


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
ren.AddVolume(volume)
ren.SetBackground(0.1, 0.1, 0.2)
ren.SetActiveCamera(camera)
ren.ResetCamera()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Vulume rendering of Liver data");
renWin.SetSize(500, 500)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)



iren.Initialize()
renWin.Render()
iren.Start()
