import numpy as np
from packages.functions import *
from packages.transformation_matrices import Transformation_matrix

class FramedElement():

    def __init__(self, NoElement, elm, No):
        
        No1 = elm[3]
        No2 = elm[4]
        CoordNo1 = No[No1]
        CoordNo2 = No[No2]

        self.NoElement = NoElement
        self.No1 = No1
        self.No2 = No2
        self.CoordNo1 = CoordNo1
        self.CoordNo2 = CoordNo2

        self.DoFNo1 = []
        self.DoFNo2 = []
        self.Ke = []
        self.Kel = []
        self.gl = []
        self.g = []
        self.ul = []
        self.f0 = []

        tipo = elm[0]

        if tipo == 1:   # Trelica plana
            T = Transformation_matrix.ElmMatTrnTrel2D(elm, No)
        elif tipo == 2: # Viga
            T = Transformation_matrix.ElmMatTrnViga(elm, No)
        elif tipo == 3: # Portica Plano
            T = Transformation_matrix.ElmMatTrnPort2D(elm, No)
        elif tipo == 4: # Grelha
            T = Transformation_matrix.ElmMatTrnGrelha(elm, No)
        elif tipo == 5: # Portico espacial
            T = Transformation_matrix.ElmMatTrnPort3D(elm, No)

        self.T = T




    def printData(self):
        print('=====================================')
        print(f'Element No.:', self.NoElement)
        print()
        print(f'No1:', self.CoordNo1)
        print(f'No2:', self.CoordNo2)
        print()
        print('Degrees of freedom:')
        print(self.DoFNo1)
        print(self.DoFNo2)
        print()
        print('K:')
        for i in self.Ke:
            print(i)
        print()
        print('K local:')
        for i in self.Kel:
            print(i)
        print()
        print('Transformation matrix:')
        for i in self.T:
            print(i)
        print()
        print('f0 Local:')
        print(self.f0)
        print()
        print('Local displacement:')
        print(self.ul)
        print()
        print('Local reactions:')
        print(self.gl)
        print()
        print('Global reactions:')
        print(self.g)
        print()
        print('=====================================')


        
        return