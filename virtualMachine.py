import sys
from virtualMem import *
import numpy as np
import statistics as statistics
import matplotlib.pyplot as plt

# Se declaran constantes
GBL = 'globales'
LCL = 'locales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 1000


# Se inicializan las instancias de memoria default, global y funcion principal
mem_GLOBAL = virtualMem('global')
mem_PRINCIPAL = virtualMem('principal')

constLista = []
cuaLista = []
cuaIndice = 0
cuadruplo = ()
pilaRetorno = []
pilaFuncion = []
sigCuaIndice = -1

pilaTemporal = []
pilaEjecucion = []
pilaCorriendo = ''

# Se declaran los espacios de memoria por tipo
limite_intGlobales = ESPACIO_MEMORIA
limite_floatGlobales = limite_intGlobales + ESPACIO_MEMORIA
limite_stringsGlobales = limite_floatGlobales + ESPACIO_MEMORIA
limite_charGlobales = limite_stringsGlobales + ESPACIO_MEMORIA
limite_dfGlobales = limite_charGlobales + ESPACIO_MEMORIA

limite_intLocales = limite_dfGlobales + ESPACIO_MEMORIA
limite_floatLocales = limite_intLocales + ESPACIO_MEMORIA
limite_stringsLocales = limite_floatLocales + ESPACIO_MEMORIA
limite_charLocales = limite_stringsLocales + ESPACIO_MEMORIA
limite_dfLocales = limite_charLocales + ESPACIO_MEMORIA

limite_intTemporales = limite_dfLocales + ESPACIO_MEMORIA
limite_floatTemporales = limite_intTemporales + ESPACIO_MEMORIA
limite_stringsTemporales = limite_floatTemporales + ESPACIO_MEMORIA
limite_charTemporales = limite_stringsTemporales + ESPACIO_MEMORIA
limite_dfTemporales = limite_charTemporales + ESPACIO_MEMORIA
limite_boolTemporales = limite_dfTemporales + ESPACIO_MEMORIA

limite_intConstantes = limite_boolTemporales + ESPACIO_MEMORIA
limite_floatConstantes = limite_intConstantes + ESPACIO_MEMORIA
limite_stringsConstantes = limite_floatConstantes + ESPACIO_MEMORIA
limite_charConstantes = limite_stringsConstantes + ESPACIO_MEMORIA
limite_dfConstantes = limite_charConstantes + ESPACIO_MEMORIA


######## Funciones que controlan las pilas

# Funcion para hacer push a las diferenes pilas y poder manear las diferentes instancias de memmoria
def push(pilaNom, mem):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        pilaTemporal.append(mem)
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        pilaEjecucion.append(mem)
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        pilaRetorno.append(mem)
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        pilaFuncion.append(mem)

