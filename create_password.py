#!/usr/bin/python3
from random import choice


def create_password():
    chars = '0123456789QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    password = ''
    for _ in range(10 + 1):
        password += choice(chars)
    return password
