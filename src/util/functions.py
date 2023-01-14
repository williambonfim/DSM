import numpy as np
from math import sqrt
from util.stiffness_matrices import Stiffness_matrix
from util.load_vectors import Load_vector



# ================================= NumGl ==================================
#
# Esta funcao numera os graus de liberdade nodais e determina o numero de
# equacoes.
#
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Sup  - matriz com os gl (0 = livre/1 = fixo) dos nos com apoio     (in)
#  Elm  - matriz com os dados (tipo, mat, sec, no1, no2)              (in)
#  ngln - numero de gl por no                                         (out)
#  ngl  - numero de gl da estrutura (numero de equacoes)              (out)
#  glno - matriz contendo os gl de todos os nos                       (out)
#
def NumGl(No, Sup, Elm, Elements):
    # Inicializa os graus de liberdade nodais.
    No = np.array(No)
    Elm = np.array(Elm)
    Sup = np.array(Sup)

    ngln = 6
    nn = len(No)
    glno = np.ones((nn, ngln))

    # Ativa os graus de liberdade de acordo com o tipo de elemento.
    ne = len(Elm)
    for e in range(0, ne):
        ativgl = ElmAtivGl(Elm[e])
        no1 = Elm[e, 3]
        no2 = Elm[e, 4]
        m = len(ativgl)
        for i in range(0, m):
            if ativgl[i] == 1:
                glno[no1, i] = 0
                glno[no2, i] = 0

    # Aplica os apoios (livre = 0 e fixo = 1)
    nsup = len(Sup) # numero de nos com apoios
    for i in range(0, nsup):
        sup = Sup[i, 0] # No com apoio
        for j in range(0, 6):
            if Sup[i, j+1] == 1:    # prende os gl fixos
                glno[sup, j] = 1

    # Numera os graus de liberdade - ao final: fixo = 0 e livre > 0.
    ngl = 0
    for i in range(0, nn):
        for j in range(0, ngln):
            if glno[i,j] == 0:
                ngl = ngl + 1
                glno[i, j] = ngl
            else:
                glno[i, j] = 0

    glno = glno.tolist()

    return ngl, glno


# ================================ DeslocNo ================================
#
# Esta funcao retorna uma matriz contendo os deslocamentos de cada no.
#
#  nn   - numero de nos                                               (in)
#  ngln - numero de gl por no                                         (in)
#  glno - matriz contendo os gl de todos os nos                       (in)
#  u    - vetor (ngl) dos deslocamentos globais                       (in)
#  desl - matrix (nn x ngln) com os deslocamentos de cada no          (out)
#
def DeslocNo(nn, ngln, glno, u):
    
    glno = np.array(glno)
    desl = np.zeros((nn, ngln))         # Inicializa a matriz dos deslocamentos
    for no in range(0, nn):
        for i in range(0, ngln):
            ii = glno[no, i]           # Obtem o gl global
            if ii > 0:                 # Verifica se o gl esta ativo (livre)
                desl[no, i] = u[int(ii)-1]    # Extrai o deslocamento do no

    return desl



# =============================== ElmAtivGl ================================
#
# Esta funcao retorna os graus de liberdade do elemento de trelica.
#
#  elm    - elemento                                                  (in)
#  ativgl - matriz contendo os gl de todos os nos                     (out)
#
def ElmAtivGl(elm):

    tipo = elm[0]

    if tipo == 1:                   # Trelica plana
        ativgl = [1, 1, 0, 0, 0, 1] # u, v
    elif tipo == 2:                 # Viga
        ativgl = [0, 1, 0, 0, 0, 1] # v, rz
    elif tipo == 3:                 # Portico plano
        ativgl = [1, 1, 0, 0, 0, 1] # u, v, rz
    elif tipo == 4:                 # Grelha
        ativgl = [0, 0, 1, 1, 1, 0] # v, rx, ry
    elif tipo == 5:                 # Portico espacial
        ativgl = [1, 1, 1, 1, 1, 1] # u, v, w, rx, ry, rz
    else:
        print(f'Error: invalid element!')

    return ativgl

