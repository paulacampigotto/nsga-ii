from globais import *
from aux import *
from nsga2 import *
import random
import copy
from math import ceil

def crossover():
    pop = copy.copy(eleicao(populacao))
    novaPop = []
    #seleciona os pais
    for i in range(ceil(TAM_POP/2)):
        while True:
            probabilidade = random.random()
            carteira = pop[random.randint(0,TAM_POP-1)]
            if(probabilidade <= (carteira.fitness()/pop[TAM_POP-1].fitness())):
                # print("primeira carteira: ")
                # carteira.printCarteira()
                pai1 = copy.copy(carteira)
                while True:
                    probabilidade = random.random()
                    carteira = pop[random.randint(0,TAM_POP-1)]
                    if(probabilidade <= (carteira.fitness()/pop[TAM_POP-1].fitness())):
                        if(pai1.getId() != carteira.getId()):
                            # print("segunda carteira: ")
                            # carteira.printCarteira()
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
        
        # print(ativosFilho1)
        filho1 = Carteira(ativosFilho1) 
        filho2 = Carteira(ativosFilho2) 
        print("pai1 ")
        pai1.printCarteira()
        print("pai2")
        pai2.printCarteira()
        print("filho1 ")
        filho1.printCarteira()
        print("filho2")
        filho2.printCarteira()

        pop.append(filho1)
        pop.append(filho2)
    
    pop = eleicao(pop).copy()



    for i in range(len(pop)-1, (len(pop)//2)-1, -1):
        novaPop.append(pop[i])

    # for i in novaPop:
    #     print(i.printCarteira())

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


def eleicao(pop):
    pop_ord = sorted(pop,key=getKey)
    return pop_ord



