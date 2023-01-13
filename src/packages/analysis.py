import matplotlib.pyplot as plt
from packages.element import FramedElement
from packages.structure import FramedStructure
from packages.functions import *



class StructuralAnalysis():
    
    def __init__(self, No, Sup, Mol, Mat, Sec, Elm, Fno, Fq):
        self.No = No
        self.Sup = Sup
        self.Mol = Mol
        self.Mat = Mat
        self.Sec = Sec
        self.Elm = Elm
        self.Fno = Fno
        self.Fq = Fq


    def analysis(self, printGeometry=True, Magnification=100000):
        
        # Initialize all individual framed elements
        Elements = []
        for elm in self.Elm:
            NoElement = self.Elm.index(elm) + 1
            Elements.append(FramedElement(NoElement, elm, self.No))

        # Initialize the whole framed structure
        ngl, glno = NumGl(self.No, self.Sup, self.Elm, Elements)
        GlobalFrame = FramedStructure(ngl, glno)
        
        for i in range(0, len(self.Elm)):
            Elements[i].DoFNo1 = GlobalFrame.DoFNo[self.Elm[i][3]]
            Elements[i].DoFNo2 = GlobalFrame.DoFNo[self.Elm[i][4]]

        # Calculate load vectors
        f, fn, f0 = VetCargExt(self.No, self.Fno, self.Elm, self.Fq, 6, GlobalFrame, Elements)
        GlobalFrame.add_forces(f, fn, f0)

        # Calculate stiffness matrix
        K = MatRigGlob(self.No, self.Mol, self.Mat, self.Sec, self.Elm, 6, GlobalFrame, Elements)

        # Calculate displacement vector
        u = np.linalg.solve(K, f)
        GlobalFrame.u = u

        # Calculate each node displacement
        desl = DeslocNo(len(self.No), 6, GlobalFrame.DoFNo, GlobalFrame.u)
        
        # Calculate global and local internal forces and local displacement
        for e in range(0, len(self.Elm)):
            gl, g, ul = ElmIntFor(e, self.No, self.Mat, self.Sec, self.Elm, self.Fq, desl, Elements)
            Elements[e].gl = gl
            Elements[e].g = g
            Elements[e].ul = ul

        
        # Draw the 2D geometry
        if printGeometry:
            analysisType = 'Plane Frame'

            if analysisType == 'Plane Frame':
                
                # Plot the initial structure
                xpoints = []
                ypoints = []
                for elm in Elements:
                    xpoints.append(elm.CoordNo1[0])
                    xpoints.append(elm.CoordNo2[0])
                    ypoints.append(elm.CoordNo1[1])
                    ypoints.append(elm.CoordNo2[1])

                plt.plot(xpoints, ypoints, 'o-.', linewidth=1)
                plt.title("Initial Structure")
                plt.xlabel("x-coordinates (m)")
                plt.ylabel("y-coordinates (m)")
                
                # Plot the deformed structure
                Nel = len(self.Elm)

                x_def, y_def = GlobalFrame.deformed_geometry(xpoints, ypoints, self.Elm, Magnification)
                
                plt.plot(x_def, y_def, c='r', linewidth=1)

                plt.show()
                
        return Elements, GlobalFrame