import ply.yacc as yacc
import os
import sys
import codecs
import re
import os
from lexer import tokens
from sys import stdin
from funcDir import *
from semanticCube import *
from extraSemanticCube import *


# Instancia de los objetos de directorio de funciones, tabla de variables y cubos semánticos
functionDirectory = funcDir()
varTable = varsTable()
semCube = semanticCube()
extraSemCube = extraSemanticCube()

# Lista/arreglo que almacena los cuadruplos generados
cuads = []

# Pilas que se utilizan en la generación de cuadruplos
pOperandos = [] #operandos
pOper = [] #operadores
pTipos = [] #tipos
pSaltos = [] #saltos para condiciones y ciclos
pFunciones = [] #funciones
pArgumentos = [] #agumentos de una funcion
pDirecciones = [] #direcciones de memoria
pDims = [] #arreglos

# CONSTANTES
GLOB = 'global'
OP_SUM_RES = ['+', '-']
OP_MUL_DIV = ['*', '/']
OP_REL = ['>', '<', '<=', '>=', '==', '!=']
OP_LOGICOS = ['&', '|']
OP_ASIG = ['=']
OP_SECUENCIALES = ['lee', 'escribe', 'regresa']
ESPACIO_MEMORIA = 1000

# Diccionarios de constantes (guardan la direccion de memoria de constantes)
intDic = {}
floatDic = {}
strDic = {}
charDic = {}
dfDic = {}

# Declaración de variables globales
currentFunc = GLOB
currentType = "void"
varName = ""
currentVarName = ""
currentCantParams = 0
currentCantVars = 0
avail = 0
constanteNegativa = False
forBool = False
varFor = ''
negativo = False
isVoid = False
isDataf = False

# Declaracion de variables para arrays y matrices
isArray = False
isMatrix = False
numRenglones = 0
numColumnas = 0
R = 1 #m0
dirBase = 0 #Direccion base
currentConstArrays = []


# Se declara espacio de memoria por tipo de memoria
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

# Se inicializa  memoria para Globales
cont_IntGlobales = 0
cont_FloatGlobales = limite_intGlobales
cont_StringGlobales = limite_floatGlobales
cont_CharGlobales = limite_stringsGlobales
cont_dfGlobales = limite_charGlobales

# Se inicializa memoria para Locales
cont_IntLocales = limite_dfGlobales
cont_FloatLocales = limite_intLocales
cont_StringLocales = limite_floatLocales
cont_CharLocales = limite_stringsLocales
cont_dfLocales = limite_charLocales

# Se inicializa memoria para Temporales
cont_IntTemporales = limite_dfLocales
cont_FloatTemporales = limite_intTemporales
cont_StringTemporales = limite_floatTemporales
cont_CharTemporales = limite_stringsTemporales
cont_dfTemporales = limite_charTemporales
cont_BoolTemporales = limite_dfTemporales

# Se inicializa memoria para Constatnes
cont_IntConstantes = limite_boolTemporales
cont_FloatConstantes = limite_intConstantes
cont_StringConstantes = limite_floatConstantes
cont_CharConstantes = limite_stringsConstantes
cont_dfConstantes = limite_charConstantes

precedence = (
    ('nonassoc','SEMICOLON'),
    ('right', 'EQUALS'),
    ('left', 'NOTEQUAL'),
    ('nonassoc','LESSTHAN','LESSEQ','GREATERTHAN','GREATEREQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','LPAREN','RPAREN'),
    ('left','LBRACKET','RBRACKET'),
    ('left','LCURBRACKET','RCURBRACKET')
)

# Producciones para el inicio de un programa
def p_programa(p):
    '''
    programa :  PROGRAMA ID SEMICOLON declara_vars gotoPrincipal declara_fun principal
    '''
    print("PROGRAMA \"", p[2], "\" terminado.")
    GenerateQuads()
    print("Poper : ", pOper)
    print("pOperandos: ", pOperandos)
    print("pTipos: ", pTipos)
    #print("programa")

def p_declara_vars(p):
    '''
    declara_vars : var
        | empty
    '''
    #print("declara_vars")

def p_declara_fun(p):
    '''
    declara_fun : funcion declara_fun
                | empty
    '''
    #print("declara fun")


def p_principal(p):
    '''
    principal : PRINCIPAL principal2 LPAREN RPAREN bloque
    '''
    #print("principal")


# Producciones para declaración de variables
def p_var(p):
    'var : VAR var2'
    #print("VAR")

def p_var2(p):
    'var2 : type COLON ids df2 var3'
    #print("VAR2")

def p_var3(p):
    '''
    var3 : var2
         | empty
    '''
    #print("VAR3")

def p_type(p): #type1 = simple, type2=compuesto
    '''
    type : type1
         | type2
    '''
    #print("P_TYPE")


# Producciones para declaración de funciones
def p_funcion(p):
    '''
    funcion : FUNCION fun_type ID funDec1 LPAREN parametros RPAREN funDec4 declara_vars bloque funDec7
    '''
    #print("FUNCION")

def p_fun_type(p):
    '''
    fun_type : VOID setCurrentType
             | type1
    '''
    #print("FUN_TYPE")

def p_parametros(p):
    '''
    parametros : param
               | empty
    '''
    #print("PARAMETROS")

def p_param(p):
    '''
    param : type1 ID funDec2 param1
    '''
    #print("PARAM")

def p_param1(p):
    '''
    param1 : COMMA param
           | empty
    '''
    #print("PARAM1")


# Producciones para tipos de datos
def p_type1(p):
    '''
    type1 : INT setCurrentType
        | FLOAT setCurrentType
        | CHAR setCurrentType
    '''
    #print("P_TYPE1")

def p_type2(p):
    '''
    type2 : DATAFRAME setCurrentType df
        | STRING setCurrentType
    '''
    #print("P_TYPE2")


# Producciones para los IDs
def p_ids(p): #Lista de IDs
    '''
    ids : lista SEMICOLON
    '''
    #print("IDs")

def p_lista(p):
    '''
    lista : ID addVariable dd lista1
    '''
    #print("lista")

def p_dd(p):
    '''
    dd : dim_dec dimDec8
       | empty
    '''
    #print("dd")

def p_lista1(p):
    '''
    lista1 : COMMA lista
           | empty
    '''
    #print("lista1")


# Producciones para la sintaxis de variables dimensionadas
def p_dim_dec(p):
    '''
    dim_dec : LBRACKET dimDec2 CTEINT dimDec5 RBRACKET decRenglones dim_dec1
    '''
    #print("dim_dec")

def p_dim_dec1(p):
    '''
    dim_dec1 : LBRACKET CTEINT dimDec6 RBRACKET decColumnas
             | empty
    '''
    #print("dim_dec1")

def p_dim_index(p):
    '''
    dim_index : LBRACKET dimAccess2 exp6 exp activaArray arregloAcc RBRACKET exp7 dim_index1
    '''
    #print("dim_index")

def p_dim_index1(p):
    '''
    dim_index1 : LBRACKET exp6 exp activaArray RBRACKET exp7 matrizAcc
               | empty
    '''
    #print("dim_index1")


# Producciones para sintaxis de un bloque
def p_bloque(p):
    '''
    bloque : LCURBRACKET est RCURBRACKET
    '''
    #print("BLOQUE")

def p_est(p):
    '''
    est : estatutos est
        | empty
    '''
    #print("EST")

