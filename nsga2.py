from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import random
import numpy as np
from pprint import pprint
from math import ceil


TAM_POP = 10
CARDINALIDADE = 9
ITERACOES = 1

def riscoRetornoCarteira(carteira, riscRet):
    risco = 0
    retorno = 0
    for i in carteira:
        risco+= riscRet[i[0]][0] * i[1]
        retorno+= riscRet[i[0]][1] * i[1]
    return (risco,retorno)


def riscoRetornoAtivos(ativos):
    riscRet = []
    for i in ativos:
        ris = cvar(i)[2] #cvar 99.9%
        ret = sum(retorno(i))/len(retorno(i)) #média das taxas de retorno
        riscRet.append((ris,ret))
    return riscRet

def peso_aux(carteira,i):
    soma = 0
    for j in range(len(carteira)):
        soma+=carteira[j][1]

    if(i == CARDINALIDADE-1):
        return 1- soma
    elif(i==0):
        return random.random()
    else:
        p = random.random()
        while(p > soma):
            p = random.random()
        return p


def populacao_inicial():
    populacao = []
    for j in range(TAM_POP):
        carteira = []
        for i in range(9):
            a = (random.randint(0,59), peso_aux(carteira,i)) ##### satisfazer a soma dos pesos = 1
            carteira.append(a)
        populacao.append(carteira)
    return populacao

def soma_aux(retorno, indice):
    s = 0
    for i in range(indice):
        s+= retorno[i]
    return s

def retorno(ativo):
    retorno = []
    for i in range(len(ativo) -1):
        if(ativo[i] != 0):
            retorno.append(( ativo[i+1] - ativo[i] ) / ativo[i])
        else:
            retorno.append(( ativo[i+1] - ativo[i] ) / 0.001)
    return retorno

def cvar(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    var95 = ret_ord[round((1-(95/100))*total_count)]
    var99 = ret_ord[round((1-(99/100))*total_count)]
    var999 = ret_ord[round((1-(99.9/100))*total_count)]

    cvar95 = (1/((1-(95/100))*total_count)*soma_aux(ret_ord, round((1-(95/100))*total_count)))
    cvar99 = (1/((1-(99/100))*total_count)*soma_aux(ret_ord, round((1-(99/100))*total_count)))
    cvar999 = (1/((1-(99.9/100))*total_count)*soma_aux(ret_ord, round((1-(99.9/100))*total_count)))

    return [cvar95, cvar99, cvar999]


def getKey(x):
    return x[1]

def crossover(carteiraRisRet):
    novaPop = []
    probabilidade = random.random()
    for i in range(ceil(TAM_POP/2)):
        while True:
            carteira = random.randint(0,len(carteiraRisRet)-1)
            if(probabilidade < (carteiraRisRet[carteira][1]/carteiraRisRet[0][1])):
                pai1 = pop[carteira]
                probabilidade = random.random()
                while True:
                    carteira = random.randint(0,len(carteiraRisRet)-1)
                    if(probabilidade < (carteiraRisRet[carteira][1]/carteiraRisRet[0][1])):
                        pai2 = pop[carteira]
                        break
                break
        filho1 = pai1[:4] + pai2[4:]
        filho2 = pai2[:4] + pai1[4:]
        novaPop.append(filho1)
        novaPop.append(filho2)
    return novaPop

def mutacao(novaPop):
    for i in novaPop:
        random = random.random()
        flag = False
        if(random < 0.1):
            while(flag == False):
                randInd1 = random.randint(0,len(novaPop)-1)
                randInd2 = random.randint(0,len(novaPop)-1)
                randomsum = 1-random
                randomAtivo = novaPop[randInd1][1]
                if novaPop[randInd2][1] - random > 0.0:
                    novaPop[randInd1][1] = random
                    novaPop[randInd2][1] = random - novaPop[randInd2][1] + randomsum
                    flag = True


def eleicao():
    indRisRet = []
    for i in risRetPop:
        indRisRet.append((i[0],i[1][1]/i[1][0])) #retorno sobre risco
    return sorted(indRisRet,key=getKey)


def otimiza(populacao):
     # print(eleicao())
     novaPop = crossover(eleicao())
#    novaPop = mutacao(novaPop)
     return novaPop


#### Le arquivo

onlyfiles = [f for f in listdir("/home/paula/Documents/IC/nsga-ii/ativos") if isfile(join("/home/paula/Documents/IC/nsga-ii/ativos", f))]
ativos = np.empty((len(onlyfiles), 996)) # 996 -> numero de dias
def leitura():
    global onlyfiles
    global ativos
    it = 0
    for i in(onlyfiles): # linha: ativos, coluna: cotações
        with open("ativos/" + i, "r+") as f:
            lines = f.readlines()
            coluna = 0
            for linha in lines:
                aux = linha.split(",")[5]
                if(aux != 'Adj Close' and aux != 'null'):
                    adj_close = float(aux)
                    ativos[it][coluna] = adj_close
                    coluna+=1
        it+=1

leitura()

riscRet = riscoRetornoAtivos(ativos) #contem o risco e o retorno de todos os ativos
pop = populacao_inicial() # vetor de populacao inicial aleatoria

risRetPop = []

cont=0
for i in pop:
    risRetPop.append((cont,riscoRetornoCarteira(i,riscRet))) # indice do ativo, risco e retorno
    cont+=1
for i in range(ITERACOES):
    pop = otimiza(pop)


# zip(*risRetPop)
# plt.scatter(*zip(*risRetPop))
# plt.axis([ -5, 0, -0.01, 0.01])
# plt.show()
