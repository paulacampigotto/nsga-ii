from os import listdir
from os.path import isfile, join
import random
import numpy as np

TAM_POP = 20

def populacao_inicial():
    populacao = []
    for j in range(TAM_POP):
        carteira = []
        for i in range(9):
            a = (random.randint(0,59), random.random()) ##### satisfazer a soma dos pesos = 1
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

onlyfiles = [f for f in listdir("/home/paula/Documents/IC/nsga-2/ativos") if isfile(join("/home/paula/Documents/IC/nsga-2/ativos", f))]

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
carteira = []
for i in range(len(pop)):
    carteira_aux = []
    for j in range(len(pop[i])):
        ativo = pop[i][j][0]
        peso = pop[i][j][1]

        razao = ( ( soma(ativos[ativo],len(ativos)-1) ) / cvar(ativos[ativo])[2] ) * peso
        carteira_aux.append(razao)
    carteira.append(carteira_aux)
    #calcular a razao risco/retorno da carteira, considerando as proporções

print(carteira)
