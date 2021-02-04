import smtplib
from config import MY_EMAIL, EMAIL_PASSWORD


def send_password(email, password):
    smtp_obj = smtplib.SMTP('smtp.mail.ru', 587)
    smtp_obj.starttls()
    smtp_obj.login(MY_EMAIL, EMAIL_PASSWORD)
    smtp_obj.sendmail(MY_EMAIL, email, f'Ваш пароль: {password}'.encode(encoding='utf-8'))
    smtp_obj.quit()
