from operadores import *
from aux import *
from globais import *
from metricas import *
from os import listdir
from os.path import isfile, join
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import timeit
import copy

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
        self.contador_n = 0 # contador_n utilizado no nds()
        self.rank = 0
        self.dist_crowd = 0
        self.rank = 0
        self.dominadas = [] # lista s de carteiras dominadas no nds()

    def getDominadas(self):
        return self.dominadas
    
    def setDominadas(self, lista):
        self.dominadas = lista
    
    def appendDominadas(self, x):
        self.dominadas.append(x)

    def setRank(self, valor):
        self.rank = valor

    def getRank(self):
        return self.rank

    def setDist_crowd(self, valor):
        self.dist_crowd = valor

    def getDist_crowd(self):
        return self.dist_crowd

    def setContador_n(self, valor):
        self.contador_n = valor

    def getContador_n(self):
        return self.contador_n

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
        return self.retorno/self.risco

    def getIndexPeloAtivo(self, ativo):
        j = 0
        for i in self.getAtivos():
            if(i == ativo):
                return j
            j+=1

    def getAtivoPeloIndex(self,index):
        return self.ativos[index]

    def setAtivoPeloIndex(self,index, ativo):
        self.ativos[index] = ativo

    def cardinalidade(self):
        cont = 0
        for i in self.ativos:
            cont += 1
        return cont

def le_arquivo_retorna_lista_ativos(data_inicial, data_final, ibovespa):

    lista = []
    nomeAtivos = []
    primeira = True
    flag = False
    
    with open("ativos.csv", "r+") as f:
        linhas = f.readlines()
        listaCotacoes = []
        

        #PERCORRE LINHAS
        for linha in linhas:
            valores = linha.split(",")
            j=-1
            #PERCORRE CADA ATIVO
            for valor in valores:
                if(valores[0] == 'CODIGOS' and valor != valores[0]):
                    if(valor == 'IBOV\n'):
                        nome = 'IBOV'
                        nomeAtivos.append(nome)
                    else:
                        nomeAtivos.append(valor)
                else:
                    if primeira and valor != 'CODIGOS':
                        for i in range(len(nomeAtivos)):
                            listaCotacoes.append([])
                        primeira = False
                    if data_inicial == valores[0]:
                        flag = True
                    if(flag and valor != valores[0])and valor != '-' and valor != '-\n':
                        listaCotacoes[j].append(float(valor))
                j+=1
            if data_final == valores[0]:
                flag = False
                
        lista_ibovespa = []
        for i in range(len(nomeAtivos)):
            codigoAtivo = nomeAtivos[i]
            if(codigoAtivo == "IBOV"):
                lista_ibovespa = copy.copy(listaCotacoes[i])
            else:
                lista.append(Ativo(codigoAtivo,listaCotacoes[i]))
    
    if ibovespa:
        return lista_ibovespa
    else:
        return lista
    
     

def populacao_inicial():
    global populacao
    for j in range(TAM_POP):
        carteira = []
        for i in range(CARDINALIDADE):
            ativo = (lista_ativos[ativo_aux(carteira)], pesoProporcional(carteira,i)) ##### satisfazer a soma dos pesos = 1
            carteira.append(ativo)
        populacao.append(Carteira(carteira))


def grafico_tempo(carteira_cvar, carteira_var, carteira_ewma, carteira_garch, carteira_lpm):
    global lista_ibovespa_2019

    cotacoes_cvar = calcula_cotacoes_carteira_2019(carteira_cvar)
    cotacoes_var = calcula_cotacoes_carteira_2019(carteira_var)
    cotacoes_ewma = calcula_cotacoes_carteira_2019(carteira_ewma)
    cotacoes_garch = calcula_cotacoes_carteira_2019(carteira_garch)
    cotacoes_lpm = calcula_cotacoes_carteira_2019(carteira_lpm)


    plt.plot(range(len(retorno_acumulado(cotacoes_cvar))),retorno_acumulado(cotacoes_cvar),linestyle = 'solid', color = '#66ffa3', label = 'CVaR')
    plt.plot(range(len(retorno_acumulado(cotacoes_var))),retorno_acumulado(cotacoes_var), linestyle = (0, (3, 1, 1, 1)), color = '#ff66c7', label = 'VaR')
    plt.plot(range(len(retorno_acumulado(cotacoes_ewma))),retorno_acumulado(cotacoes_ewma), linestyle = 'dashdot',color = '#c457ff', label = 'EWMA')
    plt.plot(range(len(retorno_acumulado(cotacoes_garch))),retorno_acumulado(cotacoes_garch), linestyle = 'dashed', color = '#ffeb57', label = 'GARCH')
    plt.plot(range(len(retorno_acumulado(cotacoes_lpm))),retorno_acumulado(cotacoes_lpm), linestyle = 'dotted',color = '#66c2ff', label = 'LPM')
    
    plt.plot(range(len(retorno_acumulado(lista_ibovespa_2019))), retorno_acumulado(lista_ibovespa_2019), color = 'black', label = 'Ibovespa')
    plt.legend()
    plt.xlabel('Tempo')
    plt.ylabel('Retorno acumulado (%)')
    plt.title("Retorno Acumulado")
    plt.savefig('graficos/MelhorCarteira.png')
    plt.show()

