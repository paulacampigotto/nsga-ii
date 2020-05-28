from globais import *
import random

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