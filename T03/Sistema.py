import sqlite3
import csv
import datetime

class Sistema:

    def __init__(self):
        self.usuario = None
        self.connection = sqlite3.connect('T03.db')

    def creacion_tablas(self):
        connection = sqlite3.connect('T03.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE Usuarios(U_ID INTEGER, Usuario TEXT, Contraseña TEXT, UNIQUE(Usuario), PRIMARY KEY(U_ID))")
        cursor.execute("CREATE TABLE Canciones(C_ID INTEGER, Artista TEXT, Album TEXT, Track TEXT, Duracion FLOAT, PRIMARY KEY(C_ID))")
        cursor.execute("CREATE TABLE Generos(G_ID INTEGER, Artista TEXT, Genero TEXT, PRIMARY KEY(G_ID))")
        cursor.execute("CREATE TABLE Reproducciones(R_ID INTEGER, Usuario INTEGER, Cancion INTEGER, Fecha TEXT, PRIMARY KEY(R_ID),FOREIGN KEY (Usuario) REFERENCES Usuarios,FOREIGN KEY (Cancion) REFERENCES Canciones)")
        connection.commit()

    def poblar_tablas(self):
        connection = sqlite3.connect('T03.db')
        cursor = connection.cursor()
        # Usuarios
        with open('usuarios.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("INSERT INTO Usuarios VALUES (?,?,?)",(n,fila['usuario'],fila['contraseña']))
                n += 1
        # Canciones
        with open('tracks.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                duracion = fila['Duration'].split(":")
                duracion = float(duracion[0]) + float(float(duracion[1])/60)
                cursor.execute("INSERT INTO Canciones VALUES (?,?,?,?,?)",(n,fila['Artist'],fila['Album'],fila['Track'],duracion))
                n += 1
        # Generos
        with open('genres.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("INSERT INTO Generos VALUES (?,?,?)",(n,fila['Artist'],fila['Genre']))
                n += 1
        connection.commit()

        # Reproducciones
        connection = sqlite3.connect('T03.db')
        cursor = connection.cursor()
        with open('reproduccion.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("SELECT C.C_ID FROM Canciones C WHERE C.Track = ?",[fila['cancion']])
                aux = int(cursor.fetchone()[0])
                cursor.execute("INSERT INTO Reproducciones VALUES (?,?,?,?)",(n,int(fila['usuario_id']),aux,fila['fecha']))
                n += 1

        connection.commit()

    def inicializar(self):
        self.creacion_tablas()
        self.poblar_tablas()


    def agregar_usuario(self, usuario, contraseña):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(U_ID) FROM Usuarios U")
        n = int(cursor.fetchone()[0]) + 1
        cursor.execute("INSERT INTO Usuarios VALUES (?,?,?)",(n,usuario,contraseña))
        self.connection.commit()
        return None

    def agregar_genero(self, artista, genero):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(G_ID) FROM Generos G")
        n = int(cursor.fetchone()[0]) + 1
        cursor.execute("INSERT INTO Generos VALUES (?,?,?)", (n, artista, genero))
        self.connection.commit()
        return None

    def agregar_cancion(self, artista, album, track, duracion):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(C_ID) FROM Canciones C")
        n = int(cursor.fetchone()[0]) + 1
        cursor.execute("INSERT INTO Canciones VALUES (?,?,?,?,?)",(n,artista,album,track,duracion))
        self.connection.commit()
        return None

    def escuchar(self, cancion):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(R_ID) FROM Reproducciones R")
        id = int(cursor.fetchone()[0]) + 1
        cursor.execute("SELECT C.C_ID FROM Canciones C WHERE C.Track = ?",[cancion])
        id_cancion = int(cursor.fetchone()[0])
        fecha = str(datetime.datetime.now()).split(' ')
        hora = fecha[1].split('.')[0].split(':')
        hora = hora[0] + ':' + hora[1]
        fecha_auxiliar = fecha[0].split('-')
        fecha = fecha_auxiliar[2] + '-' + fecha_auxiliar[1] + '-' + fecha_auxiliar[0] + '-' + hora
        cursor.execute("INSERT INTO Reproducciones VALUES (?,?,?,?)",[id, self.usuario, id_cancion, fecha])
        self.connection.commit()





sistema = Sistema()
#sistema.inicializar()