def otimiza(populacao_filtrada, lista_ativos):
    # global populacao
    popCrossover = crossover(populacao_filtrada)
    populacaoMutada = mutacao(popCrossover, lista_ativos)
    return filtragem(populacaoMutada, False).copy()


def main():

    global populacao, lista_ativos, lista_ativos_2019, lista_ibovespa_2019

    lista_ativos_semestral = []
    datas = ['01/01/2015', '30/06/2015', '01/07/2015', '31/12/2015', '01/01/2016', '30/06/2016', '01/07/2016', '31/12/2016', '01/01/2017', '30/06/2017', '01/07/2017', '31/12/2017', '01/01/2018', '30/06/2018', '01/07/2018', '31/12/2018']
    
    #Separa as cotações dos ativos em semestres (lista de matrizes)
    for i in range(0,len(datas),2):
        lista_ativos_semestral.append(le_arquivo_retorna_lista_ativos(datas[i], datas[i+1], False))

    lista_ativos_2019 = le_arquivo_retorna_lista_ativos('01/01/2019', '31/12/2019', False)
    lista_ibovespa_2019 = le_arquivo_retorna_lista_ativos('01/01/2019', '31/12/2019', True)

    

    # ITERAÇÕES POR SEMESTRE
    for semestre in range(len(lista_ativos_semestral)):

        lista_ativos = copy.copy(lista_ativos_semestral[semestre])


        pontos_x = []
        pontos_y = []
        solucao_final = []

        #pontos = [cvar, var, ewma, garch, lpm]
        
        for i in range(QUANTIDADE_METRICAS):
            pontos_x.append([])
            pontos_y.append([])
            solucao_final.append(None)

        for risco in range(QUANTIDADE_METRICAS):
            
            lista_ativos = metrica_risco(lista_ativos,risco)
            
            primeira_execucao = True  
            
            x = []
            y = [] 
            
            #EXECUÇÕES
            for j in range(EXECUCOES):
                start = timeit.default_timer()  

                #INICIALIZAÇÃO
                populacao = []
                populacao_inicial()
                pop_filtrada = filtragem(populacao, True)

                #GRAFICO INICIAL 
                x1 = []
                y1 = []
                
                for carteira in pop_filtrada:
                    x1.append(carteira.getRisco())
                    y1.append(carteira.getRetorno())
                # for i in range(len(x1)):
                #     print("x = ",x1[i], " y = ", y1[i])
                #ITERAÇÕES
                cont=0
                for i in range(ITERACOES):
                    print("RISCO: " + str(risco) + " EXEC: " + str(j) + " ITERACOES: " + str(cont))
                    cont+=1
                    pop = otimiza(pop_filtrada, lista_ativos)
                    pop_filtrada = pop.copy()
                    solucao_parcial = melhor_carteira(pop_filtrada)
                    if solucao_final[semestre] == None or solucao_parcial.fitness() > solucao_final[semestre].fitness():
                        solucao_final[semestre] = solucao_parcial

                #GRAFICO FINAL DA ITERAÇÃO
                x2 = []
                y2 = []
                for carteira in pop_filtrada:
                    x2.append(carteira.getRisco())
                    y2.append(carteira.getRetorno())   
                
                if primeira_execucao:
                    x = copy.copy(x2)
                    y = copy.copy(y2)
                    primeira_execucao = False

                else:
                    for i in range(len(pop_filtrada)):
                        x[i] += x2[i]
                        y[i] += y2[i]
                

                stop = timeit.default_timer()
                print('******Time: ', stop - start)  

            #GRAFICO FINAL DA EXECUÇÃO
            for j in range(len(pop_filtrada)):
                x[j]/=EXECUCOES
                y[j]/=EXECUCOES
            
            pontos_x[risco] = x
            pontos_y[risco] = y                       

    for i in solucao_final:
        i.printCarteira()
        print()

 
    grafico_tempo(solucao_final[0], solucao_final[1], solucao_final[2], solucao_final[3], solucao_final[4])
    grafico_risco_retorno(pontos_x[0], pontos_y[0], "paretoFinalCVaR")
    grafico_risco_retorno(pontos_x[1], pontos_y[1], "paretoFinalVaR")
    grafico_risco_retorno(pontos_x[2], pontos_y[2], "paretoFinalEWMA")
    grafico_risco_retorno(pontos_x[3], pontos_y[3], "paretoFinalGARCH")
    grafico_risco_retorno(pontos_x[4], pontos_y[4], "paretoFinalLPM")
    
if __name__ == "__main__":
    main()


