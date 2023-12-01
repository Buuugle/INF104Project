def error(message):
    print("\n\n*** ATTENTION ***\n" + message)


def min_int_input(message, fail="", value=0):
    while True:
        i = int(input(message))
        if value <= i:
            return i
        print(fail)


def max_int_input(message, fail="", value=0):
    while True:
        i = int(input(message))
        if value >= i:
            return i
        print(fail)
