#!/usr/bin/python3
import logging

from telebot import TeleBot

from config import BOT_TOKEN

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = TeleBot(token=BOT_TOKEN, parse_mode='HTML')
