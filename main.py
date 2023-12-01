from simulation import *
from util import *


def mon_main(N):
    Xwidth = 100
    n = 2
    events = min_int_input("Nombre d'événements : ", "Le nombre d'événement doit être strictement positif\n", 1)
    particles = min_int_input("Nombre de particles par événements : ", "Le nombre de particules doit être strictement "
                                                                       "positif\n", 1)
    for i in range(1, events + 1):
        matrix = create_empty_matrix(N + 2 * n)
        create_event(Xwidth, N, n, matrix, particles)
        print("\nÉvénement n°", i, " : ", sep="")
        affiche_matrice_energy(matrix)


if __name__ == "__main__":
    mon_main(20)
