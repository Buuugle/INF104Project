from util import error
from math import log


def ij_to_xy(lst_ij, n_size_mat):
    i = lst_ij[0]
    j = lst_ij[1]
    if i < 0 or j < 0:
        error("Les coordonnées i et j doivent être positives")
        return
    if n_size_mat <= 0:
        error("La taille de la matrice doit être strictement positive")
        return
    return [j, n_size_mat - 1 - i]


def mesure_xy(matrix, cell_width, has_energy=True):
    size = len(matrix)
    for line in matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return
    x_rec = 0
    y_rec = 0
    total_weight = 0
    for i in range(size):
        for j in range(size):
            energy = matrix[i][j]
            if energy > 0:
                weight = 1
                if has_energy:
                    weight = log(2 + energy)
                total_weight += weight
                lst_xy = ij_to_xy([i, j], size)
                x = lst_xy[0]
                y = lst_xy[1]
                x_rec += cell_width * (0.5 + x) * weight
                y_rec += cell_width * (0.5 + y) * weight
    x_rec /= total_weight
    y_rec /= total_weight
    return [x_rec, y_rec]


def is_cell_in_cluster(cluster, cell):
    i = cell[0]
    j = cell[1]
    for candidate in cluster:
        if i == candidate[0] and j == candidate[1]:
            return True
    return False


def loop_clusterize(cluster, matrix, cell):
    size = len(matrix)
    deltas = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]
    ]
    cluster.append(cell)
    i = cell[0]
    j = cell[1]
    for delta in deltas:
        other_i = i + delta[0]
        other_j = j + delta[1]
        if 0 <= other_i < size and 0 <= other_j < size:
            other_energy = matrix[other_i][other_j]
            other_cell = [other_i, other_j, other_energy]
            if other_energy > 0 and not is_cell_in_cluster(cluster, other_cell):
                loop_clusterize(cluster, matrix, other_cell)


def clusterize(matrix):
    size = len(matrix)
    for line in matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return
    max_cell = [0, 0, 0.0]
    for i in range(size):
        for j in range(size):
            energy = matrix[i][j]
            if energy > max_cell[2]:
                max_cell = [i, j, energy]
    cluster = []
    loop_clusterize(cluster, matrix, max_cell)
    for cell in cluster:
        i = cell[0]
        j = cell[1]
        lst_xy = ij_to_xy([i, j], size)
        x = lst_xy[0]
        y = lst_xy[1]
        cell[0] = x
        cell[1] = y
    return cluster
