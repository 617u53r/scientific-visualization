# Iso-surface rendering of segmented liver data

from vtk import *

# Read the volume
reader = vtkStructuredPointsReader()
reader.SetFileName("liver.vtk")
#reader.SetFileName("segmented.vtk")

# Isosurface
isoSurface = vtkContourFilter()
isoSurface.SetInputConnection(reader.GetOutputPort())
isoSurface.SetValue(160)
#isoSurface.SetValue(124)

surfaceMapper = vtkPolyDataMapper()
surfaceMapper.SetInputConnection(isoSurface.GetOutputPort())
#surfaceMapper.ScalarVisibilityOff()

surfaceActor = vtkActor()
surfaceActor.SetMapper(surfaceMapper)
#surfaceActor.GetProperty().SetColor(0.9, 0.6,0.0)

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
ren.AddActor(surfaceActor)
ren.SetBackground(0.2, 0.2, 0.2)
ren.SetActiveCamera(camera)
ren.ResetCamera()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("An isosurface of a liver")
renWin.SetSize(500, 500);

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