def p_estatutos(p):
    '''
    estatutos : asignacion
              | llamada
              | retorno
              | lectura
              | escritura
              | carga_datos
              | decision
              | condicional
              | ciclo
              | funciones_especiales_void
    '''
    #print("ESTATUTOS")

# Producciones para estatutos
def p_asignacion(p):
    '''
    asignacion : variable EQUALS sec1 exp SEMICOLON sec2
    '''
    #print("ASIGNACION")

def p_variable(p):
    '''
    variable : ID pExp1 di
    '''
    #print("VARIABLE")

def p_di(p):
    '''
    di : dim_index
       | empty
    '''
    #print("di")

def p_llamada(p):
    'llamada :  ID funCall1 LPAREN llamada1 RPAREN funCall5'
    p[0] = 'llamada'
    #print("LLAMADA")

def p_llamada1(p):
    '''
    llamada1 : exp funCall3 llamada2
             | empty
    '''
    #print("LLAMADA1")

def p_llamada2(p):
    '''
    llamada2 : COMMA llamada1
             | empty
    '''
    #print("LLAMADA2")

def p_retorno(p):
    '''
    retorno : REGRESA sec3 LPAREN exp RPAREN pRetorno SEMICOLON
    '''
    #print("RETORNO")

def p_lectura(p):
    'lectura : LEE sec3 LPAREN variable RPAREN SEMICOLON sec4 sec5'
    #print("LECTURA")

def p_escritura(p):
    'escritura : ESCRIBE sec3 LPAREN esc RPAREN SEMICOLON sec5'
    #print("ESCRITURA")

def p_esc(p):
    'esc : esc1 esc2'
    #print("ESC")

def p_esc1(p):
    '''
    esc1 : exp sec4
    '''
    #print("ESC1")

def p_esc2(p):
    '''
    esc2 : COMMA esc
         | empty
    '''
    #print("ESC2")

def p_carga_datos(p):
    'carga_datos : CARGAARCHIVO LPAREN ID pExp1 COMMA CTESTRING cteStr COMMA ca COMMA ca RPAREN SEMICOLON carga'
    #print("CARGA DATOS")

def p_ca(pa):
    '''
    ca : ID
       | CTEINT cteInt
    '''
    #print("CA")

# Producciones para sintaxis de condicionales y ciclos
def p_decision(p): #IF
    '''
    decision : SI LPAREN expresion RPAREN cond1 ENTONCES bloque sino cond2
    '''
    #print("DECISION")

def p_sino(p): #ELSE
    '''
    sino : SINO cond3 bloque
         | empty
    '''
    #print("SINO")

def p_condicional(p): #While
    'condicional : MIENTRAS ciclos1 LPAREN expresion RPAREN ciclos2 HAZ bloque ciclos3'
    #print("CONDICIONAL")

def p_ciclo(p): #For
    'ciclo : DESDE ciclos4 variable EQUALS sec1 exp ciclos5 HASTA ciclos6 exp ciclos7 HACER bloque ciclos8'
    #print("CICLO")


def p_funciones_especiales_void(p):
    '''
    funciones_especiales_void : VARIABLES funEsp1 LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON
                              | HISTOGRAMA funEsp1 LPAREN ID pExp1 COMMA CTEINT cteInt COMMA CTEINT cteInt RPAREN SEMICOLON funEspVoid1
                              | LINEAL funEsp1 LPAREN ca COMMA ca COMMA CTEINT cteInt RPAREN SEMICOLON funEspVoid1
    '''
    # print("FUNCIONES_ESPECIALES_VOID")


def p_funciones_especiales(p):
    '''
    funciones_especiales : fe LPAREN ID pExp1 COMMA CTEINT cteInt COMMA CTEINT cteInt RPAREN funEsp2
                         | CORRELACION funEsp1 LPAREN ID pExp1 COMMA ID pExp1 COMMA CTEINT cteInt COMMA CTEINT cteInt RPAREN funEsp3
    '''
    #print("FUNCIONES_ESPECIALES")

def p_fe(p):
    '''
    fe : MEDIA funEsp1
       | MODA funEsp1
       | VARIANZA funEsp1
    '''
    #print("FE")

#def p_v_exp(p):
#    'v_exp : VARIABLES  LBRACKET exp RBRACKET'
#    print("V_EXP")

def p_var_cte(p):
    '''
    var_cte : CTECHAR cteChar
            | CTESTRING cteStr
            | MINUS neg var_num
            | var_num
    '''
    #print("VAR_CTE")

    if p[1] == '-':
        p[0] = -1 * p[3]
    else:
        p[0] = p[1]

    global negativo
    negativo = False

def p_var_num(p):
    '''
    var_num : CTEINT cteInt
            | CTEFLOAT cteFloat
    '''
    p[0] = p[1]
    #print("VAR_NUM")

# Producciones para expresiones
def p_expresion(p):
    '''
    expresion : mega_exp expresion1
    '''
    #print("EXPRESSION")

def p_expresion1(p):
    '''
    expresion1 : EQUALS expresion
               | empty
    '''
    #print("EXPRESSION1")

def p_mega_exp(p):
    '''
    mega_exp : super_exp meg
    '''
    #print("MEGA_EXP")

def p_meg(p):
    '''
    meg : op_l exp10 mega_exp exp11
        | empty
    '''
    #print("MEG")

def p_op_l(p):
    '''
    op_l : AND
         | OR
    '''
    #print("OP_L")

def p_super_exp(p):
    'super_exp : exp sp'
    #print("SUPER_EXP")

def p_sp(p):
    '''
    sp : op_r  exp exp9
       | empty
    '''
    #print("SP")

def p_op_r(p):
    '''
    op_r : LESSTHAN exp8
         | GREATERTHAN exp8
         | LESSEQ exp8
         | GREATEREQ exp8
         | NOTEQUAL exp8
         | ISEQUAL exp8
    '''
    #print("OP_R")

def p_exp(p):
    '''
    exp : termino exp4 exp1
    '''
    #print("EXP")

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
    #print("EXP1")

def p_op_a(p):
    '''
    op_a : PLUS exp2
         | MINUS exp2
    '''
    #print("OP_A")

def p_termino(p):
    'termino : factor exp5 term'
    #print("TERMINO")

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
    #print("TERM")