# Funcion para hacer pop a las diferenes pilas y poder manear las diferentes instancias de memmoria
def pop(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        return pilaTemporal.pop()
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        return pilaEjecucion.pop()
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        return pilaRetorno.pop()
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        return pilaFuncion.pop()

# Funcion para sacar pop de las principales pilas a las diferenes pilas y poder manear las diferentes instancias de memmoria
def top(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        aux = len(pilaTemporal) - 1
        if (aux < 0):
            return 'vacia'
        return pilaTemporal[aux]
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        aux = len(pilaEjecucion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaEjecucion[aux]

# Declaramos la primera instancia de la memoria principal
push(CONST_EJECUCION, mem_PRINCIPAL)

# Permite obtener los valores de la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
def getValor(memVirtual, memDireccion, memTipo):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
        if memDireccion[-1] == '!':
            memDireccion = getValor(memVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    seccion = getSeccion(memDireccion)
    try:
        if seccion == GBL:
            valor = mem_GLOBAL.obtenerValorDeDireccion(memDireccion, memTipo)
        elif seccion == LCL:
            valor = memVirtual.obtenerValorDeDireccion(memDireccion, memTipo)
        else:
            print("Error Maquina Virtual: No se encontró sección {} de memoria".format(seccion))
            sys.exit()
    except:
        print("Error Maquina Virtual: ", sys.exc_info()[0], " en seccion {}, en direccion {}, en indice {}.".format(seccion, memDireccion, cuaIndice))
        sys.exit()
    return valor

# Permite insertar los valores a la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
def llenarValor(memVirtual, memDireccion, memTipo, valor):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
        if memDireccion[-1] == '!':
            memDireccion = getValor(memVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    seccion = getSeccion(memDireccion)

    if seccion == GBL:
        mem_GLOBAL.guardarValor(memDireccion, memTipo, valor)
    elif seccion == LCL:
        memVirtual.guardarValor(memDireccion, memTipo, valor)
    else:
        print("Error Maquina Virtual: No se encontró sección de memoria")
        sys.exit()
        return


# Obtiene la sección de la memoria mediante el número
def getSeccion(direccion):
    global pilaCorriendo
    try:
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    # GLOBALES y CONSTANTES se guardan donde mismo
    if ((direccion >= 0 and direccion < limite_dfGlobales) or (direccion >= limite_boolTemporales and direccion <= limite_dfConstantes)):
        return GBL
    # LOCALES y TEMPORALES se guardan donde mismo
    if ((direccion >= limite_dfGlobales and direccion < limite_dfLocales) or (direccion >= limite_dfLocales and direccion < limite_boolTemporales)):
        return LCL
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro de ninguna seccion".format(direccion))
        sys.exit()
        return

# Obtiene el tipo al que pertenece la direccion que recibe como parámetro
def getTipo(direccion):
    global pilaCorriendo
    try:
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    if ((direccion >= 0 and direccion < limite_intGlobales) or (direccion >= limite_dfGlobales and direccion < limite_intLocales) or (direccion >= limite_dfLocales and direccion < limite_intTemporales) or (direccion >= limite_boolTemporales and direccion < limite_intConstantes)):
        return 'int'
    if ((direccion >= limite_intGlobales and direccion < limite_floatGlobales) or (direccion >= limite_intLocales and direccion < limite_floatLocales) or (direccion >= limite_intTemporales and direccion < limite_floatTemporales) or (direccion >= limite_intConstantes and direccion < limite_floatConstantes)):
        return 'float'
    if ((direccion >= limite_floatGlobales and direccion < limite_stringsGlobales) or (direccion >= limite_floatLocales and  direccion < limite_stringsLocales) or (direccion >= limite_floatTemporales and direccion < limite_stringsTemporales) or (direccion >= limite_floatConstantes and direccion < limite_stringsConstantes)):
        return 'string'
    if ((direccion >= limite_stringsGlobales and direccion < limite_charGlobales) or (direccion >= limite_stringsLocales and direccion <limite_charLocales) or (direccion >= limite_stringsTemporales and direccion < limite_charTemporales) or (direccion >= limite_stringsConstantes and direccion < limite_charConstantes)):
        return 'char'
    if ((direccion >= limite_charGlobales and direccion < limite_dfGlobales) or (direccion >= limite_charLocales and direccion < limite_dfLocales) or (direccion >= limite_charTemporales and direccion < limite_dfTemporales) or (direccion >= limite_charConstantes and direccion < limite_dfConstantes)):
        return 'dataframe'
    if (direccion >= limite_dfTemporales and direccion < limite_boolTemporales):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(direccion))
        sys.exit()
        return

# Obtiene el signo
def operadores(signo):
    global cuadruplo
    global pilaCorriendo
    if signo == '+':
        if cuadruplo[1][0] == '{' and cuadruplo[1][-1] == '}':  # En caso de que se refiera a la suma de la direccion de vector
            valor1 = int(cuadruplo[1][1:-1])
            valor2 = getValor(pilaCorriendo, cuadruplo[2], getTipo(cuadruplo[2]))
            valor2 = int(valor2)
        else: # Suma normal de dos valores
            tipo1 = getTipo(cuadruplo[1])
            tipo2 = getTipo(cuadruplo[2])
            valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
            valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

            if tipo1 == 'int':
                valor1 = int(valor1)
            elif tipo1 == 'float':
                valor1 = float(valor1);

            if tipo2 == 'int':
                valor2 = int (valor2)
            elif tipo2 == 'float':
                valor2 = float(valor2)
            pass
        res = valor1 + valor2
    else:
        tipo1 = getTipo(cuadruplo[1])
        tipo2 = getTipo(cuadruplo[2])
        valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
        valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

        if tipo1 == 'int':
            valor1 = int(valor1)
        elif tipo1 == 'float':
            valor1 = float(valor1)

        if tipo2 == 'int':
            valor2 = int(valor2)
        elif tipo2 == 'float':
            valor2 = float(valor2)

        if signo == '-':
            res = valor1 - valor2
        elif signo == '*':
            res = valor1 * valor2
        elif signo == '/':
            res = valor1 / valor2
        elif signo == '==':
            res = valor1 == valor2
        elif signo == '<':
            res = valor1 < valor2
        elif signo == '>':
            res = valor1 > valor2
        elif signo == '<=':
            res = valor1 <= valor2
        elif signo == '>=':
            res = valor1 >= valor2
        elif signo == '!=':
            res = valor1 != valor2
        elif signo == '|':
            res = True if valor1 == valor2 and valor1 == False and valor2 == False else False
        elif signo == '&':
            res = True if valor1 == valor2 and valor1 == True else False

    llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)


# Verifica que los indices esten dentro del dataframe o arreglo
def verificar(arr, de, a):
    l = len(arr) - 1
    if de < 0 or de > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe o arreglo 0 a {} ".format(de,l))
        sys.exit()
        return False
    if  a < 0 or a > l:
        print("Error Maquina Virtual: el inidice {} no esta dentro del rango del dataframe o arreglo 0 a {} ".format(a,l))
        sys.exit()
        return False
    return True