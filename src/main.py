from util import StructuralAnalysis


# ================ INPUT PARAMETERS ================
b = 0.15
h = 0.5

# Portico Plano - Exemplo 1 - Aula.
E = 20.5 * 10**9        # Modulo de elasticidade (kN/m2)
G = E
A = b * h          # Area (m2)
Iz = (b * h**3) / 12          # Momento de inercia (m4)
Iy = (h * b**3) / 12
J = Iz

# coordenadas dos elementos
No  = [[0.0, 0.0, 0.0],  # Coordenadas x, y, z
       [0.0, 3.0, 0.0],
       [3.0, 3.0, 0.0],
       [3.0, 0.0, 0.0]]


# graus de liberdade nos apoios
Sup = [[0, 1, 1, 0, 0, 0, 0], # No, u, v, w, rx, ry, rz (0 = livre / 1 = fixo)
       [3, 1, 1, 0, 0, 0, 0]]

# mola em um dos nos
Mol = []             # No, dir, km

# propriedade do material
Mat = [[E, G]]            # Modulos de elasticidade

# Propriedade da secao transversal
Sec = [[A, Iz, J, Iy]]         # Area, Iz, J, Iy

# Determina os elementos, tipo, Mat, Sec, No1, No2
Elm = [[3, 0, 0, 0, 1],     # Tipo (1=Trelica plana, 2=Viga, 3=Portico plano, 4=Grelha, 5=Portico Espacial), Mat, Sec, No1, No2
       [3, 0, 0, 1, 2],
       [3, 0, 0, 2, 3]]

# forca nodais
Fno = [[1, 5, 0, 0, 0, 0, 0]]         # No, Fx, Fy, Fz, Mx, My, Mz

# reacao de engaste perfeito forca distribuida no elemento
Fq  = [[1,0,0,-20,0]]  # Elm, sistema local (0/1), qx, qy, qz

# ==================================================
# ==================================================

print('EA = ', E*A)
print('EI = ', E*Iz)


# ================ STRUCTURAL ANALYSIS ================
structure = StructuralAnalysis(No, Sup, Mol, Mat, Sec, Elm, Fno, Fq)
Elements, GlobalFrame = structure.analysis(printGeometry=True)


# ================ PRINT RESULTS ================
# Print all data
# Local elements data
print_results = True

if print_results:
    for element in Elements:
        element.printData()

    # Global elements data
    GlobalFrame.printData()

    print('Elements reactions g_local (Internal Reactions):')
    print('\nCompression 1\nShear 1\nMoment 1\nCompression 2\nShear 2\nMoment 2')
    for element in Elements:
        print()
        print(element.gl)