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
        aleatorio = random.randint(0,59)
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

def getKey(x):
    return x.fitness()

def printPopulacao(pop):
    for carteira in pop:
        carteira.printCarteira()
        print()