# ================================ ElmDesl =================================
#
# Esta funcao retorna os deslocamentos nodais do elemento de portico plano.
#
#  elm  - elemento                                                    (in)
#  desl - matriz contendo os deslocamentos de todos os nos            (in)
#  ue   - vetor coluna com os deslocamentos nodais do elemento        (out)
#
def ElmDesl(elm, desl):

    tipo = elm[0]
    no1 = elm[3]
    no2 = elm[4]
    if tipo == 1:     # Trelica plana
        ue  = [desl[no1, 0], desl[no1, 1], desl[no2, 0], desl[no2, 1]]
        ue = np.matrix.transpose(np.array(ue))
    elif tipo == 2: # Viga
        ue  = [desl[no1, 1], desl[no1, 5], desl[no2, 1], desl[no2, 5]]
        ue = np.matrix.transpose(np.array(ue))
    elif tipo == 3: # Portico plano
        ue  = [desl[no1, 0], desl[no1, 1], desl[no1, 5],
               desl[no2, 0], desl[no2, 1], desl[no2, 5]]
        ue = np.matrix.transpose(np.array(ue))
    elif tipo == 4: # Grelha
        ue  = [desl[no1, 2], desl[no1, 3], desl[no1, 4],
               desl[no2, 2], desl[no2, 3], desl[no2, 4]]
        ue = np.matrix.transpose(np.array(ue))
    elif tipo == 5: # Portico espacial
        ue = [desl[no1, 0], desl[no1, 1], desl[no1, 2],
              desl[no1, 3], desl[no1, 4], desl[no1, 5],
              desl[no2, 0], desl[no2, 1], desl[no2, 2],
              desl[no2, 3], desl[no2, 4], desl[no2, 5]]
    else:
        print(f'Erro: elemento invalido!\n')

    return ue



# =============================== VetCargExt ===============================
#
# Esta funcao calcula e retorna o vetor de cargas externas.
#
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Fno  - matriz com as cargas concentradas nodais                    (in)
#  Elm  - matriz com os dados (tipo, mat, sec, no1, no2)              (in)
#  Fq   - matriz com as cargas distribuidas                           (in)
#  ngln - numero de gl por no                                         (in)
#  ngl  - numero de gl da estrutura                                   (in)
#  glno - matriz contendo os gl de todos os nos                       (in)
#  f    - vetor de cargas externas (ngl)                              (out)
#

def VetCargExt(No, Fno, Elm, Fq, ngln, GlobalFrame, Elements):
    ngl = GlobalFrame.NoDoF
    glno = GlobalFrame.DoFNo
    # Forcas nodais.

    glno = np.array(glno)
    Elm = np.array(Elm)

#    print('f nodais---------------------------------')
#    print()
    f = np.zeros((ngl, 1))
    f0global = np.zeros((ngl,1))

    nc = len(Fno)
    Fno = np.array(Fno)
    for c in range(0, nc):
        no = Fno[c, 0]
        fn = Fno[c, 1:7]
        for i in range(0, ngln):
            ii = glno[int(no), i]
            if ii > 0:
                f[int(ii)-1] = f[int(ii)-1] + fn[int(i)]
    fn = f.tolist()

    nq = len(Fq)
    if nq == 0:
        return f
    
    ne = len(Elm)
    for e in range(0, ne):
        elm = Elm[e]
        ngle, gle = ElmGl(elm, glno)    # Gls do elementos
        f0 = ElmEngPerf(e, Elm, No, Fq, 'global', Elements)
        Elements[e].f0 = f0
        for i in range(0, ngle):
            ii = gle[i]
            if ii > 0:
                f[int(ii)-1] = f[int(ii)-1] - f0[int(i)]
                f0global[int(ii)-1] = f0global[int(ii)-1] - f0[int(i)]

    return f, fn, f0global



