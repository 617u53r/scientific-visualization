# File:        ctscan.py
# Description: MPR rendering

import vtk

# image reader
filename1 = "ctscan_ez.vtk"
reader1 = vtk.vtkStructuredPointsReader()
reader1.SetFileName(filename1)
reader1.Update()

W, H, D = reader1.GetOutput().GetDimensions()
a1, b1 = reader1.GetOutput().GetScalarRange()
print "Range of image: %d--%d" % (a1, b1)

# Isosurface
isoSurface1 = vtk.vtkContourFilter()
isoSurface1.SetInputConnection(reader1.GetOutputPort())
isoSurface1.SetValue(-1024, 3071)
# isoSurface.SetValue(124)

surfaceMapper1 = vtk.vtkPolyDataMapper()
surfaceMapper1.SetInputConnection(isoSurface1.GetOutputPort())
surfaceMapper1.ScalarVisibilityOff()

surfaceActor1 = vtk.vtkActor()
surfaceActor1.SetMapper(surfaceMapper1)
surfaceActor1.GetProperty().SetColor(0.9, 0.7, 0.0)

filename2 = "ctscan_ez_bin.vtk"
reader2 = vtk.vtkStructuredPointsReader()
reader2.SetFileName(filename2)
reader2.Update()

a2, b2 = reader2.GetOutput().GetScalarRange()
print "Range of segmented image: %d--%d" % (a2, b2)

# Isosurface
isoSurface2 = vtk.vtkContourFilter()
isoSurface2.SetInputConnection(reader2.GetOutputPort())
isoSurface2.SetValue(0, 255)
# isoSurface.SetValue(124)

surfaceMapper2 = vtk.vtkPolyDataMapper()
surfaceMapper2.SetInputConnection(isoSurface2.GetOutputPort())
# surfaceMapper2.SetScalar(0, 255)
# surfaceMapper.ScalarVisibilityOff()

surfaceActor2 = vtk.vtkActor()
surfaceActor2.SetMapper(surfaceMapper2)
surfaceActor2.GetProperty().SetColor(0.3, 0.9, 0.3)

# Bounding box.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader2.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(outlineMapper)
outline.GetProperty().SetColor(0.5, 0.5, 0.5)

# Set a better camera position
# camera = vtk.vtkCamera()
# camera.SetViewUp(0, 0, -1)
# camera.SetPosition(-2, -2, -2)

# renderer and render window
ren = vtk.vtkRenderer()
ren.SetBackground(.2, .2, .2)
ren.AddActor(outline)
ren.AddActor(surfaceActor1)
ren.AddActor(surfaceActor2)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(512, 512)
renWin.AddRenderer(ren)

# render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# A cutplane
plane = vtk.vtkImagePlaneWidget()
plane.SetInputData(reader1.GetOutput())
plane.SetSliceIndex(40)
plane.SetInteractor(iren)
plane.DisplayTextOn()
plane.EnabledOn()

#
# add your code here for MPR and the liver surface
#
# Help to get started...
#
# picker=vtk.vtkCellPicker() # use same picker for all
# picker.SetTolerance(0.005)
#
# ipwx = vtk.vtkImagePlaneWidget()
# ipwx.SetPicker(picker)
# ipwx.SetInput(reader.GetOutput())
# ipwx.SetCurrentRenderer(ren)
# ipwx.SetInteractor(iren)
# ipwx.PlaceWidget()
# ipwx.SetPlaneOrientationToXAxes()
# ipwx.SetSliceIndex(W/2)
# ipwx.DisplayTextOn()
# ipwx.EnabledOn()

#

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputData(reader1.GetOutput())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputData(outline.GetOutput())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)

# the actors property defines color, shading, line width,...
outlineActor.GetProperty().SetColor(0.8, 0.8, 0.8)
outlineActor.GetProperty().SetLineWidth(2.0)

# add the actors
ren.AddActor(outlineActor)
renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInputData(w2if.GetOutput())

# Python function for the keyboard interface
# count is a screenshot counter
count = 0


def Keypress(obj, event):
    global count, iv
    key = obj.GetKeySym()
    if key == "s":
        renWin.Render()
        w2if.Modified()  # tell the w2if that it should update
        fnm = "screenshot%02d.png" % (count)
        wr.SetFileName(fnm)
        wr.Write()
        print "Saved '%s'" % (fnm)
        count = count + 1
        # add your keyboard interface here
        # elif key == ...


# add keyboard interface, initialize, and start the interactor
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
