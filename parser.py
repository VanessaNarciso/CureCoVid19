import ply.yacc as yacc
from lexer import tokens
from sys import stdin
import sys
import codecs

#Funcion inicial del programa
def p_programa(p):
    '''
    programa :  PROGRAMA ID SEMICOLON declara_vars declara_fun principal
    '''
    print("programa")

def p_declara_fun(p):
    '''
    declara_fun : functions
    '''
    print("declara fun")

def p_functions(p):
    '''
    functions : function_t functions
        | function_v functions
        | empty
    '''
    print("functions")

#PRINCIPAL

def p_principal(p):
    '''
    principal : principalI declara_vars principal1 RCURBRACKET
    '''
    print("principal")

def p_principalI(p):
    '''
    principalI : principalS LCURBRACKET
    '''
    print("principalI")

def p_principalS(p):
    '''
    principalS : PRINCIPAL
    '''
    print("principal5")

def p_principal1(p):
    '''
    principal1 : stmt_v principal1
        | empty
    '''
    print("principal1")

def p_declara_vars(p):
    '''
    declara_vars : vars declara_vars
        | empty
    '''
    print("declara_vars")

def p_vars(p):
    '''
    vars : VAR type ID dimension SEMICOLON
    '''
    print("vars")

def p_type(p):
    '''
    type : INT
        | FLOAT
        | CHAR
        | STRING
        | DATAFRAME
    '''
    print("type")

def p_dimension(p):
    '''
    dimension : LBRACKET CTEINT RBRACKET
        | LBRACKET CTEINT RBRACKET LBRACKET CTEINT RBRACKET
        | empty
    '''
    print("dimension")


def p_function_t(p):
    '''
    function_t : FUNCION functionI function2 inicia_fun declara_vars function4 termina_fun
    '''
    print("function t")
def p_functionI(p):
    '''
    functionI : type ID
    '''
    print("functionI")

def p_function2(p):
    '''
    function2 : LPAREN function3 RPAREN
    '''
    print("function2")

def p_function3(p):
    '''
    function3 : funParam function5
        | empty
    '''
    print("function3")

def p_funParam(p):
    '''
    funParam : type ID
    '''
    print("funParam")

def p_inicia_fun(p):
    '''
    inicia_fun : LCURBRACKET
    '''
    print("inicia_fun")

def p_function4(p):
    '''
    function4 : statement function4
        | empty
    '''
    print("function4")

def p_statement(p):
    '''
    statement : assignment
        | condition
        | write
        | loop
        | read
        | loadData
        | funCall SEMICOLON
        | return
    '''
    print("statement")

def p_assignment(p):
    '''
    assignment : id equals assignment3 SEMICOLON
    '''
    print("assignment")


def p_id(p):
    '''
    id : identifier indice_dimension
    '''
    print("id")

def p_identifier(p):
    '''
    identifier : ID
    '''
    print("identifier")

def p_indice_dimension(p):
    '''
    indice_dimension : LBRACKET exp RBRACKET LBRACKET exp RBRACKET
        | LBRACKET exp RBRACKET
        | empty
    '''
    print("indice_dimension")

def p_equals(p):
    '''
    equals : EQUALS
    '''
    print("equals")

def p_assignment3(p):
    '''
    assignment3 : exp
        | read
    '''
    print("assignment3")

def p_condition(p):
    '''
    condition : SI head_condition ENTONCES body condition1
    '''
    print("condition")

def p_head_condition(p):
    '''
    head_condition : LPAREN expression close_condition
    '''
    print("head_condition")

def p_body(p):
    '''
    body : LCURBRACKET body1 RCURBRACKET
    '''
    print("body")

def p_body1(p):
    '''
    body1 : statement body1
        | empty
    '''
    print("body1")

def p_condition1(p):
    '''
    condition1 : SINO body
        | empty
    '''
    print("condition1")


def p_close_condition(p):
    '''
    close_condition : RPAREN
    '''
    print("close_condition")

def p_write(p):
    '''
    write : ESCRIBE LPAREN expression RPAREN SEMICOLON
    '''
    print("write")

def p_expression(p):
    '''
    expression : exp loper exp
        | exp
    '''
    print("expression")

def p_loper(p):
    '''
    loper : GREATERTHAN
        | LESSTHAN
        | GREATEREQ
        | LESSEQ
        | NOTEQUAL
        | ISEQUAL
    '''
    print("loper")

def p_exp(p):
    '''
    exp : term
        | term exp_o exp
    '''
    print("exp")

def p_exp_o(p):
    '''
    exp_o : PLUS
        | MINUS
    '''
    print("exp_o")

def p_term(p):
    '''
    term : factor term_o term
        | factor
    '''
    print("term")

def p_factor(p):
    '''
    factor : vcte
        | leftP expression rightP
    '''
    print("factor")

def p_leftP(p):
    '''
    leftP : LPAREN
    '''
    print("leftP")

def p_rightP(p):
    '''
    rightP : RPAREN
    '''
    print("rightP")
