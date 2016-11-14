# This program demonstrates how an OBJ object can be read from file

import sys
# load VTK
from vtk import *

# Read the teapot from file
object = vtkOBJReader()
object.SetFileName(sys.argv[1])

# Write to file!
#Data=vtkPolyDataWriter()
#Data.SetInput(object.GetOutput())
#Data.SetFileName(sys.argv[2])
#Data.Write()

  
objectMapper = vtkPolyDataMapper()
objectMapper.SetInputConnection(object.GetOutputPort())

objectActor=vtkActor()
objectActor.SetMapper(objectMapper)
objectActor.GetProperty().SetColor(0.2,0.6,0.6)

# Attach to a renderer
ren = vtkRenderer()
ren.AddActor(objectActor)
ren.SetBackground(0.6, 0.6, 0.7)

# Attach to a window
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Teapot")
renWin.SetSize(500,500)

# Attach to an interactor
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()


