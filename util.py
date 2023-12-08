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


# 3 fonctions d'input sécurisées qui font des boucles si la valeur n'est pas dans l'intervalle spécifié
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
            if value >= n:
                return n
        print(fail)


def max_float_input(message, fail="", value=0.0):
    while True:
        string = input(message)
        if is_str_number(string):
            n = float(string)
            if value <= n:
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


def standard_deviation(lst):  # Ecart type d'une liste
    size = len(lst)
    if size == 0:
        return 0
    m = mean(lst)
    sigma = 0
    for i in lst:
        sigma += abs(i - m) ** 2
    sigma = (sigma / size) ** 0.5
    return sigma


def sub_list(lst, index_a, index_b):  # Créer une sous liste d'une liste
    result = []
    for index in range(index_a, index_b):
        result.append(lst[index])
    return result
