from random import random, gauss
from copy import deepcopy
from util import error


def create_empty_matrix(nbCells, marge=0):  # Créer une matrice vide
    if nbCells <= 0:
        error("Le nombre de cellules doit être strictement positif")
        return
    if marge < 0:
        error("La marge doit être un nombre positif")
        return
    n = nbCells + 2 * marge
    matrix = []
    for i in range(n):
        matrix.append([0.0] * n)
    return matrix


def xy_to_ij(lst_xy, n_size_mat):  # Convertisseur de coordonnées xy en ij
    x = lst_xy[0]
    y = lst_xy[1]
    if x < 0 or y < 0:
        error("Les coordonnées x et y doivent être positives")
        return
    if n_size_mat <= 0:
        error("La taille de la matrice doit être strictement positive")
        return
    return [n_size_mat - 1 - y, x]


# Les 3 fonctions d'affichage de matrices
def affiche_matrice(matrix):
    for line in matrix:
        for element in line:
            print(round(element, 2), end=" ")
        print()


def affiche_matrix_bool(matrix):
    for line in matrix:
        for element in line:
            display = ". "
            if element > 0.0:
                display = "# "
            print(display, end="")
        print()


def affiche_matrice_energy(matrix):
    for line in matrix:
        for element in line:
            display = "--"
            if element > 0.01:
                display = ". "
            if element > 0.25:
                display = "o "
            if element > 0.5:
                display = "* "
            if element > 0.75:
                display = "# "
            print(display, end="")
        print()


# Génération la particule de manière aléatoire
def generate_partic_coords(Xwidth):
    if Xwidth <= 0:
        error("La longueur du détecteur doit être strictement positive")
        return
    x = Xwidth * random()
    y = Xwidth * random()
    return [x, y]


# Séparer les coordonnées entière et fractionnaire de la cellules
def calc_all_coords(lst_coords_in_det, cell_width):
    if cell_width <= 0:
        error("La taille des cellules doit être strictement positive")
        return
    x = lst_coords_in_det[0] / cell_width
    y = lst_coords_in_det[1] / cell_width
    if x <= 0 or y <= 0:
        error("Les coordonnées x et y doivent être strictement positives")
        return
    int_x = int(x)
    int_y = int(y)
    decimal_x = x - int_x
    decimal_y = y - int_y
    return [int_x, int_y], [decimal_x, decimal_y]


