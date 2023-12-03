from util import *
from simulation import *
from analysis import *


def mon_main(N):
    print("--- SIMULATEUR DE CALORIMÈTRE ---")
    Xwidth = 100
    n = 2
    events = min_int_input("\nNombre d'événements : ", "Le nombre d'événement doit être strictement positif.", 1)
    particles = min_int_input("\nNombre de particles par événements : ", "Le nombre de particules doit être strictement positif.", 1)
    size = N + 2 * n
    for i in range(1, events + 1):
        matrix = create_empty_matrix(size)
        create_event(Xwidth, N, n, matrix, particles)
        print("\n¤ Événement n°", i, " : ", sep="")
        affiche_matrice_energy(matrix)


def mon_main2(N):
    print("--- SIMULATEUR DE CALORIMÈTRE + RECONSTITUTION DE LA PARTICULE---")
    Xwidth = 100
    n = 2
    events = min_int_input("\nNombre d'événements : ", "Le nombre d'événement doit être strictement positif.", 1)
    size = N + 2 * n
    cell_width = Xwidth / N
    lst_dx = []
    lst_dy = []
    for i in range(1, events + 1):
        matrix = create_empty_matrix(size)
        all_coords = create_event(Xwidth, N, n, matrix, 1)
        print("\n¤ Événement n°", i, " : ", sep="")
        affiche_matrice_energy(matrix)
        lst_vrai = all_coords[0]
        x_vrai = lst_vrai[0]
        y_vrai = lst_vrai[1]
        lst_rec = mesure_xy(matrix, cell_width)
        x_rec = lst_rec[0]
        y_rec = lst_rec[1]
        print("¤ Taille d'une cellule : ", cell_width, "cm", sep="")
        print("¤ Coordonnées reconstituées :\n\t- x : ", round(x_rec, 2), "cm\n\t- y : ", round(y_rec, 2), "cm", sep="")
        dx = abs(x_vrai - x_rec)
        dy = abs(y_vrai - y_rec)
        lst_dx.append(dx)
        lst_dy.append(dy)
        print("¤ Différence entre les coordonnées réelles et reconstituées :\n\t- x : ", round(dx, 2), "cm\n\t- y : ", round(dy, 2), "cm", sep="")
    mean_dx = mean(lst_dx)
    mean_dy = mean(lst_dy)
    sigma_dx = standard_deviation(lst_dx)
    sigma_dy = standard_deviation(lst_dy)
    print("\n")
    print("¤ Performance du détecteur selon les différences entre les coordonnées réelles et reconstituées à chaque événements :")
    print("\t* Moyenne :\n\t\t- x : ", round(mean_dx, 2), "cm\n\t\t- y : ", round(mean_dy, 2), "cm", sep="")
    print("\t* Écart-type :\n\t\t- x : ", round(sigma_dx, 2), "cm\n\t\t- y : ", round(sigma_dy, 2), "cm", sep="")


def test():
    m = create_empty_matrix(10)
    launch_particle_on_detector(100, 10, 0, m)
    affiche_matrice_energy(m)
    cluster = clusterize(m)
    print(cluster)


if __name__ == "__main__":
    test()
