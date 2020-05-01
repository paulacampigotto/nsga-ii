from globais import *
from aux import *
from nsga2 import *
import random
import copy
from math import ceil

def crossover(populacao):
    pop = copy.copy(eleicao(populacao))
    novaPop = []
    #seleciona os pais
    for i in range(ceil(TAM_POP/2)):
        while True:
            print("1")
            probabilidade = random.random()
            carteira = pop[random.randint(0,TAM_POP-1)]
            if(probabilidade <= (carteira.fitness()/pop[TAM_POP-1].fitness())):
                pai1 = copy.copy(carteira)
                while True:
                    print("2")
                    probabilidade = random.random()
                    carteira = pop[random.randint(0,TAM_POP-1)]
                    if(probabilidade <= (carteira.fitness()/pop[TAM_POP-1].fitness())):
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
    
    pop = eleicao(pop).copy()

    #novaPop contém os N (tamanho da população) melhores portfólios

    for i in range(len(pop)-1, (len(pop)//2)-1, -1):
        novaPop.append(pop[i])

    return novaPop

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
    pop_ord = sorted(pop,key=getKey)
    return pop_ord



