import  ply.lex as lex

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
    'LESSTHAN',
    'GREATHERTHAN',
    'AND',
    'OR',
    'ISEQUAL',
    'NOTEQUAL',
    'LQUOTES',
    'RQUOTES',
    'COMMENT'
]

keywords = [
    'PROGRAMA',
    'VAR',
    'INT',
    'DATAFRAME',
    'STRING',
    'CHAR',
    'FUNCION',
    'SI',
    'ENTONCES',
    'REGRESA',
    'SINO',
    'VOID',
    'MIENTRAS',
    'PRINCIPAL',
    'LEE',
    'INICIA',
    'DESDE',
    'HASTA',
    'HACER',
    'CARGAARCHIVO',
    'VARIABLES',
    'ESCRIBE',
    'CORRELACION'
]

tokens += keywords

t_SEMICOLON = r'\;'
t_COMMA = r','
t_LBRACKET = r'['
t_RBRACKET = r']'
t_LPAREN = r'('
t_RPAREN = r')'
t_LCURBRACKET = r'{'
t_RCURBRACKET = r'}'
t_EQUALS = r'='
t_PLUS = r'+'
t_MINUS = r'-'
t_TIMES = r'*'
t_DIVIDE = r'/'
t_LESSTHAN = r'<'
t_GREATHERTHAN = r'>'
t_AND = r'&'
t_OR = r'|'
t_ISEQUAL = r'=='
t_NOTEQUAL = r'!='
t_LQUOTES = r'"'
t_COMMENT = r'%%'

