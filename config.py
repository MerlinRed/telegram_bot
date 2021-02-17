#!/usr/bin/python3
from os import getenv

from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = getenv('TOKEN')
PG_USER = getenv('PG_USER')
PG_PASS = str(getenv('PG_PASS'))
MY_EMAIL = getenv('MY_EMAIL')
EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
