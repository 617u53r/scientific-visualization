# Iso-surface rendering of two data sets combined

from vtk import *

# Read the volume
reader1 = vtkStructuredPointsReader()
reader1.SetFileName("liver.vtk")

reader2 = vtkStructuredPointsReader()
reader2.SetFileName("segmented.vtk")


# Isosurface
isoSurface1 = vtkContourFilter()
isoSurface1.SetInputConnection(reader1.GetOutputPort())
isoSurface1.SetValue(0,140)

surfaceMapper1 = vtkPolyDataMapper()
surfaceMapper1.SetInputConnection(isoSurface1.GetOutputPort())
surfaceMapper1.ScalarVisibilityOff()

surfaceActor1 = vtkActor()
surfaceActor1.SetMapper(surfaceMapper1)
surfaceActor1.GetProperty().SetColor(0.9, 0.7,0.0)


# Isosurface
isoSurface2 = vtkContourFilter()
isoSurface2.SetInputConnection(reader2.GetOutputPort())
isoSurface2.SetValue(0,124)

surfaceMapper2 = vtkPolyDataMapper()
surfaceMapper2.SetInputConnection(isoSurface2.GetOutputPort())
surfaceMapper2.ScalarVisibilityOff()

surfaceActor2 = vtkActor()
surfaceActor2.SetMapper(surfaceMapper2)
surfaceActor2.GetProperty().SetColor(0.9, 0.3,0.3)


# Bounding box.
outlineData = vtkOutlineFilter()
outlineData.SetInputConnection(reader1.GetOutputPort())
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
ren.AddActor(surfaceActor1)
ren.AddActor(surfaceActor2)


ren.SetBackground(0.1, 0.1, 0.2)
ren.SetActiveCamera(camera)
ren.ResetCamera()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Combination of two data sets")
renWin.SetSize(500, 500);

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
