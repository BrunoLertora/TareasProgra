from abc import ABCMeta
from T02_limpieza import limpieza


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def get(self):
        a = self.queue[0]
        self.queue = self.queue[1:]
        return a

    def put(self, cosa):
        lista = []
        for item in self.queue:
            if cosa[0] < item[0]:
                lista.append(cosa)
            elif cosa[0] == item[0]:
                lista.append(item)
                lista.append(cosa)
            else:
                lista.append(item)
        if cosa not in lista:
            lista.append(cosa)
        self.queue = lista


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
        self.gn = 0
        self.hn = 0
        self.fn = 0


class Obstaculo(Celda):
    def __init__(self, pos_x, pos_y, coordenada, dificultad="X"):
        super(Obstaculo, self).__init__(pos_x, pos_y, coordenada, dificultad)


class Espacio(Celda):
    def __init__(self, pos_x, pos_y, coordenada, dificultad):
        super(Espacio, self).__init__(pos_x, pos_y, coordenada, dificultad)


class Grafo:
    # Utilizamos la lista mapa sólo para sacar la información del archivo de texto y luego poblar el grafo.
    # A partir de ahí sólo usamos el grafo y las celdas(nodos)
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

    # Creamos conecciones en ambos sentidos entre todos los nodos que sean vecinos. Con esto poblamos el grafo
    def crear_conecciones(self):
        for linea in self.mapa:
            for nodo in linea:
                if nodo.dificultad != "X":
                    self.grafo[nodo] = set()
                    for vecino in nodo.vecinos:
                        if vecino and vecino.dificultad != "X":
                            self.grafo[nodo].add(vecino)
                else:
                    self.grafo[nodo] = set()

    # A partir de una coordenada, se retorna el nodo correspondiente
    def buscar_vertice(self, coordenada):
        nodos = self.grafo.keys()
        for key in nodos:
            if key.coordenada == coordenada:
                return key

    # Se resetean los valores de fn, gn y hn para que no influyan en la siguiente consulta de camino_minimo
    def reset(self):
        nodos = self.grafo.keys()
        for key in nodos:
            key.fn = 0
            key.gn = 0
            key.hn = 0

    def camino_minimo(self, modo, start, goal, actual, frontier=PriorityQueue(), came_from={}, cost_so_far={}):
        if actual is None:
            frontier.put((0, start))
            came_from[start] = None
            cost_so_far[start] = 0
            output = self.camino_minimo(modo, start, goal, start, frontier, came_from, cost_so_far)
            return output
        elif actual != goal:
            for next in actual.vecinos:
                if isinstance(next, Espacio):
                    new_cost = int(cost_so_far[actual]) + int(next.dificultad)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        if modo == 1:
                            priority = new_cost + distancia_manhattan(next, goal)
                        elif modo == 2:
                            priority = new_cost + distancia_euclidiana(next, goal)
                        elif modo == 3:
                            priority = new_cost + distancia_chebyshev(next, goal)
                        frontier.put((priority, next))
                        came_from[next] = actual
            try:
                actual = frontier.get()[1]
            except IndexError:
                return came_from, cost_so_far
            output = self.camino_minimo(modo, start, goal, actual, frontier, came_from, cost_so_far)
            return output
        elif actual == goal:
            return [came_from, cost_so_far]

    def ruta_optima(self):
        print("Ruta óptima considerando costos")
        origen = str(input("Ingrese coordenada de Origen: "))
        destino = str(input("Ingrese coordenada de Destino: "))
        output1 = self.camino_minimo(1, self.buscar_vertice(origen), self.buscar_vertice(destino), None)
        output2 = self.camino_minimo(1, self.buscar_vertice(origen), self.buscar_vertice(destino), None)
        output3 = self.camino_minimo(1, self.buscar_vertice(origen), self.buscar_vertice(destino), None)
        costo1 = output1[1][self.buscar_vertice(destino)]
        costo2 = output2[1][self.buscar_vertice(destino)]
        costo3 = output3[1][self.buscar_vertice(destino)]
        a = destino
        camino1 = []
        camino2 = []
        camino3 = []
        camino1.append(destino)
        camino2.append(destino)
        camino3.append(destino)
        while a:
            camino1.append(a)
            try:
                coordenada = output1[0][self.buscar_vertice(a)].coordenada
                camino1.append(coordenada)
                a = output1[0][self.buscar_vertice(coordenada)].coordenada
            except AttributeError:
                break
        a = destino
        while a:
            camino2.append(a)
            try:
                coordenada = output2[0][self.buscar_vertice(a)].coordenada
                camino2.append(coordenada)
                a = output2[0][self.buscar_vertice(coordenada)].coordenada
            except AttributeError:
                break
        a = destino
        while a:
            camino3.append(a)
            try:
                coordenada = output3[0][self.buscar_vertice(a)].coordenada
                camino3.append(coordenada)
                a = output3[0][self.buscar_vertice(coordenada)].coordenada
            except AttributeError:
                break
        camino1 = camino1[1:]
        camino2 = camino2[1:]
        camino3 = camino3[1:]
        lista1 = []
        if camino1:
            for i in range(len(camino1)-1):
                lista1.append((camino1[i], camino1[i+1]))
        lista2 = []
        if camino2:
            for i in range(len(camino2)-1):
                lista2.append((camino2[i], camino2[i+1]))
        lista3 = []
        if camino3:
            for i in range(len(camino3)-1):
                lista3.append((camino3[i], camino3[i+1]))
        string1 = "Camino Manhattan: "
        string2 = "Camino Euclides: "
        string3 = "Camino Chebyshev: "
        if lista1:
            lista11 = []
            for tupla in lista1:
                t1 = tupla[0]
                t2 = tupla[1]
                lista11.append((t2, t1))
            for tupla in reversed(lista11):
                string1 += str(tupla) + ", "
            string1 += "costo " + str(costo1)
            print(string1)
        else:
            print("Esta heuristica es inadmisible para este problema")
        if lista2:
            lista21 = []
            for tupla in lista2:
                t1 = tupla[0]
                t2 = tupla[1]
                lista21.append((t2, t1))
            for tupla in reversed(lista21):
                string2 += str(tupla) + ", "
            string2 += "costo " + str(costo2)
            print(string2)
        else:
            print("Esta heuristica es inadmisible para este problema")
        if lista3:
            lista31 = []
            for tupla in lista3:
                t1 = tupla[0]
                t2 = tupla[1]
                lista31.append((t2, t1))
            for tupla in reversed(lista31):
                string3 += str(tupla) + ", "
            string3 += "costo " + str(costo3)
            print(string3)
        else:
            print("Esta heuristica es inadmisible para este problema")
        costos = [("Manhattan", costo1), ("Euclides", costo2), ("Chebyshev", costo3)]
        if not costos[0][1] and not costos[1][1] and not costos[2][1]:
            print("Ninguna ruta es admisible para este problema")
        else:
            costos_aux = []
            for costo in costos:
                if costo[1]:
                    costos_aux.append(costo)
            costos_aux.sort(key=lambda tup: tup[1])
            print("Mejor Ruta: " + costos_aux[0][0] + "\n")

    def obstaculo_cercano(self, coordenada_origen, lista=[], visitados=set()):
        # ese paso es para inicializar el algoritmo
        if len(lista) == 0 and len(visitados) == 0:
            # se busca el vertice de la coordenada de origen
            vertice = self.buscar_vertice(coordenada_origen)
            # nodos vecinos al nodo que nos encontramos
            vecinos = vertice.vecinos
            for v in vecinos:
                if v is not None:
                    if isinstance(v, Obstaculo):  # encontramos el obstaculo
                        print('El obstaculo más cercano tiene coordenada:')
                        print(v.coordenada)
                        return v
                    # se agregan a visitados los nodos ya vistos
                    # lista tiene los nodos que se analizaran a la sgte recursión
                    else:
                        if v.coordenada not in visitados:
                            lista.append(v.coordenada)
            visitados.add(vertice.coordenada)
            if len(lista) > 0:
                # lista tiene los nodos que se analizaran, todos
                #  tienen la misma distancia a la coordenada origen
                return self.obstaculo_cercano(coordenada_origen, lista, visitados)
            else:
                return None
        elif len(lista) > 0:
            # se tiene informacion en la lista de los nodos que se van a revisar
            # y luego se actualizan los visitados

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
                return self.obstaculo_cercano(coordenada_origen, lista2, visitados)
            else:
                return None
        # caso en el que se recorretodo porque estarian todos en visitados y lista no tendría mas nodos
        else:
            return None

    def obstaculo(self):
        print("Obstáculo más cercano")
        origen = str(input("Ingrese coordenada de Origen: "))
        self.obstaculo_cercano(origen)
        print("\n")

    def camino_corto(self):
        print("Ruta con menos cantidad de movimientos")
        coordenada_origen = str(input("Ingrese coordenada de Origen: "))
        coordenada_destino = str(input("Ingrese coordenada de Destino: "))
        pasos = []
        camino = self.ruta_corta(coordenada_origen, coordenada_destino, list(), set())
        pasos.append((camino[0], camino[1]))
        while camino[0] != coordenada_origen:
            camino = self.ruta_corta(coordenada_origen, camino[0], list(), set())
            if camino is None:
                print('ERROR')
                return None
            pasos = [(camino[0], camino[1])] + pasos
        print('Camino mas corto')
        string = ""
        for tupla in pasos[:-1]:
            string += str(tupla) + ", "
        string += str(pasos[-1])
        print(string)
        print("\n")

    def ruta_corta(self, coordenada_origen, coordenada_destino, lista=[], visitados=set()):
        # funciona igual que el de obstaculo
        # pero se busca la coordenada de destino
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
                return self.ruta_corta(coordenada_origen, coordenada_destino, lista, visitados)
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
                            # entrega el destino y el último vertice antes de llegar a él
                            return [vertice.coordenada, coordenada_destino]
                        else:
                            if v.coordenada not in visitados and v.coordenada not in lista:
                                lista2.append(v.coordenada)
                visitados.add(coordenada)
            if len(lista2) > 0:
                return self.ruta_corta(coordenada_origen, coordenada_destino, lista2, visitados)
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
