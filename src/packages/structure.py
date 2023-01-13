class FramedStructure():

    def __init__(self, NoDoF, DoFNo):
        self.NoDoF = NoDoF
        self.DoFNo = DoFNo

        self.fn = []
        self.f0 = []
        self.f = []
        self.K = []
        self.u = []

    def printData(self):
        print()
        print('=====================================')
        print('Global Frame Data')
        print(f'No. of Degrees of Freedom:', self.NoDoF)
        print(f'Degree of Freedom per Node:')
        for i in self.DoFNo:
            print(i)
        print()
        print('Nodal forces:')
        for i in self.fn:
            print(i)
        print()
        print('Member forces:')
        print(self.f0)
        print()
        print('Force vector:')
        print(self.f)
        print()
        print('K global:')
        for i in self.K:
            print(i)
        print()
        print('Global displacement:')
        print(self.u)
        print('=====================================')
        
        return True



    def add_forces(self, f, fn, f0):

        self.f = f
        self.fn = fn
        self.f0 = f0
        
        return True

    
    def deformed_coordinates(self):
        u = self.u
        DoF = self.DoFNo

        pass
    
    def deformed_geometry(self, x_points, y_points, Elm, Magnification):
        u = self.u
        nodedof = self.DoFNo

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

        matrix = []
        
        for elm in Elm:
            matrix.append(u_matrix[elm[3]])
            matrix.append(u_matrix[elm[4]])
        u_matrix = matrix
        

        x_points_def = [x1 + x2 for x1, x2 in zip(x_points, [point*Magnification for point in [row[0] for row in u_matrix]])]
        y_points_def = [y1 + y2 for y1, y2 in zip(y_points, [point*Magnification for point in [row[1] for row in u_matrix]])]
        print(len(x_points_def))

        return x_points_def, y_points_def