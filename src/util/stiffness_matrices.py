from math import sqrt
import numpy as np

class Stiffness_matrix():

    # ============================ ElmMatRigTrel2D =============================

    def ElmMatRigTrel2D(elm, No, Mat, Sec):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)

        # Calcula a matriz de rigidez no sistema local.

        E  = Mat[int(elm[1])][0]
        A  = Sec[int(elm[2])][0]
        Kl = E*A/L*[ [1,  0, -1,  0],
                [0,  0,  0,  0],
                [-1,  0,  1,  0],
                [ 0,  0,  0,  0]]

        return Kl

    # ============================= ElmMatRigViga ==============================

    def ElmMatRigViga(elm, No, Mat, Sec):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        L  = abs(dx)
        L2 = L*L
        L3 = L*L2

        # Calcula a matriz de rigidez no sistema local.

        E  = Mat[int(elm[1])][0]
        A  = Sec[int(elm[2])][0]
        I  = Sec[int(elm[2])][1]
        Kl = E*I*[ [12/L3,  6/L2, -12/L3,  6/L2],
                [6/L2,  4/L,   -6/L2,  2/L],
                [-12/L3, -6/L2,  12/L3, -6/L2],
                [6/L2,  2/L,   -6/L2,  4/L]]

        return Kl

    # ============================ ElmMatRigPort2D =============================

    def ElmMatRigPort2D(elm, No, Mat, Sec):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)
        L2 = L*L
        L3 = L*L2

        # Calcula a matriz de rigidez no sistema local.
        E  = Mat[int(elm[1])][0]
        A  = Sec[int(elm[2])][0]
        I  = Sec[int(elm[2])][1]
        EA = E*A
        EI = E*I

        Kl = [ [EA/L,       0,        0,  -EA/L,        0,      0],
            [0,   12*EI/L3,  6*EI/L2,    0,   -12*EI/L3,  6*EI/L2],
            [0,    6*EI/L2,  4*EI/L,     0,    -6*EI/L2,  2*EI/L],
            [-EA/L,       0,        0,    EA/L,        0,      0 ],
            [0,  -12*EI/L3, -6*EI/L2,    0,    12*EI/L3, -6*EI/L2],
            [0,    6*EI/L2,  2*EI/L,     0,    -6*EI/L2,  4*EI/L]]

        return Kl

    # ============================ ElmMatRigGrelha =============================

    def ElmMatRigGrelha(elm, No, Mat, Sec):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)
        L2 = L*L
        L3 = L*L2

        # Calcula a matriz de rigidez no sistema local.

        E  = Mat[int(elm[1])][0]
        G  = Mat[int(elm[1])][1]
        I  = Sec[int(elm[2])][1]
        J  = Sec[int(elm[2])][2]
        EI = E*I
        GJ = G*J

        Kl = [ [12*EI/L3,     0,   -6*EI/L2,  -12*EI/L3,   0,    -6*EI/L2],
                [0,       GJ/L,     0,          0,      -GJ/L,    0],
            [-6*EI/L2,     0,    4*EI/L,     6*EI/L2,   0,     2*EI/L],
            [-12*EI/L3,     0,    6*EI/L2,   12*EI/L3,   0,     6*EI/L2],
                [0,      -GJ/L,     0,          0,       GJ/L,    0],
            [-6*EI/L2,     0,    2*EI/L,     6*EI/L2,   0,     4*EI/L]]


        return  Kl

    # ============================ ElmMatRigPort3D =============================

    def ElmMatRigPort3D(elm, No, Mat, Sec):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        dz = No[no2, 2] - No[no1, 2]
        L  = sqrt(dx*dx + dy*dy + dz*dz)
        L2 = L*L
        L3 = L*L2

        # Calcula a matriz de rigidez no sistema local.

        E   = Mat[int(elm[1])][0]
        G   = Mat[int(elm[1])][1]

        A   = Sec[int(elm[2])][0]
        Iz  = Sec[int(elm[2])][1]
        J   = Sec[int(elm[2])][2]
        Iy  = Sec[int(elm[2])][3]

        EA  = E*A;
        EIy = E*Iy;
        EIz = E*Iz;
        GJ  = G*J;
        Kl  = [[EA/L,     0,      0,       0,      0,        0,       -EA/L,    0,         0,        0,      0,        0],
            [0,  12*EIz/L3,    0,       0,      0,     6*EIz/L2,     0,   -12*EIz/L3,   0,        0,      0,     6*EIz/L2],
            [0,        0,   12*EIy/L3,  0,   -6*EIy/L,    0,         0,      0,     -12*EIy/L3,   0,   -6*EIy/L2,   0],
            [0,        0,      0,      GJ/L,    0,        0,         0,      0,         0,      -GJ/L ,   0,        0],
            [0,        0,   -6*EIy/L2,  0,   4*EIy/L,     0,         0,      0,      6*EIy/L2,    0,   2*EIy/L,     0],
            [0,  6*EIz/L2,     0,       0,      0,     4*EIz/L,      0,   -6*EIz/L2,    0,        0,      0,      2*EIz/L],
            [-EA/L,    0,      0,       0,      0,        0,       EA/L,     0,         0,        0,      0,        0],
            [0,  -12*EIz/L3,   0,       0,      0,    -6*EIz/L2,     0,   12*EIz/L3,    0,        0,      0,   -6*EIz/L2],
            [0,        0,  -12*EIy/L3,  0,   6*EIy/L2,    0,         0,      0,     12*EIy/L3,    0,   6*EIy/L2,    0],
            [0,        0,      0,     -GJ/L,    0,        0,         0,      0,         0,        GJ/L,    0,        0],
            [0,        0,  -6*EIy/L2,   0,   2*EIy/L,     0,         0,      0,      6*EIy/L2,    0,   4*EIy/L,     0],
            [0,    6*EIz/L2,   0,       0,      0,     2*EIz/L,      0,  -6*EIz/L2,     0,        0,      0,     4*EIz/L]]

        return Kl