def p_op_a1(p):
    '''
    op_a1 : TIMES exp3
          | DIVIDE exp3
    '''
    #print("OP_A1")

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN exp6 exp RPAREN exp7
           | variable
           | llamada
           | funciones_especiales
    '''
    print("AQUÍ HAY UN FACTOR")

def p_empty(p):
    '''
    empty :
    '''
    pass
    #print("NULO")

def p_error(p):
    if p:
        print("Error de sintaxis: ",p.type, p.value)
        print("En la linea "+str(p.lineno))
        print()
        parser.errok()
    else:
        print("Syntax error at EOF")

##### FUNCIONES PARA MANIPULAR LAS PILAS

# Obtiene el último elemento de la pila de operandos
def popOperandos():
    global pOperandos
    pop = pOperandos.pop()
    print("--------------------> POP Operandos")
    print("Pop Operandos= ", pop)
    return pop

# Obtiene el ultimo elemento de la pila de operadores
def popOperadores():
    global pOper
    pop = pOper.pop()
    print("--------------------> POP POper")
    print("Pop Poper= ", pop)
    return pop

# Obtiene el ultimo elemento de la pila de tipos
def popTipos():
    global pTipos
    pop = pTipos.pop()
    print("--------------------> POP Tipos")
    print("Pop Tipos = ", pop)
    return pop

# Inserta en la pila de operandos el nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)
    print("------> pushOperando : ", operando)
    print("POperandos : ", pOperandos)

# Inserta en la pila de operadores el nuevo operador
def pushOperador(operador):
    global pOper
    pOper.append(operador)
    print("------> pushOperador : ", operador)
    print("POper : ", pOper)

# Inserta en la pila de tipos el nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)
    print("------>pushTipo : ", tipo)
    print("pTipos : ", pTipos)

# Obtiene el ultimo operando ingresado a la pila de operandos
def topOperador():
    global pOper
    last = len(pOper) - 1
    if (last < 0):
        return 'empty'
    return pOper[last]

# Obtiene el ultimo tipo ingresado a la pila de tipos
def topTipo():
    global pTipos
    last = len(pTipos) - 1
    if(last < 0):
        return 'empty'
    return pTipos[last]

# Obtiene el ultimo elemento de la pila de Saltos
def popSaltos():
    global pSaltos

    return pSaltos.pop()

# Agrega el nuevo salto a la pila de Saltos.
def pushSaltos(salto):
    global pSaltos
    pSaltos.append(salto)

# Obtiene el indice del siguiente cuadruplo del arreglo de cuadruplos
def nextQuad():
    global cuads
    return len(cuads)

# Obtiene el ultimo cuadruplo
def popQuad():
    global cuads
    return cuads.pop()

# Agrega un nuevo cuadruplo al arreglo de cuadruplos
def pushQuad(quad):
    global cuads
    cuads.append(quad)


# Agrega las constantes a la pila de Operandos y Tipos
def pushConstante(constante):
    global intDic
    global floatDic
    global strDic
    global charDic
    global dfDic

    global cont_IntConstantes
    global cont_FloatConstantes
    global cont_StringConstantes
    global cont_CharConstantes
    global cont_dfConstantes

    if type(constante) == int:
        if constante not in intDic:
            if cont_IntConstantes < limite_intConstantes:
                intDic[constante] = cont_IntConstantes
                cont_IntConstantes = cont_IntConstantes + 1
                QuadGenerate('CONS', 'int', constante, intDic[constante])
            else:
                print(cont_IntConstantes, limite_intConstantes)
                errorOutOfBounds('Constantes', 'Enteras')
        pushOperando(constante)
        pushMemoria(intDic[constante])
        pushTipo('int')

    elif type(constante) == float:
        if constante not in floatDic:
            if cont_FloatConstantes < limite_floatConstantes:
                floatDic[constante] = cont_FloatConstantes
                cont_FloatConstantes = cont_FloatConstantes + 1
                QuadGenerate('CONS', 'float', constante, floatDic[constante])
            else:
                errorOutOfBounds('Constantes', 'Flotantes')
        pushOperando(constante)
        pushMemoria(floatDic[constante])
        pushTipo('float')

    elif type(constante) == str:
        if len(constante) > 3:  # String
            if constante not in strDic:
                if cont_StringConstantes < limite_stringsConstantes:
                    strDic[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    print("LENG", len(constante), constante)
                    QuadGenerate('CONS', 'string', constante, strDic[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')
            pushOperando(constante)
            pushMemoria(strDic[constante])
            pushTipo('string')
        else:  # Char
            if constante not in charDic:
                if cont_CharConstantes < limite_charConstantes:
                    charDic[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, charDic[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')
            pushOperando(constante)
            pushMemoria(charDic[constante])
            pushTipo('char')
    else:
        sys.exit("Error: Tipo de Variable desconocida")



# Obtiene la direccion de memoria de una constante, si no la encuentra la agrega
def getAddConst(constante):
    global intDic
    global floatDic
    global strDic
    global charDic
    global dfDic

    global cont_IntConstantes
    global cont_FloatConstantes
    global cont_StringConstantes
    global cont_CharConstantes
    global cont_dfConstantes

    if isDataf:
        if constante not in dfDic:
            if cont_dfConstantes < limite_dfConstantes:
                dfDic[constante] = cont_dfConstantes
                cont_dfConstantes += 1
                QuadGenerate('CONS', 'dataframe', constante, dfDic[constante])
            else:
                errorOutOfBounds('Constantes', 'dataframes')
        return dfDic[constante]

    if type(constante) == int:
        if constante not in intDic:
            if cont_IntConstantes < limite_intConstantes:
                intDic[constante] = cont_IntConstantes
                cont_IntConstantes += 1
                QuadGenerate('CONS', 'int', constante, intDic[constante])

            else:
                errorOutOfBounds('constantes', 'Enteras')
        return intDic[constante]

    elif type(constante) == float:
        if constante not in floatDic:
            if cont_FloatConstantes < limite_floatConstantes:
                floatDic[constante] = cont_FloatConstantes
                cont_FloatConstantes += 1
                QuadGenerate('CONS', 'float', constante, floatDic[constante])

            else:
                errorOutOfBounds('constantes', 'Flotantes')
        return floatDic[constante]

    elif type(constante) == str:
        if len(constante) > 1:  # String
            if constante not in strDic:
                if cont_StringConstantes < limite_stringsConstantes:
                    strDic[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    QuadGenerate('CONS', 'string', constante, strDic[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')

            return strDic[constante]

        else:  # Char
            if constante not in charDic:
                if cont_CharConstantes < limite_charConstantes:
                    charDic[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, charDic[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')

            return charDic[constante]

    else:
        sys.exit("Error en getAddConst")




##### FUNCIONES PARA IMPRESIÓN Y ERRORES

# Imprime un nuevo cuadruplo
def QuadGenerate(operator, leftOperand, rightOperand, result):
    QuadTemporal = (operator, leftOperand, rightOperand, result)
    pushQuad(QuadTemporal)
    NumQuad = nextQuad() - 1
    print(">> Quad {}: ('{}','{}','{}','{}')".format(NumQuad, operator, leftOperand, rightOperand, result))

    print("\n")


# Imprime arreglo/lista de cuadruplos
def GenerateQuads():
    print(functionDirectory.funcPrint(GLOB))
    print("-------Lista de Cuadruplos: ")

    contador = 0
    # Opción de leer tuplas directamente - TODO: Arreglar
    file = open("obj.txt", "w+")
    for quad in cuads:
        print("{}.\t{},\t{},\t{},\t{}".format(contador, quad[0], quad[1], quad[2], quad[3]))
        contador = contador + 1

        file.write(str(quad) + '\n')
    print("{}.\t{},\t{},\t{},\t{}".format(contador, 'FINPROGRAMA', '', '', ''))
    file.write("('FINPROGRAMA', '', '', '')")
    file.close()

# Muestra error de type missmatch
def errorTypeMismatch():
    sys.exit('Error: Type Mismatch')


# Muestra mensaje de error cuando se llena los maximos posibles valores temporales
def errorOutOfBounds(tipoMemoria, tipoDato):
    sys.exit("Error: Memoria llena; Muchas {} de tipo {}.".format(tipoMemoria, tipoDato))

def errorReturnTipo():
    sys.exit("Error: el tipo que intenta retornar no es correcto")



##### FUNCIONES PARA MANEJO DE MEMORIA

# Obtiene el siguiente temporal disponible, dependiendo el tipo
def nextAvailTemp(tipo):
    global cont_IntTemporales
    global cont_FloatTemporales
    global cont_BoolTemporales
    global avail

    if tipo == 'int':
        if cont_IntTemporales < limite_intTemporales:
            avail = cont_IntTemporales
            cont_IntTemporales += 1
        else:
            errorOutOfBounds('temporales', 'Enteras')
    elif tipo == 'float':

        if cont_FloatTemporales < limite_floatTemporales:
            avail = cont_FloatTemporales
            cont_FloatTemporales += 1
        else:
            errorOutOfBounds('temporales', 'Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemporales < limite_boolTemporales:
            avail = cont_BoolTemporales
            cont_BoolTemporales = cont_BoolTemporales + 1
        else:
            errorOutOfBounds('temporales', 'Boleanas')
    else:
        avail = -1
        print("Error: Tipo de variable no existente")
    return avail



# Obtiene el siguiente espacio de memoria disponible
def nextAvailMemory(contexto, tipo):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales
    global cont_dfConstantes
    global cont_dfLocales

    posMem = -1

    # Global
    if contexto == GLOB:

        if tipo == 'int':
            if cont_IntGlobales < limite_intGlobales:
                posMem = cont_IntGlobales
                cont_IntGlobales += 1
            else:
                errorOutOfBounds(GLOB, 'Enteras')


        elif tipo == 'float':
            if cont_FloatGlobales < limite_floatGlobales:
                posMem = cont_FloatGlobales
                cont_FloatGlobales += 1
            else:
                errorOutOfBounds(GLOB, 'Floats')

        elif tipo == 'string':
            if cont_StringGlobales < limite_stringsGlobales:
                posMem = cont_StringGlobales
                cont_StringGlobales += 1
            else:
                errorOutOfBounds(GLOB, 'Strings')

        elif tipo == 'char':
            if cont_CharGlobales < limite_charGlobales:
                posMem = cont_CharGlobales
                cont_CharGlobales += 1
            else:
                errorOutOfBounds(GLOB, 'Chars')

        elif tipo == 'dataframe':
            if cont_dfConstantes < limite_dfConstantes:
                posMem = cont_dfConstantes
                cont_dfConstantes += 1
            else:
                errorOutOfBounds(GLOB, 'Dataframes')
    # Locales
    else:
        if tipo == 'int':
            if cont_IntLocales < limite_intLocales:
                posMem = cont_IntLocales
                cont_IntLocales += 1
            else:
                errorOutOfBounds('Locales', 'Enteras')


        elif tipo == 'float':
            if cont_FloatLocales < limite_floatLocales:
                posMem = cont_FloatLocales
                cont_FloatLocales += 1
            else:
                errorOutOfBounds('Locales', 'Floats')

        elif tipo == 'string':
            if cont_StringLocales < limite_stringsLocales:
                posMem = cont_StringLocales
                cont_StringLocales += 1
            else:
                errorOutOfBounds('Locales', 'Strings')

        elif tipo == 'char':
            if cont_CharLocales < limite_charLocales:
                posMem = cont_CharLocales
                cont_CharLocales += 1
            else:
                errorOutOfBounds('Locales', 'Chars')

        elif tipo == 'dataframe':
            if cont_dfConstantes < limite_dfConstantes:
                posMem = cont_dfConstantes
                cont_dfConstantes += 1
            else:
                errorOutOfBounds('Locales', 'Dataframes')
    return posMem


# Sirve para modificar la memoria
def update_pointer(contexto, tipo, cont):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales
    global cont_dfConstantes

    if contexto == GLOB:

        if tipo == 'int':
            cont_IntGlobales += cont
            if cont_IntGlobales > limite_intGlobales:
                sys.exit('Error: Overflow Enteras Globales')

        if tipo == 'float':
            cont_FloatGlobales += cont
            if cont_FloatGlobales > limite_floatGlobales:
                sys.exit('Error: Overflow Flotantes Globales')

        if tipo == 'string':
            cont_StringGlobales += cont
            if cont_StringGlobales > limite_stringsGlobales:
                sys.exit('Error: Overflow Strings Globales')

        if tipo == 'char':
            cont_CharGlobales += cont
            if cont_CharGlobales > limite_charGlobales:
                sys.exit('Error: Overflow Chars Globales')

        if tipo == 'dataframe':
            cont_dfConstantes += cont
            if cont_dfConstantes > limite_dfConstantes:
                sys.exit('Error: Overflow DF Globales')
    else:
        if tipo == 'int':
            cont_IntLocales += cont
            if cont_IntLocales > limite_intLocales:
                sys.exit('Error: Overflow Enteras Locales')

        if tipo == 'float':
            cont_FloatLocales += cont
            if cont_FloatLocales > limite_floatLocales:
                sys.exit('Error: Overflow Flotantes Locales')

        if tipo == 'string':
            cont_StringLocales += cont
            if cont_StringLocales > limite_stringsLocales:
                sys.exit('Error: Overflow Strings Locales')

        if tipo == 'char':
            cont_CharLocales += cont
            if cont_CharLocales > limite_charLocales:
                sys.exit('Error: Overflow Chars Locales')

        if tipo == 'dataframe':
            cont_dfConstantes += cont
            if cont_dfConstantes > limite_dfConstantes:
                sys.exit('Error: Overflow DF Locales')

def popMemoria():
    global pDirecciones
    pop = pDirecciones.pop()
    print("--------------------> POP Memorias")
    print("Pop Memoria = ", pop)
    return pop

def pushMemoria(memoria):
    global pDirecciones
    pDirecciones.append(memoria)
    print("------>pushMemoria : ", memoria)
    print("pMemoria : ", pDirecciones)

### Producciones y acciones semánticas en los puntos neurálgicos

def p_gotoPrincipal(p):
    '''
    gotoPrincipal :
    '''
    QuadGenerate('GOTO', '', '', '')
    pushSaltos(nextQuad() - 1)
    #print("GOTOPRINCIPAL")

def p_principal2(p):
    '''
    principal2 :
    '''

    global currentFunc
    global cuads

    currentFunc = GLOB
    cuads[popSaltos()] = ('GOTO', '', '', nextQuad())

    #print("PRINCIPAL2")

def p_df(p):
    '''
    df :
    '''
    global isDataf
    isDataf = True
    #print("DF")

def p_df2(p):
    '''
    df2 :
    '''
    global isDataf
    isDataf = False
    #print("DF2")



# PRODUCCIONES DE PUNTOS NEURÁLGICOS PARA DIRFUNC Y VARS TABLE
def p_setCurrentType(p):
    '''
    setCurrentType :
    '''
    global currentType
    currentType = p[-1]
    #print("SETCURRENTTYPE")

def p_addVariable(p):
    '''
    addVariable :
    '''
    global currentFunc
    global varName
    global currentType
    global currentVarName
    global currentCantVars
    global isDataf

    varName = p[-1]
    currentVarName = varName
    PosMem = nextAvailMemory(currentFunc, currentType)

    functionDirectory.addVarFunc(currentFunc, varName, currentType, 0, 0, PosMem)

    currentCantVars += 1

    if isDataf:
        QuadGenerate('CONS', 'dataframe', varName, PosMem)
    #print("ADDVARIABLE")

def p_decRenglones(p):
    '''
    decRenglones :
    '''
    global numRenglones
    numRenglones = p[-2]

    #print("DECRENGLONES")

def p_decColumnas(p):
    '''
    decColumnas :
    '''
    global numColumnas
    numColumnas = p[-2]
    #print("DECCOLUMNAS")




###### GENERACIÓN DE CUADRUPLOS

# Cuadruplos para funciones
def p_funDec1(p):
    '''
    funDec1 :
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global currentCantVars
    global isVoid

    currentCantVars = 0
    currentCantParams = 0
    currentFunc = p[-1]
    print("CAMBIO de CONTEXTO currentFunc = ", currentFunc)
    print("\n")
    functionDirectory.addFunc(currentFunc, currentType, currentCantParams, nextQuad())

    if functionDirectory.directorio_funciones[currentFunc]['tipo'] == 'void':
        isVoid = False
    else:
        isVoid = True

    print("Return Bool : ", isVoid)
    print("\n")

    #print("FUNDEC1")

