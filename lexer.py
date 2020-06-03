import  ply.lex as lex
import sys

keywords = {
    'programa' : 'PROGRAMA',
    'var' : 'VAR',
    'int' : 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'string': 'STRING',
    'dataframe' : 'DATAFRAME',
    'funcion' : 'FUNCION',
    'si' : 'SI',
    'entonces' : 'ENTONCES',
    'regresa' : 'REGRESA',
    'sino' : 'SINO',
    'void' : 'VOID',
    'mientras' : 'MIENTRAS',
    'haz' : 'HAZ',
    'principal' : 'PRINCIPAL',
    'lee' : 'LEE',
    'inicia' : 'INICIA',
    'desde' : 'DESDE',
    'hasta' : 'HASTA',
    'hacer' : 'HACER',
    'cargaArchivo' : 'CARGAARCHIVO',
    'Variables' : 'VARIABLES',
    'escribe' : 'ESCRIBE',
    'Media' : 'MEDIA',
    'Moda' : 'MODA',
    'Varianza' : 'VARIANZA',
    'Correlacion' : 'CORRELACION',
    'lineal' : 'LINEAL',
    'histograma' : 'HISTOGRAMA'
}

tokens = [
    'ID',
    'COLON',
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
    'CTECHAR',
    'CTESTRING',
    'LESSTHAN',
    'GREATERTHAN',
    'LESSEQ',
    'GREATEREQ',
    'AND',
    'OR',
    'ISEQUAL',
    'NOTEQUAL',
    'COMMENT'
]+list(keywords.values())

t_COLON = r'\:'
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
t_GREATERTHAN = r'\>'
t_LESSEQ = r'\<='
t_GREATEREQ = r'\>='
t_AND = r'\&'
t_OR = r'\|'
t_ISEQUAL = r'\=='
t_NOTEQUAL = r'\!='
t_COMMENT = r'\%%'

t_ignore = ' \t'

def t_CTEFLOAT(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r"'[a-zA-Z]'"
    t.value = str(t.value)
    return t

def t_CTESTRING(t):
    r"(\"([^\\\"]|\\.)+\")|(\'([^\\\']|\\.)+\')"
    t.value = str(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_COMMENT (t):
    r'\%%.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

##############################
# PRUEBA CON CÓDIGO DE EJEMPLO
#
# data ='''
# programa Covid19;
# var
#     float number;
#     number = 1.5;
#     int i,j,p, maxVariables, maxRenglones;
#     int valor, Arreglo[10], OtroArreglo[10]
#     dataframe DatosCovid;
#     string VarCovid[100];
#
# funcion int fact (int j)
# var int i;
# {
#     i = j + (p- j*2 +j);
#     si (j == 1) entonces
#     {
#         regresa (j);
#     }
#     sino
#     {
#         regresa (j * fact(j-1));
#     }
# }
#
# funcion void inicia (int y)
# var int x;
# {
#     x=0;
#     mientras (x<11) haz
#     {
#         Arreglo[x] = y * x;
#         x = x+1;
#     }
# }
#
# principal ()
# {
#     lee (p); j = p*2;
#     inicia (p*j -5);
#     desde i = 0 hasta 9 hacer
#     {
#         Arreglo [i] = Arreglo[i] * fact (Arreglo[i]-p);
#     }
#     cargaArchivo (DatosCovid, "C://Documentos/Covid.txt", maxVariables, maxRenglones);
#     variables (DatosCovid, VarCovid, maxVariables);
#     desde k = 0 hasta maxVariables hacer
#     {
#         valor = Media (DatosCovid, variables[k]);
#         escribe ("Media para la Variable", variables[k], valor);
#     }
#     escribe ("Indice de correlacion entre variable 1 y variable 5 de la muestra", Correlaciona (DatosCovid, variables[1], variables[5]));
#     mientras (i>=0)
#     {
#         escribe ("resultado", Arreglo[i], fact(i+2)*valor);
#         i = i-1;
#     }
# }
# '''
#
# lexer.input(data)
# while True:
#     tok = lexer.token()
#     if not tok : break
#     print(tok)

