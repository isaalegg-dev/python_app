from decouple import config

class Config:
    SECRET_KEY="159HKJKJGJFHGFHFG"

class DevelopmentConfig(Config):
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tienda' # nombre de Base de Datos (DataBase)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  # TLS: Transport Layer Security: Seguridad de la capa de transporte
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'isaalegg@gmail.com'
    MAIL_PASSWORD = config('MAIL_PASSWORD')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}