def p_vcte(p):
    '''
    vcte : cte_int
        | cte_float
        | cte_string
        | id
        | funCall
        | vectorMatriz
    '''
    print("vcte")

def p_cte_int(p):
    '''
    cte_int : negativo CTEINT
    '''
    print("cte_int")

def p_cte_float(p):
    '''
    cte_float : negativo CTEFLOAT
    '''
    print("cte_float")

def p_cte_string(p):
    '''
    cte_string : negativo CTESTRING
    '''
    print("cte_string")

def p_negativo(p):
    '''
    negativo : MINUS
        | empty
    '''
    print("negativo")

def p_vectorMatriz(p):
    '''
    vectorMatriz : LBRACKET vm1 RBRACKET
        | vm1
    '''
    print("vectorMatriz")

def p_vm1(p):
    '''
    vm1 : LBRACKET vm2 RBRACKET COMMA vm1
        | LBRACKET vm2 RBRACKET
    '''
    print("vm1")

def p_vm2(p):
    '''
    vm2 : exp COMMA vm2
        | exp
        | empty
    '''
    print("vm2")

def p_term_o(p):
    '''
    term_o : TIMES
        | DIVIDE
    '''
    print("term_o")

def p_loop(p):
    '''
    loop : mientras
        | desde
    '''
    print("loop")

def p_mientras(p):
    '''
    mientras : mientras1 HAZ body
    '''
    print("mientras")

def p_mientras1(p):
    '''
    mientras1 : mientras_w LPAREN expression RPAREN
    '''
    print("mientras1")

def p_mientras_w(p):
    '''
    mientras_w : MIENTRAS
    '''
    print("mientras_w")


def p_desde(p):
    '''
    desde : nuevo_desde desdeBody
    '''
    print("desde")

def p_nuevo_desde(p):
    '''
    nuevo_desde : DESDE id EQUALS desde2 HASTA desde2 HACER
    '''
    print("nuevo_desde")

def p_desde2(p):
    '''
    desde2 : exp
    '''
    print("desde2")

def p_desdeBody(p):
    '''
    desdeBody : body
    '''
    print("desdeBody")

def p_read(p):
    '''
    read : LEE LPAREN id read1 RPAREN SEMICOLON
    '''
    print("read")

def p_read1(p):
    '''
    read1 : LBRACKET exp RBRACKET  LBRACKET exp RBRACKET
        | LBRACKET exp RBRACKET
        | empty
    '''
    print("read1")

def p_loadData(p):
    '''
    loadData : CARGAARCHIVO LPAREN ID route maxVariables maxRows RPAREN SEMICOLON
    '''
    print("loadData")


def p_route(p):
    '''
    route : CTESTRING
    '''
    print("route")

def p_maxVariables(p):
    '''
    maxVariables : CTEINT
    '''
    print("maxVariable")

def p_maxRows(p):
    '''
    maxRows : CTEINT
    '''
    print("maxRows")

def p_funCall(p):
    '''
    funCall : ID iniciaFunCall funCall2 terminaFunCall
    '''
    print("funCall")

def p_iniciaFunCall(p):
    '''
    iniciaFunCall : LPAREN
    '''
    print("iniciaFunCall")

def p_funCall2(p):
    '''
    funCall2 : funcallParam funCall3
        | empty
    '''
    print("funCall2")

def p_funcallParam(p):
    '''
    funcallParam : exp
    '''
    print("funcallParam")

def p_funCall3(p):
    '''
    funCall3 : COMMA funcallParam funCall3
        | empty
    '''
    print("funCall3")

def p_terminaFunCall(p):
    '''
    terminaFunCall : RPAREN
    '''
    print("terminaFunCall")


def p_return(p):
    '''
    return : REGRESA return1 SEMICOLON
    '''
    print("return")

def p_return1(p):
    '''
    return1 : vcte
        | exp
    '''
    print("return1")

def p_function5(p):
    '''
    function5 : COMMA funParam function5
        | empty
    '''
    print("function5")

def p_termina_fun(p):
    '''
    termina_fun : RCURBRACKET
    '''
    print("termina_fun")

def p_function_v(p):
    '''
    function_v : FUNCION functionV function2 inicia_fun declara_vars function9 termina_fun
    '''
    print("function_v")


def p_functionV(p):
    '''
    functionV : VOID ID
    '''
    print("functionV")

def p_function9(p):
    '''
    function9 : stmt_v function9
        | empty
    '''
    print("function9")

def p_stmt_v(p):
    '''
    stmt_v : assignment
        | condition
        | write
        | loop
        | read
        | loadData
        | funCall SEMICOLON
        | return
    '''
    print("stmt_v")










def p_empty(p):
    '''
    empty :
    '''
    pass

def p_error(p):
    print("Error de sintaxis", p)
    print("Error en la linea" + str(p.lineno))


test = './test/prueba1.covid'
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()


parser = yacc.yacc()
result = parser.parse(cadena)
print(result)

