# =============================== MatRigGlob ===============================
#
# Esta funcao calcula e retorna a matriz de rigidez da estrutura.
#
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Mol  - matriz com as propriedades das molas                        (in)
#  Mat  - matriz com as propriedades dos materiais                    (in)
#  Sec  - matriz com as propriedades das secoes                       (in)
#  Elm  - matriz com os dados (tipo, mat, sec, no1, no2)              (in)
#  ngln - numero de gl por no                                         (in)
#  ngl  - numero de gl da estrutura                                   (in)
#  glno - matriz contendo os gl de todos os nos                       (in)
#  K    - matriz de rigidez global (ngl x ngl)                        (out)
#
def MatRigGlob(No, Mol, Mat, Sec, Elm, ngln, GlobalFrame, Elements):
    ngl = GlobalFrame.NoDoF
    glno = GlobalFrame.DoFNo
    glno = np.array(glno)
    Elm = np.array(Elm)

    # Contribuicao das barras (elementos)

    K = np.zeros((ngl, ngl))      # Inicializacao
    ne = len(Elm)               # Numero de elementos
    for e in range(0, ne):

        elm = Elm[e]
        ngle, gle = ElmGl(elm, glno)    #Gl do elemento
        Ke, Kel = ElmMatRig(e, elm, No, Mat, Sec, Elements)   # Matriz de rigidez elemento
        Elements[e].Kel = Kel
        Elements[e].Ke = Ke

        for i in range(0, ngle):
            ii = gle[i]                     # Obtem o gl global (linha)
            for j in range(0, ngle):
                jj = gle[j]                 # Obtem o gl global (coluna)
                if (ii > 0 and jj > 0):     # Verifica se os gl estao ativos
                    K[int(ii)-1, int(jj)-1] = K[int(ii)-1, int(jj)-1] + Ke[i, j]    # Soma na matriz global

    # Contribuicao das molas (apoios elasticos)

    nm = len(Mol)   # Numero de molas
    for i in range(0, nm):
        no = Mol[i, 0]
        dir = Mol[i, 1]
        km = Mol[i, 2]
        ii - glno[no, dir]
        if ii > 0:
            K[int(ii), int(ii)] = K[int(ii), int(ii)] + km

    if nm > 0:
        print(f'-------------------------------------------------')


    GlobalFrame.K = K

    return K



# ================================= ElmGl ==================================
#
# Esta funcao retorna os graus de liberdade do elemento de trelica.
#
#  elm  - elemento                                                    (in)
#  glno - matriz contendo os gl de todos os nos                       (in)
#  ngle - numero de gl do elemento                                    (out)
#  gle  - vetor com os gl do elemento                                 (out)
#
def ElmGl(elm, glno):

    tipo = elm[0]
    no1 = elm[3]
    no2 = elm[4]
    if tipo == 1:   # Trelica plana
        ngle = 4
        gle = [glno[no1, 0], glno[no1, 1], glno[no2, 0], glno[no2, 1]]
    elif tipo == 2: # Viga
        ngle =  4
        gle = [glno[no1, 1], glno[no1, 5], glno[no2, 1], glno[no2, 5]]
    elif tipo == 3:
        ngle = 6    # Portico plano
        gle = [glno[no1, 0], glno[no1, 1], glno[no1, 5], glno[no2, 0], glno[no2, 1], glno[no2, 5]]
    elif tipo == 4:
        ngle = 6    # Grelha
        gle = [glno[no1, 2], glno[no1, 3], glno[no1, 4], glno[no2, 2], glno[no2, 3], glno[no2, 4]]
    elif tipo == 5:
        ngle = 12
        gle = [glno[no1, 0], glno[no1, 1], glno[no1, 2],
               glno[no1, 3], glno[no1, 4], glno[no1, 5],
               glno[no2, 0], glno[no2, 1], glno[no2, 2],
               glno[no2, 3], glno[no2, 4], glno[no2, 5]]
    else:
        print('Erro: elemento invalido!')
        print()

    return ngle, gle


# =============================== ElmEngPerf ===============================
#
# Esta funcao chama a funcao de calculo da matriz de rigidez no sistema
# global de acordo com o tipo do elemento e retorna a matriz calculada.
#
#  e    - indice do elemento cujas forcas serao calculadas            (in)
#  Elm  - matriz com os dados (tipo, mat, sec, no1, no2)              (in)
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Fq   - matriz com as cargas distribuidas                           (in)
#  sis  - sistema utilizado para calculo ('global' ou 'local')        (in)
#  f0   - vetor forcas de engastamento perfeito (ngle)                (out)
#
def ElmEngPerf(e, Elm, No, Fq, sis, Elements):
    
    # Inicializacao

    elm = Elm[e]
    tipo = elm[0]
    if tipo == 1:       # Trelica plana
        f0 = np.zeros((4, 1))
    elif tipo == 2:     # Viga
        f0 = np.zeros((4, 1))
    elif tipo == 3:     # Portico plano
        f0 = np.zeros((6, 1))
    elif tipo == 4:     # Grelha
        f0 = np.zeros((6, 1))
    elif tipo ==5:      # Portico espacial
        f0 = np.zeros((12, 1))
    else:
        print(f'Error: invalid element!')
        return

    # Soma as forcas aplicadas sobre o elemento (sistema local)

    nq = len(Fq)
    for i in range(0, nq):
        carga = Fq[i]
        if e == carga[0]:   # Verifica se a carga esta sobre o elemento
            if tipo == 2:   # Viga
                fe = Load_vector.ElmEngPerfViga(elm, No, carga)
            elif tipo == 3: # Portico plano
                fe = Load_vector.ElmEngPerfPort2D(elm, No, carga)
            elif tipo == 4: # Grelha
                fe = Load_vector.ElmEngPerfGrelha(elm, No, carga)
            elif tipo == 5: # Portico espacial
                fe = Load_vector.ElmEngPerfPort3D(elm, No, carga)

            f0 = f0 + fe


    # Transforma para o sistema global (se necessario)

    if sis == 'local':
        pass
        '''print('f0')
        print(f0)'''
        return f0


    T = Elements[e].T
    T = np.matrix.transpose(np.array(T))

    f0 = np.dot(T, f0)

    return f0


