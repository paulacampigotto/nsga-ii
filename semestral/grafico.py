from operadores import *
from aux import *
from globais import *
from metricas import *
from nsga2 import *
from os import listdir
from os.path import isfile, join
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import timeit
import copy

def grafico_tempo(carteiras, lista_ativos_proximo_semestre, lista_ibovespa_proximo_semestre):
 
    cotacoes = []
    for i in carteiras:
        cotacoes.append(calcula_cotacoes_carteira_prox_semestre(i, lista_ativos_proximo_semestre))
    
    plt.plot(range(len(retorno_acumulado(cotacoes[0]))),retorno_acumulado(cotacoes[0]),linestyle = 'solid', color = '#6f6fa3', label = 'CVaR')
    plt.plot(range(len(retorno_acumulado(cotacoes[1]))),retorno_acumulado(cotacoes[1]), linestyle = (0, (3, 1, 1, 1)), color = '#ff66c7', label = 'VaR')
    plt.plot(range(len(retorno_acumulado(cotacoes[2]))),retorno_acumulado(cotacoes[2]), linestyle = 'dashdot',color = '#c457ff', label = 'EWMA')
    plt.plot(range(len(retorno_acumulado(cotacoes[3]))),retorno_acumulado(cotacoes[3]), linestyle = 'dashed', color = 'red', label = 'GARCH')
    plt.plot(range(len(retorno_acumulado(cotacoes[4]))),retorno_acumulado(cotacoes[4]), linestyle = 'dotted',color = '#66c2ff', label = 'LPM')
    
    plt.plot(range(len(retorno_acumulado(lista_ibovespa_proximo_semestre))), retorno_acumulado(lista_ibovespa_proximo_semestre), color = 'black', label = 'Ibovespa')
    plt.legend()
    plt.xlabel('Tempo')
    plt.ylabel('Retorno acumulado (%)')
    plt.title("Retorno Acumulado")
    plt.savefig('graficos/MelhorCarteira.png')
    plt.show()

def encontraIndexAtivo(codigo_ativo, lista):
    index = 0
    for i in lista:
        if(i.getCodigo() == codigo_ativo):
            return index
        index += 1

def calcula_cotacoes_carteira_prox_semestre(carteira, lista):
    numero_cotacoes = len(lista[0].getCotacoes())
    matriz = []
    for i in range(carteira.cardinalidade()):
        matriz.append([0]*numero_cotacoes)

    for index_ativo in range(carteira.cardinalidade()):
        ativo = carteira.getAtivoPeloIndex(index_ativo)
        for cotacao in range(numero_cotacoes):
            matriz[index_ativo][cotacao] +=  lista[encontraIndexAtivo(ativo[0].getCodigo(), lista)].getCotacoes()[cotacao] * ativo[1]

    y = [0]*numero_cotacoes
    for i in range(numero_cotacoes):
        for ativo in range(len(matriz)):
            y[i] += matriz[ativo][i]
            
    return y


def grafico_tempo_barras(carteiras_semestre, lista_ativos_proximo_semestre):
    
    cotacoes_por_semestre = []
    
    for semestre in range(len(carteiras_semestre)):
        cotacoes_por_semestre.append([])
        for carteira in carteiras_semestre[semestre]:
            cotacoes_por_semestre[semestre].append(calcula_cotacoes_carteira_prox_semestre(carteira, lista_ativos_proximo_semestre))
    
    retorno_acumulado_por_semestre = []
    
    semestre = 0
    for cotacoes in cotacoes_por_semestre:
        retorno_acumulado_por_semestre.append([])
        for cotacao in cotacoes:
            ret = retorno_acumulado(cotacao)
            retorno_acumulado_por_semestre[semestre].append(ret[len(ret) - 1])
        semestre += 1
    
    retornos_por_risco = []
    cont = 0

    for i in range(len(retorno_acumulado_por_semestre[cont])):
        retornos_por_risco.append([])
        for j in retorno_acumulado_por_semestre:
            retornos_por_risco[cont].append(j[i])
        cont+=1

    for i in retornos_por_risco:
        print(i)

    n_groups = len(carteiras_semestre)


    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8

    rects1 = plt.bar(index, retornos_por_risco[0], bar_width,
    alpha=opacity,
    color='g',
    label='CVaR')

    rects2 = plt.bar(index + bar_width, retornos_por_risco[1], bar_width,
    alpha=opacity,
    color='purple',
    label='VaR')

    rects2 = plt.bar(index + bar_width*2 , retornos_por_risco[2], bar_width,
    alpha=opacity,
    color='b',
    label='EWMA')

    rects2 = plt.bar(index + bar_width*3, retornos_por_risco[3], bar_width,
    alpha=opacity,
    color='r',
    label='GARCH')
    
    rects2 = plt.bar(index + bar_width*4, retornos_por_risco[4], bar_width,
    alpha=opacity,
    color='k',
    label='LPM')

    plt.xlabel('Tempo (semestre)')
    plt.ylabel('Retorno acumulado')
    plt.title('Retorno acumulado por semestre das métricas')
    plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6'))
    plt.legend()

    plt.tight_layout()
    plt.show()