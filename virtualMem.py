import sys

class virtualMem:

    def __init__(self, fun):
        # Nombre de la funcion a la que pertenece la tabla
        self.funNombre = fun
        # Diccionario para las direcciones constantes
        self.direcciones = {
            #tipo       #direcciones : valor
            'int'       : {},
            'float'     : {},
            'char'      : {},
            'string'    : {},
            'bool'      : {},
            'dataframe' : {}
        }


    # Guarda valor en una dirección específica
    def guardarValor(self, direccion, tipo, valor):
        self.direcciones[str(tipo)][str(direccion)] = valor


    #Obtiene el valor de una direccion en específico
    def obtenerValorDeDireccion(self, direccion, tipo):
        try:
            valor = self.direcciones[str(tipo)][str(direccion)]
            return valor
        except:
            print("Error Memoria Virtual: ", sys.exc_info()[0], "No existe valor, en memoria {} en la direccion {}, de tipo {}.".format( self.funNombre, direccion, tipo))
            raise


    # Obtiene la siguiente dirreccion disponible
    def sigDireccionDisponible(self, tipo, direccion_inicial, tam):
        if tipo == 'int':
            aux = 0
        elif tipo == 'float':
            aux = tam
        elif tipo == 'char':
            aux = tam * 2
        elif tipo == 'string':
            aux = tam * 3
        elif tipo == 'dataframe':
            aux = tam * 4

        return direccion_inicial + aux + len(self.direcciones[tipo])


    # Imprime diccionario de la memoria
    def imprimirDir(self):
        print("Nombre {}: ".format(self.funNombre))
        print(self.direcciones)
        print("\n")
