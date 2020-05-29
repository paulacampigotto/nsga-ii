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

def otimiza(populacao_filtrada):
    # global populacao
    popCrossover = crossover(populacao_filtrada)
    populacaoMutada = mutacao(popCrossover)
    return filtragem(populacaoMutada, False).copy()


def main():

    global populacao, lista_ativos, lista_ativos_2019, lista_ativos_ibovespa

    lista_ativos_semestral = []
    datas = ['01/01/2015', '30/06/2015', '01/07/2015', '31/12/2015', '01/01/2016', '30/06/2016', '01/07/2016', '31/12/2016', '01/01/2017', '30/06/2017', '01/07/2017', '31/12/2017', '01/01/2018', '30/06/2018', '01/07/2018', '31/12/2018']
    
    #Separa as cotações dos ativos em semestres (lista de matrizes)
    for i in range(0,len(datas),2):
        print(datas[i], datas[i+1])
        lista_ativos_semestral.append(le_arquivo_retorna_lista_ativos(datas[i], datas[i+1], False))

    lista_ativos_2019 = le_arquivo_retorna_lista_ativos('01/01/2019', '31/12/2019', False)
    lista_ibovespa_2019 = le_arquivo_retorna_lista_ativos('01/01/2019', '31/12/2019', True)


    # ITERAÇÕES POR SEMESTRE
    for i in range(len(lista_ativos_semestral)):

        lista_ativos = copy.copy(lista_ativos_semestral[i])

        pontos_x_cvar = []
        pontos_y_cvar = []
        solucao_final_cvar = None

        pontos_x_var = []
        pontos_y_var = []
        solucao_final_var = None


        pontos_x_ewma = []
        pontos_y_ewma = []
        solucao_final_ewma = None

        pontos_x_garch = []
        pontos_y_garch = []
        solucao_final_garch = None

        pontos_x_lpm = []
        pontos_y_lpm = []
        solucao_final_lpm = None
        
        for risco in range(QUANTIDADE_METRICAS):
            metrica_risco(risco)
            primeira_execucao = True  
            
            pontos_x = []
            pontos_y = []
            solucao_final = None  
            
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

                #ITERAÇÕES
                cont=0
                for i in range(ITERACOES):
                    print("RISCO: " + str(risco) + " EXEC: " + str(j) + " ITERACOES: " + str(cont))
                    cont+=1
                    pop = otimiza(pop_filtrada)
                    pop_filtrada = pop.copy()
                    solucao_parcial = melhor_carteira(pop_filtrada)
                    if solucao_final == None or solucao_parcial.fitness() > solucao_final.fitness():
                        solucao_final = solucao_parcial

                #GRAFICO FINAL DA ITERAÇÃO
                x2 = []
                y2 = []
                for carteira in pop_filtrada:
                    x2.append(carteira.getRisco())
                    y2.append(carteira.getRetorno())   

                if primeira_execucao:
                    pontos_x = copy.copy(x2)
                    pontos_y = copy.copy(y2)
                    primeira_execucao = False

                else:
                    for i in range(len(pop_filtrada)):
                        pontos_x[i] += x2[i]
                        pontos_y[i] += y2[i]
                

                stop = timeit.default_timer()
                print('******Time: ', stop - start)  

            #GRAFICO FINAL DA EXECUÇÃO
            for i in range(len(pop_filtrada)):
                pontos_x[i]/=EXECUCOES
                pontos_y[i]/=EXECUCOES
            
            if(risco == 0):
                solucao_final_cvar = solucao_final
                pontos_x_cvar = pontos_x
                pontos_y_cvar = pontos_y
            elif(risco == 1):
                solucao_final_ewma = solucao_final
                pontos_x_ewma = pontos_x
                pontos_y_ewma = pontos_y
            elif(risco == 2):
                solucao_final_garch = solucao_final
                pontos_x_garch = pontos_x
                pontos_y_garch = pontos_y
            elif(risco == 3):
                solucao_final_var = solucao_final
                pontos_x_var = pontos_x
                pontos_y_var = pontos_y
            else:
                solucao_final_lpm = solucao_final
                pontos_x_lpm = pontos_x
                pontos_y_lpm = pontos_y
            

        print("CVAR")
        solucao_final_cvar.printCarteira()
        
        print("VAR")
        solucao_final_var.printCarteira()

        print("EWMA")
        solucao_final_ewma.printCarteira()

        print("GARCH")
        solucao_final_garch.printCarteira()

        print("LPM")
        solucao_final_lpm.printCarteira()

 

    grafico_tempo(solucao_final_cvar, solucao_final_var, solucao_final_ewma, solucao_final_garch, solucao_final_lpm)
    grafico_risco_retorno(x1,y1,"paretoInicial")
    grafico_risco_retorno(pontos_x_cvar, pontos_y_cvar, "paretoFinalCVaR")
    grafico_risco_retorno(pontos_x_var, pontos_y_var, "paretoFinalVaR")
    grafico_risco_retorno(pontos_x_ewma, pontos_y_ewma, "paretoFinalEWMA")
    grafico_risco_retorno(pontos_x_garch, pontos_y_garch, "paretoFinalGARCH")
    grafico_risco_retorno(pontos_x_lpm, pontos_y_lpm, "paretoFinalLPM")
if __name__ == "__main__":
    main()


