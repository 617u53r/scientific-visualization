# Volume rendering of Liver data

from vtk import *

reader = vtkStructuredPointsReader()
reader.SetFileName("Liver.vtk")

MIP = vtkVolumeRayCastMIPFunction()
volumeMapper = vtkVolumeRayCastMapper()
volumeMapper.SetVolumeRayCastFunction(MIP)
volumeMapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volumeMapper)

# Create the Renderer, Window and Interator
ren = vtkRenderer()
ren.AddVolume(volume)
ren.SetBackground(0.1, 0.1, 0.2)

renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Volume rendering of Liver data");
renWin.SetSize(500, 500)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()

iren.Start()
