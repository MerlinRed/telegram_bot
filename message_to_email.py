#!/usr/bin/python3
import smtplib

from config import MY_EMAIL, EMAIL_PASSWORD
from create_url import create_url


def send_password_to_email(email, password):
    smtp_obj = smtplib.SMTP('smtp.mail.ru', 587)
    smtp_obj.starttls()
    smtp_obj.login(MY_EMAIL, EMAIL_PASSWORD)
    smtp_obj.sendmail(MY_EMAIL, email,
                      f'Ваш пароль от аккаунта: {password}\nСсылка для подтверждения почты: {create_url(email=email)}'.encode(
                          encoding='utf-8'))
    smtp_obj.quit()
