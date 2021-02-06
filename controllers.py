from endpoints import Controller

from work_with_db import update_mail_activated


class Mail(Controller):
    def GET(self, **param):
        email = param['param2']
        update_mail_activated(email=email)
        return f'Email {email} activated'
