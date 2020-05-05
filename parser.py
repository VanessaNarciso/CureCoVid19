import ply.yacc as yacc
from lexer import tokens
from sys import stdin
import sys


def p_programa(p):
    '''
    programa :  PROGRAMA ID SEMICOLON declara_vars declara_fun principal
    '''
    #p[0] = p[1]
    print('programa')
