from random import choice


def create_password():
    chars = '0123456789QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    password = ''
    for letter in range(10 + 1):
        password += choice(chars)
    return password
