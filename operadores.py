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
            print("fitness: " + str(carteira.fitness()))
            print("denominador: " + str(pop[TAM_POP-1].fitness()))
            if(probabilidade <= (carteira.fitness()/pop[TAM_POP-1].fitness())):
                pai1 = copy.copy(carteira)
                while True:
                    print("2")
                    probabilidade = random.random()
                    carteira = pop[random.randint(0,TAM_POP-1)]
                    print("prob:" + str(probabilidade))
                    print("div: " + str(carteira.fitness()/pop[TAM_POP-1].fitness()))
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
    
   # pop = eleicao(pop).copy()

    #novaPop contém os N (tamanho da população) melhores portfólios

    # for i in range(len(pop)-1, 0, -1):
    #     novaPop.append(pop[i])

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
    pop_ord = sorted(pop,key=getKey)
    return pop_ord

# def filtragem(pop, fronteira):
#     populacao = eleicao(pop)
#     i = 0
#     cont = 0
#     while cont != len(fronteira[i])//2:
#         tam = len(fronteira[i])
#         if tam + cont < populacao//2:
#             nova_pop.append(fronteira[i])
#             cont += tam???
#         else:
#             aux = dist_aglomeracao(fronteira[i])
#             nova_pop.append(aux???)
#             cont = cont + (len(populacao)//2 - cont)
#         i+=1

#     return nova_pop

# def domina(carteira1, carteira2): #verificar condições de dominância
#     if carteira1.getRisco() < carteira2.getRisco() and carteira1.getRetorno() > carteira2.getRetorno()
#         return True
#     return False

# def nds(pop):
#     populacao = pop.copy()
    
#     for carteira1 in populacao:
#         cont = 0
#         fronteira = []
#         front_aux = []
#         for carteira2 in populacao:
#             if carteira1 != carteira2:
#                 if domina(carteira2, carteira1):
#                     cont += 1
#         if cont == 0:
#             front_aux.append(carteira1)
#             populacao.remove(carteira1)
        
#     k = 0
#     while 

def p_individuos(pop):
    pop_nova = eleicao(pop)
    populacao = []
    for i in range(pop//2):
        populacao.append(pop_nova[i])
    return populacao


def fnds(pop):
    S=[]
    front = [[]]
    n=[]
    rank = [0 for i in range(0, len(pop))]

    for p in pop:
        Si=[]
        ni=0
        for q in pop:
            if (p.getRetorno() > q.getRetorno() and p.getRisco() < q.getRisco()):
                if q not in S[p.getId()]:
                    Si.append(q)
            else:
                ni += 1

        if ni==0:
            rank[p.getId()] = 0
            if p not in front[0]:
                front[0].append(p)
        S.append(Si)
        n.append(ni)

    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p.getId()]:
                n[q.getId()] =n[q.getId()] - 1
                if( n[q.getId()]==0):
                    rank[q.getId()]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)
    
    del front[len(front)-1]
    return front

