#!/usr/bin/python3
import logging
import re

from create_password import create_password
from load_all import bot
from message_to_email import send_password_to_email
from work_with_db import insert_user_in_db, select_user_account


def registration(message):
    pattern = re.compile('^[a-zA-Z0-9]+([\.-]?[a-zA-Z0-9]+)*@[a-zA-Z]+([\.-]?[a-zA-Z]+)*(\.[a-zA-Z]{2,3})+$')
    bot.send_message(chat_id=message.chat.id, text='Проверка адреса почты')
    email = message.text

    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    logging.info(msg=f'Registration email: {email}\n')

    sep_dog = email.partition('@')
    after_dog = ''.join(sep_dog[-1])
    sep_dot = after_dog.partition('.')
    after_dot = ''.join(sep_dot[-1])
    full_valid_email = email if after_dot.isalpha() else ''
    is_valid = pattern.match(full_valid_email)
    is_valid_email = is_valid.group() if is_valid else False
    if is_valid_email:
        password = create_password()
        insert_user_in_db(user_id=message.from_user.id, first_name=message.chat.first_name,
                          last_name=message.chat.last_name,
                          email=email, password=password)
        send_password_to_email(email=email, password=password)
        bot.send_message(chat_id=message.chat.id,
                         text="""Перейдите на ранее введенную вами почту.\nВам было прислано сообщение в котором содержится ваш пароль от аккаунта и ссылка для подтверждения вашей почты.\nБез подтверждения почты аккаунт не активен.\nЕсли вы не нашли сообщение, посмотрите в спаме.""")
    else:
        bot.send_message(chat_id=message.chat.id, text='Вы ввели некорректный адрес почты.')


def check_registration_user(user_id):
    return True if select_user_account(user_id) else False
