import sys
from varsTable import *

class funcDir:
    #Inicializa el directorio de funciones (diccionario)
    def __init__(self):
        self.directorio_funciones = {'global': {'nombre' : 'global', 'tipo' : 'void', 'numParams' : 0, 'variables': varsTable(), 'numQuads' : 0}}
        print("Se creó funcion global void")

    #Verifica si la funcion ya existe en el directorio
    def existeFunc(self, nombre):
        return nombre in self.directorio_funciones.keys()

    #Agrega función nueva al directorio
    def addFunc(self, nombre, tipo, numParams, numQuads):
        if self.existeFunc(nombre):
            print ("Error: Declaracion multiple funcion: ", str(nombre), "\n")
        else:
            self.directorio_funciones[nombre] = {
                'nombre': nombre,
                'tipo': tipo,
                'numParams': numParams,
                'variables': varsTable(),
                'numQuads': numQuads
            }
            print ("Funcion: ", nombre, " de tipo: ", tipo, " agregada al directorio", "\n")

    #Busca la función y regresa los metadatos de ella
    def searchFunc(self, nombre):
        if self.existeFunc(nombre):
            return self.directorio_funciones[nombre]
        else:
            return None

    #Agrega variable a la tabla de variables correspondiente a la función
    def addVarFunc(self, nombre, nombreVar, tipoVar, renglonesVar, columnasVar, memPos):

        if self.directorio_funciones[nombre]['variables'].var_add(nombreVar, tipoVar, renglonesVar, columnasVar,
                                                                  memPos):
            print("Variable: ", nombreVar, " creada en la funcion:  ", nombre)
        else:
            print("Error: La variable: ", nombreVar, " NO fue creada en la funcion: ", nombre)

    #Verifica si una variable es dimensionada y dado el caso lo actualiza
    def updateDimFunc(self, nombre, nombreVar, renglones, columnas):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            if columnas > 0:
                return self.directorio_funciones[nombre]['variables'].var_upadateDims(nombreVar, renglones, columnas)
            else:
                return self.directorio_funciones[nombre]['variables'].var_upadateDims(nombreVar, renglones, -1)
        else:
            print("Error: La variable ", nombreVar, "no existe en este contexto ", nombre)
            return None

    #Verifica si una variable es dimensionada en determinado contexto
    def isDimensionadaVar(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            print("Directorio de func de ", nombreVar, "col: ", self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'])

            if self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'] > 0 or self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['renglones'] > 0:
                return 1
            else:
                return 0
        else:
            return -1 #No existe esa variable en este contexto

    #Genera una lista con las dimensiones de una variable dimensionada
    def getDimsVar(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            dim = [self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['columnas'], self.directorio_funciones[nombre]['variables'].tabla_variables[nombreVar]['renglones']]
            return dim
        else:
            return -1 #No existe esa variable en este contexto

    #Busca el tipo de una variable que ya ha sido creada
    def searchVarType(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            return self.directorio_funciones[nombre]['variables'].var_searchType(nombreVar)
        else:
            print("Error: Variable: ", nombreVar ," no existe en este contexto: ", nombre)
            return None

    #Verifica si la variable existe en la tabla de variables de una función determinada
    def varExist(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            return True
        else:
            return False

    #Actualiza el número de parámetros de una función determinada
    def updateFuncParams(self, nombre, numParams):
        if self.existeFunc(nombre):
            self.directorio_funciones[nombre]['numParams'] = numParams
        else:
            print("Error: la funcion: ", nombre, " no existe")

    #Regresa una lista de tipos de variables
    def listaTipos(self, funcion):
        return [self.directorio_funciones[funcion]['variables'].tabla_variables[x]['tipo'] for x in self.directorio_funciones[funcion]['variables'].tabla_variables]

    #Obtiene la posición de memoria virtual de una variable
    def funcMemory(self, nombre, nombreVar):
        if self.directorio_funciones[nombre]['variables'].varExist(nombreVar):
            return  self.directorio_funciones[nombre]['variables'].var_searchMemPos(nombreVar)
        else:
            print("Error: La variable: ", nombreVar, "no existe en este contexto: ", nombre)

    #Imprime el directorio de la función actual
    def funcPrint(self, nombre):
        print (self.directorio_funciones[nombre]['variables'].tabla_variables)
        print("\n")

    #Borra el directorio de funciones
    def deleteFuncDic(self):
        self.directorio_funciones.clear()
