from os import getenv

from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = getenv('TOKEN')
ADMIN_ID = getenv('ADMIN_ID')
PG_USER = getenv('PG_USER')
PG_PASS = getenv('PG_PASS')
MY_EMAIL = getenv('MY_EMAIL')
EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')
