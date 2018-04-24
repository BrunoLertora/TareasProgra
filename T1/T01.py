from abc import ABCMeta
from datetime import datetime


class Persona(metaclass=ABCMeta):
    def __init__(self, dinero, nombre):
        self.dinero = dinero
        self.nombre = nombre


class Dueno(Persona):
    def __init__(self, dinero, nombre, lista_atracciones):
        super().__init__(dinero, nombre)
        self.atracciones_compradas = []
        self.atracciones_no_compradas = lista_atracciones
        self.duplicacion = False

    def comprar_4_atracciones(self):
        # Para cada atraccion, guardamos en una lista la atraccion y su costo de compra.
        lista_aux = []
        for atrac in self.atracciones_no_compradas:
            lista_aux.append((atrac, atrac.costo_atraccion))
        # Adquirimos las 4 atracciones con menor costo de compra
        for i in range(4):
            atrac, costo = min(lista_aux, key=lambda t: t[1])
            self.atracciones_compradas.append(atrac)
            lista_aux.remove((atrac, costo))
            print("El dueño ha comprado la atracción {}".format(atrac.nombre))
            if atrac.duracion == 1:
                print(
                    "Capacidad Máxima: {} personas\nCosto de Entrada: {} HC\nDuración de la Vuelta: {} minuto\n".format(
                        atrac.capacidad, atrac.costo_entrada, atrac.duracion))
            else:
                print(
                    "Capacidad Máxima: {} personas\nCosto de Entrada: {} HC\nDuración de la Vuelta: {} minutos\n".format
                    (atrac.capacidad, atrac.costo_entrada, atrac.duracion))
        # Actalizamos la lista de atracciones que no se han comprado
        self.atracciones_no_compradas = list(set(self.atracciones_no_compradas) - set(self.atracciones_compradas))

    def agregar_atraccion_costo_entrada(self):
        if self.dinero >= 500000:
            # Para cada atraccion no comprarda, guardamos en una lista la atraccion y su costo de entrada.
            lista_aux = []
            for atrac in self.atracciones_no_compradas:
                lista_aux.append((atrac, atrac.costo_entrada))
            # Compramos la atracción con mayor costo de entrada y actualizamos el dinero del dueño
            atrac, entrada = max(lista_aux, key=lambda t: t[1])
            self.atracciones_compradas.append(atrac)
            self.dinero = self.dinero / 2
            print("El dueño ha comprado la atracción {}".format(atrac.nombre))
            print("Capacidad Máxima: {}\nCosto de Entrada: {}\nDuración de la Vuelta: {}\n".format(atrac.capacidad,
                                                                                                   atrac.costo_entrada,
                                                                                                   atrac.duracion))
            # Actalizamos la lista de atracciones que no se han comprado
            self.atracciones_no_compradas = list(set(self.atracciones_no_compradas) - set(self.atracciones_compradas))

    def agregar_atraccion_capacidad(self):
        if self.dinero >= 500000:
            # Para cada atraccion no comprarda, guardamos en una lista la atraccion y su capacidad.
            lista_aux = []
            for atrac in self.atracciones_no_compradas:
                lista_aux.append((atrac, atrac.capacidad))
            # Compramos la atracción con mayor capacidad y actualizamos el dinero del dueño
            atrac, capacidad = max(lista_aux, key=lambda t: t[1])
            self.atracciones_compradas.append(atrac)
            self.dinero = self.dinero / 2
            # Actalizamos la lista de atracciones que no se han comprado
            self.atracciones_no_compradas = list(set(self.atracciones_no_compradas) - set(self.atracciones_compradas))

    def duplicar_precios(self):
        if self.dinero < 100000 and not self.duplicacion:
            # Duplicamos el costo de la entrada de cada atraccion que ya ha sido comprada por el dueño
            print("El dueño ha duplicado el precio de las atracciones")
            print("Nuevos Precios:")
            for atrac in self.atracciones_compradas:
                atrac.costo_entrada = 2 * atrac.costo_entrada
                print("{}: {} HC".format(atrac.nombre, atrac.costo_entrada))
            print("\n")
            self.duplicacion = True

    def cobrar(self, visitante, precio):
        if visitante.edad < 8:
            self.dinero += precio/2
        else:
            self.dinero += precio
        visitante.pagar(precio)

    def pagar_demanda(self, visitante):
        if visitante.edad < 18:
            self.dinero -= 20000
        else:
            self.dinero -= 10000


class Visitante(Persona):
    def __init__(self, dinero, llegada, nombre, nacimiento):
        super().__init__(dinero, nombre)
        self.llegada = llegada
        self.nacimiento = nacimiento
        b_date = datetime.strptime(nacimiento, '%Y-%m-%d')
        self.edad = int((datetime.today() - b_date).days/365)
        self.en_parque = False
        self.en_atraccion = False

    def retirada(self):
        self.en_parque = False
        print("{} se retira del parque dignamente con {} HC".format(self.nombre, self.dinero))

    def pagar(self, precio):
        if self.edad < 8:
            self.dinero -= precio/2
        else:
            self.dinero -= precio