def p_funDec2(p):
    '''
    funDec2 :
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global currentCantVars
    global varName

    varName = p[-1]
    PosMem = nextAvailMemory(currentFunc, currentType)
    functionDirectory.addVarFunc(currentFunc, varName, currentType, 0, 0, PosMem)

    currentCantParams += 1
    currentCantVars += 1

    #print("FUNDEC2")

def p_funDec4(p):
    '''
    funDec4 :
    '''
    global currentFunc
    global currentCantParams

    functionDirectory.updateFuncParams(currentFunc, currentCantParams)

    #print("FUNDEC4")

def p_funDec7(p):
    '''
    funDec7 :
    '''
    global isVoid
    # global returnDone

    global cont_IntLocales
    global cont_FloatLocales
    global cont_StringLocales
    global cont_CharLocales
    global cont_dfLocales

    global cont_IntTemporales
    global cont_FloatTemporales
    global cont_StringTemporales
    global cont_CharTemporales
    global cont_dfTemporales

    # Reinicio de apuntadores de meomria Locales y Temporales

    cont_IntLocales = limite_dfGlobales
    cont_FloatLocales = limite_intLocales
    cont_StringLocales = limite_floatLocales
    cont_CharLocales = limite_stringsLocales
    cont_dfLocales = limite_charLocales

    cont_IntTemporales = limite_dfLocales
    cont_FloatTemporales = limite_intTemporales
    cont_StringTemporales = limite_floatTemporales
    cont_CharTemporales = limite_stringsTemporales
    cont_dfTemporales = limite_charTemporales
    cont_BoolTemporales = limite_dfTemporales

    QuadGenerate('ENDFUNC', '', '', '')
    isVoid = False

    #print("FUNDEC7")

### Cuadruplos para llamadas de funciones
def p_funCall1(p):
    '''
    funCall1 :
    '''
    global pFunciones
    global pArgumentos
    funcId = p[-1]

    if funcId in functionDirectory.directorio_funciones:
        pFunciones.append(funcId)

        QuadGenerate('ERA', funcId, '', '')
        pArgumentos.append(0)

    else:
        print("Error: la funcion no existe")
        sys.exit()
        return
    #print("FUNCALL1")


def p_funCall3(p):
    '''
    funCall3 :
    '''
    global pArgumentos
    global pFunciones
    global currentFunc

    argument = popOperandos()
    argumentType = popTipos()
    argumentMem = popMemoria()
    function = pFunciones.pop()
    args = pArgumentos.pop() + 1

    pArgumentos.append(args)
    parametro = 'param' + str(args)

    Func_Parameters = functionDirectory.directorio_funciones[function]['numParams']

    lista = functionDirectory.listaTipos(function)  ######PENDIENTE

    if Func_Parameters >= args:
        if lista[args - 1] == argumentType:
            QuadGenerate('PARAMETER', argumentMem, '', parametro)
        else:
            print("Error: Parametros incorrectos")
    else:
        print("Error, muchos argumentos")
        sys.exit()

    pFunciones.append(function)
    #print("FUNCALL3")



def p_funCall5(p):
    '''
    funCall5 :
    '''
    global isVoid
    global pFunciones
    global pArgumentos

    args = pArgumentos.pop()
    funcion = pFunciones.pop()

    # Verify that the last parameter points to null
    if args == functionDirectory.directorio_funciones[funcion]['numParams']:
        quadStartFunc = functionDirectory.directorio_funciones[funcion]['numQuads']

        # Generate action GOSUB, procedure-name, '', initial address
        QuadGenerate('GOSUB', funcion, nextQuad() + 1, quadStartFunc)

    else:
        print("Error: Mismatch de Argumentos")
        sys.exit()
        # FIXME:resultE

    tipo = functionDirectory.directorio_funciones[funcion]['tipo']
    if tipo != 'void':
        quad_resultIndex = nextAvailTemp(tipo)
        QuadGenerate('=', funcion, '', quad_resultIndex)
        pushOperando(quad_resultIndex)
        pushMemoria(quad_resultIndex)
        pushTipo(tipo)
    #print("FUNCALL5")


### PRODUCCIONES PARA GENERAR CUADRUPLOS DE FUNCIONALIDADES EXTRA
def p_funEsp1(p):
    '''
    funEsp1 :
    '''
    pFunciones.append(str(p[-1]))
    #print("FUNESP1")


def p_funEsp2(p):
    '''
    funEsp2 :
    '''
    global pFunciones

    funName = pFunciones.pop()

    indice2 = popOperandos()
    indiceTipo2 = popTipos()
    indiceMem2 = popMemoria()

    indice1 = popOperandos()
    indiceTipo1 = popTipos()
    indiceMem1 = popMemoria()

    dfName = popOperandos()
    dfTipo = popTipos()
    dfMem = popMemoria()

    if (indiceTipo1 != 'int' or indiceTipo2 != 'int'):
        sys.exit("Error en Funcion especial: {}".format(funName))

    if (dfTipo == 'string' or dfTipo == 'char'):
        sys.exit(
            "Error en Funcion especial: {} . El tipo del primer parametro no es dataframe o arreglo de enteros o flotantes.".format(
                funName))

    temporal = nextAvailTemp('float')
    tempTipo = 'float'
    indice1 = indice1 - 1
    indice2 = indice2 - 1

    indices = '%' + str(indice1) + '#' + str(indice2)

    QuadGenerate(funName, dfMem, indices, temporal)
    pushOperando(temporal)
    pushTipo(tempTipo)
    pushMemoria(temporal)
    #print("FUNESP2")

def p_funEsp3(p):
    '''
    funEsp3 :
    '''
    global pFunciones

    funName = pFunciones.pop()

    indice2 = popOperandos()
    indiceTipo2 = popTipos()
    indiceMem2 = popMemoria()

    indice1 = popOperandos()
    indiceTipo1 = popTipos()
    indiceMem1 = popMemoria()

    dfName2 = popOperandos()
    dfTipo2 = popTipos()
    dfMem2 = popMemoria()

    dfName1 = popOperandos()
    dfTipo1 = popTipos()
    dfMem1 = popMemoria()

    if (indiceTipo1 == 'int' and indiceTipo2 == 'int'):
        if (dfTipo1 == 'dataframe' and dfTipo2 == 'dataframe'):
            temporal = nextAvailTemp('float')
            tempTipo = 'float'

            dfs = "%" + str(dfMem1) + "#" + str(dfMem2)
            indxs = "%" + str(int(indice1) - 1) + "#" + str(int(indice2) - 1)

            QuadGenerate('correlacion', dfs, indxs, temporal)

            pushOperando(temporal)
            pushTipo(tempTipo)
            pushMemoria(temporal)
        else:
            sys.exit("Error en Funcion Especial Correlaciona. Los primeros dos parametros no son dataframes")
    else:
        sys.exit("Error en Funcion Especial Correlaciona. Los indices deben ser enteros")

    #print("FUNESP3")

def p_funEspVoid1(p):
    '''
    funEspVoid1 :
    '''
    #print("FUNESPVOID1")

    funName = pFunciones.pop()

    parName3 = popOperandos()
    parTipo3 = popTipos()
    parMem3 = popMemoria()

    parName2 = popOperandos()
    parTipo2 = popTipos()
    parMem2 = popMemoria()

    parName1 = popOperandos()
    parTipo1 = popTipos()
    parMem1 = popMemoria()

    if (funName == 'histograma'):
        if (parTipo1 == 'dataframe' or parTipo1 == 'int' or parTipo1 == 'float'):
            if (parTipo2 == 'int' and parTipo3 == 'int'):
                QuadGenerate("histograma", parMem1, int(parName2) - 1, int(parName3) - 1)
            else:
                sys.exit(
                    "Error en Funciones Especiales Void (Histograma). El tipo del segundo y tercer parametro debe ser int.")
        else:
            sys.exit(
                "Error en Funciones Especiales Void (Histograma). El tipo del primer parametro debe ser dataframe, int o float.")
    elif (funName == 'lineal'):
        if ((parTipo1 == 'dataframe' or parTipo1 == 'int' or parTipo1 == 'float') and (
                parTipo2 == 'dataframe' or parTipo2 == 'int' or parTipo2 == 'float') and (parTipo1 == parTipo2)):
            if (parTipo3 == 'int'):
                QuadGenerate("lineal", parMem1, parMem2, parMem3)
            else:
                sys.exit("Error en Funciones Especiales Void (Plotline). El tipo del tercer parametro debe ser entera")

        else:
            sys.exit(
                "Error en Funciones Especiales Void (Plotline). El tipo del primer y segundo parametro debe ser dataframe o constante entera o flotante")




### Producciones para puntos neurálgicos de CONSTANTES

def p_neg(p):
    '''
    neg :
    '''
    global negativo
    negativo = True
    #print("NEG")

def p_cteInt(p):
    '''
    cteInt :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])
    #print("CTEINT")

