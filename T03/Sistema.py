import sqlite3
import csv
import datetime


class Sistema:

    def __init__(self, usuario=None):
        self.usuario = usuario
        self.connection = sqlite3.connect('T03.db')

    def creacion_tablas(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE Usuarios(U_ID INTEGER, Usuario TEXT, Contrasena TEXT, UNIQUE(Usuario), "
                       "PRIMARY KEY(U_ID))")
        cursor.execute("CREATE TABLE Canciones(C_ID INTEGER, Artista TEXT, Album TEXT, Track TEXT, Duracion FLOAT, "
                       "PRIMARY KEY(C_ID))")
        cursor.execute("CREATE TABLE Generos(G_ID INTEGER, Artista TEXT, Genero TEXT, UNIQUE(Genero) PRIMARY KEY(G_ID))")
        cursor.execute("CREATE TABLE Reproducciones(R_ID INTEGER, Usuario INTEGER, Cancion INTEGER, Fecha TEXT, "
                       "PRIMARY KEY(R_ID),FOREIGN KEY (Usuario) REFERENCES Usuarios,FOREIGN KEY (Cancion) REFERENCES "
                       "Canciones)")
        self.connection.commit()

    def poblar_tablas(self):
        cursor = self.connection.cursor()
        # Usuarios
        with open('usuarios.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("INSERT INTO Usuarios VALUES (?,?,?)", (n, fila['usuario'], fila['contrasena']))
                n += 1
        # Canciones
        with open('tracks.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                duracion = fila['Duration'].split(":")
                duracion = float(duracion[0]) + float(float(duracion[1])/60)
                cursor.execute("INSERT INTO Canciones VALUES (?,?,?,?,?)", (n, fila['Artist'], fila['Album'],
                                                                            fila['Track'], duracion))
                n += 1
        # Generos
        with open('genres.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("INSERT INTO Generos VALUES (?,?,?)", (n, fila['Artist'], fila['Genre']))
                n += 1
        self.connection.commit()

        # Reproducciones
        connection = sqlite3.connect('T03.db')
        cursor = connection.cursor()
        with open('reproduccion.csv', encoding='utf8') as file:
            datos = csv.DictReader(file)
            n = 1
            for fila in datos:
                cursor.execute("SELECT C.C_ID FROM Canciones C WHERE C.Track = ?", [fila['cancion']])
                aux = int(cursor.fetchone()[0])
                cursor.execute("INSERT INTO Reproducciones VALUES (?,?,?,?)", (n, int(fila['usuario_id']), aux,
                                                                               fila['fecha']))
                n += 1

        connection.commit()
        return None

    def inicializar(self):
        self.creacion_tablas()
        self.poblar_tablas()

    def agregar_usuario(self, usuario, contrasena):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(U_ID) FROM Usuarios U")
        n = int(cursor.fetchone()[0]) + 1
        cursor.execute("INSERT INTO Usuarios VALUES (?,?,?)", (n, usuario, contrasena))
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
        cursor.execute("INSERT INTO Canciones VALUES (?,?,?,?,?)", (n, artista, album, track, duracion))
        self.connection.commit()
        return None

    def escuchar(self, cancion):
        cursor = self.connection.cursor()
        cursor.execute("SELECT MAX(R_ID) FROM Reproducciones R")
        id1 = int(cursor.fetchone()[0]) + 1
        cursor.execute("SELECT C.C_ID FROM Canciones C WHERE C.Track = ?", [cancion])
        id_cancion = int(cursor.fetchone()[0])
        fecha = str(datetime.datetime.now()).split(' ')
        hora = fecha[1].split('.')[0].split(':')
        hora = hora[0] + ':' + hora[1]
        fecha_auxiliar = fecha[0].split('-')
        fecha = fecha_auxiliar[2] + '-' + fecha_auxiliar[1] + '-' + fecha_auxiliar[0] + '-' + hora
        cursor.execute("INSERT INTO Reproducciones VALUES (?,?,?,?)", [id1, self.usuario, id_cancion, fecha])
        self.connection.commit()

    def modificar_cancion(self, artista1, album1, track1, duracion1, artista2, album2, track2, duracion2):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE CANCIONES SET Artista = ?, Album = ?, Track = ?, Duracion = ? WHERE Artista = ? "
                       "AND Album = ? AND Track = ? AND Duracion = ?",
                       [artista1, album1, track1, duracion1, artista2, album2, track2, duracion2])
        self.connection.commit()

    def generos_repetidos(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT C.Artista, count(C.Artista) FROM Canciones C, Reproducciones R, Usuarios U WHERE "
                       "C.C_ID = R.Cancion AND R.Usuario = U.U_ID AND U.Usuario = ? GROUP BY C.Artista ORDER BY "
                       "count(C.Artista) LIMIT 1", [self.usuario])
        a_mas_escuchado = cursor.fetchall()[0][0]
        cursor.execute("SELECT G.Genero FROM Generos G WHERE G.Artista = ?", [a_mas_escuchado])
        tabla = cursor.fetchall()
        print("Los generos del artista más escuchado son: {}".format(tabla))
        self.connection.commit()

    def tiempo_invertido(self, k):
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(C.Duracion) FROM Canciones C, Reproducciones R, Usuarios U WHERE C.C_ID = "
                       "R.Cancion AND R.Usuario = U.U_ID AND U.Usuario = ? ORDER BY datetime(R.Fecha) DESC LIMIT ?",
                       [self.usuario, k])
        tabla = cursor.fetchall()[0][0]
        print("Se invirtieron: {} minutos en las últimas {} canciones".format(tabla, k))
        self.connection.commit()

    def busqueda_amigos(self, k):
        cursor = self.connection.cursor()
        info = {}
        cursor.execute("SELECT U.Usuario FROM Usuarios U")
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            info[usuario[0]] = []

        for usuario in info.keys():
            cursor.execute("SELECT DISTINCT C.C_ID FROM Canciones C, Reproducciones R, Usuarios U WHERE "
                           "C.C_ID = R.Cancion AND R.Usuario = U.U_ID AND U.Usuario = ?", [usuario])
            canciones = cursor.fetchall()
            info[usuario].append(canciones)
            cursor.execute("SELECT DISTINCT C.Artista FROM Canciones C, Reproducciones R, Usuarios U WHERE "
                           "C.C_ID = R.Cancion AND R.Usuario = U.U_ID AND U.Usuario = ?", [usuario])
            artistas = cursor.fetchall()
            info[usuario].append(artistas)
            cursor.execute("SELECT DISTINCT G.Genero FROM Canciones C, Reproducciones R, Usuarios U, Generos G WHERE "
                           "C.C_ID = R.Cancion AND R.Usuario = U.U_ID AND U.Usuario = ? and C.Artista = G.Artista",
                           [usuario])
            generos = cursor.fetchall()
            info[usuario].append(generos)
            info[usuario].append(0)
        output = []
        for usuario_aux, datos in info.items():
            if usuario_aux != self.usuario:
                puntaje = 0
                for cancion in info[self.usuario][0]:
                    if cancion in info[usuario_aux][0]:
                        puntaje += 1.5

                for artista in info[self.usuario][1]:
                    if artista in info[usuario_aux][1]:
                        puntaje += 1

                for genero in info[self.usuario][2]:
                    if genero in info[usuario_aux][2]:
                        puntaje += 0.5

                output.append((usuario_aux, puntaje))

        output = sorted(output, key=lambda tup: tup[1], reverse=True)

        if k > len(output):
            for usuario in output:
                print(usuario[0], usuario[1])
        else:
            for usuario in output[0:k]:
                print(usuario[0], usuario[1])

    def eliminar_usuario(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Reproducciones WHERE R.Usuario = U.U_ID AND U.Usuario = ?", [self.usuario])
        cursor.execute("DELETE FROM Usuarios WHERE Usuario = ?", [self.usuario])
        self.connection.commit()



sistema = Sistema()
# sistema.inicializar()
i1, i2, i3 = 1, 1, 1

while i1 == 1:
    sistema = Sistema()
    print("\n")
    print("Hola, ¿qué quieres hacer?: ")
    print("1) Ingresar a mi cuenta")
    print("2) Crear un usuario")
    a1 = (input("Ingrese opción: "))
    print("\n")
    if int(a1) == 1:
        while i2 == 1:
            print("Ingrese su usuario y contraseña")
            user = input("Usuario: ")
            password = input("Constraseña: ")
            print("\n")
            connect = sqlite3.connect('T03.db')
            cur = connect.cursor()
            cur.execute("SELECT U.U_ID FROM Usuarios U WHERE U.Usuario = ?", [user])
            verificacion1 = cur.fetchall()
            if len(verificacion1) == 0:
                print("Usuario ingresado no existe en la base de datos. Inténtelo de nuevo")
                print("\n")
            else:
                sistema = Sistema(user)
                cur.execute("SELECT U.U_ID FROM Usuarios U WHERE U.Usuario = ? AND U.Contrasena = ?", [user, password])
                verificacion2 = cur.fetchone()
                if verificacion2:
                    while i3 == 1:
                        print("Hola {}! que consulta deseas realizar hoy:".format(user))
                        print("0) Cerrar Sesión")
                        print("1) Agregar una nueva canción")
                        print("2) Agregar un nuevo género")
                        print("3) Escuchar una canción")
                        print("4) Modificar datos de una canción")
                        print("5) Solicitar los géneros más repetidos entre los artistas más escuchados")
                        print("6) Solicitar el total de tiempo invertido para las últimas canciones escuchadas")
                        print("7) Buscar Amiguitos")
                        print("8) Eliminar mi cuenta de usuario")
                        a2 = input("Ingrese opción: ")
                        if int(a2) == 0:
                            i3 = 0
                            i2 = 0
                        elif int(a2) == 1:
                            track = input("Ingrese el nombre de la canción: ")
                            artista = input("Ingrese el nombre de artista de la canción: ")
                            album = input("Ingrese el nombre del album de la canción: ")
                            duracion = input("Ingrese duración de la canción: ")
                            sistema.agregar_cancion(artista, album, track, duracion)
                        elif int(a2) == 2:
                            genero = input("Ingrese el nombre del género musical: ")
                            artista = input("Ingrese el nombre del artista al que le quiere asignar el género: ")
                            sistema.agregar_genero(artista, genero)
                        elif int(a2) == 3:
                            track = input("Ingrese el nombre de la canción: ")
                            sistema.escuchar(track)
                        elif int(a2) == 4:
                            track1 = input("Ingrese el nombre de la canción: ")
                            artista1 = input("Ingrese el nombre de artista de la canción: ")
                            album1 = input("Ingrese el nombre del album de la canción: ")
                            duracion1 = input("Ingrese duración de la canción: ")
                            track2 = input("Ingrese el nombre con el que quiere que quede la canción: ")
                            artista2 = input("Ingrese el nombre de artista con el que quiere que quede la canción: ")
                            album2 = input("Ingrese el nombre del album con el que quiere que quede la canción: ")
                            duracion2 = input("Ingrese la duración con la que quiere que quede la canción: ")
                            sistema.modificar_cancion(artista2, album2, track2, duracion2, artista1, album1, track1,
                                                      duracion1)
                        elif int(a2) == 5:
                            sistema.generos_repetidos()
                        elif int(a2) == 6:
                            m = int(input("Ingrese el numero de canciones que quiere consultar: "))
                            sistema.tiempo_invertido(m)
                        elif int(a2) == 7:
                            m = int(input("Ingrese el número de amiguitos mas cercanos que quiere buscar: "))
                            sistema.busqueda_amigos(m)
                        elif int(a2) == 8:
                            sistema.eliminar_usuario()
                        else:
                            print("Ingrese un número de la lista de opciones")
                else:
                    print("Contraseña incorrecta. Inténtelo de nuevo")
    elif a1 == 2:
        print("Ingrese su usuario y contraseña")
        user = input("Usuario: ")
        password = input("Constraseña: ")
        sistema.agregar_usuario(user, password)
        sistema = Sistema(user)

    else:
        print("Ingrese un número de la lista de opciones")
