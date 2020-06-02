class extraSemanticCube:
    def __init__(self):
        self.ExtraSemCube = {
            ('Media', 'int', ''): 'float',
            ('Media', 'float', ''): 'float',

            ('Mediana', 'int', ''): 'float',
            ('Mediana', 'float', ''): 'float',

            ('Moda', 'int', ''): 'int',
            ('Moda', 'float', ''): 'float',

            ('Varianza', 'int', ''): 'float',
            ('Varianza', 'float', ''): 'float',

            ('Correlaciona', 'int', 'int'): 'float',
            ('Correlaciona', 'float', 'int'): 'float',
            ('Correlaciona', 'int', 'float'): 'float',
            ('Correlaciona', 'float', 'float'): 'float',

            ('plothist', 'int', 'int'): 'histogram',
            ('plothist', 'float', 'int'): 'histogram',

            ('plotline', 'int', 'int'): 'line',
            ('plotline', 'int', 'float'): 'line',
            ('plotline', 'float', 'int'): 'line',
            ('plotline', 'float', 'float'): 'line'
        }

    # Obtiene el tipo de dato resultante
    def getType(self, funcion_especial, operando1, operando2):
        try:
            TypeResult = self.ExtraSemCube[funcion_especial, operando1, operando2]
        except:
            TypeResult = 'error'

        return TypeResult