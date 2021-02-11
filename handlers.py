#!/usr/bin/python3
from telebot import types

from authorization import authorization_email, check_user_authorization
from load_all import bot
from registration import registration


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
        msg_password = bot.send_message(message.chat.id, 'Введите почту для авторизации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg_password, authorization_email)

    elif message.text == 'Регистрация':
        msg = bot.send_message(message.chat.id, 'Введите почту для регистрации.\nПример почты: email@mail.ru')
        bot.register_next_step_handler(msg, registration)

    elif not check_user_authorization(user_id=message.from_user.id):
        bot.send_message(chat_id=message.chat.id, text='Вы не авторизованы. Доступ к боту закрыт')
    else:
        bot.send_message(chat_id=message.chat.id, text='А тут ничего и нет')
