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
        self.vecinos = [self.nodo_diag_izq1, self.nodo_izq, self.nodo_diag_izq2, self.nodo_arriba, self.nodo_abajo, self.nodo_diag_der1, self.nodo_der, self.nodo_diag_der2]


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
        lectura = open('mapa_arreglado.txt', "r", encoding='utf-8')
        datos = []
        for linea in lectura:
            linea = linea.replace('\n', "")
            lista = linea.split(',')
            datos.append(lista)
        for linea in range(len(datos)):
            self.mapa.append([])
            for vertice in range(len(datos[linea])):
                coordenada = str(chr(linea + 65)) + str(vertice)
                if datos[linea][vertice] == "X":
                    obstaculo = Obstaculo(vertice, linea, coordenada)
                    self.mapa[linea].append(obstaculo)
                else:
                    camino = Espacio(vertice, linea, datos[linea][vertice], coordenada)
                    self.mapa[linea].append(camino)

    def actualizar_nodos(self):
        for linea in self.mapa:
            for nodo in linea:
                x = nodo.pos_x
                y = nodo.pos_y
                if self.mapa[y][x-1] and x > 0:
                    nodo.nodo_izq = self.mapa[y][x-1]
                try:
                    nodo.nodo_der = self.mapa[y][x+1]
                except IndexError:
                    pass
                try:
                    nodo.nodo_abajo = self.mapa[y+1][x]
                except IndexError:
                    pass
                if y > 0:
                    try:
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
for b in a.mapa:
    for c in b:
        print(c.pos_x, c.pos_y, c.coordenada)
        try:
            print(c.nodo_diag_izq1.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_izq.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_diag_izq2.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_arriba.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_abajo.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_diag_der1.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_der.coordenada)
        except:
            print("No")
        try:
            print(c.nodo_diag_der2.coordenada)
        except:
            print("No")
        print("\n")
