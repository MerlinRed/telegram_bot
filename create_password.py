from random import shuffle, choice


def create_password():
    num_str = list("0123456789")
    eng_str = list("QWERTYUIOPLKJHGFDSAZXCVBNM".lower())

    shuffle(num_str)
    shuffle(eng_str)

    p1 = choice(num_str)
    p2 = choice(num_str)
    p3 = choice(num_str)
    p4 = choice(eng_str)
    p5 = choice(eng_str)
    p6 = choice(eng_str)

    lst_passwords = list(p1 + p2 + p3 + p4 + p5 + p6)
    shuffle(lst_passwords)
    password = ''.join(lst_passwords)

    return password