def p_cteFloat(p):
    '''
    cteFloat :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])
    #print("CTEFLOAT")

def p_cteChar(p):
    '''
    cteChar :
    '''
    pushConstante(p[-1])
    #print("CTECHAR")

def p_cteStr(p):
    '''
    cteStr :
    '''
    print("p-1 : ", p[-1])
    pushConstante(p[-1])
    #print("CTESTR")


## Producciones para puntos neurálgicos de EXPRESIONES
def p_pExp1(p):
    '''
    pExp1 :
    '''
    global currentFunc
    global functionDirectory
    global pOperandos
    global pTipos
    global forBool
    global varFor
    global isArray
    global currentVarName

    idName = p[-1]
    idType = functionDirectory.searchVarType(currentFunc, idName)
    if not idType:  # Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = functionDirectory.searchVarType(GLOB, idName)
        print("Ahora busca la variable en el contexto Global ")

    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return

    varPosMem = functionDirectory.funcMemory(currentFunc, idName)
    if not varPosMem:
        varPosMem = functionDirectory.funcMemory(GLOB, idName)

    if varPosMem < 0:
        print("Error: Variable ", idName, " no declarada")
        return

    if forBool:
        varFor = idName

    isDim = functionDirectory.isDimensionadaVar(currentFunc, idName)

    print("Exp1, DIMENSIONADA: ", isDim)

    if isDim == -1:  # sigfinica que no esta en este contexto
        isDim = functionDirectory.isDimensionadaVar(GLOB, idName)

    if isDim == 1:
        isArray = True
        currentVarName = idName
    elif isDim == 0:
        isArray = False
    else:
        isArray = False
        sys.exit("Error. No se ha declarado la variable : ", idName)
        return

    pushOperando(idName)
    pushMemoria(varPosMem)
    pushTipo(idType)

    print("\n")
    #print("PEXP1")

def p_exp2(p):
    '''
    exp2 :
    '''
    global pOper

    if p[-1] not in OP_SUM_RES:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    #print("EXP2")

def p_exp3(p):
    '''
    exp3 :
    '''
    global pOper

    if p[-1] not in OP_MUL_DIV:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    print("EXP3")

def p_exp4(p):
    '''
    exp4 :
    '''
    if topOperador() in OP_SUM_RES:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            errorTypeMismatch()
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)
    #print("EXP4")

def p_exp5(p):
    '''
    exp5 :
    '''
    if topOperador() in OP_MUL_DIV:

        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)
    #print("EXP5")

def p_exp6(p):
    '''
    exp6 :
    '''
    global pOper
    pushOperador('(')
    print("pushOperador: '('")
    #print("EXP6")

def p_exp7(p):
    '''
    exp7 :
    '''
    tipo = popOperadores()
    print("Quita fondo Falso ')'")
    #print("EXP7")

def p_exp8(p):
    '''
    exp8 :
    '''
    global popOperadores
    if p[-1] not in OP_REL:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    #print("EXP8")

def p_exp9(p):
    '''
    exp9 :
    '''
    if topOperador() in OP_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)

    #print("EXP9")

def p_exp10(p):
    '''
    exp10 :
    '''
    global pOper
    if p[-1] not in OP_LOGICOS:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    #print("EXP10")

def p_exp11(p):
    '''
    exp11 :
    '''
    if topOperador() in OP_LOGICOS:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftMem, quad_rightMem, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushMemoria(quad_resultIndex)
            pushTipo(quad_resultType)
    #print("EXP11")


# Inserta "=" en la pila de operadores
def p_sec1(p):
    '''
    sec1 :
    '''
    global pOper
    if p[-1] not in OP_ASIG:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    #print("SEC1")

def p_sec2(p):
    '''
    sec2 :
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_leftOperand = popOperandos()
        quad_leftMem = popMemoria()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        global functionDirectory

        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if functionDirectory.varExist(currentFunc, quad_leftOperand) or functionDirectory.varExist(GLOB, quad_leftOperand):
            if quad_resultType == 'error':
                print("Error: Operacion invalida")
            else:
                QuadGenerate(quad_operator, quad_rightMem, '', quad_leftMem)
        else:
            print("Error al intentar asignar una variable")
    #print("SEC2")

