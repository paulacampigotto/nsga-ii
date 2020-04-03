from globais import *
from aux import *
import random
from math import ceil

def crossover(pop):
    novaPop = []
    #seleciona os pais
    for i in range(ceil(TAM_POP/2)):
        while True:
            probabilidade = random.random()
            carteira = random.randint(0,len(pop)-1)
            if(probabilidade <= (pop[carteira][1]/pop[0][1])):
                indicePai1 = pop[carteira]
                pop.remove(pop[carteira]) #Estamos removendo a carteira da população geral
                while True:
                    probabilidade = random.random()
                    carteira = random.randint(0,len(pop)-1)
                    if(probabilidade <= (pop[carteira][1]/pop[0][1])):
                        indicePai2 = pop[carteira]
                        pop.remove(pop[carteira]) #Estamos removendo a carteira da população geral
                        break
                break

        # cria os filhos


        filho1 = populacao[indicePai1[0]]
        filho2 = populacao[indicePai2[0]]


        probabilidade = random.random()
        for j in range(CARDINALIDADE):
            filho1.setProporcao(j, (filho1.getProporcao(j) * probabilidade + filho2.getProporcao(j) * (1-probabilidade)))
            filho2.setProporcao(j, (filho2.getProporcao(j) * probabilidade + filho1.getProporcao(j) * (1-probabilidade)))
       
        novaPop.append(filho1)
        novaPop.append(filho2)
        

    return novaPop


def mutacao(novaPop):
    for i in novaPop:
        randomm = random.random()
        flag = False
        if(randomm < 0.1):
            while(flag == False):
                randInd1 = random.randint(0,len(novaPop)-1)
                randInd2 = random.randint(0,len(novaPop)-1)
                randomsum = 1-randomm
                randomAtivo = novaPop[randInd1][1]
                if novaPop[randInd2][1] - randomm > 0.0:
                    novaPop[randInd1][1] = randomm
                    novaPop[randInd2][1] = randomm - novaPop[randInd2][1] + randomsum
                    flag = True


# eleicao() = lista de (indice da carteira, retorno sobre risco)
def eleicao():
    global populacao
    populacaoOrdenada = []
    for i in populacao:
        populacaoOrdenada.append((i.getId(),i.getTaxaRetornoRisco())) #retorno sobre risco
    return sorted(populacaoOrdenada,key=getKey)
