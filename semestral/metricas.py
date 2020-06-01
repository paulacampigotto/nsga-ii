
from nsga2 import *
from operadores import *
from aux import *
from globais import *
from grafico import *
from os import listdir
from os.path import isfile, join
from pprint import pprint
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random
import timeit

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

def var(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    var95 = ret_ord[ceil((1-(95/100))*total_count)]
    var99 = ret_ord[ceil((1-(99/100))*total_count)]
    var999 = ret_ord[ceil((1-(99.9/100))*total_count)]

    return [(-var95), (-var99), (-var999)]
    

def soma_aux(retorno, indice):
    s = 0
    for i in range(indice):
        s+= retorno[i]
    return s

def cvar(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    cvar95 = -((1/((1-(95/100))*total_count))*soma_aux(ret_ord, ceil((1-(95/100))*total_count)))
    cvar99 = -((1/((1-(99/100))*total_count))*soma_aux(ret_ord, ceil((1-(99/100))*total_count)))
    cvar999 = -((1/((1-(99.9/100))*total_count))*soma_aux(ret_ord, ceil((1-(99.9/100))*total_count)))

    return [(cvar95), (cvar99), (cvar999)]


def metrica_risco(lista_ativos, valor):

    #calcula o risco e o retorno de cada ativo e atualiza os valores de listaAtivos
    for i in lista_ativos:
        if(valor == 0):
            ris = cvar(i.getCotacoes())[1] #[0] = CVaR 95% | [1] = CVaR 99% | [2] = CVaR 99.9%
        elif(valor == 1):
            ris = var(i.getCotacoes())[1]
        elif(valor == 2):
            ris = ewma(i.getCotacoes())
        elif(valor == 3):
            ris = garch(i.getCotacoes())
        elif(valor == 4):
            ris = lpm(i.getCotacoes())
        i.setRisco(ris)
        ret = sum(retorno(i.getCotacoes()))/len(i.getCotacoes())
        i.setRetorno(ret)

    return lista_ativos