def p_sec3(p):
    '''
    sec3 :
    '''
    global pOper
    if p[-1] not in OP_SECUENCIALES:
        print("Error: Operador no esperado")
    else:
        pushOperador(p[-1])
    #print("SEC3")

def p_sec4(p):
    '''
    sec4 :
    '''
    global semCube
    if topOperador() in OP_SECUENCIALES:
        print("Voy a ejecutar pnSEc4")
        quad_Operando = popOperandos()
        quad_rightType = popTipos()
        quad_rightMem = popMemoria()
        quad_operator = popOperadores()

        quad_resultType = semCube.getResultType(quad_operator, quad_rightType, '')

        if quad_resultType == 'error':
            print("Error: Operacion invalida")
        else:
            QuadGenerate(quad_operator, quad_rightMem, '', quad_operator)
            pushOperador(quad_operator)
    #print("SEC4")

def p_sec5(p):
    '''
    sec5 :
    '''
    popOperadores()
    #print("SEC5")


# Generación de código para estatutos no lineales, condicionales

# Genera el cuadruplo GOTOF en la condicion SI depues de recibir el booleano generado por la expresion
def p_cond1(p): #IF
    '''
    cond1 :
    '''
    global cuads
    memPos = popMemoria()
    exp_type = popTipos()

    if (exp_type != 'error'):
        result = popOperandos()
        QuadGenerate('GOTOF', result, '', '')
        pushSaltos(nextQuad() - 1)

    else:
        errorTypeMismatch()
    #print("COND1")

