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
import math

def grafico_tempo(carteiras, lista_ativos_proximo_semestre, lista_ibovespa_proximo_semestre):
 
    cotacoes = []
    for i in carteiras:
        cotacoes.append(calcula_cotacoes_carteira_prox_semestre(i, lista_ativos_proximo_semestre))
    
    plt.plot(range(len(retorno_acumulado(cotacoes[0]))),retorno_acumulado(cotacoes[0]),linestyle = 'solid', color = '#66ff66', label = 'CVaR')
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


def desvio_padrao(lista):
    n = len(lista)
    media = sum(lista)/n
    cont = 0
    for i in lista:
        cont += (abs(i - media))**2
    cont/=n
    cont = math.sqrt(cont)
    return cont

def grafico_tempo_barras(carteiras_semestre, lista_ativos_proximo_semestre, lista_ativos_ibovespa):
    
    cotacoes_por_semestre = []
    
    #percorre os semestres (6)
    for semestre in range(len(lista_ativos_proximo_semestre)):
        cotacoes_por_semestre.append([])
        #percorre as carteiras (5)
        for carteira in range(len(carteiras_semestre)):
            cotacoes_por_semestre[semestre].append(calcula_cotacoes_carteira_prox_semestre(carteiras_semestre[carteira], lista_ativos_proximo_semestre[semestre]))
    

    retorno_acumulado_por_semestre = []

    #SEPARA EM UMA LISTA DE SEMESTRES
    index = 0
    for semestre in cotacoes_por_semestre:
        retorno_acumulado_por_semestre.append([])
        contRisco = 0
        for risco in semestre:
            if(index >= len(cotacoes_por_semestre)-1):
                ret = retorno_acumulado(risco)
                retorno_acumulado_por_semestre[index].append(ret[len(ret) - 1])
            else:    
                ret = retorno_acumulado_barras(risco, cotacoes_por_semestre[index+1][contRisco][0])
                retorno_acumulado_por_semestre[index].append(ret[len(ret) - 1])
            contRisco += 1
        index += 1
    
    #SEPARA EM UMA LISTA DE METRICAS DE RISCO
    retornos_por_risco = []
    cont = 0
    for i in range(len(retorno_acumulado_por_semestre[cont])):
        retornos_por_risco.append([])
        for j in retorno_acumulado_por_semestre:
            retornos_por_risco[cont].append(j[i])
        cont+=1
    
    #SALVA EM ARQUIVO O RETORNO ACUMULADO DE TODOS OS SEMESTRES
    lista_soma_acumulada = []
    lista_desvio_padrao = []
    for semestre in retornos_por_risco:
        lista_soma_acumulada.append(sum(semestre))
        lista_desvio_padrao.append(desvio_padrao(semestre))

    
    arquivo = open("retorno_acumulado.txt", "w+")
    cont = 0
    for i in lista_soma_acumulada:
        if(cont == len(lista_soma_acumulada) - 1):
            arquivo.write(str(i) + "," + str(lista_desvio_padrao[cont]))
        else:
            arquivo.write(str(i) + "," + str(lista_desvio_padrao[cont]) + ",")
        cont+=1
    arquivo.close()    
    
                
    n_groups = len(lista_ativos_proximo_semestre)
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.5

    rects1 = plt.bar(index, retornos_por_risco[0], bar_width,
    alpha=opacity,
    color='#cccccc',
    label='CVaR', hatch= "///")

    rects2 = plt.bar(index + bar_width, retornos_por_risco[1], bar_width,
    alpha=opacity,
    color='#808080',
    label='VaR', hatch= "..")

    rects2 = plt.bar(index + bar_width*2 , retornos_por_risco[2], bar_width,
    alpha=opacity,
    color='#999999',
    label='EWMA', hatch= "xx")

    rects2 = plt.bar(index + bar_width*3, retornos_por_risco[3], bar_width,
    alpha=opacity,
    color='#666666',
    label='GARCH', hatch= "--")
    
    rects2 = plt.bar(index + bar_width*4, retornos_por_risco[4], bar_width,
    alpha=opacity,
    color='#333333',
    label='LPM', hatch= "")
    
    plt.xlabel('Tempo (semestre)')
    plt.ylabel('Retorno acumulado')
    plt.title('Retorno acumulado direto')
    plt.xticks(index + bar_width+.15, ['1', '2', '3', '4', '5', '6'])
    plt.legend()

    plt.tight_layout()
    plt.savefig('graficos/MelhorCarteiraSemestre.png')
    plt.show()


def grafico_risco_retorno(x,y,nome):
    
    plt.scatter(x, y, marker = '*', color = '#ff66c7')
    plt.axis([min(x), max(x), min(y), max(y)])
    plt.xlabel('Risco')
    plt.ylabel('Retorno')
    plt.title(nome)
    plt.savefig("graficos/"+nome + '.png')
    plt.show()


