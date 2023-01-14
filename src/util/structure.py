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
        
        return



    def add_forces(self, f, fn, f0):

        self.f = f
        self.fn = fn
        self.f0 = f0
        
        return