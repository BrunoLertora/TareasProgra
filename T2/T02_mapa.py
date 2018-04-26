from abc import ABCMeta
from T02_limpieza import es_salto_linea, cambiar_salto


class Celda(metaclass=ABCMeta):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.nodo_izq = None
        self.nodo_der = None
        self.nodo_arriba = None
        self.nodo_abajo = None
        self.nodo_diag_izq1 = None
        self.nodo_diag_izq2 = None
        self.nodo_diag_der1 = None
        self.nodo_diag_der2 = None


class Obstaculo(Celda):
    def __init__(self, pos_x, pos_y):
        super(Obstaculo, self).__init__(pos_x, pos_y)


class Espacio(Celda):
    def __init__(self, pos_x, pos_y, dificultad):
        super(Espacio, self).__init__(pos_x, pos_y)
        self.dificultad = dificultad


class Grafo:
    def __init__(self):
        file = open('mapa_arreglado.txt', "r", encoding='utf-8')
        self.mapa = [linea.split(',') for linea in file]
        self.mapa = [cambiar_salto(linea) for linea in self.mapa]

    def agregar_nodos(self):
        for linea in range(len(self.mapa)):
            for vertice in range(len(self.mapa[linea])):
                if self.mapa[linea][vertice] == "X":
                    self.mapa[linea][vertice] = Obstaculo(vertice, linea)
                else:
                    self.mapa[linea][vertice] = Espacio(vertice, linea, self.mapa[linea][vertice])

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
        # for linea in self.mapa:
        #     for nodo in linea:
        #         x = nodo.pos_x
        #         y = nodo.pos_y
        #         if nodo.nodo_arriba and nodo.nodo_izq:
        #             nodo.nodo_diag_izq1 = self.mapa[y-1][x-1]
        #         if nodo.nodo_abajo and nodo.nodo_izq:
        #             nodo.nodo_diag_izq2 = self.mapa[y+1][x-1]
        #         if nodo.nodo_arriba and nodo.nodo_der:
        #             nodo.nodo_diag_der1 = self.mapa[y-1][x+1]
        #         if nodo.nodo_abajo and nodo.nodo_der:
        #             nodo.nodo_diag_der2 = self.mapa[y+1][x+1]





a = Grafo()
a.agregar_nodos()
a.actualizar_nodos()
for b in a.mapa:
    for nodo in b:
        #print(c.pos_x, c.pos_y, c.nodo_arriba, c.nodo_abajo, c.nodo_izq, c.nodo_der, c.nodo_diag_izq1, c.nodo_diag_izq2, c.nodo_diag_der1, c.nodo_diag_der2)
