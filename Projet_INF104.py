from copy import deepcopy
from math import sqrt
from random import random, gauss


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def create_empty_matrix(x_width, marge=0):
    matrix = []
    i = 0
    while i < x_width + marge * 2:
        matrix.append([0] * (x_width + marge * 2))
        i += 1
    return matrix


def xy_to_ij(lst_xy, n_size_mat):
    return [n_size_mat - lst_xy[1] - 1, lst_xy[0]]


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def affiche_matrice(matrix):
    for line in matrix:
        for e in line:
            print(e, end=" ")
        print()
    return


def affiche_matrice_bool(matrix):
    for line in matrix:
        for e in line:
            if e != 0:
                print("#", end=" ")
            else:
                print(".", end=" ")
        print()
    return


def affiche_matrice_energy(matrix):
    for line in matrix:
        for e in line:
            if e > 0.75:
                print("#", end=" ")
            elif e > 0.5:
                print("*", end=" ")
            elif e > 0.25:
                print("o", end=" ")
            elif e > 0.01:
                print(".", end=" ")
            else:
                print("--", end="")
        print()
    return


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def generate_particle_coords(x_width):
    return [random() * x_width, random() * x_width]


def calc_all_coords(lst_coords_in_det, len_cell):
    lst_cell_coords = [int(lst_coords_in_det[0] // len_cell), int(lst_coords_in_det[1] // len_cell)]
    lst_coords_in_cell = [(lst_coords_in_det[0] % len_cell) / len_cell, (lst_coords_in_det[1] % len_cell) / len_cell]
    return lst_cell_coords, lst_coords_in_cell


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def calculate_fraction_e_in_cells(lst_coords_in_cell, mat_e, x_width, n_cells):
    mat_size = 5
    if len(mat_e) != mat_size:
        print(
            "\n\n*** ATTENTION ***\nLa taille de la matrice fournie en argument de calculate_fraction_E_in_cells n'a "
            "pas l'air correcte.\nSortie anormale de la fonction.\n\n\n")
        return None
    if x_width != 100:
        print("\n\n*** ATTENTION ***\nLa largeur de détecteur recue est", x_width,
              "cm au lieu de 100 cm.\nSortie anormale de la fonction.\n\n\n")
        return None
    if not (5 <= n_cells <= 50):
        print("\n\n*** ATTENTION ***\nLe nombre", n_cells,
              " de cellules recu est invalide.\nSortie anormale de la fonction.\n\n\n")
        return None
    # Quick trick to see an actual center for large n_cells and still keep fluctuations for low n_cells:
    # nb_tirages = int(100 * (n_cells / 20))
    # Let's not use it eventually, fluctuations may be closer to reality this way.
    nb_tirages = 100
    # Calo config rather than pixel. In this situation, shower width = 2.5 cm (a-la Moliere radius). In variable
    # sigma though, shower width is stored in units of cell width. Therefore, sigma = 2.5cm / cell_width, ie sigma =
    # 2.5cm * n_cells / detector_width. 1st limit is when 3 sigmas (in cm) becomes larger than 5x5 matrix diagonal =
    # 2.5 cell_width sqrt(2). This gives n_cells < 2.5 x_width sqrt(2) / 3*2.5cm ~ 47. 2nd limit is when 3 sigmas (in
    # cm) is all in a single tower, ie n_cells > x_width / 3sigma ~ 13.
    sigma = 2.5 * n_cells / x_width
    # Just in case the user doesn't provide an empty matrix...
    mat_rdm = create_empty_matrix(mat_size)
    for i in range(0, nb_tirages):
        x_rdm = gauss(float(mat_size // 2) + lst_coords_in_cell[0], sigma)
        y_rdm = gauss(float(mat_size // 2) + lst_coords_in_cell[1], sigma)
        # In rare cases the random number is picked outside the interval [0,mat_size[, which triggers an out-of-range
        # error when used in xy_to_ij / mat_rdm.
        if x_rdm < 0:
            x_rdm = 0
        if y_rdm < 0:
            y_rdm = 0
        if x_rdm >= mat_size:
            x_rdm = mat_size - 0.001
        if y_rdm >= mat_size:
            y_rdm = mat_size - 0.001
        lst_rdm = xy_to_ij([int(x_rdm), int(y_rdm)], mat_size)
        mat_rdm[lst_rdm[0]][lst_rdm[1]] += 1
    for i in range(mat_size):
        for j in range(mat_size):
            mat_e[i][j] = mat_rdm[i][j] / nb_tirages
    return None


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def smear_energy(mat_e):
    mat_e_smear = deepcopy(mat_e)
    moy = 1
    sigma = 0.05
    i = 0
    while i < len(mat_e_smear):
        j = 0
        while j < len(mat_e_smear[i]):
            mat_e_smear[i][j] *= gauss(moy, sigma)
            j += 1
        i += 1
    return mat_e_smear


def apply_threshold(mat_e_smear):
    i = 0
    while i < len(mat_e_smear):
        j = 0
        while j < len(mat_e_smear[i]):
            if mat_e_smear[i][j] < 0.05:
                mat_e_smear[i][j] = 0
            j += 1
        i += 1
    return


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def simulate_signal(lst_coords_in_cell, x_width, n_cells):
    mat_e = create_empty_matrix(5)
    calculate_fraction_e_in_cells(lst_coords_in_cell, mat_e, x_width, n_cells)
    mat_e = smear_energy(mat_e)
    apply_threshold(mat_e)
    return mat_e


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def launch_particle_on_detector(x_width, n_cells, marge, matrice):
    lst_coords_in_det = [None] * 2
    lst_coords_in_det[0], lst_coords_in_det[1] = generate_particle_coords(x_width)  # lst_coords_in_det = generate...?
    len_cell = x_width / n_cells
    lst_coords_in_det[0] += len_cell * marge
    lst_coords_in_det[1] += len_cell * marge
    lst_xy, lst_coords_in_cell = calc_all_coords(lst_coords_in_det, len_cell)
    lst_ij = xy_to_ij(lst_xy, n_cells + 2 * marge)
    mat_e = simulate_signal(lst_coords_in_cell, x_width, n_cells)
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            matrice[lst_ij[0] - 2 + i][lst_ij[1] - 2 + j] += mat_e[i][j]
            j += 1
        i += 1
    lst_coords_in_det[0] -= len_cell * marge
    lst_coords_in_det[1] -= len_cell * marge
    return lst_coords_in_det


def create_event(x_width, n_cells, marge, matrice, n_particles):
    lst_coords_particles = []
    i = 0
    while i < n_particles:
        lst_coords_particles.append(launch_particle_on_detector(x_width, n_cells, marge, matrice))
        i += 1
    for i in range(marge):
        matrice.pop(0)
        matrice.pop(-1)
    for line in matrice:
        for i in range(marge):
            line.pop(0)
            line.pop(-1)
    return lst_coords_particles


def mon_main(n_cells):
    x_width = 100
    marge = 2
    n_events = int(input("Nombre d'événements à simuler : "))
    n_particles = int(input("Nombre de particules par événement : "))
    for i in range(n_events):
        detector = create_empty_matrix(n_cells, marge)
        create_event(x_width, n_cells, marge, detector, n_particles)
        print()
        affiche_matrice_energy(detector)
    return


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def mesure_xy(detector, len_cell, with_energy=True):
    x_rec = 0
    y_rec = 0
    if with_energy:
        e_cells_touched = 0
        i = 0
        while i < len(detector):
            j = 0
            while j < len(detector[i]):
                energy = detector[i][j]
                if energy > 0:
                    e_cells_touched += energy
                    x_rec += j * energy
                    y_rec += (len(detector) - i - 1) * energy
                j += 1
            i += 1
        x_rec /= e_cells_touched
        y_rec /= e_cells_touched
        return [x_rec * len_cell, y_rec * len_cell]

    n_cells_touched = 0
    i = 0
    while i < len(detector):
        j = 0
        while j < len(detector[i]):
            print(detector[i][j])
            if detector[i][j] > 0:
                n_cells_touched += 1
                x_rec += j
                y_rec += len(detector) - i - 1
            j += 1
        i += 1
    x_rec /= n_cells_touched
    y_rec /= n_cells_touched
    return [x_rec * len_cell, y_rec * len_cell]


# ------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------#


def mon_main2(n_cells):
    x_width = 100
    marge = 2
    n_events = int(input("Nombre d'événements à simuler : "))
    n_particles = int(input("Nombre de particules par événement : "))
    avec_energie = bool(input("Avec énergie (True/False)? "))
    d_xy = [[], []]
    for i in range(n_events):
        detector = create_empty_matrix(n_cells, marge)
        xy_vrai = create_event(x_width, n_cells, marge, detector, n_particles)
        print()
        affiche_matrice_energy(detector)
        xy_rec = mesure_xy(detector, x_width / n_cells, avec_energie)
        j = 0
        while j < len(xy_vrai):
            d_xy[0].append(xy_rec[0] - xy_vrai[j][0])
            d_xy[1].append(xy_rec[1] - xy_vrai[j][1])
            print(xy_vrai[j][0], xy_vrai[j][1])
            j += 1
    n_mesures = len(d_xy[0])
    moyenne = [0, 0]
    ecart_type = [0, 0]
    for i in range(2):
        for j in range(n_mesures):
            moyenne[i] += d_xy[i][j]
        moyenne[i] /= n_mesures
        for j in range(n_mesures):
            # print(d_xy[i][j], moyenne[i], (d_xy[i][j] - moyenne[i])**2)
            ecart_type[i] += (d_xy[i][j] - moyenne[i]) ** 2
        # print(ecart_type)
        ecart_type[i] = sqrt(ecart_type[i] / n_mesures)
    print(d_xy)
    print("précision x :", moyenne[0], "plus ou moins", ecart_type[0], "cm")
    print("précision y :", moyenne[1], "plus ou moins", ecart_type[1], "cm")
    return


mon_main2(10)
