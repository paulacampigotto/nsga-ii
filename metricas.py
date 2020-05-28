
from nsga2 import *
from operadores import *
from aux import *
from globais import *
import itertools
import matplotlib.pyplot as plt
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint
import numpy as np
import timeit
from math import ceil

def retorno(ativo):
    retorno = []
    for i in range(len(ativo) -1):
        retorno.append((ativo[i+1] - ativo[i]) / ativo[i])
    return retorno

def retorno_acumulado(ativo):
    retorno = []
    for i in range(len(ativo) -1):
        if(i == 0):
            retorno.append(((ativo[i+1]  / ativo[i]) -1 )* 100)
        else:    
            retorno.append(retorno[i-1]+((ativo[i+1]  / ativo[i]) -1 )* 100)
    return retorno

def ewma(ativo):
    retornos = retorno(ativo)
    ewma_variance = []
    ewma_variance.append(abs(retornos[0]))
    for i in range(1,len(retornos)):
        ewma_variance.append((1-λ)*retornos[i] + λ*ewma_variance[i-1])
    return sum(ewma_variance)/len(ewma_variance)

def garch(ativo):
    retornos = retorno(ativo)
    garch_variance = []
    garch_variance.append(abs(retornos[0]))
    for i in range(1,len(retornos)):
        garch_variance.append(ω + ( α * abs(retornos[i]) ) + 
        ( β * abs(garch_variance[i-1]) ))
    return sum(garch_variance)/len(garch_variance)
    
def lpm(ativo):
    retornos = retorno(ativo)
    lpm_variance = []
    lpm_variance.append(abs(retornos[0]))
    for i in range(1,len(retornos)):
        lpm_variance.append(pow((min(pow(retornos[i] - τ, 0),k)),(1/k)))
    return sum(lpm_variance)/len(lpm_variance)

def cvar(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    var95 = ret_ord[ceil((1-(95/100))*total_count)]
    var99 = ret_ord[ceil((1-(99/100))*total_count)]
    var999 = ret_ord[ceil((1-(99.9/100))*total_count)]

    cvar95 = -((1/((1-(95/100))*total_count))*soma_aux(ret_ord, ceil((1-(95/100))*total_count)))
    cvar99 = -((1/((1-(99/100))*total_count))*soma_aux(ret_ord, ceil((1-(99/100))*total_count)))
    cvar999 = -((1/((1-(99.9/100))*total_count))*soma_aux(ret_ord, ceil((1-(99.9/100))*total_count)))

    return [(cvar95), (cvar99), (cvar999)]
