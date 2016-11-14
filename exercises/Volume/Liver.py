# A single cutplane

from vtk import *

# Read the volume images
reader = vtkStructuredPointsReader()
reader.SetFileName("liver.vtk")

# Create the Volume 
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.VisibilityOff()

# Bounding box.
outlineData = vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineData.GetOutputPort())
outline = vtkActor()
outline.SetMapper(outlineMapper)
outline.GetProperty().SetColor(0.5, 0.5, 0.5)

# Set a better camera position
camera = vtkCamera()
camera.SetViewUp(0, 0, -1)
camera.SetPosition(-2, -2, -2)

# Create the Renderer, Window and Interator
ren = vtkRenderer()
ren.AddActor(outline)
ren.AddVolume(volume)
ren.SetBackground(0.2, 0.2, 0.2)
ren.SetActiveCamera(camera)
ren.ResetCamera()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("A cutplane of a volume")
renWin.SetSize(500, 500);

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# A cutplane
plane=vtkImagePlaneWidget()
plane.SetInput(reader.GetOutput())
plane.SetSliceIndex(40)
plane.SetInteractor(iren)
plane.DisplayTextOn()
plane.EnabledOn()

iren.Initialize()
iren.Start()
