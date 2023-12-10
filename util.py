# Ce fichier contient des fonctions utilitaires utilisées surtout dans les fonctions main


def error(message):  # Cette fonction est un print décoré
    print("\n\n*** ATTENTION ***\n", message, sep="")


def is_str_number(string):  # Est-ce qu'une chaine de caractères peut être convertie en int ou float ?
    if len(string) == 0:
        return False
    digits = "0123456789."
    for char in string:
        if not (char in digits):
            return False
    return True


# 6 fonctions d'input sécurisées qui font des boucles si la valeur n'est pas dans l'intervalle spécifié
def min_int_input(message, fail="", value=0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = int(string)
            if value <= n:
                return n
        print(fail)


def max_int_input(message, fail="", value=0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = int(string)
            if value >= n:
                return n
        print(fail)


def range_int_input(message, fail="", min_value=0, max_value=100):
    if min_value > max_value:
        temp = min_value
        min_value = max_value
        max_value = temp
    while True:
        string = input(message)
        if is_str_number(string):
            n = int(string)
            if min_value <= n <= max_value:
                return n
        print(fail)


def min_float_input(message, fail="", value=0.0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = float(string)
            if value <= n:
                return n
        print(fail)


def max_float_input(message, fail="", value=0.0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = float(string)
            if value >= n:
                return n
        print(fail)


def range_float_input(message, fail="", min_value=0.0, max_value=100.0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = float(string)
            if min_value <= n <= max_value:
                return n
        print(fail)


def mean(lst):  # Moyenne d'une liste
    size = len(lst)
    if size == 0:
        return 0
    m = 0
    for i in lst:
        m += i
    m /= size
    return m


def standard_deviation(lst):  # Écart type d'une liste
    size = len(lst)
    if size == 0:
        return 0
    m = mean(lst)
    sigma = 0
    for i in lst:
        sigma += abs(i - m) ** 2
    sigma = (sigma / size) ** 0.5
    return sigma


def print_table(table):  # Affichage d'une matrice sous la forme d'un tableau
    line_size = len(table[0])
    for line in table:
        if len(line) != line_size:
            error("Toutes les lignes du tableau doivent avoir le même nombre d'éléments")
            return
    max_lengths = []  # On récupère la longueur maximale des éléments de chaque colonne pour pouvoir faire un affichage aligné
    for i in range(line_size):
        max_length = 0
        for line in table:
            length = len(line[i])
            if length > max_length:
                max_length = length
        max_lengths.append(max_length)

    separator = "+"
    for length in max_lengths:
        separator += "-" * (length + 2) + "+"
    print(separator)  # Cette chaîne de caractère représente une ligne séparatrice entre les lignes
    for line in table:  # On affiche chaque ligne de données
        current = "| "
        for index in range(len(line)):
            element = line[index]
            length = max_lengths[index]
            spaces = length - len(element)
            current += element + " " * spaces + " | "
        print(current)
        print(separator)
