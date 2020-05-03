import  ply.lex as lex
import sys

keywords = {
    'programa' : 'PROGRAMA',
    'var' : 'VAR',
    'int' : 'INT',
    'dataframe' : 'DATAFRAME',
    'string' : 'STRING',
    'char' : 'CHAR',
    'function' : 'FUNCION',
    'si' : 'SI',
    'entonces' : 'ENTONCES',
    'regresa' : 'REGRESA',
    'sino' : 'SINO',
    'void' : 'VOID',
    'mientras' : 'MIENTRAS',
    'principal' : 'PRINCIPAL',
    'lee' : 'LEE',
    'inicia' : 'INICIA',
    'desde' : 'DESDE',
    'hasta' : 'HASTA',
    'hacer' : 'HACER',
    'cargaarchivo' : 'CARGAARCHIVO',
    'variables' : 'VARIABLES',
    'escribe' : 'ESCRIBE',
    'correlacion' : 'CORRELACION'
}

tokens = [
    'ID',
    'SEMICOLON',
    'COMMA',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'LCURBRACKET',
    'RCURBRACKET',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'CTEINT',
    'CTEFLOAT',
    'CTESTRING',
    'LESSTHAN',
    'GREATHERTHAN',
    'AND',
    'OR',
    'ISEQUAL',
    'NOTEQUAL',
    'QUOTES',
    'RQUOTES',
    'COMMENT'
]+list(keywords.values())


t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURBRACKET = r'\{'
t_RCURBRACKET = r'\}'
t_EQUALS = r'\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LESSTHAN = r'\<'
t_GREATHERTHAN = r'\>'
t_AND = r'\&'
t_OR = r'\|'
t_ISEQUAL = r'\=='
t_NOTEQUAL = r'\!='
t_QUOTES = r'\"'
t_COMMENT = r'\%%'

t_ignore = r' '

def t_CTEFLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    # r'"[a-zA-Z][a-zA-Z_0-9]*"'
    r'\"(\\.|[^"\\])*\"'
    t.value = str(t.value)
    return t


#def t_INT(t):
#    r'\d+'
#    t.value = int(t.value)
#    return t

#def t_FLOAT(t):
#    r'\d\.\d+'
#    t.value = float(t.value)
#    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print('Illegal characters!')
    t.lexer.skip(1)


lexer = lex.lex()
lexer.input(""""
a = 1+2
""")

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)