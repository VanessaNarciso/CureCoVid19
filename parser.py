import ply.yacc as yacc
import os
from lexer import tokens
from sys import stdin
import sys
import codecs
import re
import os

precedence = (
    ('nonassoc','SEMICOLON'),
    ('right', 'EQUALS'),
    ('left', 'NOTEQUAL'),
    ('nonassoc','LESSTHAN','LESSEQ','GREATERTHAN','GREATEREQ')
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','LPAREN','RPAREN'),
    ('left','LCURBRACKET','RCURBRACKET'),
    ('left','LBRACKET','RBRACKET')
)

# INICIO DE UN PROGRAMA
def p_programa(p):
    '''
    programa :  PROGRAMA ID SEMICOLON declara_vars declara_fun principal
    '''
    print("programa")

def p_declara_vars(p):
    '''
    declara_vars : var
        | empty
    '''
    print("declara_vars")

def p_declara_fun(p):
    '''
    declara_fun : funcion declara_fun
    '''
    print("declara fun")

def p_functions(p):
    '''
    functions : function_t functions
        | function_v functions
        | empty
    '''
    print("functions")

def p_principal(p):
    '''
    principal : PRINCIPAL principal2 LPAREN RPAREN bloque
    '''
    print("principal")


# DECLARACIÓN DE VARIABLES
def p_var(p):
    'var : VAR var2'
    print("VAR")

def p_var2(p):
    'var2 : type SEMICOLON ids var3'
    print("VAR2")

def p_var3(p):
    '''
    var3 : var2
         | empty
    '''
    print("VAR3")

def p_type(p): #type1 = simple, type2=compuesto
    '''
    type : type1
         | type2
    '''
    print("P_TYPE")

# DECLARACIÓN DE FUNCIONES
def p_funcion(p):
    'funcion : FUNCION fun_type ID funDec1 LPAREN parametros RPAREN funDec4 var1 bloque funDec7'
    print("FUNCION")

def p_fun_type(p):
    '''
    fun_type : VOID setCurrentType
             | type1
    '''
    print("FUN_TYPE")

def p_parametros(p):
    '''
    parametros : param
               | empty
    '''
    print("PARAMETROS")

def p_param(p):
    'param : type1 ID funDec2 param1'
    print("PARAM")

def p_param1(p):
    '''
    param1 : COMMA param
           | empty
    '''


# TIPOS
def p_type1(p):
    '''
    type1 : INT setCurrentType
        | FLOAT setCurrentType
        | CHAR setCurrentType
    '''
    print("P_TYPE1")

def p_type2(p):
    '''
    type2 : DATAFRAME setCurrentType
        | STRING setCurrentType
    '''
    print("P_TYPE2")

# IDs
def p_ids(p): #Lista de IDs
    'ids : lista SEMICOLON'
    print("IDs")

def p_lista(p):
    'lista : ID addVariable dd lista1'
    print("lista")

def p_dd(p):
    '''
    dd : dim_dec dimDec8
       | empty
    '''
    print("dd")

def p_lista1(p):
    '''
    lista1 : COMMA lista
           | empty
    '''
    print("lista1")

# DIMENSIONES
def p_dim_dec(p):
    'dim_dec : LBRACKET dimDec2 CTEINT dimDec5 RBRACKET decRenglones dim_dec1'
    print("dim_dec")

def p_dim_dec1(p):
    '''
    dim_dec1 : LBRACKET CTEINT dimDec6 RBRACKET decColumnas
             | empty
    '''
    print("dim_dec1")

def p_dim_index(p):
    '''
    dim_index : LBRACKET dimAccess2 exp6 exp activaArray arregloAcc RBRACKET exp7 dim_index1
    '''
    print("dim_index")

def p_dim_index1(p):
    '''
    dim_index1 : LBRACKET exp6 exp activaArray RBRACKET exp7 matrizAcc
               | empty
    '''
    print("dim_index1")

# BLOQUE
def p_bloque(p):
    'bloque : LCURBRACKET est RCURBRACKET'
    print("BLOQUE")

def p_est(p):
    '''
    est : estatutos est
        | empty
    '''
    print("EST")

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
    print("ESTATUTOS")

# ESTATUTOS
def p_asignacion(p):
    'asignacion : variable EQUALS sec1 exp SEMICOLON sec2'
    print("ASIGNACION")

def p_variable(p):
    'variable : ID exp1 di'
    print("VARIABLE")

def p_di(p):
    '''
    di : dim_index
       | empty
    '''
    print("di")

def p_llamada(p):
    'llamada :  ID funCall1 LPAREN llamada1 RPAREN funCall_5'
    print("LLAMADA")

def p_llamada1(p):
    '''
    llamada1 : exp funCall3 llamada2
             | empty
    '''
    print("LLAMADA1")

def p_llamada2(p):
    '''
    llamada2 : COMMA llamada1
             | empty
    '''
    print("LLAMADA2")

def p_retorno(p):
    'retorno : REGRESA sec3 LPAREN exp RPAREN retorno SEMICOLON'
    print("RETORNO")
