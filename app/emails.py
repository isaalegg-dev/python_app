from flask_mail import Message
from flask import current_app,render_template

def confirmacion_compra(mail, usuario, libro):
    try:
        message = Message(
            'Alguien ha comprado un libro',
            sender=current_app.config.MAIL_USERNAME,
            recipients=['zaphir930@gmail.com'])
        message.html=render_template(
            'emails/confirmacion_compra.html',
            usuario=usuario,
            libro=libro
        )
        mail.send(message)
    except Exception as ex:
        raise Exception(ex)