from functools import reduce


# Verificamos si un caracter contiene un salto de linea. De contenerlo, se lo quitamos
def es_salto_linea(letra):
    if "\n" in letra:
        return letra.replace("\n", "")
    return letra


# A partir de una lista de caracteres, se aplica es_salto_linea para cada caracter
def cambiar_salto(lista):
    lista2 = [es_salto_linea(letra) for letra in lista]
    return lista2


# Verificamos si el caracter es un simbolo. De serlo, lo cambiamos a un obstaculo
def es_simbolo(letra):
    simbolos = ["!", "#", "$", "%", "&", "(", ")", "=", "?"]
    if letra in simbolos:
        return "X"
    return letra


# A partir de una lista de caracteres, se aplica es_simbolo para cada caracter
def cambiar_simbolo(lista):
    lista2 = [es_simbolo(letra) for letra in lista]
    return lista2


# Verificamos si el caracter es una letra o no
def no_es_letra(letra):
    if letra == "X":
        return True
    elif letra.isalpha():
        return False
    else:
        return True


# A partir de una lista se deveuelve un lista cumple con no_es_letra
def quitar_letras(lista):
    return list(filter(no_es_letra, lista))


# A partir de una lista se devuelve una lista con las operaciones resueltas
def resolver_operacion(lista):
    lista2 = [eval(letra) if letra != "X" else letra for letra in lista]
    return lista2


# Agregar comas entre espacios
def agregar_comas(lista):
    lista2 = reduce(lambda x, y: str(x) + "," + str(y), lista)
    return lista2 + "\n"


# Arregla el archivo mapa.txt
def limpieza():
    # Abrimos el archivo que se quiere arreglar
    file = open('mapa.txt', "r", encoding='utf-8')
    # Guardamos el contenido de cada linea del archivo
    lineas = [linea for linea in file]
    # Guardamos los espacios del mapa de cada linea en listas
    lineas = [linea.split(',') for linea in lineas]
    # Quitamos los saltos de linea de la lista
    lineas = [cambiar_salto(linea) for linea in lineas]
    # Cambiamos los simbolos por obstaculos
    lineas = [cambiar_simbolo(linea) for linea in lineas]
    # Quitamos las letras que no sean X
    lineas = [quitar_letras(linea) for linea in lineas]
    # Resolvemos las operaciones
    lineas = [resolver_operacion(linea) for linea in lineas]
    # Agregamos comas entre caracteres
    lineas = [agregar_comas(linea) for linea in lineas]
    # Eliminamos el ultimo salto de linea
    lineas[-1] = lineas[-1][:-1]
    outfile = open('mapa_arreglado.txt', "w", encoding='utf-8')
    outfile.writelines(item for item in lineas)