class Atraccion:
    def __init__(self, nombre, capacidad, costo_entrada, costo_atraccion, duracion):
        self.nombre = nombre
        self.capacidad = capacidad
        self.costo_entrada = costo_entrada
        self.costo_atraccion = costo_atraccion
        self.duracion = duracion
        # El atributo tiempo indica cuanto tiempo falta para que termine la vuelta de la atraccion
        self.tiempo = duracion
        self.usuarios = []
        self.cola = []
        self.vida = 100
        self.abierta = True
        self.tiempo_cerrada = 0
        self.recaudacion = 0
        self.indemnizacion = 0

    def ingresar(self, visitante):
        self.cola.append(visitante)
        visitante.en_atraccion = True

    def funcionar(self, dueno):
        # Caso en que la atraccion esté abierta
        if self.abierta:
            # Caso en que atraccion esté disponible para ser usada y que haya gente en cola esperando para subir
            if self.duracion == self.tiempo and len(self.cola) > 0:
                # Se suben las personas hasta que no hayan más en cola o que la atracción se llene
                while len(self.usuarios) < self.capacidad and len(self.cola) > 0:
                    visitante = self.cola[0]
                    # Se verifica si los precios actuales de la atracción siguen siendo pagables por la persona
                    if visitante.edad < 8:
                        if visitante.dinero < self.costo_entrada / 2:
                            visitante.en_atraccion = False
                        else:
                            dueno.cobrar(visitante, self.costo_entrada)
                            self.usuarios.append(visitante)
                    else:
                        if visitante.dinero < self.costo_entrada:
                            visitante.en_atraccion = False
                        else:
                            dueno.cobrar(visitante, self.costo_entrada)
                            self.usuarios.append(visitante)
                    self.cola = self.cola[1:]
                for visitante in self.usuarios:
                    if visitante.edad < 8:
                        self.recaudacion += self.costo_entrada / 2
                    else:
                        self.recaudacion += self.costo_entrada
                    self.vida -= 1
                print("Se subieron {} personas a {}. Se recaudaron {} HC en esta vuelta".format(len(self.usuarios),
                                                                                                self.nombre,
                                                                                                self.recaudacion))
                self.tiempo -= 1
                # Inmediatamente después de empezar la vuelta se chequea si la atracción falla o no
                self.chequear(dueno)
            # Caso en que atracción esté en vuelta
            elif self.duracion > self.tiempo > 0:
                self.tiempo -= 1
            # Caso en que atraccion haya terminado de la vuelta
            elif self.tiempo == 0:
                for visitante in self.usuarios:
                    visitante.en_atraccion = False
                self.usuarios = []
                self.tiempo = self.duracion
                self.recaudacion = 0
            # Caso en que atraccion esté disponible para ser usada y no haya nadie en cola esperando para subir
            else:
                self.tiempo -= 1
        # Caso en que atraccion esté cerrada
        else:
            # La atraccion abre 1 hora despues de estar cerrada entonces al minuto 60 self.abierta ya tiene que ser True
            if self.tiempo_cerrada == 59:
                self.abierta = True
                self.tiempo_cerrada = 0
            else:
                self.tiempo_cerrada += 1

    def chequear(self, dueno):
        # Si ya se han subido 100 o más personas a la atracción, esta falla y se pagan las indemnizaciones
        if self.vida <= 0:
            for visitante in self.usuarios:
                dueno.pagar_demanda(visitante)
                if visitante.edad < 18:
                    self.indemnizacion += 20000
                else:
                    self.indemnizacion += 10000
            print("Falló {}! Se evacuaron a {} personas, que fueron indemnizados por {} HC".format(self.nombre,
                                                                                                   len(self.usuarios),
                                                                                                   self.indemnizacion))
            # Usuarios que se tuvieron que bajar se van del parque, usuarios en cola se retiran de la cola y quedan
            # disponibles para ir a otra atracción al siguiente minuto de la simulación
            for visitante in self.usuarios:
                visitante.en_atraccion = False
                visitante.retirada()
            for visitante in self.cola:
                visitante.en_atraccion = False
            self.usuarios = []
            self.cola = []
            self.vida = 100
            self.abierta = False
            self.tiempo = self.duracion
            self.indemnizacion = 0
            self.tiempo_cerrada += 1


class Parque:
    def __init__(self, dueno):
        self.dueno = dueno
        self.atracciones_compradas = dueno.atracciones_compradas
        self.atracciones_no_compradas = dueno.atracciones_no_compradas
        self.visitantes = []

    def persona_ingresa(self, visitante):
        print("Entró {} de {} años al parque con {} HC".format(visitante.nombre, visitante.edad, visitante.dinero))
        visitante.en_parque = True
        self.visitantes.append(visitante)

    def entrar_atracciones(self):
        self.atracciones_compradas = sorted(self.atracciones_compradas, reverse=True, key=lambda x: x.costo_entrada)
        barato = self.atracciones_compradas[-1].costo_entrada
        # Para cada visitante en el parque se chequea que no esté en ninguna atracción y que tenga el dinero para
        # comprar, por lo menos, la entrada mas barata. Si tiene dinero suficiente se sube a la atraccion más cara que
        # pueda pagar, de lo contrario, se retira del parque
        for visitante in self.visitantes:
            if not visitante.en_atraccion and visitante.en_parque:
                if visitante.edad < 8:
                    if visitante.dinero < barato/2:
                        visitante.retirada()
                        self.visitantes.remove(visitante)
                    else:
                        for atraccion in self.atracciones_compradas:
                            if not visitante.en_atraccion and atraccion.costo_entrada / 2 <= visitante.dinero and\
                                    atraccion.abierta:
                                atraccion.ingresar(visitante)
                else:
                    if visitante.dinero < barato:
                        visitante.retirada()
                        self.visitantes.remove(visitante)
                    else:
                        for atraccion in self.atracciones_compradas:
                            if not visitante.en_atraccion and atraccion.costo_entrada <= visitante.dinero and\
                                    atraccion.abierta:
                                atraccion.ingresar(visitante)

    def funcionar_atracciones(self):
        # Se hacen funcionar todas las atracciones que ya han sido compradas por el dueño
        for atraccion in self.atracciones_compradas:
            atraccion.funcionar(self.dueno)
