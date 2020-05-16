import ply.yacc as yacc
from lexer import tokens
from sys import stdin
import sys


def p_programa(p):
    '''
    programa :  PROGRAMA ID SEMICOLON declara_vars declara_fun principal
    '''

def p_declara_vars(p):
    '''
    declara_vars : vars declara_vars
        | empty
    '''

def p_vars(p):
    '''
    vars : VAR type ID dimension SEMICOLON
    '''

def p_type(p):
    '''
    type : INT
        | FLOAT
        | CHAR
        | STRING
        | DATAFRAME
    '''

def p_dimension(p):
    '''
    dimension : LBRACKET CTEINT RBRACKET
        | LBRACKET CTEINT RBRACKET
        | empty
    '''

def p_declara_fun(p):
    '''
    declara_fun : functions
    '''

def p_functions(p):
    '''
    functions : function_t functions
        | function_v functions
        | empty
    '''

def p_function_t(p):
    '''
    function_t : FUNCION functionI function2 inicia_fun declara_vars function4 termina_fun
    '''

def p_functionI(p):
    '''
    functionI : type ID
    '''

def p_function2(p):
    '''
    function2 : LPAREN function3 RPAREN
    '''

def p_function3(p):
    '''
    function3 : funParam function5
        | empty
    '''

def p_funParam(p):
    '''
    funParam : type ID
    '''

def p_inicia_fun(p):
    '''
    inicia_fun : LCURBRACKET
    '''

def p_function4(p):
    '''
    function4 : statement function4
        | empty
    '''

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

def p_assignment(p):
    '''
    assignment : id equals assignment3 SEMICOLON
    '''


def p_id(p):
    '''
    id : identifier indice_dimension
    '''

def p_identifier(p):
    '''
    identifier : ID
    '''

def p_indice_dimension(p):
    '''
    indice_dimension : LBRACKET exp RBRACKET LBRACKET exp RBRACKET
        | LBRACKET exp RBRACKET
        | empty
    '''

def p_equals(p):
    '''
    equals : EQUALS
    '''

def p_assignment3(p):
    '''
    assignment3 : exp
        | read
    '''

def p_condition(p):
    '''
    condition : SI head_condition ENTONCES body condition1
    '''

def p_head_condition(p):
    '''
    head_condition : LPAREN expression close_condition
    '''

def p_body(p):
    '''
    body : LCURBRACKET body1 RCURBRACKET
    '''

def p_body1(p):
    '''
    body1 : statement body1
        |empty
    '''
def p_condition1(p):
    '''
    condition1 : SINO body
        | empty
    '''


def p_close_condition(p):
    '''
    close_condition : RPAREN
    '''

def p_write(p):
    '''
    write : WRITE LPAREN expression RPAREN SEMICOLON
    '''

def p_expression(p):
    '''
    expression: exp loper exp
        | exp
    '''

def p_loper(p):
    '''
    loper : GREATERTHAN
        | LESSTHAN
        | GREATEREQ
        | LESSEQ
        | NOTEQUAL
        | ISEQUAL
    '''

def p_exp(p):
    '''
    exp : term
        | term exp_o exp
    '''

def p_exp_o(p):
    '''
    exp_o : PLUS
        | TIMES
    '''

def p_term(p):
    '''
    term : factor term_o term
    '''

def p_factor(p):
    '''
    factor : vcte
        | leftP expression rightP
    '''

def p_leftP(p):
    '''
    leftP : LPAREN
    '''

def p_rightP(p):
    '''
    rightP : RPAREN
    '''

def p_vcte(p):
    '''
    vcte : cte_int
        | cte_float
        | cte_string
        | id
        | funCall
        | vectorMatriz
    '''

def p_cte_int(p):
    '''
    cte_int : negativo CTEINT
    '''

def p_cte_float(p):
    '''
    cte_float : negativo CTEFLOAT
    '''

def p_cte_string(p):
    '''
    cte_string : negativo CTESTRING
    '''

def p_negativo(p):
    '''
    negativo : MINUS
        | empty
    '''

def p_vectorMatriz(p):
    '''
    vectorMatriz : LBRACKET vm1 RBRACKET
        | vm1
    '''

def p_vm1(p):
    '''
    vm1 : LBRACKET vm2 RBRACKET COMMA vm1
        | LBRACKET vm2 RBRACKET
    '''

def p_vm2(p):
    '''
    vm2 : exp COMMA vm2
        | exp
        | empty
    '''

def p_term_o(p):
    '''
    term_o : TIMES
        | DIVIDE
    '''

def p_loop(p):
    '''
    loop : mientras
        | desde
    '''

def p_mientras(p):
    '''
    mientras : mientras1 HAZ body
    '''

def p_mientras1(p):
    '''
    mientras1 : mientras_w LPAREN expression RPAREN
    '''

def p_mientras_w(p):
    '''
    mientras_w : MIENTRAS
    '''

def p_expression(p):
    '''
    expression : exp loper exp
        | exp
    '''

def p_desde(p):
    '''
    desde : nuevo_desde desdeBody
    '''

def p_nuevo_desde(p):
    '''
    nuevo_desde : DESDE id EQUALS desde2 HASTA desde2 HACER
    '''

def p_desde2(p):
    '''
    desde2: exp
    '''

def p_desdeBody(p):
    '''
    desdeBody : body
    '''

def p_read(p):
    '''
    read : LEE LPAREN id read1 RPAREN SEMICOLON
    '''

def p_read1(p):
    '''
    read1 : LBRACKET exp RBRACKET  LBRACKET exp RBRACKET
        | LBRACKET exp RBRACKET
        | empty
    '''

def p_loadData(p):
    '''
    loadData : LPAREN ID route maxVariables maxRows RPAREN SEMICOLON
    '''


def p_route(p):
    '''
    route : CTESTRING
    '''

def p_maxVariables(p):
    '''
    maxVariables : CTEINT
    '''

def p_maxRows(p):
    '''
    maxRows : CTEINT
    '''

def p_funCall(p):
    '''
    funCall : ID iniciaFunCall funCall2 terminaFunCall
    '''

def p_iniciaFunCall(p):
    '''
    iniciaFunCall : LPAREN
    '''

def p_funCall2(p):
    '''
    funCall2 : funCallParam funCall3
        | empty
    '''

def p_funcallParam(p):
    '''
    funcallParam : exp
    '''

def p_funCall3(p):
    '''
    funCall3 : COMMA funCallParam funCall3
        | empty
    '''

def p_terminaFunCall(p):
    '''
    terminaFunCall : RPAREN
    '''


def p_return(p):
    '''
    return : REGRESA return1 SEMICOLON
    '''

def p_return1(p):
    '''
    return1 : vcte
        | exp
    '''

def p_function5(p):
    '''
    function5 : COMMA funParam function5
        | empty
    '''

def p_termina_fun(p):
    '''
    termina_fun : RCURBRACKET
    '''

def p_function_v(p):
    '''
    function_v : FUNCION functionV function2 inicia_fun declara_vars function9 termina_fun
    '''


def p_functionV(p):
    '''
    functionV : VOID ID
    '''

def p_function9(p):
    '''
    function9 : stmt_v function9
        | empty
    '''

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

def p_principal(p):
    '''
    principal : principalI declara_vars principal1 RCURBRACKET
    '''

def p_principalI(p):
    '''
    principalI : principalS LCURBRACKET
    '''

def p_principalS(p):
    '''
    principalS : PRINCIPAL
    '''

def p_prncipal1(p):
    '''
    prncipal1 : smt_v principal1
        | empty
    '''

def p_empty(p):
    '''
    empty :
    '''
















