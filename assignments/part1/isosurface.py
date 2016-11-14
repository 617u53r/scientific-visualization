"""Isosurface extraction.

This script should extract and display isosurfaces of the probability
density of a hydrogen atom in a volume dataset.

You can run the script from the command line by typing
python isosurface.py

"""

import vtk


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You should
    extend this interface with keyboard shortcuts for changing the
    isovalue interactively.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        # Add the extra attributes you need here...

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        key = obj.GetKeySym()
        if key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" %
                                   (self.screenshot_counter))
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % (screenshot_filename))
            self.screenshot_counter += 1
        # Add your keyboard shortcuts here. You can use, e.g., the
        # "Up" key to increase the isovalue and the "Down" key to
        # decrease it. Don't forget to call the render window's
        # Render() function to update the rendering after you have
        # changed the isovalue.
        # elif key == ...

# Read the volume dataset
filename = "hydrogen.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
print("Reading volume dataset from " + filename + " ...")
reader.Update()  # executes the reader
print("Done!")

# Just for illustration, extract and print the dimensions of the
# volume. The string formatting used here is similar to the sprintf
# style in C.
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))

# Create an outline of the volume
# create an outline of the dataset
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

# Define actor properties (color, shading, line width, etc)
outline_actor.GetProperty().SetColor(0.0,0.0,1.0)
outline_actor.GetProperty().SetLineWidth(2.0)
outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
outline_actor.GetProperty().SetLineWidth(2.0)

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
tp.BoldOn()
tp.ShadowOn()
tp.ItalicOn()
tp.SetColor(1.0,0.2,0.3)
tp.SetFontFamilyToArial()
tp.SetFontSize(30)
textActor.SetTextProperty(tp)


tpc = textActor.GetPositionCoordinate()
tpc.SetCoordinateSystemToNormalizedViewport()
tpc.SetValue(0.75,0.9)

textActor.SetInput(str(isovalue))

#textActor.SetWidth(0.25)
#textActor.SetHeight(0.25)
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
ren.AddActor(isosurfaceActor)
ren.AddActor(scalarBar)
ren.AddActor(textActor)
ren.AddActor(outline_actor)
renWin.Render()

# create window to image filter to get the window to an image
w2if = vtk.vtkWindowToImageFilter()
w2if.SetInput(renWin)

# create png writer
wr = vtk.vtkPNGWriter()
wr.SetInputConnection(w2if.GetOutputPort())


# # Create a renderer and add the actors to it
# renderer = vtk.vtkRenderer()
# renderer.SetBackground(0.2, 0.2, 0.2)
# renderer.AddActor(outline_actor)
# # renderer.AddActor(...)
#
# # Create a render window
# render_window = vtk.vtkRenderWindow()
# render_window.SetWindowName("Isosurface extraction")
# render_window.SetSize(500, 500)
# render_window.AddRenderer(renderer)
#
# # Create an interactor
# interactor = vtk.vtkRenderWindowInteractor()
# interactor.SetRenderWindow(render_window)
#
# # Create a window-to-image filter and a PNG writer that can be used
# # for taking screenshots
# window2image_filter = vtk.vtkWindowToImageFilter()
# window2image_filter.SetInput(render_window)
# png_writer = vtk.vtkPNGWriter()
# png_writer.SetInputConnection(window2image_filter.GetOutputPort())

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

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = renWin
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
