class Book():

    def __init__(self, isbn, titulo, autor, anoedicion, precio):
        "Columnas de la base de datos"
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.ano_edicion = anoedicion
        self.precio = precio
        self.unidades_vendidas = 0