# Llena el cuadruplo para saber cuando terminar la condicion
def p_cond2(p): #IF
    '''
    cond2 :
    '''
    global cuads

    end = popSaltos()

    QuadTemporal = (cuads[end][0], cuads[end][1], cuads[end][2], nextQuad())
    cuads[end] = QuadTemporal
    #print("COND2")

# Genera el cuadruplo GOTO para SINO (else) y completa el cuadruplo
def p_cond3(p): #IF
    '''
    cond3 :
    '''
    global cuads
    QuadGenerate('GOTO', '', '', '')
    falso = popSaltos()
    pushSaltos(nextQuad() - 1)
    QuadTemporal = (cuads[falso][0], cuads[falso][1], cuads[falso][2], nextQuad())
    cuads[falso] = QuadTemporal
    #print("COND3")

#Mete el siguiente cuadruplo a pSaltos. Que representa la ubicacion a donde regresara al final del ciclo para volver a evaluar la condicion
def p_ciclos1(p):
    '''
    ciclos1 :
    '''
    pushSaltos(nextQuad())

    #print("CICLOS1")

# Genera el cuadruplo de GOTOF
def p_ciclos2(p):
    '''
    ciclos2 :
    '''
    exp_type = popTipos()
    memPos = popMemoria()
    if exp_type != 'error':
        result = popOperandos()
        QuadGenerate('GOTOF', result, '', '')
        pushSaltos(nextQuad() - 1)
    else:
        errorTypeMismatch()
    #print("CICLOS2")


# Genera el cuadruplo GOTO para regresar al inicio del ciclo y volver evaluar la nueva condicion. Aqui tambien se rellena el GOTOF anterior
def p_ciclos3(p):
    '''
    ciclos3 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    QuadGenerate('GOTO', '', '', retorno) #Genetare quad: GOTO

    QuadTemporal = (cuads[end][0], cuads[end][1], cuads[end][2], nextQuad())
    cuads[end] = QuadTemporal #FILL (end, cont)
    #print("CICLOS3")


# Activa la variable bool de ForBool para indicar que esta entrando a un For
def p_ciclos4(p):
    '''
    ciclos4 :
    '''
    global forBool
    forBool = True
    #print("CICLOS4")

def p_ciclos5(p):
    '''
    ciclos5 :
    '''
    if topOperador() in OP_ASIG:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        global functionDirectory

        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if functionDirectory.varExist(currentFunc, quad_leftOperand) or functionDirectory.varExist(GLOB, quad_leftOperand):
            if quad_resultType == 'error':
                print("Error: Operacion invalida")
            else:
                QuadGenerate(quad_operator, quad_rightOperand, '', quad_leftOperand)
        else:
            print("Error")
    #print("CICLOS5")

def p_ciclos6(p):
    '''
    ciclos6 :
    '''
    pushOperando(varFor)

    idType = functionDirectory.searchVarType(currentFunc, varFor)
    if not idType:  # Si no la encuentra en el contexto actual, cambia de contexto a Tipos
        idType = functionDirectory.searchVarType(GLOB, varFor)

    if not idType:
        print("Error: Variable ", idName, " no declarada")
        return

    pushTipo(idType)
    pushOperador('<=')
    pushSaltos(nextQuad())
    #print("CICLOS6")

def p_ciclos7(p):
    '''
    ciclos7 :
    '''
    if topOperador() in OP_REL:
        quad_rightOperand = popOperandos()
        quad_rightType = popTipos()
        quad_leftOperand = popOperandos()
        quad_leftType = popTipos()
        quad_operator = popOperadores()

        global semCube
        quad_resultType = semCube.getResultType(quad_leftType, quad_rightType, quad_operator)

        if quad_resultType == 'error':
            print('Error: Type Mismatch')
        else:
            quad_resultIndex = nextAvailTemp(quad_resultType)
            QuadGenerate(quad_operator, quad_leftOperand, quad_rightOperand, quad_resultIndex)
            pushOperando(quad_resultIndex)
            pushTipo(quad_resultType)

        exp_type = popTipos()
        if (exp_type != 'bool' or exp_type == 'error'):
            errorTypeMismatch()
        else:
            result = popOperandos()
            QuadGenerate('GOTOF', result, '', '')
            pushSaltos(nextQuad() - 1)
    #print("CICLOS7")

def p_ciclos8(p):
    '''
    ciclos8 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    QuadGenerate('GOTO', '', '', retorno) #Genetare quad: GOTO

    QuadTemporal = (cuads[end][0], cuads[end][1], cuads[end][2], nextQuad())
    cuads[end] = QuadTemporal #FILL (end, cont)
    #print("CICLOS8")


### Producciones para puntos neurálgicos de ESTATUTOS
# Punto neurálgico en retorno
def p_pRetorno(p):
    '''
    pRetorno :
    '''
    global currentFunc
    global isVoid
    print("return Bool: ", isVoid)
    if isVoid:
        print(pOperandos)
        print(pTipos)
        operador = popOperadores()
        operandoRetorno = popOperandos()
        tipoRetorno = popTipos()
        memRetorno = popMemoria()

        if functionDirectory.directorio_funciones[currentFunc]['tipo'] == tipoRetorno:
            QuadGenerate(operador, '', '', memRetorno)
        else:
            errorReturnTipo()
    else:
        print ("Error: Esta funcion no debe regresar nada")
    #print("PRETORNO")


### Producciones para los puntos neurálgicos de ARREGLOS
def p_dimDec2(p):
    '''
    dimDec2 :
    '''
    global isArray
    isArray = True
    #print("DIMDEC2")

def p_dimDec5(p):
    '''
    dimDec5 :
    '''
    global R
    global numColumnas
    global functionDirectory
    global currentFunc
    global currentVarName

    columnas = p[-1]
    if columnas > 0:
        R = R * columnas # R = (LimSup - LimInf + 1) * R
        print("PN5Arreglos.  R = ", R)
        numColumnas = columnas

        functionDirectory.updateDimFunc(currentFunc, currentVarName, 0, columnas)
    else:
        sys.exit("Error: Index de arreglo invalido: ", columnas)
    #print("DIMDEC5")

def p_dimDec6(p):
    '''
    dimDec6 :
    '''
    global R
    global numRenglones
    global functionDirectory
    global currentFunc
    global currentVarName

    isMatrix = True
    renglones = p[-1]
    if renglones > 0:
        R = R * renglones
        print("PN6Matriz.  R = ", R)
        numRenglones = renglones

        functionDirectory.updateDimFunc(currentFunc, currentVarName, renglones, -1)
    else:
        sys.exit("Error. Index menor o igual a cero no es valido")
        return

    #print("DIMDEC6")

