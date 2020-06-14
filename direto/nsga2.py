import operadores as operadores
import aux as aux
import grafico as grafico
from globais import *
import metricas as metricas
import classes as classes
from os import listdir
from os.path import isfile, join
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import timeit
import copy


def main():

    lista_ativos_grafico = []
    lista_ibovespa_grafico = []

    datas = ['01/01/2015', '31/12/2016']
    datas_grafico = ['01/01/2017', '30/06/2017', '01/07/2017', '31/12/2017',
                     '01/01/2018', '30/06/2018', '01/07/2018', '31/12/2018',
                     '01/01/2019', '30/06/2019', '01/07/2019', '31/12/2019']
    
    #Separa as cotações dos ativos em semestres (lista de matrizes)
    
    for i in range(0,len(datas_grafico) - 1,2):
        lista_ativos_grafico.append(aux.le_arquivo_retorna_lista_ativos(datas_grafico[i], datas_grafico[i+1], False))
        lista_ibovespa_grafico.append(aux.le_arquivo_retorna_lista_ativos(datas_grafico[i], datas_grafico[i+1], True))
   
    #len(lista_ativos_grafico) = 6
    
    pontos_x = []
    pontos_y = []
    solucao_final = []
  
    #pontos = [cvar, var, ewma, garch, lpm]

    for risco in range(QUANTIDADE_METRICAS):

        lista_ativos = aux.le_arquivo_retorna_lista_ativos(datas[0], datas[1], False)
        lista_ativos_metrica = metricas.metrica_risco(lista_ativos,risco)
        
        pontos_x.append([])
        pontos_y.append([])
        solucao_final.append(None)
        x_soma_execucoes = []
        y_soma_execucoes = []
        primeira_execucao = True  
        
        #EXECUÇÕES
        for j in range(EXECUCOES):

            x_iteracao = []
            y_iteracao = [] 

            #INICIALIZAÇÃO
            populacao = operadores.populacao_inicial(lista_ativos_metrica)
            pop_filtrada = operadores.filtragem(populacao, True)

            #GRAFICO INICIAL 
            x1 = []
            y1 = []            
            for carteira in pop_filtrada:
                x1.append(carteira.getRisco())
                y1.append(carteira.getRetorno())

            #ITERAÇÕES
            cont=0
            for i in range(ITERACOES):
                print("RISCO: " + str(risco + 1) + " EXEC: " + str(j + 1) + " ITERACOES: " + str(cont + 1))
                cont+=1
                pop = operadores.otimiza(pop_filtrada, lista_ativos_metrica)
                pop_filtrada = pop.copy()
                solucao_parcial = aux.melhor_carteira(pop_filtrada)
                if solucao_final[risco] == None or solucao_parcial.fitness() > solucao_final[risco].fitness():
                    solucao_final[risco] = solucao_parcial

            #GRAFICO FINAL DA ITERAÇÃO
            for carteira in pop_filtrada:
                x_iteracao.append(carteira.getRisco())
                y_iteracao.append(carteira.getRetorno())   
            
            x_iteracao.sort()
            y_iteracao.sort()

            if primeira_execucao:
                x_soma_execucoes = x_iteracao
                y_soma_execucoes = y_iteracao
                primeira_execucao = False
            else:
                for i in range(len(pop_filtrada)):
                    x_soma_execucoes[i] += x_iteracao[i]
                    y_soma_execucoes[i] += y_iteracao[i]

        #GRAFICO FINAL DA EXECUÇÃO
        for i in range(len(pop_filtrada)):
            x_soma_execucoes[i]/=EXECUCOES
            y_soma_execucoes[i]/=EXECUCOES
        
        pontos_x[risco] = x_soma_execucoes
        pontos_y[risco] = y_soma_execucoes
        
        # print('soma', x_soma_execucoes)
        # print('pontos', pontos_x)
        # print()
    
    # for i in solucao_final:
    #     i.printCarteira()
    #     print()


    grafico.grafico_tempo_barras(solucao_final, lista_ativos_grafico, lista_ibovespa_grafico)
    
    grafico.grafico_tempo(solucao_final, aux.le_arquivo_retorna_lista_ativos(datas_grafico[0], datas_grafico[len(datas_grafico)-1], False),
    aux.le_arquivo_retorna_lista_ativos(datas_grafico[0], datas_grafico[len(datas_grafico)-1], True))
    
    pareto_dos_riscos = ['paretoFinalCVaR', 'paretoFinalVaR', 'paretoFinalEWMA', 'paretoFinalGARCH', 'paretoFinalLPM']

    for i in range(len(pontos_x)):
        grafico.grafico_risco_retorno(pontos_x[i], pontos_y[i], pareto_dos_riscos[i])   
    
    
if __name__ == "__main__":
    main()


