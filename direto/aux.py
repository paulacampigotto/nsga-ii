from globais import *
from nsga2 import *
from operadores import *
from metricas import *
from os.path import isfile, join
from os import listdir
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random
import timeit

def pesoProporcional(carteira,i):
    soma = 0.0

    for j in range(len(carteira)):
        soma+=carteira[j][1]

    if(i == CARDINALIDADE-1):
        return 1- soma

    elif(i==0):
        p = random.uniform(0, 0.2)
        return p

    else:
        p = random.uniform(0, 1 - soma)
        return p

def ativo_aux(carteira):
    while True:
        flag = True
        aleatorio = random.randint(0,QUANTIDADE_ATIVOS -1)
        for i in carteira:
            if i[0] == aleatorio:
                flag = False
                break
        if flag:
            return aleatorio
                      
def soma_aux(retorno, indice):
    s = 0
    for i in range(indice):
        s+= retorno[i]
    return s

def fitnessKey(x):
    return x.fitness()

def retornoKey(x):
    return x.getRetorno()

def riscoKey(x):
    return x.getRisco()

def printPopulacao(pop):
    for carteira in pop:
        carteira.printCarteira()
        print()

def seleciona_dois_ativos(populacao):
    a = random.choice(populacao)
    while(True):
        b = random.choice(populacao)
        if(a.getId() != b.getId()):
            return a,b

def eleicao(pop):
    pop_ord = sorted(pop,key=fitnessKey)
    return pop_ord

def domina(carteira1, carteira2): #verificar condições de dominância
    if(carteira1.getRisco() < carteira2.getRisco() and carteira1.getRetorno() > carteira2.getRetorno()):
            return True
    return False

def melhor_carteira(pop):
    melhor = pop[0]
    for carteira in pop:
        if carteira.fitness() > melhor.fitness():
            melhor = carteira
    return carteira


def calcula_cotacoes_carteira_2015_2018(carteira):
    numero_cotacoes = len(carteira.getAtivoPeloIndex(0)[0].getCotacoes())
    print(numero_cotacoes)
    matriz = []
    for i in range(carteira.cardinalidade()):
        matriz.append([0]*numero_cotacoes)

    for ativo in range(carteira.cardinalidade()):
        for cotacao in range(numero_cotacoes):
            matriz[ativo][cotacao] +=  carteira.getAtivoPeloIndex(0)[0].getCotacoes()[cotacao] * carteira.getAtivoPeloIndex(ativo)[1]

    y = [0]*numero_cotacoes
    for i in range(numero_cotacoes):
        for ativo in range(len(matriz)):
            y[i] += matriz[ativo][i]
            
    return y

def encontraIndexAtivo(codigo_ativo):
    global listaAtivos_2019
    index = 0
    for i in listaAtivos_2019:
        if(i.getCodigo() == codigo_ativo):
            return index
        index += 1
        

def calcula_cotacoes_carteira_2019(carteira):
    global listaAtivos_2019
    numero_cotacoes = len(listaAtivos_2019[0].getCotacoes())
    # print(numero_cotacoes)
    matriz = []
    for i in range(carteira.cardinalidade()):
        matriz.append([0]*numero_cotacoes)

    for index_ativo in range(carteira.cardinalidade()):
        ativo = carteira.getAtivoPeloIndex(index_ativo)
        for cotacao in range(numero_cotacoes):
            matriz[index_ativo][cotacao] +=  listaAtivos_2019[encontraIndexAtivo(ativo[0].getCodigo())].getCotacoes()[cotacao] * ativo[1]

    y = [0]*numero_cotacoes
    for i in range(numero_cotacoes):
        for ativo in range(len(matriz)):
            y[i] += matriz[ativo][i]
            
    return y


def grafico_risco_retorno(x,y,nome):
    
    plt.scatter(x, y, marker = '*', color = '#ff66c7')
    plt.axis([min(x), max(x), min(y), max(y)])
    plt.xlabel('Risco')
    plt.ylabel('Retorno')
    plt.title(nome)
    plt.savefig("graficos/"+nome + '.png')
    plt.show()

def escolhe_ativo(carteira):
    verifica = True# 
    while(verifica):
        novoAtivo1 = random.choice(listaAtivos_2015_2018) #gera um ativo novoAtivo1 para substituir o ativo atual
        for i in carteira.getAtivos():
            if i[0].getCodigo() == novoAtivo1.getCodigo():
                verifica = False
        if verifica:
            return novoAtivo1
        else:
            verifica = True