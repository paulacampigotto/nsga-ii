from globais import *
from aux import *
from nsga2 import *
import random
import copy
from math import ceil
import sys

def crossover(populacao):
    pop = (eleicao(populacao)).copy()
    novaPop = []
    #seleciona os pais
    for i in range(ceil(len(pop)/2)):
        while True:
            # print("1")
            probabilidade = random.random()
            carteira = pop[random.randint(0,len(pop)-1)]
            if(probabilidade <= (carteira.fitness()/pop[len(pop)-1].fitness())):
                pai1 = copy.copy(carteira)
                contt = 0
                while True:
                    contt+=1
                    # print("2")
                    probabilidade = random.random()
                    carteira = pop[random.randint(0,len(pop) - 1)]
                    # print("prob: ", probabilidade)
                    # print("primeiro: ", carteira.fitness())
                    if(pop[len(pop) - 1].fitness() < 0):
                        print("segundo: ", pop[len(pop) - 1].fitness())
                        print(contt)
                    # print("fitness: ", carteira.fitness()/pop[len(pop) - 1].fitness())
                    if(probabilidade <= (carteira.fitness()/pop[len(pop) - 1].fitness())):
                        if(pai1.getId() != carteira.getId()):
                            pai2 = copy.copy(carteira)
                            break
                break
                
        # cria os filhos

        ativosFilho1 = []
        ativosFilho2 = []

        probabilidade = random.random()
        for j in range(CARDINALIDADE):
            ativosFilho1.append((pai1.getAtivos()[j][0],pai1.getProporcao(j) * probabilidade + pai2.getProporcao(j) * (1-probabilidade)))
            ativosFilho2.append((pai2.getAtivos()[j][0],pai2.getProporcao(j) * probabilidade + pai1.getProporcao(j) * (1-probabilidade)))
        
        filho1 = Carteira(ativosFilho1) 
        filho2 = Carteira(ativosFilho2) 

        pop.append(filho1)
        pop.append(filho2)
    

    return pop

def mutacao(populacao):
    for carteira in populacao:
        index1 = 0
        for ativo in carteira.getAtivos():
            probabili = random.random()
            if (probabili <= 0.1):
                prob = random.random() # mutar proporção ou ativo
                if(prob < 0.5):
                    r = random.uniform(0,ativo[1]) #gera um valor r aleatório para ser subtraído da proporção atual
                    carteira.setAtivoPeloIndex(index1, (ativo[0], ativo[1]-r))
                    novoAtivo2 = random.choice(carteira.getAtivos())
                    index2 = carteira.getIndexPeloAtivo(novoAtivo2)
                    carteira.setAtivoPeloIndex(index2, (novoAtivo2[0], novoAtivo2[1]+r))
                else:
                    novoAtivo1 = random.choice(listaAtivos) #gera um ativo novoAtivo1 para substituir o ativo atual
                    carteira.setAtivoPeloIndex(index1, (novoAtivo1, ativo[1]))

            index1+=1
    return populacao


def eleicao(pop):
    pop_ord = sorted(pop,key=fitnessKey)
    return pop_ord


def domina(carteira1, carteira2): #verificar condições de dominância
    if(carteira1.getRisco() < carteira2.getRisco() and carteira1.getRetorno() > carteira2.getRetorno()):
            return True
    return False


def nds(pop):
    popu = pop.copy()
    fronteira = [[]]
    for p in popu:
        p.setContador_n(0)
        for q in popu:
            if p != q:
                if domina(p,q):
                    p.appendDominadas(q)
                else:
                    if(domina(q,p)):
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

        if(len(fronteira) == i):
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

def filtragem(populacao_entrada):
    pop = populacao_entrada.copy()
    p = len(pop)//2
    fronteiras = nds(pop)
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