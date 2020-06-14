import operadores as operadores
from aux import *
import grafico as grafico
from globais import *
import metricas as metricas
from classes import *
from os import listdir
from os.path import isfile, join
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import timeit
import copy
import sys


def otimiza(populacao_filtrada, lista_ativos):
    # global populacao
    popCrossover = crossover(populacao_filtrada)
    populacaoMutada = mutacao(popCrossover, lista_ativos)
    return filtragem(populacaoMutada, False).copy()

def populacao_inicial(lista_ativos):
    populacao = []
    for j in range(TAM_POP):
        carteira = []
        for i in range(CARDINALIDADE):
            ativo = (lista_ativos[aux.ativo_aux(carteira)], 1/CARDINALIDADE) ##### satisfazer a soma dos pesos = 1
            carteira.append(ativo)
        populacao.append(Carteira(carteira))
    return populacao

def crossover(pop):
    pares = selecao(pop)
    novaPop = []
    novaPop = copy.copy(pop)
    

    for par in pares:
        pai1 = copy.copy(par[0])
        pai2 = copy.copy(par[1])
        probabilidade = random.random()
        ativosFilho1 = []
        ativosFilho2 = []
        for j in range(CARDINALIDADE): #percorre a carteira j da população

            ativosFilho1.append((pai1.getAtivos()[j][0],pai1.getProporcao(j) * 
            probabilidade + pai2.getProporcao(j) * (1-probabilidade)))

            ativosFilho2.append((pai2.getAtivos()[j][0],pai2.getProporcao(j) * 
            probabilidade + pai1.getProporcao(j) * (1-probabilidade)))

        filho1 = Carteira(ativosFilho1)  
        filho2 = Carteira(ativosFilho2) 
        novaPop.append(filho1)
        novaPop.append(filho2)  
    
    return novaPop

def mutacao(pop, lista_ativos):
    for carteira in pop:
        index1 = 0
        for ativo in carteira.getAtivos():
            probabili = random.random()
            if (probabili <= PROBABILIDADE_MUTACAO):
                prob = random.random() # mutar proporção ou ativo
                if(prob < 0.5):
                    novoAtivo2 = random.choice(carteira.getAtivos())
                    index2 = carteira.getIndexPeloAtivo(novoAtivo2)
                    while(True):
                        r = random.uniform(0,ativo[1]) #gera um valor r aleatório para ser subtraído da proporção atual
                        if(r + novoAtivo2[1] <= PROPORCAO_MAXIMA_CARTEIRA):
                            break
                    carteira.setAtivoPeloIndex(index1, (ativo[0], ativo[1]-r))
                    carteira.setAtivoPeloIndex(index2, (novoAtivo2[0], novoAtivo2[1]+r))
                else:
                    novoAtivo1 = aux.escolhe_ativo(carteira, lista_ativos)
                    carteira.setAtivoPeloIndex(index1, (novoAtivo1, ativo[1]))
            index1+=1
            
    return pop

def selecao(pop):
    popu = pop.copy()
    pares = []
    p_a = []
    p_b = []
    tam = len(pop)
    qtd_pares = tam//2
    for i in range(qtd_pares):
        ind_a, ind_b = aux.seleciona_dois_ativos(popu)
        if ind_a.getRank() < ind_b.getRank():
            p_a = copy.copy(ind_a)
        else: 
            p_a = copy.copy(ind_b)
        for k in popu:
            if k.getId() == p_a.getId():
                popu.remove(k)
        ind_c, ind_d = aux.seleciona_dois_ativos(popu)
        
        if ind_c.getRank() < ind_d.getRank():
            p_b = copy.copy(ind_c)
        else:
            p_b = copy.copy(ind_d)
        pares.append((p_a,p_b))

    return pares   

def nds(popu):
    fronteira = [[]]
    for p in popu:
        p.setContador_n(0)
        for q in popu:
            if p != q:
                if aux.domina(p,q):
                    p.appendDominadas(q)
                else:
                    if(aux.domina(q,p)):
                        p.setContador_n(p.getContador_n() + 1)
        if p.getContador_n() == 0:
            p.setRank(1)
            fronteira[0].append(p)

    i = 0
    while(fronteira[i]):
        Q = []
        for p in fronteira[i]:
            for q in p.getDominadas():
                q.setContador_n(q.getContador_n() - 1)
                if q.getContador_n() == 0:
                    q.setRank(i+1)
                    Q.append(q)
        i+=1
        fronteira.append([])
        fronteira[i] = Q.copy()
        
    return fronteira

def crowding_distance(fronteira):
    n = len(fronteira)
    pop_ord = []
    for i in fronteira:
        i.setDist_crowd(0)
    
    for m in range (2):
        if m == 1:
            pop_ord = sorted(fronteira,key=retornoKey)
            # for i in pop_ord:
            pop_ord[0].setDist_crowd(sys.maxsize)
            pop_ord[n-1].setDist_crowd(sys.maxsize)
            for j in range(1, n-2, 1):
                pop_ord[j].setDist_crowd(pop_ord[j].getDist_crowd() + 
                (pop_ord[j+1].getDist_crowd() - pop_ord[j-1].getDist_crowd())/(pop_ord[n-1].getRetorno() - pop_ord[0].getRetorno()))
        
        else:
            pop_ord = sorted(fronteira, key=riscoKey)
            pop_ord[0].setDist_crowd(sys.maxsize)
            pop_ord[n-1].setDist_crowd(sys.maxsize)
            for j in range(1, n-2, 1):
                pop_ord[j].setDist_crowd(pop_ord[j].getDist_crowd() + 
                (pop_ord[j+1].getDist_crowd() - pop_ord[j-1].getDist_crowd())/(pop_ord[n-1].getRisco() - pop_ord[0].getRisco()))
    
    return pop_ord

def filtragem(populacao_entrada, primeira_iteracao):
    pop = copy.copy(populacao_entrada)
    if primeira_iteracao:
        p = len(pop) 
    else:        
        p = len(pop)//2
    fronteiras = nds(pop)
    fronteiras.pop(len(fronteiras) - 1)
    pop_linha = []
    i = 0
    cont = 0
    while(True):
        tam = len(fronteiras[i])
        if(tam + cont < p):
            pop_linha.append(fronteiras[i])
            cont += tam
        else:
            aux = crowding_distance(fronteiras[i])
            pop_linha.append(aux[0:p-cont])
            cont += (p-cont)
        i += 1
        if(cont == p):
            break

    pop = []
    for i in pop_linha:
        for j in i:
            pop.append(j)

    return pop
