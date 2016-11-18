"""Air currents.

This script should display a visualization of a vtkStructuredPoints
dataset containing the direction and speed of air currents over North
America.

You can run the script from the command line by typing
python wind.py

"""

import vtk
import math


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.

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
        # Add your keyboard shortcuts here. If you modify any of the
        # actors or change some other parts or properties of the
        # scene, don't forget to call the render window's Render()
        # function to update the rendering.
        # elif key == ...


# Read the dataset
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("wind.vtk")
reader.Update()

# Just for illustration, extract and print the dimensions of the volume.
# like the previous assignment
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))

#Outline
outline = vtk.vtkOutlineFilter()
outline.SetInput(reader.GetOutput())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInput(outline.GetOutput())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
outline_actor.GetProperty().SetLineWidth(2.0)

# The range and bounds of the data
a,b = reader.GetOutput().GetScalarRange()
W,H,D = reader.GetOutput().GetDimensions()
xmi, xma, ymi, yma, zmi, zma = reader.GetOutput().GetBounds()

# Color Transfer Function
color_transfer_function = vtk.vtkLookupTable()
color_transfer_function.SetHueRange(0.667, 0.0)
color_transfer_function.SetValueRange(1.0, 1.0)
color_transfer_function.SetSaturationRange(1.0, 1.0)
color_transfer_function.SetTableRange(a, b)

# A plane for the seeds
plane = vtk.vtkPlaneSource()
plane.SetOrigin(xmi,math.ceil(ymi),zmi)
plane.SetPoint1(xma,math.ceil(ymi),zmi)
plane.SetPoint2(xmi,math.ceil(ymi),zma)
plane.SetXResolution(6)
plane.SetYResolution(6)

# Streamlines
stream = vtk.vtkStreamLine()
stream.SetSource(plane.GetOutput())
stream.SetInput(reader.GetOutput())
stream.SetIntegrationDirectionToForward()
stream.SetIntegrator(vtk.vtkRungeKutta4())
stream.SetStepLength(0.1)

stream_mapper = vtk.vtkPolyDataMapper()
stream_mapper.SetLookupTable(color_transfer_function)
stream_mapper.SetInput(stream.GetOutput())
stream_mapper.SetScalarRange(a, b)
stream_actor = vtk.vtkActor()
stream_actor.SetMapper(stream_mapper)
stream_actor.GetProperty().SetLineWidth(3.0)

#Colour Bar
color_bar = vtk.vtkScalarBarActor()
color_bar.SetLookupTable(color_transfer_function)
color_bar.SetOrientationToHorizontal()
color_bar.SetPosition(0.1, 0.03)
color_bar.SetHeight(0.1)
color_bar.SetWidth(0.8)
color_bar.SetTitle("Wind speed")

#Sliceplane
slice_plane = vtk.vtkImageDataGeometryFilter()
slice_plane.SetInput(reader.GetOutput())
slice_plane.SetExtent(0, W, 0, H, D / 2, D / 2)

slice_plane_mapper = vtk.vtkPolyDataMapper()
slice_plane_mapper.SetLookupTable(color_transfer_function)
slice_plane_mapper.SetInput(slice_plane.GetOutput())
slice_plane_mapper.SetScalarRange(a, b)

slice_plane_actor = vtk.vtkActor()
slice_plane_actor.SetMapper(slice_plane_mapper)

#Glyphs
arrow = vtk.vtkArrowSource()
arrow.SetTipRadius(0.03)
arrow.SetShaftRadius(0.01)

arrow_glyph = vtk.vtkGlyph3D()
arrow_glyph.SetInput(slice_plane.GetOutput())
arrow_glyph.SetSourceConnection(arrow.GetOutputPort())

arrow_glyph.SetScaleFactor(0.05)

arrow_mapper = vtk.vtkPolyDataMapper()
arrow_mapper.SetInputConnection(arrow_glyph.GetOutputPort())

lut = vtk.vtkLookupTable()
arrow_mapper.SetLookupTable(lut)
lut.SetHueRange(0.0,0.0)
lut.Build()

arrowActor = vtk.vtkActor()
arrowActor.SetMapper(arrow_mapper)

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
# renderer.SetBackground(0, 0, 0)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.AddActor(outline_actor)
renderer.AddActor(stream_actor)
renderer.AddActor(arrowActor)
renderer.AddActor(slice_plane_actor)
renderer.AddActor(color_bar)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Air currents")
render_window.SetSize(800, 600)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a window-to-image filter and a PNG writer that can be used
# to take screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInputConnection(window2image_filter.GetOutputPort())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
