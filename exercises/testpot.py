# This program demonstrates how an OBJ object can be read from file


from math import *
# load VTK
from vtk import *
from numpy import *
import sys

def DumpQualityStats(iq, arrayname):
    an = iq.GetOutput().GetFieldData().GetArray(arrayname)
    cardinality = an.GetComponent(0, 4)
    range = list()
    range.append(an.GetComponent(0, 0))
    range.append(an.GetComponent(0, 2))
    average = an.GetComponent(0, 1)
    stdDev = math.sqrt(math.fabs(an.GetComponent(0, 3)))
    outStr = '%s%g%s%g%s%g\n%s%g%s%g' % (
                                         '  cardinality: ', cardinality,
                                         '  , range: ', range[0], '  -  ', range[1],
                                         '  average: ', average, '  , standard deviation: ', stdDev)
    return outStr

def main():
    
    verts={}
    neighb={}
    triangs={}
    width=100
    area = vtk.vtkFloatArray()
    arr=[]
    for ix in range(0,width):
        arr.append(0)

    mr = vtk.vtkDataSetReader()
    iq = vtk.vtkMeshQuality()
    
    mr.SetFileName(sys.argv[1])
    mr.Update()
    
    ug = mr.GetOutput()
    iq.SetInputConnection(mr.GetOutputPort())
    
    # Here we define the various mesh types and labels for output.
    meshTypes = [['Triangle', 'Triangle',
                  [['QualityMeasureToEdgeRatio', ' Edge Ratio:'],
                   ['QualityMeasureToAspectRatio', ' Aspect Ratio:'],
                   ['QualityMeasureToRadiusRatio', ' Radius Ratio:'],
                   ['QualityMeasureToAspectFrobenius', ' Frobenius Norm:'],
                   ['QualityMeasureToMinAngle', ' Minimal Angle:']
                   ]
                  ],
                 
                 ['Quad', 'Quadrilateral',
                  [['QualityMeasureToEdgeRatio', ' Edge Ratio:'],
                   ['QualityMeasureToAspectRatio', ' Aspect Ratio:'],
                   ['QualityMeasureToRadiusRatio', ' Radius Ratio:'],
                   ['QualityMeasureToMedAspectFrobenius',
                    ' Average Frobenius Norm:'],
                   ['QualityMeasureToMaxAspectFrobenius',
                    ' Maximal Frobenius Norm:'],
                   ['QualityMeasureToMinAngle', ' Minimal Angle:']
                   ]
                  ],
                 
                 ['Tet', 'Tetrahedron',
                  [['QualityMeasureToEdgeRatio', ' Edge Ratio:'],
                   ['QualityMeasureToAspectRatio', ' Aspect Ratio:'],
                   ['QualityMeasureToRadiusRatio', ' Radius Ratio:'],
                   ['QualityMeasureToAspectFrobenius', ' Frobenius Norm:'],
                   ['QualityMeasureToMinAngle', ' Minimal Dihedral Angle:'],
                   ['QualityMeasureToCollapseRatio', ' Collapse Ratio:']
                   ]
                  ],
                 
                 ['Hex', 'Hexahedron',
                  [['QualityMeasureToEdgeRatio', ' Edge Ratio:']
                   ]
                  ]
                 
                 ]
    
    if ug.GetNumberOfCells() > 0 :
        res = ''
        for meshType in meshTypes:
            if meshType[0] == 'Tet':
                res += '\n%s%s\n   %s' % ('Tetrahedral',
                                          ' quality of the mesh:', mr.GetFileName())
            elif meshType[0] == 'Hex':
                res += '\n%s%s\n   %s' % ('Hexahedral',
                                          ' quality of the mesh:', mr.GetFileName())
            else:
                res += '\n%s%s\n   %s' % (meshType[1],
                                          ' quality of the mesh:', mr.GetFileName())
            
            for measure in meshType[2]:
                eval('iq.Set' + meshType[0] + measure[0] + '()')
                iq.Update()
                res += '\n%s\n%s' % (measure[1],
                                     DumpQualityStats(iq, 'Mesh ' + meshType[1] + ' Quality'))
            
            res += '\n'
        
        print res
    else:
        print ":p"

    Data = mr.GetOutput()
    CellArray = Data.GetPolys()
    Polygons = CellArray.GetData()
    triangles= CellArray.GetNumberOfCells()
    polys= Polygons.GetNumberOfTuples()/triangles
    vertices = Data.GetNumberOfPoints()

