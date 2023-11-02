from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario


class ModeloUsuario():

    @classmethod
    def login(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql = f"""SELECT id, usuario, password
                    FROM usuario WHERE usuario = '{usuario.usuario}'"""
            cursor.execute(sql)
            data = cursor.fetchone()
            if data != None:
                coincide = usuario.verificar_password(data[2], usuario.password)
                print(coincide)
                if coincide:
                    usuario_loggeado = Usuario(data[0], data[1], None, None)
                    return usuario_loggeado
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)  # levanta una excepcion y se le pase la excepcion que sucedio

    @classmethod
    def obtener_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT USU.id, USU.usuario, TIP.id, TIP.nombre 
                            FROM usuario USU JOIN tipousuario TIP ON USU.tipousuario_id = TIP.id 
                            WHERE USU.id = {0}""".format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            print(data)
            tipousuario = TipoUsuario(data[2], data[3])
            usuario_logeado = Usuario(data[0], data[1], None, tipousuario)
            return usuario_logeado
        except Exception as ex:
            raise Exception(ex) # levanta una excepcion y se le pase la excepcion que sucedio
