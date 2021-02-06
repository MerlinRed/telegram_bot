from random import choice


def create_url(email):
    chars = 'QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    param = ''
    for _ in range(10 + 1):
        param += choice(chars)
    url = f'http://localhost:8000/mail?param1={param}&param2={email}'
    return url
