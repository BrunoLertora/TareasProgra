from T02_mapa import Grafo

grafo = Grafo()

#grafo.ruta_optima()
#grafo.obstaculo()
#grafo.camino_corto()
print(grafo.camino_minimo(1,grafo.buscar_vertice('C0'), grafo.buscar_vertice('C9'), None))
