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
                         | CORRELACIONA funEsp1 LPAREN ID pExp1 COMMA ID pExp1 COMMA CTEINT cteInt COMMA CTEINT cteInt RPAREN funEsp3
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
    #print("PUSH SALTO: ", salto)
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
    print(functionDirectory.func_print(GLOB))
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


### Producciones y acciones semánticas en los puntos neurálgicos

def p_gotoPrincipal(p):
    '''
    gotoPrincipal :
    '''
    print("GOTOPRINCIPAL")

def p_principal2(p):
    '''
    principal2 :
    '''
    print("PRINCIPAL2")

def p_df(p):
    '''
    df :
    '''
    print("DF")

def p_df2(p):
    '''
    df2 :
    '''
    print("DF2")

# PRODUCCIONES PARA DIRFUNC Y TABLA DE VARIABLES
def p_setCurrentType(p):
    '''
    setCurrentType :
    '''
    print("SETCURRENTTYPE")

def p_addVariable(p):
    '''
    addVariable :
    '''
    print("ADDVARIABLE")

def p_decRenglones(p):
    '''
    decRenglones :
    '''
    print("DECRENGLONES")

def p_decColumnas(p):
    '''
    decColumnas :
    '''
    print("DECCOLUMNAS")

# GENERACIÓN DE CUADRUPLOS
def p_funDec1(p):
    '''
    funDec1 :
    '''
    print("FUNDEC1")

def p_funDec2(p):
    '''
    funDec2 :
    '''
    print("FUNDEC2")

def p_funDec4(p):
    '''
    funDec4 :
    '''
    print("FUNDEC4")

def p_funDec7(p):
    '''
    funDec7 :
    '''
    print("FUNDEC7")

def p_funCall1(p):
    '''
    funCall1 :
    '''
    print("FUNCALL1")

def p_funCall3(p):
    '''
    funCall3 :
    '''
    print("FUNCALL3")

def p_funCall5(p):
    '''
    funCall5 :
    '''
    print("FUNCALL5")


def p_funEsp1(p):
    '''
    funEsp1 :
    '''
    print("FUNESP1")

def p_funEsp2(p):
    '''
    funEsp2 :
    '''
    print("FUNESP2")

def p_funEsp3(p):
    '''
    funEsp3 :
    '''
    print("FUNESP3")

def p_funEspVoid1(p):
    '''
    pnFunEspVoid1 :
    '''
    print("FUNESPVOID1")

def p_neg(p):
    '''
    neg :
    '''
    print("NEG")

def p_cteInt(p):
    '''
    cteInt :
    '''
    print("CTEINT")

def p_cteFloat(p):
    '''
    cteFloat :
    '''
    print("CTEFLOAT")

def p_cteChar(p):
    '''
    cteChar :
    '''
    print("CTECHAR")

def p_cteStr(p):
    '''
    cteStr :
    '''
    print("CTESTR")

def p_pExp1(p):
    '''
    pExp1 :
    '''
    print("PEXP1")

def p_exp2(p):
    '''
    exp2 :
    '''
    print("EXP2")

def p_exp3(p):
    '''
    exp3 :
    '''
    print("EXP3")

def p_exp4(p):
    '''
    exp4 :
    '''
    print("EXP4")

def p_exp5(p):
    '''
    exp5 :
    '''
    print("EXP5")

def p_exp6(p):
    '''
    exp6 :
    '''
    print("EXP6")

def p_exp7(p):
    '''
    exp7 :
    '''
    print("EXP7")

def p_exp8(p):
    '''
    exp8 :
    '''
    print("EXP8")

def p_exp9(p):
    '''
    exp9 :
    '''
    print("EXP9")

def p_exp10(p):
    '''
    exp10 :
    '''
    print("EXP10")

def p_exp11(p):
    '''
    exp11 :
    '''
    print("EXP11")

def p_sec1(p):
    '''
    sec1 :
    '''
    print("SEC1")

def p_sec2(p):
    '''
    sec2 :
    '''
    print("SEC2")

def p_sec3(p):
    '''
    sec3 :
    '''
    print("SEC3")

def p_sec4(p):
    '''
    sec4 :
    '''
    print("SEC4")

def p_sec5(p):
    '''
    sec5 :
    '''
    print("SEC5")

def p_cond1(p): #IF
    '''
    cond1 :
    '''
    print("COND1")

def p_cond2(p): #IF
    '''
    cond2 :
    '''
    print("COND2")

def p_cond3(p): #IF
    '''
    cond3 :
    '''
    print("COND3")

def p_ciclos1(p):
    '''
    ciclos1 :
    '''
    print("CICLOS1")

def p_ciclos2(p):
    '''
    ciclos2 :
    '''
    print("CICLOS2")

def p_ciclos3(p):
    '''
    ciclos3 :
    '''
    print("CICLOS3")

def p_ciclos4(p):
    '''
    ciclos4 :
    '''
    print("CICLOS4")

def p_ciclos5(p):
    '''
    ciclos5 :
    '''
    print("CICLOS5")

def p_ciclos6(p):
    '''
    ciclos6 :
    '''
    print("CICLOS6")

def p_ciclos7(p):
    '''
    ciclos7 :
    '''
    print("CICLOS7")

def p_ciclos8(p):
    '''
    ciclos8 :
    '''
    print("CICLOS8")

def p_pRetorno(p):
    '''
    pRetorno :
    '''
    print("PRETORNO")

def p_dimDec2(p):
    '''
    dimDec2 :
    '''
    print("DIMDEC2")

def p_dimDec5(p):
    '''
    dimDec5 :
    '''
    print("DIMDEC5")

def p_dimDec6(p):
    '''
    dimDec6 :
    '''
    print("DIMDEC6")

def p_dimDec8(p):
    '''
    dimDec8 :
    '''
    print("DIMDEC8")

def p_dimAccess2(p):
    '''
    dimAccess2 :
    '''
    print("DIMACCESS2")

def p_arregloAcc(p):
    '''
    arregloAcc :
    '''
    print("ARREGLOACC")

def p_matrizAcc(p):
    '''
    matrizAcc :
    '''
    print("MATRIZACC")

def p_activaArray(p):
    '''
    activaArray :
    '''
    print("ACTIVAARRAY")


def p_carga(p):
    '''
    carga :
    '''
    print("CARGA")

parser = yacc.yacc()

# CODIGO PARA PRUEBAS (EN FOLDER DE PRUEBAS)
def main():
    #name = input('File name: ')
    name = "test/" + "prueba3" + ".covid" #Para probar, cambia el nombre del archivo
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