from flask_script import Manager, Server
from app import iniciar_app
from config import config


configuration = config['development']
app = iniciar_app(configuration)

manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=5000))

if __name__ == '__main__':
    manager.run()