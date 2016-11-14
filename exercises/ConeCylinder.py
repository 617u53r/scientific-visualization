# This program demonstrates how different objects can be rendered in the same time,
# and how attributes like size and color can be changed

# load VTK
from vtk import *

# Create a Cylinder, giving size, resolution and color
cylinder = vtkCylinderSource()
cylinder.SetResolution(8)
cylinder.SetHeight(4)
cylinder.SetRadius(4)

cylinderMapper = vtkPolyDataMapper()
cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

cylinderActor = vtkActor()
cylinderActor.SetMapper(cylinderMapper)
cylinderActor.GetProperty().SetColor(0.0,1.0,1.0)

# Create a Cone, giving size, resolution, position and color
cone = vtkConeSource()
cone.SetResolution(12)
cone.SetHeight(12)
cone.SetRadius(3)
cone.SetCenter(5,0,0)

coneMapper = vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())

coneActor = vtkActor()
coneActor.SetMapper(coneMapper)
coneActor.GetProperty().SetColor(1.0,0.0,1.0)

# Create a renderer and assign the actors to the renderer
ren = vtkRenderer()
ren.AddActor(cylinderActor)
ren.AddActor(coneActor)
ren.SetBackground(0.6, 0.6, 0.7)

# Create the window and set the name and size of the window
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Cone & Cylinder")
renWin.SetSize(500,500)

# Make sure that we can interact with the application 
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Initialze and start the application
iren.Initialize()
iren.Start()


