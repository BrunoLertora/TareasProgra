import csv


class Track:
    def __init__(self, artist, album, track, duration, genres):
        self.artist = artist
        self.album = album
        self.track = track
        self.duration = duration
        self.genres = genres


class Reproduccion:
    def __init__(self, id_reproduccion, usuario_id, cancion, fecha):
        self.id_reproduccion = id_reproduccion
        self.usuario_id = usuario_id
        self.cancion = cancion
        self.fecha = fecha


class Usuario:
    def __init__(self, usuario_id, usuario, contrasena, reproducciones):
        self.usuario_id = usuario_id
        self.usuario = usuario
        self.contrasena = contrasena
        self.reproducciones = reproducciones


def cargar_datos():
    generos = {}  # {artist: [genres]}
    with open('genres.csv', encoding='utf8') as file:
        datos = csv.DictReader(file)
        for fila in datos:
            if fila['Artist'] not in generos:
                generos[fila['Artist']] = [fila['Genre']]
            else:
                generos[fila['Artist']].append(fila['Genre'])

    tracks = []
    with open('tracks.csv', encoding='utf8') as file:
        datos = csv.DictReader(file)
        for fila in datos:
            try:
                tracks.append(Track(fila['Artist'], fila['Album'], fila['Track'], fila['Duration'],
                                    generos[fila['Artist']]))
            except KeyError:
                tracks.append(Track(fila['Artist'], fila['Album'], fila['Track'], fila['Duration'], None))

    reproducciones = {}  # {artist: [genres]}
    with open('reproduccion.csv', encoding='utf8') as file:
        datos = csv.DictReader(file)
        for fila in datos:
            cancion = None
            for track in tracks:
                if track.track == fila['cancion']:
                    cancion = track
                    break

            if fila['usuario_id'] not in reproducciones:
                reproducciones[fila['usuario_id']] = [Reproduccion(fila['id_reproduccion'], fila['usuario_id'], cancion,
                                                                   fila['fecha'])]
            else:
                reproducciones[fila['usuario_id']].append(Reproduccion(fila['id_reproduccion'], fila['usuario_id'],
                                                                       cancion, fila['fecha']))
    usuarios = {}
    with open('usuarios.csv', encoding='utf8') as file:
        datos = csv.DictReader(file)
        for fila in datos:
            usuarios[fila['usuario_id']] = Usuario(fila['usuario_id'], fila['usuario'], fila['contrasena'],
                                                   reproducciones[fila['usuario_id']])
    return usuarios


def generos_populares(limite):
    usuarios = cargar_datos()
    print(usuarios)
    output1 = {}
    output2 = {}
    for usuario in usuarios.values():
        output1[usuario.usuario] = {}
        for reproduccion in usuario.reproducciones:
            for genero in reproduccion.cancion.genres:
                if genero not in output1[usuario.usuario]:
                    output1[usuario.usuario][genero] = 1
                else:
                    output1[usuario.usuario][genero] += 1

    for key in output1.keys():
        output2[key] = []
        for tupla in output1[key].items():
            if tupla[1] > limite:
                output2[key].append(tupla)
    return output2


def tiempo_gastado(limite):
    usuarios = cargar_datos()
    output = []
    for usuario in usuarios.values():
        tiempo = 0
        for reproduccion in usuario.reproducciones:
            cancion = reproduccion.cancion
            duracion = cancion.duration.split(':')
            minutos = float(duracion[0])
            segundos = float(duracion[1])
            tiempo_cancion = minutos + segundos/60
            tiempo = tiempo + float(tiempo_cancion)
        if tiempo > limite:
            output.append(usuario.usuario)

    return output


print(generos_populares(2))
print(tiempo_gastado(16))
