"""Molecular dynamics.

This script should display the atoms (and their connections) in a
molecular dynamics simulation dataset.

You can run the script from the command line by typing
python molecules.py

"""

import vtk
import molecules_io


# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for manipulating the
    molecule visualization.

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


# Read the data into a vtkPolyData object using the functions in
# molecules_io.py
data = vtk.vtkPolyData()
data.SetPoints(molecules_io.read_points("coordinates.txt"))
data.GetPointData().SetScalars(molecules_io.read_scalars("radii.txt"))
data.SetLines(molecules_io.read_connections("connections.txt"))


# Glyphs
sphere = vtk.vtkSphereSource()
sphere.SetRadius(0.25)
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)

sphere_glyph = vtk.vtkGlyph3D()
sphere_glyph.SetInput(data)
sphere_glyph.SetSourceConnection(sphere.GetOutputPort())
sphere_glyph.SetScaleModeToScaleByScalar()
sphere_glyph.SetColorModeToColorByScalar()
sphere_glyph.SetScaleFactor(2.0)

color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0.37, 0.545098, 0.0, 0.545098)
color_transfer_function.AddRGBPoint(0.68, 1.0, 1.0, 0.0)
color_transfer_function.AddRGBPoint(0.73, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(0.74, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(0.77, 0.0, 1.0, 1.0)
color_transfer_function.AddRGBPoint(2.0, 0.0, 1.0, 0.0)

sphere_mapper = vtk.vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_glyph.GetOutputPort())
sphere_mapper.SetLookupTable(color_transfer_function)

sphere_actor = vtk.vtkActor()
sphere_actor.SetMapper(sphere_mapper)

#Tubes
tube_filter = vtk.vtkTubeFilter()
tube_filter.SetInput(data)
tube_filter.SetRadius(0.15)
tube_filter.SetNumberOfSides(7)

tube_mapper = vtk.vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube_filter.GetOutputPort())
tube_mapper.ScalarVisibilityOff()

tube_actor = vtk.vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
tube_actor.GetProperty().SetSpecularColor(1, 1, 1)
tube_actor.GetProperty().SetSpecular(0.3)
tube_actor.GetProperty().SetSpecularPower(20)
tube_actor.GetProperty().SetAmbient(0.2)
tube_actor.GetProperty().SetDiffuse(0.8)

# Add keyboard interaction for changing the isovalue interactively.
# Nice addition but still too cluttered
colorbar = vtk.vtkLegendBoxActor()
colorbar.SetNumberOfEntries(6)
colorbar.BoxOn()
colorbar.SetPosition(0, 0.8)

colorbar.SetEntrySymbol(0, sphere.GetOutput())
colorbar.SetEntryString(0, "0.37")
colorbar.SetEntryColor(0, 0.545098, 0.0, 0.545098)

colorbar.SetEntry(0, sphere.GetOutput(), "0.37", (0.5, 0.0, 0.5))
colorbar.SetEntry(1, sphere.GetOutput(), "0.68", (1.0, 1.0, 0.0))
colorbar.SetEntry(2, sphere.GetOutput(), "0.73", (0.0, 0.0, 1.0))
colorbar.SetEntry(3, sphere.GetOutput(), "0.74", (1.0, 0.0, 0.0))
colorbar.SetEntry(4, sphere.GetOutput(), "0.77", (0.0, 1.0, 1.0))
colorbar.SetEntry(5, sphere.GetOutput(), "2.0", (0.0, 1.0, 0.0))

# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(sphere_actor)
renderer.AddActor(tube_actor)
renderer.AddActor(colorbar)

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Molecular dynamics")
render_window.SetSize(500, 500)
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