def p_lectura(p):
    'lectura : LEE sec3 LPAREN variable RPAREN SEMICOLON sec4 sec5'
    print("LECTURA")

def p_escritura(p):
    'escritura : ESCRIBE sec3 LPAREN esc RPAREN SEMICOLON sec5'
    print("ESCRITURA")

def p_esc(p):
    'esc : esc1 esc2'
    print("ESC")

def p_esc1(p):
    '''
    esc1 : exp pnSec4
    '''
    print("ESC1")

def p_esc2(p):
    '''
    esc2 : COMMA esc
         | empty
    '''
    print("ESC2")

def p_carga_datos(p):
    'carga_datos : CARGAARCHIVO LPAREN ID COMMA CTESTRING COMMA ca COMMA ca RPAREN SEMICOLON'
    print("CARGA DATOS")

def p_ca(pa):
    '''
    ca : ID
       | CTEINT
    '''
    print("CA")

# CONDICIONALES Y CICLOS
def p_decision(p): #IF
    'decision : SI LPAREN expresion RPAREN cond1 ENTONCES bloque sino cond2'
    print("DECISION")

def p_sino(p): #ELSE
    '''
    sino : SINO cond3 bloque
         | empty
    '''
    print("SINO")

def p_condicional(p): #While
    'condicional : MIENTRAS ciclos1 LPAREN expresion RPAREN ciclos2 HAZ bloque ciclos3'
    print("CONDICIONAL")

def p_ciclo(p): #For
    'ciclo : DESDE ciclos4 variable EQUALS sec1 exp ciclos5 HASTA ciclos6 exp ciclos7 HACER bloque ciclos8'
    print("CICLO")

def p_funciones_especiales_void(p):
    '''
    funciones_especiales_void : VARIABLES funEsp1 LPAREN ID COMMA ID COMMA ID RPAREN SEMICOLON
                              | fev LPAREN ID COMMA v_exp RPAREN SEMICOLON
    '''
    print("FUNCIONES_ESPECIALES_VOID")

def p_fev(p):
    '''
    fev : HISTOGRAMA funEsp1
        | LINEAL funEsp1
    '''
    print("FEV")

def p_funciones_especiales(p):
    '''
    funciones_especiales : fe LPAREN ID COMMA v_exp RPAREN
                         | CORRELACIONA funEsp1 LPAREN ID COMMA v_exp COMMA v_exp RPAREN
    '''
    print("FUNCIONES_ESPECIALES")

def p_fe(p):
    '''
    fe : MEDIA funEsp1
       | MODA funEsp1
       | VARIANZA funEsp1
    '''
    print("FE")

def p_v_exp(p):
    'v_exp : VARIABLES  LBRACKET exp RBRACKET'
    print("V_EXP")

def p_var_cte(p):#Se modificaran los PN
    '''
    var_cte : CTECHAR cteChar
            | CTESTRING cteStr
            | SUB neg var_num
            | var_num
    '''
    print("VAR_CTE")

def p_var_num(p):
    '''
    var_num : CTEINT cteInt
            | CTEFLOAT cteFloat
    '''
    print("VAR_NUM")

# EXPRESIONES
def p_expresion(p):
    'expresion : mega_exp expresion1'
    print("EXPRESSION")

def p_expresion1(p):
    '''
    expresion1 : EQUALS expresion
               | empty
    '''
    print("EXPRESSION1")

def p_mega_exp(p):
    'mega_exp : super_exp meg'
    print("MEGA_EXP")

def p_meg(p):
    '''
    meg : op_l exp10 mega_exp exp11
        | empty
    '''
    print("MEG")

def p_op_l(p):
    '''
    op_l : AND
         | OR
    '''
    print("OP_L")

def p_super_exp(p):
    'super_exp : exp sp'
    print("SUPER_EXP")

def p_sp(p):
    '''
    sp : op_r  exp exp9
       | empty
    '''
    print("SP")

def p_op_r(p):
    '''
    op_r : LESSTHAN exp8
         | GREATERTHAN exp8
         | LESSEQ exp8
         | GREATEREQ exp8
         | NOT_EQUAL exp8
         | ISEQUAL exp8
    '''
    print("OP_R")

def p_exp(p):
    'exp : termino exp4 exp1'
    print("EXP")

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
    print("EXP1")

def p_op_a(p):
    '''
    op_a : PLUS exp2
         | MINUS exp2
    '''
    print("OP_A")

def p_termino(p):
    'termino : factor exp5 term'
    print("TERMINO")

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
    print("TERM")

def p_op_a1(p):
    '''
    op_a1 : TIMES exp3
          | DIVIDE exp3
    '''
    print("OP_A1")

def p_factor(p):
    '''
    factor : var_cte
           | LPAREN exp6 exp RPAREN exp7
           | variable
           | llamada
           | funciones_especiales
    '''
    print("FACTOR")

def p_empty(p):
    '''empty :'''
    pass
    print("NULO")

def p_error(p):
    if p:
        print("Error de sintaxis ",p.type, p.value)
        print("Error en la linea "+str(p.lineno))
        print()
        parser.errok()
    else:
        print("Syntax error at EOF")
##########AQUÍ ME QUEDÉ

















