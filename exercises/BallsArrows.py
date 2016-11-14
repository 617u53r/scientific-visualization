# Visualizing vector data from Matlab
# One file "data1.txt" contains the position and the other "data2.txt" contains a vector

import sys
from vtk import *

# This import style makes it possible to write just readPoints() in the call instead of using the whole name: Readpoints.readPoints()
from ReadPoints import *

# Read the data into a vtkUnstructedGrid using the functions in ReadPoints.py
data=vtkUnstructuredGrid()

# Read arguments
data.SetPoints(readPoints(sys.argv[1]))
data.GetPointData().SetVectors(readVectors(sys.argv[2]))

# Put spheres at each point in the dataset.
ball = vtkSphereSource()
ball.SetRadius(0.05)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

ballGlyph = vtkGlyph3D()
ballGlyph.SetInputData(data)
ballGlyph.SetSourceConnection(ball.GetOutputPort())

ballMapper = vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())

ballActor = vtkActor()
ballActor.SetMapper(ballMapper)
ballActor.GetProperty().SetColor(0.8,0.4,0.4)

#Put an arrow (vector) at each ball
arrow = vtkArrowSource()
arrow.SetTipRadius(0.2)
arrow.SetShaftRadius(0.075)

arrowGlyph = vtkGlyph3D()
arrowGlyph.SetInputData(data)
arrowGlyph.SetSourceConnection(arrow.GetOutputPort())
arrowGlyph.SetScaleFactor(0.2)

arrowMapper = vtkPolyDataMapper()
arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())

arrowActor = vtkActor()
arrowActor.SetMapper(arrowMapper)
arrowActor.GetProperty().SetColor(0.9,0.9,0.1)

# Create the RenderWindow, Renderer and Interator
ren = vtkRenderer()
ren.AddActor(ballActor)
ren.AddActor(arrowActor)
ren.SetBackground(0.4, 0.4, 0.6)

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Balls and Arrows")
renWin.SetSize(500,500)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
