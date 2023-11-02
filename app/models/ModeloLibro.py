from .entities.Author import Author
from .entities.Book import Book

class ModeloLibro():
    @classmethod
    def listar_libros(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT BOOK.isbn, BOOK.titulo, BOOK.anoedicion, BOOK.precio,
                    AUT.apellidos, AUT.nombres
                    FROM libro BOOK JOIN autor AUT ON BOOK.autor_id = AUT.id
                    ORDER BY BOOK.titulo ASC"""
            # "author AUT y book BOOK" (GENERA UN ALIAS PARA LA TABLA)
            # "JOIN author AUT ON BOOK.author_id = AUT.id" junta ambas tablas por id del autor
            cursor.execute(sql)
            data = cursor.fetchall()
            books = []
            for row in data:
                author = Author(0, row[4], row[5])
                book = Book(row[0], row[1], author, row[2], row[3])
                books.append(book)

            return books

        except Exception as ex:
            raise Exception(ex)  # levanta una excepcion y se le pase la excepcion que sucedio

    @classmethod
    def listar_libros_vendidos(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COM.libro_isbn, LIB.titulo, LIB.precio, 
                        COUNT(COM.libro_isbn) AS Unidades_Vendidas
                        FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.isbn 
                        GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros = []
            for row in data:
                lib = Book(row[0], row[1], None, None, row[2])
                lib.unidades_vendidas = int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def leer_libro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, titulo, anoedicion, precio 
                    FROM libro WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            libro = Book(data[0], data[1], None, data[2], data[3])
            return libro
        except Exception as ex:
            raise Exception(ex)