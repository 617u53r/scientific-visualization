#Read output from Matlab

# We will work with vtk objects
import vtk

#Read Points
def readPoints(file_name):
  
    # Create an array of Points
    points = vtk.vtkPoints()

    #Open the file
    with open(file_name) as file:
    
        # Read all lines
        all = file.read()
        lines=all.split("\n")
        
        # Loop through lines
        for line in lines:
            # Split the line into data
            data = line.split()

            # Skip the commented lines
            if data and data[0] != '#':
                # Convert data into floats
                x, y, z = float(data[0]), float(data[1]), float(data[2])

                # Insert floats into the point array
                points.InsertNextPoint(x, y, z)

    return points;
    

# Read Vectors.
# This method works in the same way as readPoints but returns a different type of array
def readVectors(file_name):
    # Create a Double array which represents the vectors
    vectors = vtk.vtkDoubleArray()
    # Define number of elements
    vectors.SetNumberOfComponents(3)
    
    with open(file_name) as file:
        # Read all lines
        all = file.read()
        lines=all.split("\n")
        
        # Loop through lines
        for line in lines:
            data = line.split()
            if data and data[0] != '#':
                x, y, z = float(data[0]), float(data[1]), float(data[2])
                vectors.InsertNextTuple3(x, y, z)
    return vectors

#Read Scalars
def readScalars(file_name):
  
    # Create an array of Scalars
    scalars = vtk.vtkFloatArray()

    #Open the file
    with open(file_name) as file:
    
        # Read all lines
        all = file.read()
        lines=all.split("\n")
        
        # Loop through lines
        for line in lines:
            # Split the line into data
            data = line.split()

            # Skip the commented lines
            if data and data[0] != '#':
                # Convert data into floats
                x, y = float(data[0]), float(data[1])

                # Insert floats into the point array
                z=abs(x-y); # Funny combination...
                scalars.InsertNextValue(z)

    return scalars;
