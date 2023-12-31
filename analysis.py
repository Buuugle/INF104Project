from util import error
from math import log
from copy import deepcopy

# Ce fichier contient toutes les fonctions liées à l'analyse des données fournies par la simulation


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
    for i in range(size):  # Application des sommes sous la forme de boucle
        for j in range(size):
            energy = matrix[i][j]
            if energy > 0:
                weight = 1
                if has_energy:  # Option pour utiliser ou non l'énergie de la cellule comme un poids pour la somme
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


# Fonction récursive pour déterminer les cellules voisines
def loop_clusterize(cluster, matrix, cell, threshold=0.0):
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
    matrix[i][j] = 0.0  # On réinitialise la cellule de la matrice pour qu'elle ne soit pas prise en compte dans les prochaines itérations de la fonction récursive
    for delta in deltas:
        other_i = i + delta[0]
        other_j = j + delta[1]
        if 0 <= other_i < size and 0 <= other_j < size:
            other_energy = matrix[other_i][other_j]
            other_cell = [other_i, other_j, other_energy]
            if other_energy > threshold:
                loop_clusterize(cluster, matrix, other_cell)  # La récursion a lieu ici


# Est-ce que la matrice est vide ?
def is_matrix_empty(matrix, threshold=0.0):  # threshold représente le seuil à partir duquel on considère une cellule vide
    for line in matrix:
        for element in line:
            if element > threshold:
                return False
    return True


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


# Création de la liste de clusters
def clusterize(matrix, threshold=0.0):
    copy_matrix = deepcopy(matrix)
    size = len(copy_matrix)
    for line in copy_matrix:
        if len(line) != size:
            error("La matrice doit être carrée")
            return
    clusters = []
    while not is_matrix_empty(copy_matrix, threshold):  # On applique la détection de cluster tant qu'il reste des cellules
        max_cell = [0, 0, 0.0]
        for i in range(size):
            for j in range(size):
                energy = copy_matrix[i][j]
                if energy > max_cell[2]:
                    max_cell = [i, j, energy]
        cluster = []
        loop_clusterize(cluster, copy_matrix, max_cell, threshold)
        cluster_ij_to_xy(matrix, cluster)  # On convertit les coordonnées ij en xy seulement ici, car on a besoin des coordonnées ij pour la récursivité
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
    for cell in cluster:  # Le code est très similaire à mesure_xy, mais on se limite ici au cluster
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


def link_rec_true_coords(rec_coords_list, init_true_coords_list):  # Permet de lier les coordonnées réelles à celles reconstituées (sous la forme de couple) afin de pouvoir les comparer
    linked_coords_list = []
    true_coords_list = init_true_coords_list.copy()
    for rec_coords in rec_coords_list:  # On minimise l'écart entre les coordonnées réelles et reconstituées pour former un couple
        if len(true_coords_list) == 0:
            return linked_coords_list
        true_coords = true_coords_list[0]
        true_x = true_coords[0]
        true_y = true_coords[1]
        rec_x = rec_coords[0]
        rec_y = rec_coords[1]
        min_distance = abs(rec_x - true_x) + abs(rec_y - true_y)
        min_index = 0
        for index in range(1, len(true_coords_list)):  # L'indice 0 a déjà été vérifié avant la boucle
            true_coords = true_coords_list[index]
            true_x = true_coords[0]
            true_y = true_coords[1]
            distance = abs(rec_x - true_x) + abs(rec_y - true_y)  # Cette distance ne représente pas de grandeur réelle, c'est un nombre indicatif pour comparer les coordonnées entre elle
            if distance < min_distance:
                min_distance = distance
                min_index = index
        linked_coords_list.append(true_coords_list[min_index])
        true_coords_list.pop(min_index)  # On retire la coordonnée afin qu'elle ne soit pas dans deux couples en même temps
    for true_coords in true_coords_list:
        linked_coords_list.append(true_coords)  # Les coordonnées vraies restantes ne sont pas associées à des coordonnées reconstituées
    return linked_coords_list  # La liste retournée contient les coordonnées réelles. Les coordonnées réelles et reconstituées d'un même couple ont le même indice dans les deux listes réelle et reconstituée
