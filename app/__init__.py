from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_mysqldb import MySQL
from flask_mail import Mail
from .models.ModeloCompra import ModeloCompra
from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import  ModeloUsuario
from .models.entities.Usuario import Usuario
from .models.entities.compra import Compra
from .models.entities.Book import Book
from .emails import confirmacion_compra


from .conts import *

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

csrf = CSRFProtect() # CSRF (solicitud de falsificacion entre sitios) seguridad de login
db = MySQL(app)
login_manager_app = LoginManager(app) #administrador de sesiones
mail = Mail()

@app.route('/password/<password>')
def generar_password(password):
    crip = generate_password_hash(password)
    key = check_password_hash(crip, password)
    print(f'encriptado: {crip}, contrase;a: {password}')
    return render_template('index.html')

@login_manager_app.user_loader
def load_user(id):
    """funcion que hay que implementar para
    que funciones correctamente las sesiones (flask_login)"""
    return ModeloUsuario.obtener_id(db, id)

@app.route('/libros')
@login_required #decorador para no mostrar paginas que requieran login
def listar_libros():
    try:
        books = ModeloLibro.listar_libros(db)
        data = {
            'titulo':'Libros',
            'libros': books
        }
        return render_template('listado_libros.html', data=data)
    except Exception as ex:#levanta una excepcion y se le pase la excepcion que sucedio
        return render_template('errores/error.html', mensaje=format(ex))

@app.route('/comprarLibro',methods=['POST'])
@login_required
def comprar_libros():
    data_request = request.get_json()
    data = {}
    try:
        libro = ModeloLibro.leer_libro(db, data_request['isbn'])
        compra = Compra(None, libro, current_user)
        data['exito'] = ModeloCompra.registrar_compra(db, compra)
        confirmacion_compra(mail,current_user,libro)
    except Exception as ex:
        data['mensaje']=format(ex)
        data['exito'] = False

    return jsonify(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
        # CSRF (Cross-site Request Forgery): Solicitud de falsificación entre sitios.
        if request.method == 'POST':
            usuario = Usuario(
                None, request.form['usuario'], request.form['password'], None)
            usuario_logeado = ModeloUsuario.login(db, usuario)
            if usuario_logeado != None:
                login_user(usuario_logeado)
                flash(MENSAJE_BIENVENIDA)
                return redirect(url_for('index'))
            else:
                flash(LOGIN_CREDENCIALES_INVALIDAS, 'warning')
                return render_template('authentication/login.html')
        else:
            return render_template('authentication/login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                data={
                    'titulo':'Libros vendidos',
                    'libros_vendidos': libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
        else:
            try:
                compras = ModeloCompra.listar_compras_usuario(db, current_user)
                data = {
                    'titulo': 'Mis compras',
                    'compras': compras
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('login'))


def not_found(error):
    # definir pagina para error 404
    return render_template('errores/404.html'), 404

def iniciar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    app.register_error_handler(404, not_found) # manejo de errores
    app.register_error_handler(401, pagina_no_autorizada)  # manejo de errores (401 codigo http del error)
    return app

def pagina_no_autorizada(error):
    return redirect(url_for('login'))

# boostrap remote link
#<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
#<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.6/dist/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
#<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.2.1/dist/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.2.1/dist/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">