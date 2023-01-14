import numpy as np
from math import sqrt

class Load_vector():
    # ============================= ElmEngPerfViga =============================

    def ElmEngPerfViga(elm, No, carga):
        elm = np.array(elm)
        No = np.array(No)
        # Calcula o comprimento da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        L  = abs(dx)

        # Calcula as forcas de engastamento no sistema local.

        qy = carga(3)
        fl = qy*[[-L/2],
                [-L**2/12],
                [-L/2],
                [L**2/12]]

        return fl
    
    # ============================ ElmEngPerfPort2D ============================

    def ElmEngPerfPort2D(elm, No, carga):
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

        # Determina as cargas distribuidas no sistema local.

        local = carga[1]
        if local == 1:
            qx = carga[2]
            qy = carga[3]
        else:
            qx =  c*carga[2] + s*carga[3]
            qy = -s*carga[2] + c*carga[3]


        # Calcula as forcas de engastamento no sistema local.

        fl = [[-qx*L/2],
            [-qy*L/2],
            [-qy*L**2/12],
            [-qx*L/2],
            [-qy*L/2],
            [qy*L**2/12]]
        return fl

    # ============================ ElmEngPerfGrelha ============================

    def ElmEngPerfGrelha(elm, No, carga):
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

        # Determina as cargas distribuidas no sistema local.

        qz = carga[4]

        # Calcula as forcas de engastamento no sistema local.

        fl = [[-qz*L/2],
            [0],
            [qz*L**2/12]
            [-qz*L/2]
            [0]
            [-qz*L**2/12]]

        return fl
    

    # ============================ ElmEngPerfPort3D ============================

    def ElmEngPerfPort3D(elm, No, carga):
        elm = np.array(elm)
        No = np.array(No)
        # Determina a geometria da barra.

        no1 = elm[3]
        no2 = elm[4]
        dx = No[no2, 0] - No[no1, 0]
        dy = No[no2, 1] - No[no1, 1]
        dz = No[no2, 2] - No[no1, 2]
        L  = sqrt(dx*dx + dy*dy + dz*dz)

        """

        c  = dx/L
        s  = dy/L

        # Determina as cargas distribuidas no sistema local.

        local = carga[1]
        if local == 1:
            qx = carga[2]
            qy = carga[3]
        else:
            qx =  c*carga[2] + s*carga[3]
            qy = -s*carga[2] + c*carga[3]


        # Calcula as forcas de engastamento no sistema local.

        fl = [[-qx*L/2],
            [-qy*L/2],
            [-qy*L**2/12],
            [-qx*L/2],
            [-qy*L/2],
            [qy*L**2/12]]
        return fl

        """
