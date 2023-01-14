import matplotlib.pyplot as plt
from util.element import FramedElement
from util.structure import FramedStructure
from util.functions import *



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

                StructuralAnalysis.plot_initial_geometry(Elements=Elements)

                # Plot the deformed structure

                xyz_def = StructuralAnalysis.deformed_geometry(GlobalFrame, self.No, Magnification)
                StructuralAnalysis.plot_def_geometry(self.Elm, xyz_def)
            
                plt.show()

        return Elements, GlobalFrame

    def plot_initial_geometry(Elements):

        xpoints = []
        ypoints = []

        for elm in Elements:
            xpoints.append(elm.CoordNo1[0])
            xpoints.append(elm.CoordNo2[0])
            ypoints.append(elm.CoordNo1[1])
            ypoints.append(elm.CoordNo2[1])

            plt.plot(xpoints, ypoints, 'o-.', c='b',linewidth=1)

            xpoints = []
            ypoints = []
        
        plt.title("Structure Geometry")
        plt.xlabel("x-coordinates (m)")
        plt.ylabel("y-coordinates (m)")
        
        return
    
    def plot_def_geometry(Elm, xyz_def):

        xpoints = []
        ypoints = []
        
        for elm in Elm:
            xpoints.append(xyz_def[elm[3]][0])
            xpoints.append(xyz_def[elm[4]][0])
            ypoints.append(xyz_def[elm[3]][1])
            ypoints.append(xyz_def[elm[4]][1])

            plt.plot(xpoints, ypoints, c='r', linewidth=1)

            xpoints = []
            ypoints = []
        
        return

    def deformed_geometry(GlobalFrame, No, Magnification):

        u = GlobalFrame.u
        nodedof = GlobalFrame.DoFNo

        non_zero_count = sum(1 for row in nodedof for element in row if element != 0)
        if len(u) != non_zero_count:
            raise ValueError('The length of u and the number of non-zero elements in nodedof do not match.')
        
        u_matrix = [[0.0 for _ in range(len(nodedof[0]))] for _ in range(len(nodedof))]
        
        u_index = 0

        for i in range(len(nodedof)):
            for j in range(len(nodedof[i])):
                if nodedof[i][j] != 0:
                    u_matrix[i][j] = u[u_index][0]
                    u_index += 1

        u_matrix_xyz = [row[:3] for row in u_matrix]
        u_matrix_xyz = list(map(lambda x: [i * Magnification for i in x], u_matrix_xyz))

        xyz_def = [[x+y for x, y in zip(inner_list1, inner_list2)] for inner_list1, inner_list2 in zip(u_matrix_xyz, No)]

        return xyz_def