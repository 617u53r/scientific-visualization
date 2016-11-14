#Convert the data into a .vtk file

import sys
from vtk import *
from ReadPoints import *

# Read the data into a vtkPolyData using the functions in ReadPoints.py
data=vtk.vtkUnstructuredGrid()

# Read arguments
data.SetPoints(readPoints(sys.argv[1]))
data.GetPointData().SetVectors(readVectors(sys.argv[2]))
data.GetPointData().SetScalars(readScalars(sys.argv[3])) 

# Make a new file!
Data=vtk.vtkUnstructuredGridWriter()
Data.SetInput(data) #Data.SetInputData(data) # For newer versions of VTK
# http://www.vtk.org/Wiki/VTK/VTK_6_Migration/Replacement_of_SetInput
Data.SetFileName(sys.argv[4])
Data.Write()


