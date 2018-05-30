class Vehiculo:
    def __init__(self, patente, tipo, rendimiento, capacidad, id_vehiculo):
        self.patente = patente
        self.tipo = tipo
        self.rendimiento = rendimiento
        self.capacidad = capacidad
        self.id_vehiculo = id_vehiculo
        self.en_uso = False
        self.conductor = None


class Conductor:
    def __init__(self, nombre, apellido, id_conductor):
        self.nombre = nombre
        self.apellido = apellido
        self.id_conductor = id_conductor
        self.en_ruta = False


class Dideco:
    def __init__(self, lista_vehiculos, lista_conductores):
        self.vehiculos = {}
        self.conductores = {}
        self.cronograma = {}
        self.agregar_vehiculos(lista_vehiculos)
        self.agregar_conductores(lista_conductores)
        self.agregar_cronograma()

    # Por cada vehiculo, crear una instancia Vehiculo y agregarla al diccionario self.vehiculos
    def agregar_vehiculos(self, lista_vehiculos):
        i = 1
        for vehiculo in lista_vehiculos:
            patente, tipo, rendimiento, capacidad, id_vehiculo = vehiculo[0], vehiculo[1], vehiculo[2], vehiculo[3], i
            veh = Vehiculo(patente, tipo, rendimiento, capacidad, id_vehiculo)
            self.vehiculos[id_vehiculo] = veh
            i += 1

    # Por cada conductor, crear una instancia Conductor y agregarla al diccionario self.conductores
    def agregar_conductores(self, lista_conducores):
        i = 1
        for conductor in lista_conducores:
            nombre, apellido, id_conductor = conductor[0], conductor[1], i
            con = Conductor(nombre, apellido, id_conductor)
            self.conductores[id_conductor] = con
            i += 1

    def agregar_cronograma(self):
        # Diccionario con los id de vehiculos como llaves y listas del tipo [Vehiculo, dependencia] como valores
        asignacion = {}
        for id_veh, veh in self.vehiculos.items():
            asignacion[id_veh] = [veh, None]
        # Diccionario con las horas cada media hora como llaves y diccionarios de asignación como valores
        # Cada hora representa un bloque de media hora que comienza en dicha hora y termina media hora más tarde
        horario = {}
        t = "8:30"
        termino = "17:30"
        while t != termino:
            horario[t] = asignacion
            t_aux = t.split(":")
            hora = int(t_aux[0])
            min = t_aux[1]
            if min == "30":
                min = "00"
                hora += 1
            elif min == "00":
                min = "30"
            t = str(hora) + ":" + min
        # Actualizamos self.cronograma con los dias de la semana como llaves y diccionarios de horario como valores
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]
        for dia in dias:
            self.cronograma[dia] = horario


class Pedido:
    def __init__(self, dia, salida_min, salida_max, duracion, destino, tipo_vehiculo, dependencia):
        self.dia = dia
        self.salida_min = salida_min
        self.salida_max = salida_max
        self.duracion = duracion
        self.destino = destino
        self.tipo_vehiculo = tipo_vehiculo
        self.dependencia = dependencia
        self.costo_viaje = None


