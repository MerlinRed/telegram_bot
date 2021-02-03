import re

from psycopg2.errors import UniqueViolation
from telebot import types

from load_all import bot
from work_with_db import insert_user_in_db, select_user_from_db

CLIENT_AUTH = False
EMAIL = None
PASSWORD = None


@bot.message_handler(commands=['start', 'help'])
def start_chat(message):
    keyboard_start_msg = types.ReplyKeyboardMarkup(True, True)
    keyboard_start_msg.row('Авторизация', 'Регистрация')
    bot.send_message(chat_id=message.chat.id, text='Бот запущен', reply_markup=keyboard_start_msg)


@bot.message_handler(content_types=['text'])
def auth_reg(message):
    if message.text == 'Авторизация':
        msg_password = bot.send_message(message.chat.id, 'Введите почту для авторизации')
        bot.register_next_step_handler(msg_password, authorization_email)

    elif message.text == 'Регистрация':
        msg = bot.send_message(message.chat.id, 'Введите почту для регистрации')
        bot.register_next_step_handler(msg, registration)

    elif not CLIENT_AUTH:
        bot.send_message(chat_id=message.chat.id, text='Вы не авторизованы')


def authorization(message):
    if select_user_from_db(user_id=message.from_user.id, email=EMAIL, password=PASSWORD):
        bot.send_message(chat_id=message.chat.id, text='Авторизация прошла успешна')
        global CLIENT_AUTH
        CLIENT_AUTH = True
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы не зарегестрированы')


def authorization_email(message):
    bot.send_message(chat_id=message.chat.id, text='email введен')
    email = message.text
    global EMAIL
    EMAIL = email
    msg_password = bot.send_message(message.chat.id, 'Введите пароль для авторизации')
    bot.register_next_step_handler(msg_password, authorization_email_password)


def authorization_email_password(message):
    bot.send_message(chat_id=message.chat.id, text='пароль введен')
    password = message.text
    global PASSWORD
    PASSWORD = password
    authorization(message)


def registration(message):
    pattern = re.compile('[\w.-]+@[\w.-]+\.?[\w]+?')
    bot.send_message(chat_id=message.chat.id, text='email введен')
    email = message.text
    is_valid = pattern.match(email)
    is_valid_email = is_valid.group() if is_valid else False
    if is_valid_email:
        bot.send_message(chat_id=message.chat.id, text='Для вас сгенерирован пароль и отправлен на вашу почту')
        password = bot.send_message(chat_id=message.chat.id, text=1)
        try:
            insert_user_in_db(user_id=message.from_user.id, first_name=message.chat.first_name,
                              last_name=message.chat.last_name,
                              email=email, password=password.text)
        except UniqueViolation:
            bot.send_message(chat_id=message.chat.id, text='Вы уже зарегестрированы')
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели некорректный адрес почты')


bot.polling()
