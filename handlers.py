import logging
import re

from telebot import types

from create_password import create_password
from load_all import bot
from message_to_email import send_password_to_email
from work_with_db import insert_user_in_db, select_user_email, select_user_from_db, select_active_from_db

CLIENT_AUTH = False
EMAIL = None
PASSWORD = None


@bot.message_handler(commands=['start', 'help'])
def start_chat(message):
    keyboard_start_msg = types.ReplyKeyboardMarkup(True, True)
    keyboard_start_msg.row('Авторизация', 'Регистрация')
    text = 'Для продолжения взаимодействий с ботом необходимо зарегестрироваться и авторизоваться.\n\n' \
           'Если вы уже зарегестрированы, необходимо только авторизоваться'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard_start_msg)


@bot.message_handler(content_types=['text'])
def auth_reg(message):
    if message.text == 'Авторизация':
        msg_password = bot.send_message(message.chat.id, 'Введите почту для авторизации: email@mail.ru')
        bot.register_next_step_handler(msg_password, authorization_email)

    elif message.text == 'Регистрация':
        msg = bot.send_message(message.chat.id, 'Введите почту для регистрации: email@mail.ru')
        bot.register_next_step_handler(msg, registration)

    elif not CLIENT_AUTH:
        bot.send_message(chat_id=message.chat.id, text='Вы не авторизованы. Доступ к боту закрыт')
    else:
        bot.send_message(chat_id=message.chat.id, text='А тут ничего и нет')


def authorization(message):
    if select_user_from_db(user_id=message.from_user.id, email=EMAIL, password=PASSWORD):
        if not check_authorization(message.from_user.id):
            bot.send_message(chat_id=message.chat.id,
                             text='Вы не можете пользоваться ботом пока не подтвердите свою почту')
            return
        bot.send_message(chat_id=message.chat.id, text='Авторизация прошла успешна. Доступ к боту открыт')
        global CLIENT_AUTH
        CLIENT_AUTH = True
    else:
        bot.send_message(chat_id=message.chat.id, text='Ошибка при авторизации. Попробуйте еще раз')


def authorization_email(message):
    if CLIENT_AUTH:
        bot.send_message(chat_id=message.chat.id, text='Вы уже авторизованы')
        return
    pattern = re.compile('[\w.-]+@[\w.-]+\.?[\w]+?')
    bot.send_message(chat_id=message.chat.id, text='Проверка адреса почты')
    email = message.text

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logging.info(msg=f'Authorization email: {email}\n')

    is_valid = pattern.match(email)
    is_valid_email = is_valid.group() if is_valid else False
    if is_valid_email:
        global EMAIL
        EMAIL = email
        msg_password = bot.send_message(message.chat.id, 'Введите пароль для авторизации')
        bot.register_next_step_handler(msg_password, authorization_email_password)
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели некорректный адрес почты')


def authorization_email_password(message):
    password = message.text
    global PASSWORD
    PASSWORD = password
    authorization(message)


def registration(message):
    pattern = re.compile('[\w.-]+@[\w.-]+\.?[\w]+?')
    bot.send_message(chat_id=message.chat.id, text='Проверка адреса почты')
    email = message.text

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logging.info(msg=f'Registration email: {email}\n')

    is_valid = pattern.match(email)
    is_valid_email = is_valid.group() if is_valid else False
    if is_valid_email:
        if check_registration_user(user_id=message.from_user.id, email=email):
            bot.send_message(chat_id=message.chat.id, text='Вы уже зарегестрированы')
            return
        password = create_password()
        insert_user_in_db(user_id=message.from_user.id, first_name=message.chat.first_name,
                          last_name=message.chat.last_name,
                          email=email, password=password)
        send_password_to_email(email=email, password=password)
        bot.send_message(chat_id=message.chat.id, text='Для вас сгенерирован пароль и отправлен на вашу почту')
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели некорректный адрес почты')


def check_registration_user(user_id, email):
    return True if select_user_email(user_id, email) else False


def check_authorization(user_id):
    return True if select_active_from_db(user_id) else False


if __name__ == '__main__':
    bot.polling()
