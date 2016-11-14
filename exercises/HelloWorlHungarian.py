# This program demonstrates how VTK can be used to render a text
# The user can also interact with the text by using the mouse

# load VTK
from vtk import *

# Create a Text source and set the text
sText = vtkTextSource()
sText.SetText("UPPMAX")
sText.SetForegroundColor(0.6,1.0,0.2)

# Create a mapper and set the Text source as input 
mText = vtkPolyDataMapper()
mText.SetInputConnection(sText.GetOutputPort())

# Create an actor and set the mapper as input
aText = vtkActor()
aText.SetMapper(mText)

# Create a renderer
rMain = vtkRenderer()

# Assign the actor to the renderer
rMain.AddActor(aText)

# Create a rendering window
wMain = vtkRenderWindow()

# Add the renderer to the window
wMain.AddRenderer(rMain)

# Set the name of the window (this is optional)
wMain.SetWindowName("Hello World!")

# Make sure that we can interact with the application 
iMain = vtkRenderWindowInteractor()
iMain.SetRenderWindow(wMain)

# Initialze and start the application
iMain.Initialize()
iMain.Start()