# Fonction fournie pour calculer les dépôts d'énergie
def calculate_fraction_E_in_cells(lst_coords_in_cell, matE, Xwidth, n_cells):
    mat_size = 5
    if len(matE) != mat_size:
        print(
            "\n\n*** ATTENTION ***\nLa taille de la matrice fournie en argument de calculate_fraction_E_in_cells n'a pas l'air correcte.\nSortie anormale de la fonction.\n\n\n")
        return
    if Xwidth != 100:
        print("\n\n*** ATTENTION ***\nLa largeur de detecteur recue est", Xwidth,
              "cm au lieu de 100 cm.\nSortie anormale de la fonction.\n\n\n")
        return
    if not (5 <= n_cells <= 50):
        print("\n\n*** ATTENTION ***\nLe nombre", n_cells,
              " de cellules recu est invalide.\nSortie anormale de la fonction.\n\n\n")
        return
    # Quick trick to see an actual center for large n_cells and still keep fluctuations for low n_cells:
    # nbTirages = int(100 * (n_cells / 20))
    # Let's not use it eventually, fluctuations may be closer to reality this way.
    nbTirages = 100
    # Calo config rather than pixel. In this situation, shower width = 2.5 cm (a-la Moliere radius). In variable
    # sigma though, shower width is stored in units of cell width. Therefore, sigma = 2.5cm / cell_width, ie sigma =
    # 2.5cm * n_cells / detector_width. 1st limit is when 3 sigmas (in cm) becomes larger than 5x5 matrix.py diagonal =
    # 2.5 cell_width sqrt(2). This gives n_cells < 2.5 Xwidth sqrt(2) / 3*2.5cm ~ 47. 2nd limit is when 3 sigmas (in
    # cm) is all in a single tower, ie n_cells > Xwidth / 3sigma ~ 13.
    sigma = 2.5 * n_cells / Xwidth
    # Just in case the user doesn't provide an empty matrix.py...
    matRdm = create_empty_matrix(mat_size)
    for i in range(0, nbTirages):
        xRdm = gauss(float(mat_size // 2) + lst_coords_in_cell[0], sigma)
        yRdm = gauss(float(mat_size // 2) + lst_coords_in_cell[1], sigma)
        # In rare cases the random number is picked outside the interval [0,mat_size[, which triggers an out-of-range
        # error when used in xy_to_ij / matRdm.
        if xRdm < 0:
            xRdm = 0
        if yRdm < 0:
            yRdm = 0
        if xRdm >= mat_size:
            xRdm = mat_size - 0.001
        if yRdm >= mat_size:
            yRdm = mat_size - 0.001
        lst_Rdm = xy_to_ij([int(xRdm), int(yRdm)], mat_size)
        matRdm[lst_Rdm[0]][lst_Rdm[1]] += 1
    for i in range(mat_size):
        for j in range(mat_size):
            matE[i][j] = matRdm[i][j] / nbTirages


# Dissipation de l'énergie
def smear_energy(matrix):
    copy_matrix = deepcopy(matrix)
    for line in copy_matrix:
        for index in range(len(line)):
            line[index] *= gauss(1, 0.05)
    return copy_matrix


# Application du seuil de détection
def apply_threshold(matrix):
    for line in matrix:
        for index in range(len(line)):
            if line[index] < 0.05:
                line[index] = 0.0


# Simulation complète du signal
def simulate_signal(lst_coords_in_cell, Xwidth, N):
    if Xwidth <= 0:
        error("La longueur du détecteur doit être strictement positive")
        return
    if N <= 0:
        error("Le nombre de cellules doit être strictement positif")
        return
    matrix = create_empty_matrix(5)
    calculate_fraction_E_in_cells(lst_coords_in_cell, matrix, Xwidth, N)
    smeared_matrix = smear_energy(matrix)
    apply_threshold(smeared_matrix)
    return smeared_matrix


# Lancer la particule sur le détecteur
def launch_particle_on_detector(Xwidth, N, n, matrix):
    if Xwidth <= 0:
        error("La longueur du détecteur doit être strictement positive")
        return
    size = N + 2 * n
    if len(matrix) != size:
        error(
            "La taille de la matrice doit correspondre à la taille calculée à partir du nombre de cellules et de la marge")
        return
    for line in matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return
    if size < 5:
        error("La taille de la matrice doit être supérieure ou égale à 5")
        return
    cell_width = Xwidth / N
    lst_coords_in_det = generate_partic_coords(Xwidth)
    lst_coords_xy, lst_coords_in_cell = calc_all_coords(lst_coords_in_det, cell_width)
    lst_coords_ij = xy_to_ij(lst_coords_xy, N)
    signal_matrix = simulate_signal(lst_coords_in_cell, Xwidth, N)
    i = lst_coords_ij[0]
    j = lst_coords_ij[1]
    signal_matrix_size = len(signal_matrix)
    for signal_i in range(signal_matrix_size):
        for signal_j in range(signal_matrix_size):
            new_i = i + signal_i + n - 2  # On change les index pour faire correspondre les éléments des deux matrices
            new_j = j + signal_j + n - 2
            if (0 <= new_i < size) and (0 <= new_j < size):
                matrix[new_i][new_j] += signal_matrix[signal_i][signal_j]
    return lst_coords_in_det


# Ajout de bruit
def add_noise(matrix, ratio=0.05):
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if random() < ratio:
                matrix[i][j] += 0.1 * random()


# Lancement de plusieurs particules
def create_event(Xwidth, N, n, matrix, particles, noise_ratio):
    if particles <= 0:
        error("Le nombre de particules doit être strictement positif")
        return
    if noise_ratio < 0 or noise_ratio > 0.1:
        error("La proportion de cellules touchées par le bruit doit être comprise entre 0.0 et 0.1")
        return
    all_coords = []
    add_noise(matrix, noise_ratio)  # On ajoute le bruit avant de faire toutes les autres opérations
    for i in range(particles):
        coords = launch_particle_on_detector(Xwidth, N, n, matrix)
        all_coords.append(coords)
    for i in range(n):  # On supprime les marges
        matrix.pop(0)
        matrix.pop(-1)
    for i in range(n):
        for line in matrix:
            line.pop(0)
            line.pop(-1)
    return all_coords
