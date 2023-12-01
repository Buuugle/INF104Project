from util import *


def create_empty_matrix(nbCells, marge=0):
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


def xy_to_ij(lst_xy, n_size_mat):
    x = lst_xy[0]
    y = lst_xy[1]
    if x < 0 or y < 0:
        error("Les coordonnées x et y doivent être positives")
        return
    if n_size_mat <= 0:
        error("La taille de la matrice doit être strictement positive")
        return
    return [n_size_mat - 1 - y, x]


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
