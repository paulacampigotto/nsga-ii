from operadores import *
from aux import *
from globais import *
import itertools
import matplotlib.pyplot as plt
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint
import numpy as np

class Ativo:
    idAtivo = itertools.count()
    def __init__(self, codigo, cotacoes):
        self.codigo = codigo
        self.cotacoes = cotacoes
        self.risco = 0
        self.retorno = 0
        self.id = next(Ativo.idAtivo)

    def getId(self):
        return self.id

    def getCodigo(self):
        return self.codigo

    def getCotacoes(self):
        return self.cotacoes

    def getRisco(self):
        return self.risco
    
    def setRisco(self, risco):
        self.risco = risco

    def getRetorno(self):
        return self.retorno

    def setRetorno(self, retorno):
        self.retorno = retorno


class Carteira:
    idCarteira = itertools.count()
    def __init__(self, ativos):
        self.ativos = ativos.copy() # ativos = (Ativo, proporção)
        self.risco = self.defineRisco()
        self.retorno = self.defineRetorno()
        self.id = next(Carteira.idCarteira)

    def getId(self):
        return self.id

    def getAtivos(self):
        return self.ativos

    def setAtivos(self, ativos):
        self.ativos = ativos

    def defineRisco(self):
        r = 0
        for i in self.getAtivos():
            r += i[0].getRisco() * i[1] # i[0] = Ativo | [1] = Proporção
        return r

    def defineRetorno(self):
        r = 0
        for i in self.getAtivos():
            r += i[0].getRetorno() * i[1] # i[0] = Ativo | [1] = Proporção
        return r

    def getRisco(self):
        return self.risco
    
    def getRetorno(self):
        return self.retorno

    def getProporcao(self, index):
        return self.ativos[index][1]

    def setProporcao(self, index, proporcao):
        self.ativos[index] = (self.ativos[index][0], proporcao)

    def printCarteira(self):
        for i in self.ativos:
            print(i[0].getCodigo(), round(i[1],4))
        # print("Fitness: " + str(self.fitness()))

    def fitness(self):
        print("ret: " + str(self.retorno) + " risco: " + str(self.risco))
        return self.retorno/self.risco

    def getIndexPeloAtivo(self, ativo):
        j = 0
        for i in self.getAtivos():
            if(i == ativo):
                return j
            j+=1

    def setAtivoPeloIndex(self,index, ativo):
        self.ativos[index] = ativo
                

def inicializa():    
    
    global listaAtivos

    nomesArquivos = [f for f in listdir("/home/paula/Documents/IC/nsga-ii/ativos") if isfile(join("/home/paula/Documents/IC/nsga-ii/ativos", f))]
    
    #lê os arquivos e armazena os códigos e cotações em listaAtivos
    for i in nomesArquivos: 
        with open("ativos/" + i, "r+") as f:
            linhas = f.readlines()
            listaCotacoes = []
            for linha in linhas:
                aux = linha.split(",")[5]
                if(aux != 'Adj Close' and aux != 'null' and aux != "\n"):
                    adj_close = float(aux)
                    listaCotacoes.append(adj_close)
            codigoAtivo = i[:5]
            listaAtivos.append(Ativo(codigoAtivo,listaCotacoes))


    #calcula o risco e o retorno de cada ativo e atualiza os valores de listaAtivos
    for i in listaAtivos:
        ris = cvar(i.getCotacoes())[1] #[0] = CVaR 95% | [1] = CVaR 99% | [2] = CVaR 99.9%
        i.setRisco(ris)
        ret = sum(retorno(i.getCotacoes()))/len(i.getCotacoes())
        i.setRetorno(ret)
    
    for i in listaAtivos:
        print(i.getRetorno())

def populacao_inicial():
    global populacao
    for j in range(TAM_POP):
        carteira = []
        for i in range(CARDINALIDADE):
            ativo = (listaAtivos[ativo_aux(carteira)], pesoProporcional(carteira,i)) ##### satisfazer a soma dos pesos = 1
            carteira.append(ativo)
        populacao.append(Carteira(carteira))

def retorno(ativo):
    retorno = []
    for i in range(len(ativo) -1):
        #if(ativo[i] != 0):
        #retorno.append(np.log(ativo[i+1] / (ativo[i])))
        retorno.append((ativo[i+1] - ativo[i]) / ativo[i])
        #else:
        #    retorno.append(( ativo[i+1] - ativo[i] ) / 0.001)
    return retorno

def cvar(ativo):
    ret_ord = retorno(ativo)
    ret_ord.sort()
    total_count = len(ret_ord)

    var95 = ret_ord[ceil((1-(95/100))*total_count)]
    var99 = ret_ord[ceil((1-(99/100))*total_count)]
    var999 = ret_ord[ceil((1-(99.9/100))*total_count)]

    cvar95 = abs((1/((1-(95/100))*total_count))*soma_aux(ret_ord, ceil((1-(95/100))*total_count)))
    cvar99 = abs((1/((1-(99/100))*total_count))*soma_aux(ret_ord, ceil((1-(99/100))*total_count)))
    cvar999 = abs((1/((1-(99.9/100))*total_count))*soma_aux(ret_ord, ceil((1-(99.9/100))*total_count)))

    return [(cvar95), (cvar99), (cvar999)]

def otimiza():
    global populacao
    popCrossover = crossover(populacao)
    populacaoMutacao = mutacao(popCrossover)
    populacao = fnds(populacaoMutacao)
    #popfiltragem = filtragem(populacaoMutacao)
    #populacao = popfiltragem.copy()

def main():

    inicializa()
    print("oi")
    populacao_inicial()
    

    x1 = []
    y1 = []
    for carteira in populacao:
        x1.append(carteira.getRisco())
        y1.append(carteira.getRetorno())

    for i in range(ITERACOES):
        otimiza()

    #rint("------------------------------------")
    #printPopulacao(populacao)
    
    x2 = []
    y2 = []
    for carteira in populacao:
        x2.append(carteira.getRisco())
        y2.append(carteira.getRetorno())

    
    plt.scatter(x1, y1)
    plt.axis([min(x1), max(x1), min(y1), max(y1)])
    plt.xlabel('Risco')
    plt.ylabel('Retorno')
    plt.savefig('paretoInicial.png')
    plt.show()
        
    plt.scatter(x2, y2)
    plt.axis([min(x2), max(x2), min(y2), max(y2)])
    plt.xlabel('Risco')
    plt.ylabel('Retorno')
    plt.savefig('paretoFinal.png')
    plt.show()

if __name__ == "__main__":
    main()


