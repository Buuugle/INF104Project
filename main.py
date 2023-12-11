from util import *
from simulation import *
from analysis import *

# Ce fichier contient la véritable fonction main du programme qui test la version définitive du détecteur de particule (avec les clusters)


def main():

    # On demande à l'utilisateur de saisir les paramètres de la simulation avec des inputs sécurisés

    print("=== PARAMÈTRES DE LA SIMULATION ===\n")

    print("--- Propriétés du détecteur ---")
    detector_width = 100
    print("- Taille du détecteur : ", detector_width, "cm", sep="")
    cells = range_int_input("- Nombre de cellules : ", "Le nombre de cellule doit être compris entre 5 et 50.", 5, 50)
    cell_width = detector_width / cells
    print("- Taille d'une cellule : ", cell_width, "cm", sep="")
    padding = min_int_input("- Nombre de cellules de la marge : ", "La taille de la marge doit être positive.", 0)
    size = cells + 2 * padding
    print("- Nombre total de cellules :", size)
    cluster_threshold = min_float_input("- Seuil de la mise en clusters : ", "Le seuil de la mise en clusters doit être positif.", 0.0)

    print("\n--- Propriétés des événements ---")
    events = min_int_input("- Nombre d'événements : ", "Le nombre d'événement doit être strictement positif.", 1)
    particles = min_int_input("- Nombre de particles par événements : ", "Le nombre de particules doit être strictement positif.", 1)
    noise_ratio = range_float_input("- Proportions de cellules touchées par le bruit : ", "La proportion de cellules touchées par le bruit doit être comprise entre 0.0 et 0.1.", 0.0, 0.1)

    print("\n\n=== DÉMARRAGE DE LA SIMULATION ===")

    all_lst_dx = []
    all_lst_dy = []
    all_success_rec = 0
    for i in range(1, events + 1):  # On simule tous les événements

        matrix = create_empty_matrix(cells, padding)
        true_coords_list = create_event(detector_width, cells, padding, matrix, particles, noise_ratio)
        clusters = clusterize(matrix, cluster_threshold)
        rec_coords_list = []
        for cluster in clusters:
            rec_coords_list.append(mesure_xy_cluster(matrix, cell_width, cluster))
        linked_coords_list = link_rec_true_coords(rec_coords_list, true_coords_list)
        lst_dx = []
        lst_dy = []
        coords_table = [
            ["Coordonnées réelles (x, y)", "Coordonnées reconstituées (x, y)", "Différences (x, y)"]
        ]  # Cette matrice représente un tableau d'affichage des valeurs liées aux coordonnées
        rec_size = len(rec_coords_list)
        success_rec = 0  # Compteur de coordonnées reconstituées
        for j in range(len(linked_coords_list)):  # Dans cette boucle, on calcule les écarts pour chaque couple de coordonnées
            linked_coords = linked_coords_list[j]
            x_true = linked_coords[0]
            y_true = linked_coords[1]
            x_rec = "*****"  # Par défaut, les coordonnées ne sont pas forcément reconstituées, donc on met des étoiles à la place des valeurs pour signifier l'absence de données
            y_rec = "*****"
            dx = "*****"
            dy = "*****"
            if j < rec_size:  # Si le couple existe, les coordonnées ont été reconstituées avec succès
                rec_coords = rec_coords_list[j]
                x_rec = rec_coords[0]
                y_rec = rec_coords[1]
                dx = abs(x_true - x_rec)
                dy = abs(y_true - y_rec)
                lst_dx.append(dx)
                lst_dy.append(dy)
                dx = str(round(dx, 2))
                dy = str(round(dy, 2))
                x_rec = str(round(x_rec, 2))
                y_rec = str(round(y_rec, 2))
                success_rec += 1
            x_true = str(round(x_true, 2))
            y_true = str(round(y_true, 2))
            coords_table.append([  # On ajoute une ligne au tableau d'affichage pour afficher les données
                "(" + x_true + ", " + y_true + ")",
                "(" + x_rec + ", " + y_rec + ")",
                "(" + dx + ", " + dy + ")"
            ])
        all_lst_dx.extend(lst_dx)  # On utilisera ces listes pour les calculs de statistiques globaux
        all_lst_dy.extend(lst_dy)
        all_success_rec += success_rec
        mean_dx = round(mean(lst_dx), 2)
        mean_dy = round(mean(lst_dy), 2)
        sigma_dx = round(standard_deviation(lst_dx), 2)
        sigma_dy = round(standard_deviation(lst_dy), 2)

        # On affiche toutes les informations
        print("\n--- Événement n°" + str(i) + " ---")
        print("- Détecteur :")
        affiche_matrice_energy(matrix)
        print("- Résumé des mesures en cm :")
        print_table(coords_table)  # Voir util.py
        print("- Moyenne des différences en cm (x, y) : (", mean_dx, ", ", mean_dy, ")", sep="")
        print("- Écart type des différences en cm (x, y) : (", sigma_dx, ", ", sigma_dy, ")", sep="")
        print("- Nombre de coordonnées de particules reconstituées : ", success_rec, "/", particles, sep="")

    total_mean_dx = round(mean(all_lst_dx), 2)
    total_mean_dy = round(mean(all_lst_dy), 2)
    total_sigma_dx = round(standard_deviation(all_lst_dx), 2)
    total_sigma_dy = round(standard_deviation(all_lst_dy), 2)
    ratio_success = round(all_success_rec / (particles * events) * 100, 2)

    print("\n--- Statistiques finaux ---")
    print("- Moyenne totale des différences en cm (x, y) : (", total_mean_dx, ", ", total_mean_dy, ")", sep="")
    print("- Écart type total des différences en cm (x, y) : (", total_sigma_dx, ", ", total_sigma_dy, ")", sep="")
    print("- Proportion totale de particules reconstituées : ", ratio_success, "%", sep="")


if __name__ == "__main__":
    main()