def p_dimDec8(p):
    '''
    dimDec8 :
    '''
    global R
    global functionDirectory
    global currentFunc
    global currentVarName
    global isArray
    global currentConstArrays
    NumEspacios = R - 1

    currentType = functionDirectory.searchVarType(currentFunc, currentVarName)

    update_pointer(currentFunc, currentType, NumEspacios)  # Separa los espacios que va a usar para el arreglo o matriz

    # Reseteo
    R = 1
    isArray = False
    currentConstArrays = []
    #print("DIMDEC8")


def p_dimAccess2(p):
    '''
    dimAccess2 :
    '''
    global isArray
    global pDims
    isArray = True

    varid = popOperandos()
    varmem = popMemoria()
    vartipo = popTipos()
    pDims.append(varid)
    #print("DIMACCESS2")

def p_arregloAcc(p):
    '''
    arregloAcc :
    '''
    global isArray
    global currentFunc
    global currentVarName

    auxID = popOperandos()
    auxMem = popMemoria()
    auxTipo = popTipos()

    auxDIM = pDims.pop()
    if isArray:
        if auxTipo != 'int':
            sys.exit("Error. Es necesario que el tipo sea un entero para acceder al arreglo")
            return

        varDimensiones = functionDirectory.getDimsVar(currentFunc, auxDIM)

        if varDimensiones == -1:
            varDimensiones = functionDirectory.getDimsVar(GLOB, auxDIM)

            if varDimensiones == -1:
                sys.exit("Error. No existe variable dimensionada")
                return

        # Cuadruplo verifica
        QuadGenerate('VER', auxMem, 0, varDimensiones[0] - 1)

        # Si no es Matriz...
        if varDimensiones[1] == 0:
            # Memoria Base
            PosicionMemoria = functionDirectory.funcMemory(currentFunc, auxDIM)
            if not PosicionMemoria:
                PosicionMemoria = functionDirectory.funcMemory(GLOB, auxDIM)

            if PosicionMemoria < 0:
                sys.exit("Error. Variable no declarada: ", auxDIM)
                return

            TipoActual = functionDirectory.searchVarType(currentFunc, auxDIM)
            if not TipoActual:
                TipoActual = functionDirectory.searchVarType(GLOB, auxDIM)

            if not TipoActual:
                sys.exit("Error. Variable no declarada: ", auxDIM)
                return

            tMem = nextAvailTemp('int')
            QuadGenerate('+', '{' + str(PosicionMemoria) + '}', auxMem, tMem)

            valorTMem = str(tMem) + '!'

            pushOperando(auxDIM)
            pushMemoria(valorTMem)
            pushTipo(TipoActual)
            isArray = False
            currentVarName = ''
        else:  # Si es matriz, hay que generar el cuadruplo de *
            print("\n")
            print("Si es matriz...")
            print("\n")
            print("\n")
            print("\n")
            print("\n")
            print("pOperandos: ", pOperandos)

            tMem = nextAvailTemp('int')
            QuadGenerate('*', auxMem, getAddConst(varDimensiones[1] - 1), tMem)
            pushOperando(tMem)
            pushMemoria(tMem)
            pushTipo('int')
            pDims.append(auxDIM)
    else:
        sys.exit("Error. No se puede acceder al index porque la variable no es dimensionada")
        return
    #print("ARREGLOACC")

def p_matrizAcc(p):
    '''
    matrizAcc :
    '''
    print("AQUI HAY UNA MATRIZ")
    global isArray
    global currentVarName
    global currentFunc
    global pDims
    print("pOperandos: ", pOperandos)

    auxID = popOperandos()
    auxMem = popMemoria()
    auxTipo = popTipos()

    auxDIM = pDims.pop()

    if isArray:
        if auxTipo != 'int':
            sys.exit("Error. Es necesario que el tipo sea un entero para acceder al arreglo")
            return

        # Checa las dimensiones
        varDimensiones = functionDirectory.getDimsVar(currentFunc, auxDIM)
        print("MAT: ", auxDIM)
        if varDimensiones == -1:
            varDimensiones = functionDirectory.getDimsVar(GLOB, auxDIM)  # Busca en global
            if varDimensiones == -1:  # si no hay en global...
                sys.exit("Error. La variable no es matriz...")
                return

        # Si obtiene las dimensiones correctamente.....
        # Genera los cuadruplos
        QuadGenerate('VER', auxMem, 0, varDimensiones[1] - 1)

        # Memoria Base
        PosicionMemoria = functionDirectory.funcMemory(currentFunc, auxDIM)
        if not PosicionMemoria:
            PosicionMemoria = functionDirectory.funcMemory(GLOB, auxDIM)
        if PosicionMemoria < 0:
            sys.exit("Error. La variable no ha sido declarada: ", auxDIM)
            return

        # AHORA checamos los tipos
        TipoActual = functionDirectory.searchVarType(currentFunc, auxDIM)
        if not TipoActual:
            TipoActual = functionDirectory.searchVarType(GLOB, auxDIM)

        if not TipoActual:  # Si no está en globales
            sys.exit("Error. La variable no ha sido declarada: ", auxDIM)
            return

        auxID2 = popOperandos()
        auxMem2 = popMemoria()
        auxTipo2 = popTipos()

        tMem2 = nextAvailTemp('int')
        QuadGenerate('+', auxMem2, auxMem, tMem2)
        pushOperando(tMem2)
        pushMemoria(tMem2)
        pushTipo('int')

        tMem3 = nextAvailTemp('int')
        base = str(PosicionMemoria)  # ESta es la base
        QuadGenerate('+', '{' + str(base) + '}', tMem2, tMem3)

        valorTMem = str(tMem3) + '!'

        pushOperando(auxDIM)
        pushMemoria(valorTMem)
        pushTipo(TipoActual)

        isArray = False
        currentVarName = ''

    else:
        sys.exit("Error. La variable no es dimensionada y no se puede acceder al indice")
        return
    #print("MATRIZACC")

def p_activaArray(p):
    '''
    activaArray :
    '''
    global isArray
    isArray = True
    #print("ACTIVAARRAY")


### Producciones para puntos neurálgicos de CARGA DE ARCHIVOS
def p_carga(p):
    '''
    carga :
    '''
    maxRenglones = popOperandos()
    maxRenglonesTipo = popTipos()
    maxRenglonesMem = popMemoria()

    maxVariables = popOperandos()
    maxVariablesTipo = popTipos()
    maxVariablesMem = popMemoria()

    path = popOperandos()
    pathTipo = popTipos()
    pathMem = popMemoria()

    dfName = popOperandos()
    dfTipo = popTipos()
    dfMem = popMemoria()

    if (pathTipo != 'string'):
        sys.exit("Error al cargar archivo. El tipo del segundo parametro no es string.")

    if (dfTipo != 'dataframe'):
        sys.exit("Error al cargar archivo. El tipo del primer parametro no es dataframe.")

    QuadGenerate("carga", dfMem, path, '')

    #print("CARGA")

parser = yacc.yacc()

# CODIGO PARA PRUEBAS (EN FOLDER DE PRUEBAS)
def main():
    #name = input('File name: ')
    name = "test/" + "prueba2" + ".covid" #Para probar, cambia el nombre del archivo
    print(name)
    try:
        f = open(name,'r', encoding='utf-8')
        #QuadTemporal = ('0', '0', '0', '0')
        #pushQuad(QuadTemporal)
        result = parser.parse(f.read())
        print(result)
        f.close()
    except EOFError:
        print (EOFError)

main()