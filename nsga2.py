from os import listdir
from os.path import isfile, join
import random
import numpy as np
import matplotlib.pyplot as plt


TAM_POP = 50
CARDINALIDADE = 9

def peso(carteira,i):
    soma = 0
    for j in range(len(carteira)):
        soma+=carteira[j][1]

    if(i == CARDINALIDADE):
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
            a = (random.randint(0,59), peso(carteira,i)) ##### satisfazer a soma dos pesos = 1
            carteira.append(a)
        populacao.append(carteira)
    return populacao


def soma(retornos, indice):
    s = 0
    for i in range(indice):
        s+= retornos[i]
    return s

def retorno(ativo):
    retorno = []
    for i in range(len(ativo) -1):
        if(ativo[i] != 0):
            retorno.append(( ativo[i+1] - ativo[i] ) / ativo[i])
    return retorno

def cvar(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    var95 = ret_ord[round((1-(95/100))*total_count)]
    var99 = ret_ord[round((1-(99/100))*total_count)]
    var999 = ret_ord[round((1-(99.9/100))*total_count)]

    cvar95 = (1/((1-(95/100))*total_count)*soma(ret_ord, round((1-(95/100))*total_count)))
    cvar99 = (1/((1-(99/100))*total_count)*soma(ret_ord, round((1-(99/100))*total_count)))
    cvar999 = (1/((1-(99.9/100))*total_count)*soma(ret_ord, round((1-(99.9/100))*total_count)))

    return [cvar95, cvar99, cvar999]

onlyfiles = [f for f in listdir("/home/paula/Documents/IC/nsga-ii/ativos") if isfile(join("/home/paula/Documents/IC/nsga-ii/ativos", f))]

it = 0
ativos = np.empty((len(onlyfiles), 996)) # 996 -> numero de dias

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


pop = populacao_inicial()
print(pop)
carteira = []
for i in range(len(pop)):
    retorno_carteira = 0
    cvar999_carteira = 0
    for j in range(len(pop[i])):
        ativo = pop[i][j][0]
        peso = pop[i][j][1]
        retorno_ativo = sum(retorno(ativos[ativo]))/len(ativos[ativo])
        # if(i==0 and j==0):
        #     print("-----------")
        #     print(retorno(ativos[ativo]))
        #     print(sum(retorno(ativos[ativo])))
        #     print("-----------")
        cvar999_ativo = cvar(ativos[ativo])[2] * peso
        retorno_carteira+=retorno_ativo * peso
        cvar999_carteira+=cvar999_ativo * peso
    carteira.append((cvar999_carteira, retorno_carteira))

print(carteira)

zip(*carteira)
plt.scatter(*zip(*carteira))
plt.axis([ -5, 0, -0.01, 0.01])
plt.show()
