from util import *
from simulation import *
from analysis import *


def main():

    print("=== SIMULATEUR DE CALORIMÈTRE ULTIME ===\n")

    print("--- Propriétés du détecteur ---")
    detector_width = 100
    print("- Taille du détecteur : ", detector_width, "cm", sep="")
    cells = min_int_input("- Nombre de cellules : ", "Le nombre de cellule doit être supérieur ou égal à 5.", 5)
    cell_width = detector_width / cells
    print("- Taille d'une cellule : ", cell_width, "cm", sep="")
    padding = min_int_input("- Nombre de cellules de la marge : ", "La taille de la marge doit être positive.", 0)
    size = cells + 2 * padding
    print("- Nombre total de cellules :", size)

    print("\n--- Propriétés de la simulation ---")
    events = min_int_input("Nombre d'événements : ", "Le nombre d'événement doit être strictement positif.", 1)
    particles = min_int_input("Nombre de particles par événements : ", "Le nombre de particules doit être strictement positif.", 1)
    noise_ratio = range_float_input("Proportions de cellules touchées par le bruit : ", "La proportion de cellules touchées par le bruit doit être comprise entre 0.0 et 0.1.", 0.0, 0.1)

    print("\n--- Début de la simulation ---\n")
    for i in range(1, events + 1):

        matrix = create_empty_matrix(cells, padding)
        true_coords_list = create_event(detector_width, cells, padding, matrix, particles, noise_ratio)
        clusters = clusterize(matrix)
        rec_coords_list = []
        for j in range(len(clusters) - 1, -1, -1):  # On parcourt la liste à l'envers pour ajouter les coordonnées des clusters par odre croissant, car ils sont rangés initialement dans l'ordre décroissant
            cluster = clusters[j]
            rec_coords_list.append(mesure_xy_cluster(matrix, cell_width, cluster))
        affiche_matrice_energy(matrix)
        linked_coords_list = link_rec_true_coords(rec_coords_list, true_coords_list)
        lst_dx = []
        lst_dy = []
        for j in range(len(linked_coords_list)):
            linked_coords = linked_coords_list[j]
            true_coord = true_coords_list[j]
            x_true = true_coord[0]
            y_true = true_coord[1]
            x_link = linked_coords[0]
            y_link = linked_coords[1]
            dx = abs(x_true - x_link)
            dy = abs(y_true - y_link)
            lst_dx.append(dx)
            lst_dy.append(dy)
        print("\n- Événement n°", i, " : ", sep="")
        affiche_matrice_energy(matrix)
        mean_dx = mean(lst_dx)
        mean_dy = mean(lst_dy)
        sigma_dx = standard_deviation(lst_dx)
        sigma_dy = standard_deviation(lst_dy)


if __name__ == "__main__":
    main()
