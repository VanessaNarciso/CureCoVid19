from collections import deque

class VariableTable: 
    def __init__(self, name, vtype)
        self.name = name 
        self.vtype = vtype 

    def name(self):
        return self.name
import ply.lex as lex
import ply.yacc as yacc
import sys

# Librerias necesarias para el analalisis estadistico
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
import matplotlib
import matplotlib.colors
import scipy.special as sps


# Inicializacion de diccionarios,variables y listas necesarias para el compilador
aprobado = True
dir_func = {}
pOper = []
pType = []
pilaO = []
quad = []
pJumps = []
pIterator = []
pReturnTo = []
pFunc = []
pVar = []
pArr = []
contQuads = 0
contParam = 0
funcToCall = ''
currentQuad = 0
memFunc = 30000
Dim = 0
R = 1
toDim = ''
axuDim = 0

# Inicilizacion del scope global
actual_scope = 'global'

# Inicializacion del directorio de funciones vacio
dir_func[actual_scope] = {'type': 'VOID', 'scope': {}, 'numParams': 0, 'quadStart': -1}

# Declaracion de direcciones para variables globales y temporales
nextAvailable = {'gInt': 1000, 'gFloat': 5000, 'gBool': 10000,
                 'tInt': 15000, 'tFloat': 20000, 'tBool': 25000}

# Inicializacion de la memoria vacia
memoria = {}

# Funcion que en base a un tipo de resultado regresa el siguiente valor de memoria para Temp disponible
def nextTemp(result_type):
    if result_type == 'INT':
        availableTemp = nextAvailable['tInt']
        nextAvailable['tInt'] = availableTemp + 1
        return availableTemp
    elif result_type == 'FLOAT':
        availableTemp = nextAvailable['tFloat']
        nextAvailable['tFloat'] = availableTemp + 1
        return availableTemp
    elif result_type == 'BOOL':
        availableTemp = nextAvailable['tBool']
        nextAvailable['tBool'] = availableTemp + 1
        return availableTemp


# Funcion que en base a un tipo de resultado regresa el siguiente valor de memoria para Global disponible
def nextGlobal(result_type):
    global actual_scope
    if actual_scope == 'global':
        if result_type == 'INT':
            availableGlobal = nextAvailable['gInt']
            nextAvailable['gInt'] = availableGlobal + 1
            return availableGlobal
        elif result_type == 'FLOAT':
            availableGlobal = nextAvailable['gFloat']
            nextAvailable['gFloat'] = availableGlobal + 1
            return availableGlobal
        elif result_type == 'BOOL':
            availableGlobal = nextAvailable['gBool']
            nextAvailable['gBool'] = availableGlobal + 1
            return availableGlobal
    else:
        print('Es una funcion')


# Funciones para agregar valores a las pilas
def add_pArr(id):
    pArr.append(id)

def add_pFunc(id):
    pFunc.append(id)

def add_pVar(num):
    pVar.append(num)

def add_pilaReturn(quad):
    pReturnTo.append(quad)

def add_pilaO(id):
    pilaO.append(id)

def add_pOper(oper):
    pOper.append(oper)

def add_pType(type):
    pType.append(type)

def add_pJumps(quad):
    pJumps.append(quad)

def add_pIterator(iterator):
    pIterator.append(iterator)


# funciones para sacar el ultimo elemento de las pilas
def pop_pArr():
    if (len(pArr) > 0):
        return pArr.pop()

def pop_pFunc():
    if (len(pFunc) > 0):
        return pFunc.pop()

def pop_pVar():
    if (len(pVar) > 0):
        return pVar.pop()

def pop_pilaReturn():
    if (len(pReturnTo) > 0):
        return pReturnTo.pop()

def pop_pilaO():
    if (len(pilaO) > 0):
        return pilaO.pop()

def pop_pOper():
    if (len(pOper) > 0):
        return pOper.pop()

def pop_pType():
    if (len(pType) > 0):
        return pType.pop()

def pop_pJumps():
    if (len(pJumps) > 0):
        return pJumps.pop()

def pop_pIterator():
    if (len(pIterator) > 0):
        return pIterator.pop()

# Funciones para regresar el tope de las pilas
def top_pArr():
    if (len(pArr) > 0):
        temp = pop_pArr()
        add_pArr(temp)
        return temp
    else:
        return -1

def top_pOper():
    if (len(pOper) > 0):
        temp = pop_pOper()
        add_pOper(temp)
        return temp
    else:
        return -1

def top_pIterator():
    if (len(pIterator) > 0):
        temp = pop_pIterator()
        add_pIterator(temp)
        return temp
    else:
        return -1

def top_pFunc():
    if (len(pFunc) > 0):
        temp = pop_pFunc()
        add_pFunc(temp)
        return temp
    else:
        return -1

def top_pVar():
    if (len(pVar) > 0):
        temp = pop_pVar()
        add_pVar(temp)
        return temp
    else:
        return -1

# Declaracion del cubo semantico
sem_cube = {'INT': {'INT': {'+': 'INT',
                            '-': 'INT',
                            '/': 'FLOAT',
                            '*': 'INT',
                            '%': 'INT',
                            '<': 'BOOL',
                            '>': 'BOOL',
                            '<=': 'BOOL',
                            '>=': 'BOOL',
                            '!=': 'BOOL',
                            '==': 'BOOL',
                            '=': 'INT'},
                    'FLOAT': {'+': 'FLOAT',
                             '-': 'FLOAT',
                             '/': 'FLOAT',
                             '*': 'FLOAT',
                             '<': 'BOOL',
                             '>': 'BOOL',
                             '<=': 'BOOL',
                             '>=': 'BOOL',
                             '!=': 'BOOL',
                             '==': 'BOOL',
                             '=': 'INT'}},
            'FLOAT': {'INT': {'+': 'FLOAT',
                             '-': 'FLOAT',
                             '/': 'FLOAT',
                             '*': 'FLOAT',
                             '<': 'BOOL',
                             '>': 'BOOL',
                             '<=': 'BOOL',
                             '>=': 'BOOL',
                             '!=': 'BOOL',
                             '==': 'BOOL',
                             '=': 'FLOAT'},
                     'FLOAT': {'+': 'FLOAT',
                              '-': 'FLOAT',
                              '/': 'FLOAT',
                              '*': 'FLOAT',
                              '<': 'BOOL',
                              '>': 'BOOL',
                              '<=': 'BOOL',
                              '>=': 'BOOL',
                              '!=': 'BOOL',
                              '==': 'BOOL',
                              '=': 'FLOAT'}},
            'BOOL': {'BOOL': {'AND': 'BOOL',
                              'OR': 'BOOL',
                              '=': 'BOOL'}}}


