#!/usr/bin/python3
import logging
import re

from load_all import bot
from work_with_db import select_user_from_db, select_active_from_db, update_user_authorization, select_auth_user
from work_with_db import update_exit_user_from_account

EMAIL = None
PASSWORD = None


def authorization(message):
    if select_user_from_db(user_id=message.from_user.id, email=EMAIL, password=PASSWORD):
        if not check_email_authorization(message.from_user.id):
            bot.send_message(chat_id=message.chat.id,
                             text='Вы не можете пользоваться ботом пока не подтвердите свою почту.')
            return
        bot.send_message(chat_id=message.chat.id, text='Авторизация прошла успешно. Доступ к боту открыт.')
        update_user_authorization(user_id=message.from_user.id)
    else:
        bot.send_message(chat_id=message.chat.id, text='Ошибка при авторизации. Попробуйте еще раз.')


def authorization_email(message):
    pattern = re.compile('[\w.-]+@[\w.-]+\.?[\w]+?')
    bot.send_message(chat_id=message.chat.id, text='Проверка адреса почты.')
    email = message.text

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logging.info(msg=f'Authorization email: {email}\n')

    is_valid = pattern.match(email)
    is_valid_email = is_valid.group() if is_valid else False
    if is_valid_email:
        global EMAIL
        EMAIL = email
        msg_password = bot.send_message(message.chat.id, 'Введите пароль для авторизации.')
        bot.register_next_step_handler(msg_password, authorization_email_password)
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели некорректный адрес почты.')


def authorization_email_password(message):
    password = message.text
    global PASSWORD
    PASSWORD = password
    authorization(message)


def check_email_authorization(user_id):
    return True if select_active_from_db(user_id=user_id) else False


def check_user_authorization(user_id):
    return True if select_auth_user(user_id=user_id) else False


def exit_user_from_account(user_id):
    update_exit_user_from_account(user_id=user_id)
