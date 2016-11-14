# Volume renderer
from vtk import *

reader = vtkStructuredPointsReader()
reader.SetFileName("liver.vtk")

# Opacity
opacityTransferFunction = vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(   120.0,  0.0 )
opacityTransferFunction.AddPoint(   150.0,  0.1 )
opacityTransferFunction.AddPoint(   200.0,  0.9 )
opacityTransferFunction.AddPoint(  255.0,  0.0 )

# Colour
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint( 0.0,  1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint( 60.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint( 120.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint( 180.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint( 240.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint( 300.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint( 360.0, 1.0, 0.0, 0.0)


# Properties
volprop = vtkVolumeProperty()
volprop.SetColor(colorTransferFunction)
volprop.SetScalarOpacity(opacityTransferFunction)
volprop.ShadeOn() # try this one!


# Mapper
compositeFunction = vtkVolumeRayCastCompositeFunction()
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(compositeFunction )
volumeMapper.SetInputConnection(reader.GetOutputPort() )

# Sample distance along each ray
volumeMapper.SetSampleDistance(.5)

# Set the volume
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volprop)

# renderer, render window, and interactor
ren = vtkRenderer()
ren.SetBackground(1.0,1.0,1.0)
ren.AddVolume(volume)

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Volume rendering of Liver data");
renWin.SetSize(500, 500)


iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Without this line the volume is black in the first image.
renWin.Render()

iren.Initialize()
iren.Start()
