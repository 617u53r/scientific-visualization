# Interaction with an Isosurface visualization
# as well as screenshots
# Original program written by Erik Vidholm 2004-09-13 and then rewritten by Anders Hast

import vtk

# image reader
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("hydrogen.vtk")

# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.0,0.0,1.0)
outlineActor.GetProperty().SetLineWidth(2.0)

# color lookup table (an alternative is vtkLookUpTable)
lut=vtk.vtkColorTransferFunction()
lut.AddRGBPoint(0,1,0,0)
lut.AddRGBPoint(0.5,1,1,0)
lut.AddRGBPoint(1,0,1,0)

# Define initial iso value 
isovalue=0.5

# The contour filter
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(reader.GetOutputPort())
isosurface.SetValue(0,isovalue)

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetLookupTable(lut)
isosurfaceMapper.SetScalarRange(0.0, 1.0)
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)

# A colorbar
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(isosurfaceMapper.GetLookupTable())
scalarBar.SetTitle("Probability")
scalarBar.GetLabelTextProperty().SetColor(0,0,1)
scalarBar.GetTitleTextProperty().SetColor(0,0,1)

spc = scalarBar.GetPositionCoordinate()
spc.SetCoordinateSystemToNormalizedViewport()
spc.SetValue(0.05,0.05)

scalarBar.SetWidth(.12)
scalarBar.SetHeight(.95)

# a text actor
textActor = vtk.vtkTextActor()
tp = vtk.vtkTextProperty()
#tp.BoldOn()
#tp.ShadowOn()
#tp.ItalicOn()
tp.SetColor(1.0,0.2,0.3)
#tp.SetFontFamilyToArial()
tp.SetFontSize(30)
textActor.SetTextProperty(tp)

tpc = textActor.GetPositionCoordinate()
tpc.SetCoordinateSystemToNormalizedViewport()
tpc.SetValue(0.75,0.9)

textActor.SetWidth(.25)
textActor.SetHeight(.25)
textActor.SetInput(str(isovalue))

# renderer and render window 
ren = vtk.vtkRenderer()
ren.SetBackground(.8, .8, .8)

renWin = vtk.vtkRenderWindow()
renWin.SetWindowName("Hydrogen Visualization")

renWin.SetSize(500, 500)
renWin.AddRenderer(ren)

# Render window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors
ren.AddActor(outlineActor)
ren.AddActor(isosurfaceActor)
ren.AddActor(scalarBar)
ren.AddActor(textActor)
#renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInputConnection(w2if.GetOutputPort())

# Python function for the keyboard interface
# count is a screenshot counter
count = 0
def Keypress(obj, event):
    global count, isovalue, renWin
    key = obj.GetKeySym()
    if key == "s":
        renWin.Render()     
        w2if.Modified() # tell the w2if that it should update
        fnm = "screenshot%02d.png" %(count)
        wr.SetFileName(fnm)
        wr.Write()
        print "Saved '%s'" %(fnm)
        count = count+1
    elif key == "i":
        isovalue = isovalue + 0.01
        isosurface.SetValue(0,isovalue)
        textActor.SetInput("%4.2f" %(isovalue))
        tp.SetColor(lut.GetColor(isovalue))
        renWin.Render()
    elif key == "o":
        isovalue = isovalue - 0.01
        isosurface.SetValue(0,isovalue)
        textActor.SetInput("%4.2f" %(isovalue))
        tp.SetColor(lut.GetColor(isovalue))
        renWin.Render()
    # add your keyboard interface here
    # elif key == ...

# add keyboard interface, initialize, and start the interactor
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
