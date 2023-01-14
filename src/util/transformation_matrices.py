from math import sqrt
import numpy as np

class Transformation_matrix():

    # ============================ ElmMatTrnTrel2D =============================

    def ElmMatTrnTrel2D(elm, No):
        elm = np.array(elm)
        No = np.array(No)
        # Determina a geometria da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)
        c  = dx/L
        s  = dy/L

        # Determina a matriz de transformacao.

        T = [[c, s, 0, 0],
            [-s, c, 0, 0],
            [0, 0, c, s],
            [0, 0, -s, c]]

        return T

    # ============================= ElmMatTrnViga ==============================

    def ElmMatTrnViga(elm, No):

        T = np.identity(4)

        return T
    
    # ============================ ElmMatTrnPort2D =============================

    def ElmMatTrnPort2D(elm, No):
        elm = np.array(elm)
        No = np.array(No)
        # Determina a geometria da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)
        c  = dx/L
        s  = dy/L

        # Determina a matriz de transformacao.

        T = [[c,  s,  0,  0,  0,  0],
            [-s,  c,  0,  0,  0,  0],
            [0,  0,  1,  0,  0,  0],
            [0,  0,  0,  c,  s,  0],
            [0,  0,  0, -s,  c,  0],
            [0,  0,  0,  0,  0,  1]]

        return T
    
    # ============================ ElmMatTrnGrelha =============================

    def ElmMatTrnGrelha(elm, No):
        elm = np.array(elm)
        No = np.array(No)
        # Determina a geometria da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        L  = sqrt(dx*dx + dy*dy)
        c  = dx/L
        s  = dy/L

        # Determina a matriz de transformacao.

        T = [ [1,  0,  0,  0,  0,  0],
            [0,  c,  s,  0,  0,  0],
            [0, -s,  c,  0,  0,  0],
            [0,  0,  0,  1,  0,  0],
            [0,  0,  0,  0,  c,  s],
            [0,  0,  0,  0, -s,  c]]

        return T
    
    # ============================ ElmMatTrnPort3D =============================

    def ElmMatTrnPort3D(elm, No):
        elm = np.array(elm)
        No = np.array(No)
        # Determina a geometria da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        dz = No[no2, 2] - No[no1, 2]
        L  = sqrt(dx*dx + dy*dy + dz*dz)



        # Sistema local 1
        if dx != 0:
            xl = [dx,       dy,        dz] / L
            yl = [-dy/dx,    1 ,        0] / sqrt(dy*dy/(dx*dx) + 1)
            zl = [-dz ,   -dz*dy/dx,   dx+dy*dy/dx] / sqrt(dz*dz + dz*dz*dy*dy/(dx*dx) + (dx+dy*dy/dx)**2)
        elif dx == 0:
            xl = [0 ,  dy,   dz]/sqrt(dy*dy + dz*dz)
            yl = [1 ,  0 ,   0]
            zl = [0 ,  dz,  -dy]/sqrt(dz*dz + dy*dy)
        #xl = [dx       dy        dz] / L
        #yl = ay(elm(6),:)
        #zl = [xl(2)*yl(3)-xl(3)*yl(2)   xl(3)*yl(1)-xl(1)*yl(3)   xl(1)*yl(2)-xl(2)*yl(1)]


        if xl[0] == 0:
            cxx = 0
        else:
            cxx = xl[0]

        if xl[1] == 0:
            cxy = 0
        else:
            cxy = xl[1]

        if xl[2] == 0:
            cxz = 0
        else:
            cxz = xl[2]

        if yl[0] == 0:
            cyx = 0
        else:
            cyx = yl[0]

        if yl[1] == 0:
            cyy = 0
        else:
            cyy = yl[1]

        if yl[2] == 0:
            cyz = 0
        else:
            cyz = yl[2]

        if zl[0] == 0:
            czx = 0
        else:
            czx = zl[0]

        if zl[1] == 0:
            czy = 0
        else:
            czy = zl[1]

        if zl[2] == 0:
            czz = 0
        else:
            czz = zl[2]

        # Determina a matriz de transformacao.

        T = [[xl[0],  xl[1],  xl[2],   0,     0,      0,     0,     0,      0,     0,     0,     0],
            [yl[0],  yl[1],  yl[2],   0,     0,      0,     0,     0,      0,     0,     0,     0],
            [zl[0],  zl[1],  zl[2],   0,     0,      0,     0,     0,      0,     0,     0,     0],
            [0,      0,      0,    xl[0],  xl[1],  xl[2],  0,     0,      0,     0,     0,     0],
            [0,      0,      0,    yl[0],  yl[1],  yl[2],  0,     0,      0,     0,     0,     0],
            [0,      0,      0,    zl[0],  zl[1],  zl[2],  0,     0,      0,     0,     0,     0],
            [0,      0,      0,      0,     0,     0,    xl[0],  xl[1],  xl[2],  0,     0,     0],
            [0,      0,      0,      0,     0,     0,    yl[0],  yl[1],  yl[2],  0,     0,     0],
            [0,      0,      0,      0,     0,     0,    zl[0],  zl[1],  zl[2],  0,     0,     0],
            [0,      0,      0,      0,     0,     0,      0,     0,     0,   xl[0],  xl[1],  xl[2]],
            [0,      0,      0,      0,     0,     0,      0,     0,     0,   yl[0],  yl[1],  yl[2]],
            [0,      0,      0,      0,     0,     0,      0,     0,     0,   zl[0],  zl[1],  zl[2]]]


        return T