#!/usr/bin/env python
#
# File:        protein.py
# Author:      Erik Vidholm <erik@cb.uu.se>
# Date:        2004-09-12
# Description: Rendering of an antibody volume via VTK's
#              ray casting function. To run this example,
#              type "vtkpython protein.py"

from vtk import *

# renderer, render window, and interactor
ren = vtkRenderer()
ren.SetBackground(0.188,0.373,0.647)
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(500,500)
renWin.SetWindowName("protein")

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# data reader
reader = vtkStructuredPointsReader()
reader.SetFileName("Protein.vtk")

# outline filter (bounding box)
outline = vtkOutlineFilter()
outline.SetInput( reader.GetOutput() )
outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInput( outline.GetOutput() )
outlineActor = vtkActor()
outlineActor.SetMapper( outlineMapper )
outlineActor.GetProperty().SetColor(.9,.9,.9)

# transfer function that maps scalar value to opacity
opacityTF = vtkPiecewiseFunction()
opacityTF.AddPoint(    0.0,  0.0 )
opacityTF.AddPoint(   20.0,  0.0 )
opacityTF.AddPoint(   80.0,  0.7 )
opacityTF.AddPoint(  200.0,  0.9 )
opacityTF.AddPoint(  250.0,  0.95)
opacityTF.AddPoint(  300.0,  1.0 )

# transfer functoin that maps scalar value to color
colorTF = vtkColorTransferFunction()
colorTF.AddRGBPoint( 20.0, 0.15, 0.4, 0.3)
colorTF.AddRGBPoint( 80.0, 0.15, 0.4, 0.3)
colorTF.AddRGBPoint(100.0, 0.3, 0.8, 0.0)
colorTF.AddRGBPoint(500.0, 0.3, 0.8, 0.0)

# property of the volume (lighting, transfer functions) 
volprop = vtkVolumeProperty()
volprop.SetColor(colorTF)
volprop.SetScalarOpacity(opacityTF)
volprop.ShadeOn()
volprop.SetInterpolationTypeToLinear()
volprop.SetSpecularPower(10.0)
volprop.SetSpecular(.7) 
volprop.SetAmbient(.5)
volprop.SetDiffuse(.5)

# mapper
# the composite function is the line integrator
compositeFunction = vtkVolumeRayCastCompositeFunction()
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction( compositeFunction )
volumeMapper.SetInput( reader.GetOutput() )
# sample distance along each ray
volumeMapper.SetSampleDistance(.2)

# volume is a specialized actor
volume = vtkVolume() 
volume.SetMapper(volumeMapper)
volume.SetProperty(volprop)

# add the actors
ren.AddVolume( volume )
ren.AddActor( outlineActor )

# render the window
renWin.Render()

iren.Initialize()
iren.Start()