# =============================== ElmIntFor ================================
#
# Esta funcao chama a funcao de calculo do vetor de forcas internas de
# acordo com o tipo do elemento e retorna o vetor calculado.
#
#  e    - indice do elemento cujas forcas serao calculadas            (in)
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Mat  - matriz com as propriedades dos materiais                    (in)
#  Sec  - matriz com as propriedades das secoes                       (in)
#  Elm  - matriz com os dados (tipo, mat, sec, no1, no2)              (in)
#  Fq   - matriz com as cargas distribuidas                           (in)
#  desl - matriz com os deslocamentos dos nos                         (in)
#  gl   - vetor de forcas internas no sistema local (ngle)            (out)
#  g    - vetor de forcas internas no sistema global (ngle)           (out)
#
def ElmIntFor(e, No, Mat, Sec, Elm, Fq, desl, Elements):

    # Calcula a matriz de rigidez no sistema local e a matriz de transformacao.

    T = Elements[e].T
    Kl = Elements[e].Kel

    elm  = Elm[e]
    tipo = elm[0]


    # Calcula os esforcos de engastamento perfeito.

    f0 = ElmEngPerf(e, Elm, No, Fq, 'local', Elements)

    # Extrai os deslocamentos do elemento e calcula das forcas internas.
    u=[]
    u1  = ElmDesl(elm, desl)     # Deslocamentos do elemento no sistema global
    for i in u1:
        u.append([i])

    ul = np.dot(T, np.array(u))           # Deslocamentos do elemento no sistema local
    gl = np.dot(Kl, ul) + f0    # Forcas internas do elemento no sistema local
    g  = np.dot(np.matrix.transpose(np.array(T)), np.array(gl))              # Forcas internas do elemento no sistema global
    return gl, g, ul




# =============================== ElmMatRig ================================
#
# Esta funcao chama a funcao de calculo da matriz de rigidez no sistema
# local e da matriz de transformacao de acordo com o tipo do elemento e
# retorna a matriz do elemnto no sistema global.
#
#  elm  - elemento (tipo, mat, sec, no1, no2)                         (in)
#  No   - matriz com as coordenadas (x, y, z) dos nos                 (in)
#  Mat  - matriz com as propriedades dos materiais                    (in)
#  Sec  - matriz com as propriedades das secoes                       (in)
#  K    - matriz de rigidez (ngle x ngle)                             (out)
#
def ElmMatRig(ne, elm, No, Mat, Sec, Elements):

    # Calcula a matriz de rigidez no sistema local e a matriz de transformacao.

    tipo = elm[0]
    if tipo == 1:     # Trelica plana
        Kl = Stiffness_matrix.ElmMatRigTrel2D(elm, No, Mat, Sec)
    elif tipo == 2: # Viga
        Kl = Stiffness_matrix.ElmMatRigViga(elm, No, Mat, Sec)
    elif tipo == 3: # Portico plano
        Kl = Stiffness_matrix.ElmMatRigPort2D(elm, No, Mat, Sec)
    elif tipo == 4: # Grelha
        Kl = Stiffness_matrix.ElmMatRigGrelha(elm, No, Mat, Sec)
    elif tipo == 5:
        Kl = Stiffness_matrix.ElmMatRigPort3D(elm, No, Mat, Sec)
    else:
        print(f'Erro: elemento invalido!')
        return


    # Transforma a matriz para o sistema global.
    
    T = Elements[ne].T

    T = np.array(T)
    K = np.dot(np.dot(np.matrix.transpose(T), Kl), T)

    return  K, Kl