from util import error, sub_list
from math import log
from copy import deepcopy


# Fonction inverse de xy_to_ij
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


# On reconstitue les coordonnées d'une particule sur le détecteur entier
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
                x_rec += (0.5 + x) * weight
                y_rec += (0.5 + y) * weight
    x_rec *= cell_width / total_weight
    y_rec *= cell_width / total_weight
    return [x_rec, y_rec]


# Est-ce que la cellule est déjà sur le cluster ?
def is_cell_in_cluster(cluster, cell):
    i = cell[0]
    j = cell[1]
    for candidate in cluster:
        if i == candidate[0] and j == candidate[1]:
            return True
    return False


# Fonction récursive pour déterminer les cellules voisines
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


# Est-ce que la matrice est vide ?
def is_matrix_empty(matrix):
    for line in matrix:
        for element in line:
            if element > 0.0:
                return False
    return True


# Création de la liste de clusters
def clusterize(matrix):
    copy_matrix = deepcopy(matrix)
    size = len(copy_matrix)
    for line in copy_matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return

    clusters = []
    while not is_matrix_empty(copy_matrix):
        max_cell = [0, 0, 0.0]
        for i in range(size):
            for j in range(size):
                energy = copy_matrix[i][j]
                if energy > max_cell[2]:
                    max_cell = [i, j, energy]
        cluster = []
        loop_clusterize(cluster, copy_matrix, max_cell)
        for cell in cluster:
            i = cell[0]
            j = cell[1]
            copy_matrix[i][j] = 0.0
        clusters.append(cluster)
    return clusters


# Reconstitution des coordonnées dans un cluster
def mesure_xy_cluster(matrix, cell_width, cluster, has_energy=True):
    size = len(matrix)
    for line in matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return
    x_rec = 0
    y_rec = 0
    total_weight = 0
    for cell in cluster:
        energy = cell[2]
        if energy > 0:
            weight = 1
            if has_energy:
                weight = log(2 + energy)
            total_weight += weight
            x = cell[0]
            y = cell[1]
            x_rec += (0.5 + x) * weight
            y_rec += (0.5 + y) * weight
    x_rec *= cell_width / total_weight
    y_rec *= cell_width / total_weight
    return [x_rec, y_rec]


# --- CETTE PARTIE N'EST PAS TERMINEE --- Elle concerne l'estimation des performances du détecteur avec les clusters


# Fonction récursive pour le tri fusion
def fusion(lst_a, lst_b, isCell=True):
    n_a = len(lst_a)
    n_b = len(lst_b)
    if n_a == 0:
        return lst_b
    if n_b == 0:
        return lst_a
    if isCell:
        if lst_a[0][2] <= lst_b[0][2]:
            return [lst_a[0]] + fusion(sub_list(lst_a, 1, n_a), lst_b, isCell)
    else:
        if lst_a[0][0][2] <= lst_b[0][0][2]:
            return [lst_a[0]] + fusion(sub_list(lst_a, 1, n_a), lst_b, isCell)
    return [lst_b[0]] + fusion(lst_a, sub_list(lst_b, 1, n_b), isCell)


# Tri fusion récursif
def fusion_sort(lst, isCell=True):
    n = len(lst)
    if n <= 1:
        return lst
    mid = n // 2
    return fusion(fusion_sort(sub_list(lst, 0, mid)), fusion_sort(sub_list(lst, mid, n)), isCell)


# Tri des clusters et des vraies coordonnées des particules par ordre croissant d'énergie afin de les faire correspondre pour les calculs statistiques des performances
def sort_cluster_and_vrai(matrix, clusters, coords_vrai_ij):
    cells_vrai = []
    for lst_coords_ij in coords_vrai_ij:
        i = lst_coords_ij[0]
        j = lst_coords_ij[1]
        cells_vrai.append([i, j, matrix[i][j]])
    sorted_clusters = fusion_sort(clusters, False)
    sorted_cells_vrai = fusion_sort(cells_vrai)
    return sorted_clusters, sorted_cells_vrai


# Conversion des cellules d'un cluster en coordonnées ij vers xy
def cluster_ij_to_xy(matrix, cluster):
    size = len(matrix)
    for cell in cluster:
        i = cell[0]
        j = cell[1]
        lst_xy = ij_to_xy([i, j], size)
        x = lst_xy[0]
        y = lst_xy[1]
        cell[0] = x
        cell[1] = y