#   for i in xrange(0,  Polygons.GetNumberOfTuples()):
            #print Polygons.GetValue(i)
        #    for i in range(0, Data.GetNumberOfPoints()):
            #print Data.GetPoint(i)
    for i in range(0, vertices):
        verts[i]={i:[]}
    for i in range(0, triangles):
        neighb[i]=[]
        triangs[i]=[]

    
    print polys, triangles, Polygons.GetNumberOfTuples(), vertices
    pos=[0,0,0]
    print
    i=0
    for k in range(0, triangles):
        nr=Polygons.GetValue(i)
        i=i+1
        for j in range(0,nr):
            pos[j]= Polygons.GetValue(i)
            #        print pos[j]
            i=i+1

        try:
            verts[pos[0]][pos[1]].append(k)
        except KeyError:
            verts[pos[0]][pos[1]]=[k]

        try:
            verts[pos[0]][pos[2]].append(k)
        except KeyError:
            verts[pos[0]][pos[2]]=[k]

        try:
            verts[pos[1]][pos[0]].append(k)
        except KeyError:
            verts[pos[1]][pos[0]]=[k]

        try:
            verts[pos[1]][pos[2]].append(k)
        except KeyError:
            verts[pos[1]][pos[2]]=[k]

        try:
            verts[pos[2]][pos[0]].append(k)
        except KeyError:
            verts[pos[2]][pos[0]]=[k]

        try:
            verts[pos[2]][pos[1]].append(k)
        except KeyError:
            verts[pos[2]][pos[1]]=[k]

        triangs[k]=[pos[0], pos[1], pos[2]]
        v1=array(Data.GetPoint(pos[0]))
        v2=array(Data.GetPoint(pos[1]))
        v3=array(Data.GetPoint(pos[2]))

        #print v1, v2, v3
        #print cross(v2-v1,v3-v1)


        ix=int(round(MQ1(v1, v2, v3)*width))
        arr[ix]=arr[ix]+1
            # print triangs
    
    
    for i in range(10, triangles):
        #       print i,triangs[i]
#print verts[triangs[i][0]], verts[triangs[i][1]], verts[triangs[i][2]]
    #  i=2100
        #print i, triangs[i]
        #print

        vi={0:[1,2], 1:[0,2], 2:[0,1]}
        neig=[]
        for j in range(0,3):
            for l in range(0,2):
                for m in range(0,2):
                    try:
                        b=verts[triangs[i][j]][triangs[i][vi[j][l]]][m]
                        if b != i and not b in neig:
                            neig.append(b)
                    except IndexError:
                        if not [] in neig:
                            neig.append([])
        neighb[i]=neig
    #The triangle and its neighbours
        pr=False
        if pr:
            print neig
            d=triangs[i]
            for k in range(0,3):
                print array(Data.GetPoint(d[k]))
            print
            for j in range(0,len(neig)):
                if neig[j] !=[]:
                    a=triangs[neig[j]]
                    for k in range(0,3):
                        print array(Data.GetPoint(a[k]))
                    print
    print neighb

    for ix in range(0, width):
        area.InsertNextValue(arr[ix])

    return area

def MQ2(v1, v2, v3):
    a=cross(v2-v1,v3-v1)
    return math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])

def MQ3(v1, v2, v3):
    a=v2-v1
    b=v3-v2
    c=v1-v3
    a=math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    b=math.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])
    c=math.sqrt(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])
    q=min(min(a,b),c)
    return q/(a+b+c)
def MQ4(v1, v2, v3):
    a=v2-v1
    b=v3-v2
    c=v1-v3
    a=math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    b=math.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])
    c=math.sqrt(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])
    q=min(min(a,b),c)
    r=max(max(a,b),c)
    return q/r
def MQ5(v1, v2, v3):
    a=v2-v1
    b=v3-v2
    c=v1-v3
    a=math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    b=math.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])
    c=math.sqrt(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])
    r=max(max(a,b),c)
    if a==r:
        q=b/r
        s=c/r
    elif b==r:
        q=a/r
        s=c/r
    else:
        q=a/r
        s=b/r

    t=(1-q)*(1-s)
    return abs(t)
def MQ6(v1, v2, v3):
    a=v2-v1
    b=v3-v2
    c=v1-v3
    a=math.sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])
    b=math.sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2])
    c=math.sqrt(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])
    r=max(max(a,b),c)
    if a==r:
        q=b/(r/sqrt(2.0))
        s=c/(r/sqrt(2.0))
    elif b==r:
        q=a/(r/sqrt(2.0))
        s=c/(r/sqrt(2.0))
    else:
        q=a/(r/sqrt(2.0))
        s=b/(r/sqrt(2.0))
    
    t=(1-q)*(1-s)
    return abs(t)

def MQ1(v1, v2, v3):
#return ((MQ5(v1, v2, v3))*(MQ6(v1, v2, v3)))
    return (MQ5(v1, v2, v3))

if __name__ == '__main__':
    arrs=main()

    dataObject = vtkDataObject()
    dataObject.GetFieldData().AddArray(arrs)
    barChart = vtkBarChartActor()
    barChart.SetInput(dataObject)
    barChart.SetTitle("Histogram")
    barChart.LegendVisibilityOff()
    barChart.LabelVisibilityOff()


  
    #barChart.GetPositionCoordinate().SetValue(0.05,0.05,0.0)
    #barChart.GetPosition2Coordinate().SetValue(0.95,0.85,0.0)
    # barChart.GetProperty().SetColor(1,1,1)

   
    ren = vtkRenderer()
    ren.AddActor(barChart)
    ren.SetBackground(0.6, 0.6, 0.7)

    # Attach to a window
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetWindowName("Teapot")
    renWin.SetSize(500,500)

    # Attach to an interactor
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


