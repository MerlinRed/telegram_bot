import logging
import re

from create_password import create_password
from load_all import bot
from message_to_email import send_password_to_email
from work_with_db import insert_user_in_db, select_user_email


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
