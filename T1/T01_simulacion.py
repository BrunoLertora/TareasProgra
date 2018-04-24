from CONSTANTES_INFORME import ATRACCIONES, PERSONAS
from T01 import Dueno, Visitante, Atraccion, Parque


class Simulacion:
    def __init__(self):
        self.dueno = None
        self.parque = None
        self.juegos = None
        self.visitantes = []
        self.tiempo = 0
        self.tabla = []

    def inicializar(self):
        # Creamos instancias de la clase atracción y las guardamos en una lista con las atracciones que el dueño
        # podrá comprar. Creamos al dueño Antonio y a su parque, quien compra las 4 atracciones mas baratas
        self.juegos = []
        for key, value in ATRACCIONES.items():
            atraccion = Atraccion(key, value[0], value[1], value[2], value[3])
            self.juegos.append(atraccion)
        self.dueno = Dueno(100000, "Antonio", self.juegos)
        self.parque = Parque(self.dueno)
        self.dueno.comprar_4_atracciones()
        # Creamos instancias de la clase persona y las guardamos en una lista ordenadas por hora de llegada
        for persona in PERSONAS:
            visitante = Visitante(persona[0], persona[1], persona[2], persona[3])
            self.visitantes.append(visitante)
        self.visitantes = sorted(self.visitantes, key=lambda x: x.llegada)

    def entrar_parque(self):
        # Chequeamos si llega algún visitante para un tiempo dado en la simuación
        for visitante in self.visitantes:
            if visitante.llegada == self.tiempo:
                self.parque.persona_ingresa(visitante)
                self.visitantes.remove(visitante)
            elif visitante.llegada > self.tiempo:
                break

    def entrar_atracciones(self):
        self.parque.entrar_atracciones()

    def funcionar_parque(self):
        self.parque.funcionar_atracciones()

    def partir(self, n):
        dias_tabla = [3, 6, 9, 15, 30, 60]
        dias_tabla = [x * 60 * 24 for x in dias_tabla]
        while self.tiempo <= 86400:
            # Imprimir tiempo
            if self.tiempo == 1:
                print("\nt = {} minuto".format(self.tiempo))
            else:
                print("\nt = {} minutos".format(self.tiempo))
            #if len(self.dueno.atracciones_no_compradas) == 0:
            #    print("Se compraron todas")
            #    break
            # Caso en que dueño compra atracciones segun su costo de entrada
            if n == 1:
                if len(self.dueno.atracciones_no_compradas) != 0:
                    self.dueno.agregar_atraccion_costo_entrada()
                    self.parque.atracciones_compradas = self.dueno.atracciones_compradas
            # Caso en que dueño compra atracciones segun su capacidad
            elif n == 2:
                if len(self.dueno.atracciones_no_compradas) != 0:
                    self.dueno.agregar_atraccion_capacidad()
                    self.parque.atracciones_compradas = self.dueno.atracciones_compradas
            # Cambiamos atributo de duplicacion cuando el dinero del dueño supera nuevamente los 100.000 HC
            if self.dueno.dinero > 100000 and self.dueno.duplicacion:
                self.dueno.duplicacion = False
            # Se revisa si se necesitan duplicar los precios, luego se verifica si alguien entra al parque en el
            # tiempo t, las personas que esten disponibles van a la atraccion mas cara que pueden comprar y estas
            # comienzan a funcionar
            self.dueno.duplicar_precios()
            self.entrar_parque()
            self.entrar_atracciones()
            self.funcionar_parque()
            if self.tiempo in dias_tabla:
                self.tabla.append([self.tiempo, int(self.dueno.dinero)])
            self.tiempo += 1


simulacion = Simulacion()
simulacion2 = Simulacion()
simulacion.inicializar()
simulacion.partir(1)
simulacion2.inicializar()
simulacion2.partir(2)
print(simulacion.tabla)
print(simulacion2.tabla)

