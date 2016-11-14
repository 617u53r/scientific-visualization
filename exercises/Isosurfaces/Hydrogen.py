# Interaction with an Isosurface visualization

from vtk import *

# A reader
reader = vtkStructuredPointsReader()
reader.SetFileName("Hydrogen.vtk")

# Create an outline of the dataset
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.0,0.0,1.0)

# Color lookup table
lut=vtkColorTransferFunction()
lut.AddRGBPoint(0,1,0,0)
lut.AddRGBPoint(0.5,1,1,0)
lut.AddRGBPoint(1,0,1,0)

# Define initial iso value 
isovalue=0.5

# The contour filter
isosurface = vtkContourFilter()
isosurface.SetInputConnection(reader.GetOutputPort())
isosurface.SetValue(0,isovalue)


isosurfaceMapper = vtkPolyDataMapper()
isosurfaceMapper.SetLookupTable(lut)
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())

isosurfaceActor = vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)


# Renderer and render window 
ren = vtkRenderer()
ren.SetBackground(.8, .8, .8)

# Add the actors
ren.AddActor(outlineActor)
ren.AddActor(isosurfaceActor)

renWin = vtkRenderWindow()
renWin.SetWindowName("Hydrogen Visualization")

renWin.SetSize(500, 500)
renWin.AddRenderer(ren)



# Python function for the keyboard interface

def Keypress(obj, event):
    global isovalue, renWin
    key = obj.GetKeySym()
    if key == "i":
        isovalue = isovalue + 0.01
        isosurface.SetValue(0,isovalue)
        renWin.Render()
    elif key == "o":
        isovalue = isovalue - 0.01
        isosurface.SetValue(0,isovalue)
        renWin.Render()
 
# add keyboard interface, initialize, and start the interactor

# Render window interactor
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
