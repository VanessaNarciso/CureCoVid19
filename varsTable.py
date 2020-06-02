class varsTable:

    #Se inicializa la tabla de variables (diccionario)
    def __init__(self):
        self.tabla_variables = {}

    #Verifica si la variable ya existe
    def existVar(self, nombre):
        return nombre in self.tabla_variables.keys()

    #Agrega variable nueva a la tabla
    def addVar(self, nombre, tipo, renglones, columnas, pos_memoria ):
        if self.existVar(nombre):
            print("Error : la variable ", str(nombre), " está duplicada")
            return False
        else:
            self.tabla_variables[nombre] = {
                'nombre' : nombre,
                'tipo': tipo,
                'renglones': renglones,
                'columnas' : columnas,
                'pos_memoria' : pos_memoria
            }
            return True

    #Obtiene los metadatos de la variable siempre y cuando exista
    def searchVar(self, nombre):
        if self.existVar(nombre):
            return self.tabla_variables[nombre]
        else:
            return None

    #Obtiene el tipo de la variable
    def searchVarType(self, nombre):
        if self.existVar(nombre):
            return self.tabla_variables[nombre]['tipo']
        else:
            return None

    #Sirve para indicar que la variable es dimensionada (se actualizan valores de renglones y columnas)
    def updateVarDims(self, nombre, renglones, columnas):

        if self.existVar(nombre):

            if columnas < 0:
                self.tabla_variables[nombre]['renglones'] = renglones
            else:
                self.tabla_variables[nombre]['columnas'] = columnas

            print("Se actualizaron las dimensiones de: ", nombre)
            print("Renglones: ", self.tabla_variables[nombre]['renglones'], "Columnas: ",
                  self.tabla_variables[nombre]['columnas'])

        else:
            print("Error. La variable: ", nombre, " no existe")

    #Obtiene la posición de memoria virtual de una variable determinada
    def searchVarMemPos(self, nombre):
        if self.existVar(nombre):
            return self.tabla_variables[nombre]['pos_memoria']
        else:
            return None