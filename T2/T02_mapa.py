from abc import ABCMeta
from T02_limpieza import limpieza

class Celda(metaclass=ABCMeta):
    def __init__(self, pos_x, pos_y, coordenada):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.coordenada = coordenada
        self.nodo_izq = None
        self.nodo_der = None
        self.nodo_arriba = None
        self.nodo_abajo = None
        self.nodo_diag_izq1 = None
        self.nodo_diag_izq2 = None
        self.nodo_diag_der1 = None
        self.nodo_diag_der2 = None


class Obstaculo(Celda):
    def __init__(self, pos_x, pos_y, coordenada):
        super(Obstaculo, self).__init__(pos_x, pos_y, coordenada)


class Espacio(Celda):
    def __init__(self, pos_x, pos_y, dificultad, coordenada):
        super(Espacio, self).__init__(pos_x, pos_y, coordenada)
        self.dificultad = dificultad


class Grafo:
    def __init__(self):
        self.mapa = []

    def agregar_nodos(self):
        limpieza()
        datos = []
        largos = []
        lectura = open('mapa_arreglado.txt', "r", encoding='utf-8')
        for linea in lectura:
            linea = linea.replace('\n', "")
            lista = linea.split(',')
            largos.append(len(lista))
            datos.append(lista)
        columnas = max(largos)
        filas = len(datos)

        for y in range(filas):
            self.mapa.append([])
            for x in range(columnas):
                coordenada = str(chr(y+65)) + str(x+1)
                try:
                    dato = datos[y][x]
                    if dato == 'X':
                        obstaculo = Obstaculo(x,y, coordenada)
                        self.mapa[y].append(obstaculo)
                    else:
                        camino = Espacio(x,y, dato, coordenada)
                        self.mapa[y].append(camino)
                except:
                    vacio = Espacio(x,y,0,coordenada)
                    self.mapa[y].append(vacio)

    def actualizar_nodos(self):
        for linea in self.mapa:
            for nodo in linea:
                x = nodo.pos_x
                y = nodo.pos_y
                try:
                    if x > 0:
                        nodo.nodo_izq = self.mapa[y][x-1]
                except IndexError:
                    pass
                try:
                    nodo.nodo_der = self.mapa[y][x+1]
                except IndexError:
                    pass
                try:
                    nodo.nodo_abajo = self.mapa[y+1][x]
                except IndexError:
                    pass
                try:
                    if y > 0:
                        nodo.nodo_arriba = self.mapa[y - 1][x]
                except IndexError:
                    pass
        for linea in self.mapa:
            for nodo in linea:
                x = nodo.pos_x
                y = nodo.pos_y
                try:
                    if x > 0 and y > 0:
                        nodo.nodo_diag_izq1 = self.mapa[y-1][x-1]
                except IndexError:
                        pass
                try:
                    if x > 0:
                        nodo.nodo_diag_izq2 = self.mapa[y+1][x-1]
                except IndexError:
                        pass
                try:
                    if y > 0:
                        nodo.nodo_diag_der1 = self.mapa[y-1][x+1]
                except IndexError:
                        pass
                try:
                     nodo.nodo_diag_der2 = self.mapa[y+1][x+1]
                except IndexError:
                        pass





a = Grafo()
a.agregar_nodos()
a.actualizar_nodos()

for nodos in a.mapa:
    for nodo in nodos:
        print('......')
        print(nodo.pos_x, nodo.pos_y)
        print('diagder1')
        try:
            print(nodo.nodo_diag_der1.pos_x, nodo.nodo_diag_der1.pos_y)
        except:
            pass



