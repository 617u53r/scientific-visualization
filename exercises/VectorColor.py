# Visualizing vector data
# Read data from a vtk file

import sys
from vtk import *

# Use the VTK reader to read the vtk file
reader = vtkUnstructuredGridReader()

# Don't forget to give the file name as an argument: "python Vectors.py data.vtk"
reader.SetFileName(sys.argv[1])

# Create a color transfer function to be used for both the balls and arrows.
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(5.0 , 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(10.0, 0.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(15.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(20.0, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(25.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(30.0, 1.0, 0.0, 1.0)

# Put spheres at each point in the dataset.
ball = vtkSphereSource()
ball.SetRadius(0.12)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)

ballGlyph = vtkGlyph3D()
ballGlyph.SetSourceConnection(ball.GetOutputPort())
ballGlyph.SetInputConnection(reader.GetOutputPort())

# We do not want the Ball to have the size depending on the Scalar
ballGlyph.SetScaleModeToDataScalingOff()

ballMapper = vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())

# Set colors depending on the color transfer functions
ballMapper.SetLookupTable(colorTransferFunction)

ballActor = vtkActor()
ballActor.SetMapper(ballMapper)

#Put an arrow (vector) at each ball
arrow = vtkArrowSource()
arrow.SetTipRadius(0.2)
arrow.SetShaftRadius(0.075)

arrowGlyph = vtkGlyph3D()
arrowGlyph.SetInputConnection(reader.GetOutputPort())
arrowGlyph.SetSourceConnection(arrow.GetOutputPort())
arrowGlyph.SetScaleFactor(0.4)

# We do not want the Arrow's size to depend on the Scalar
arrowGlyph.SetScaleModeToDataScalingOff()

arrowMapper = vtkPolyDataMapper()
arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())

# Set colors depending on the color transfer functions
arrowMapper.SetLookupTable(colorTransferFunction)

arrowActor = vtkActor()
arrowActor.SetMapper(arrowMapper)

# Create the RenderWindow,Renderer and Interator
ren = vtkRenderer()
ren.AddActor(ballActor)
ren.AddActor(arrowActor)
ren.SetBackground(0.2, 0.2, 0.3)

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Balls and Arrows from a VTK file")
renWin.SetSize(600,600)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
