# This program demonstrates how VTK can be used to render and interact with a Cylinder
# It also shows how the size of the window and the background color can be set

# load VTK
from vtk import *

# Create a Cylinder
cylinder = vtkCylinderSource()
cylinder.SetResolution(8)
cylinder.SetHeight(12)
cylinder.SetRadius(3)

# Create a Mapper
cylinderMapper = vtkPolyDataMapper()
cylinderMapper.SetInputConnection(cylinder.GetOutputPort())
cylinderActor = vtkActor()
cylinderActor.SetMapper(cylinderMapper)

# Create a renderer and assign the actor to the renderer
ren = vtkRenderer()
ren.AddActor(cylinderActor)

# Create the window and add the renderer
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)

# Set the name of the window
renWin.SetWindowName("Cylinder")

# Make sure that we can interact with the application 
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Initialze and start the application
iren.Initialize()
iren.Start()


