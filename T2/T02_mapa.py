from abc import ABCMeta
from T02_limpieza import limpieza


class Celda(metaclass=ABCMeta):
    def __init__(self, pos_x, pos_y, coordenada, dificultad):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.coordenada = coordenada
        self.dificultad = dificultad
        self.nodo_izq = None
        self.nodo_der = None
        self.nodo_arriba = None
        self.nodo_abajo = None
        self.nodo_diag_izq1 = None
        self.nodo_diag_izq2 = None
        self.nodo_diag_der1 = None
        self.nodo_diag_der2 = None
        self.vecinos = [self.nodo_diag_izq1, self.nodo_izq, self.nodo_diag_izq2, self.nodo_arriba, self.nodo_abajo,
                        self.nodo_diag_der1, self.nodo_der, self.nodo_diag_der2]


class Obstaculo(Celda):
    def __init__(self, pos_x, pos_y, coordenada, dificultad="X"):
        super(Obstaculo, self).__init__(pos_x, pos_y, coordenada, dificultad)


class Espacio(Celda):
    def __init__(self, pos_x, pos_y, coordenada, dificultad):
        super(Espacio, self).__init__(pos_x, pos_y, coordenada, dificultad)


class Grafo:
    def __init__(self):
        self.mapa = []
        self.grafo = {}
        self.agregar_nodos()
        self.actualizar_vecinos()
        self.crear_conecciones()

    def agregar_nodos(self):
        limpieza()
        lectura = open('mapa_arreglado.txt', "r", encoding='utf-8')
        datos = []
        # Guardamos los datos del mapa en una lista
        for linea in lectura:
            linea = linea.replace('\n', "")
            lista = linea.split(',')
            datos.append(lista)
        # Inicializamos los nodos, ya sean obstaculos o espacicos
        for linea in range(len(datos)):
            self.mapa.append([])
            for vertice in range(len(datos[linea])):
                coordenada = str(chr(linea + 65)) + str(vertice)
                if datos[linea][vertice] == "X":
                    obstaculo = Obstaculo(vertice, linea, coordenada)
                    self.mapa[linea].append(obstaculo)
                else:
                    camino = Espacio(vertice, linea, coordenada, datos[linea][vertice])
                    self.mapa[linea].append(camino)

    def actualizar_vecinos(self):
        # Para cada nodo, actualizamos sus 8 vecinos. Primero los verticales u horizontales, y luego los diagonales
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
                nodo.vecinos = [nodo.nodo_diag_izq1, nodo.nodo_izq, nodo.nodo_diag_izq2, nodo.nodo_arriba,
                                nodo.nodo_abajo, nodo.nodo_diag_der1, nodo.nodo_der, nodo.nodo_diag_der2]
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
                nodo.vecinos = [nodo.nodo_diag_izq1, nodo.nodo_izq, nodo.nodo_diag_izq2, nodo.nodo_arriba,
                                nodo.nodo_abajo, nodo.nodo_diag_der1, nodo.nodo_der, nodo.nodo_diag_der2]

    # Creamos conecciones en ambos sentidos entre todos los nodos que sean vecinos
    def crear_conecciones(self):
        for linea in self.mapa:
            for nodo in linea:
                if nodo.dificultad != "X":
                    self.grafo[nodo.coordenada] = set()
                    for vecino in nodo.vecinos:
                        if vecino and vecino.dificultad != "X":
                            self.grafo[nodo.coordenada].add(vecino)
                else:
                    self.grafo[nodo.coordenada] = set()

    # A partir de una coordenada, se retorna el nodo correspondiente
    def buscar_vertice(self, coordenada):
        fila = int(coordenada[1])
        columna = int(ord(coordenada[0])-65)
        vertice = self.mapa[columna][fila]
        return vertice

    def obstaculo_cercano(self, coordenada_origen, lista=list(), visitados=set()):
        vertice = self.buscar_vertice(coordenada_origen)
        vecinos = vertice.vecinos
        for v in vecinos:
            if v is not None:
                if isinstance(v, Obstaculo):
                    print('El obstaculo más cercano tiene coordenada:')
                    print(v.coordenada)
                    return v
                else:
                    if v.coordenada not in visitados:
                        lista.append(v.coordenada)
        visitados.add(coordenada_origen)
        if len(lista) > 0:
            coordenada_origen = lista[0]
            lista = lista[1:]
            self.obstaculo_cercano(coordenada_origen, lista, visitados)
        else:
            return 'No hay'

    def ruta_corta1(self, coordenada_origen, coordenada_destino, lista=list(), visitados=set()):
        vertice = self.buscar_vertice(coordenada_origen)
        vecinos = vertice.vecinos
        for v in vecinos:
            if v is not None and isinstance(v, Espacio):
                if v.coordenada == coordenada_destino:
                    camino = []
                    camino.append(coordenada_origen)
                    camino.append(coordenada_destino)
                    return camino
                else:
                    if v.coordenada not in visitados and v.coordenada not in lista:
                        lista.append(v.coordenada)
        print('aqui')
        print(coordenada_origen, coordenada_destino)
        print(lista)
        print(visitados)

        visitados.add(coordenada_origen)
        if len(lista) > 0:
            coordenada_origen = lista[0]
            lista = lista[1:]
            return self.ruta_corta1(coordenada_origen, coordenada_destino, lista, visitados)
        else:
            return None

    def ruta_corta(self, coordenada_origen, coordenada_destino):
        print(coordenada_origen, coordenada_destino)
        pasos = []
        camino = self.ruta_corta2(coordenada_origen, coordenada_destino, list(), set())
        print(camino)
        pasos.append((camino[0], camino[1]))
        print(pasos)
        while camino[0] != coordenada_origen:
            camino = self.ruta_corta2(coordenada_origen, camino[0], list(), set())
            if camino is None:
                print('ERROR')
                return None

            pasos = [(camino[0], camino[1])] + pasos
        print('Camino mas corto')
        for i in pasos:
            print(i)

    def obstaculo_cercano1(self, coordenada_origen, lista=[], visitados=set()):
        if len(lista) == 0 and len(visitados) == 0:
            vertice = self.buscar_vertice(coordenada_origen)
            vecinos = vertice.vecinos
            for v in vecinos:
                if v is not None:
                    if isinstance(v, Obstaculo):
                        print('El obstaculo más cercano tiene coordenada:')
                        print(v.coordenada)
                        return v
                    else:
                        if v.coordenada not in visitados:
                            lista.append(v.coordenada)
            visitados.add(vertice.coordenada)
            if len(lista) > 0:
                return self.obstaculo_cercano1(coordenada_origen, lista, visitados)
            else:
                return None

        elif len(lista) > 0:
            lista2 = []
            for coordenada in lista:
                vertice = self.buscar_vertice(coordenada)
                vecinos = vertice.vecinos
                for v in vecinos:
                    if v is not None and v.coordenada not in visitados:
                        if isinstance(v, Obstaculo):
                            print('El obstaculo más cercano tiene coordenada:')
                            print(v.coordenada)
                            return v
                        else:
                            if v.coordenada not in visitados and v.coordenada not in lista:
                                lista2.append(v.coordenada)
                visitados.add(coordenada)
            if len(lista2) > 0:
                return self.obstaculo_cercano1(coordenada_origen, lista2, visitados)
            else:
                return None

        else:
            return None

    def ruta_corta2(self, coordenada_origen, coordenada_destino, lista=[], visitados=set()):
        print(lista, visitados)
        if len(lista) == 0 and len(visitados) == 0:
            vertice = self.buscar_vertice(coordenada_origen)
            vecinos = vertice.vecinos
            for v in vecinos:
                if v is not None and isinstance(v, Espacio):
                    if v.coordenada == coordenada_destino:
                        return [vertice.coordenada, coordenada_destino]
                    else:
                        if v.coordenada not in visitados:
                            lista.append(v.coordenada)
            visitados.add(vertice.coordenada)
            if len(lista) > 0:
                return self.ruta_corta2(coordenada_origen, coordenada_destino, lista, visitados)
            else:
                return None

        elif len(lista) > 0:
            lista2 = []
            for coordenada in lista:
                vertice = self.buscar_vertice(coordenada)
                vecinos = vertice.vecinos
                for v in vecinos:
                    if v is not None and v.coordenada not in visitados and isinstance(v, Espacio):
                        if v.coordenada == coordenada_destino:
                            return [vertice.coordenada, coordenada_destino]
                        else:
                            if v.coordenada not in visitados and v.coordenada not in lista:
                                lista2.append(v.coordenada)
                visitados.add(coordenada)
            if len(lista2) > 0:
                return self.ruta_corta2(coordenada_origen,coordenada_destino, lista2, visitados)
            else:
                return None

        else:
            return None






















# Calcular distancia Manhattan a partir de dos objetos de la clase Celda
def distancia_manhattan(nodo_a, nodo_b):
    return abs(nodo_a.pos_x - nodo_b.pos_x) + abs(nodo_a.pos_y - nodo_b.pos_y)


# Calcular distancia euclidiana a partir de dos objetos de la clase Celda
def distancia_euclidiana(nodo_a, nodo_b):
    return ((nodo_a.pos_x - nodo_b.pos_x)**2 + (nodo_a.pos_y - nodo_b.pos_y)**2)**(1/2)


def distancia_chebyshev(nodo_a, nodo_b):
    a = abs(nodo_a.pos_x - nodo_b.pos_x)
    b = abs(nodo_a.pos_y - nodo_b.pos_y)
    return max(a, b)
