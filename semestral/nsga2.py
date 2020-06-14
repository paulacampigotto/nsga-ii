from operadores import *
from grafico import *
from globais import *
import metricas as metricas
from classes import *
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

    lista_ativos_proximo_semestre = [] 
    lista_ibovespa_proximo_semestre = []

    lista_ativos_semestral = []
    lista_ibovespa_semestral = []

    datas = ['01/07/2016', '31/12/2016', '01/01/2017', '30/06/2017', 
             '01/07/2017', '31/12/2017', '01/01/2018', '30/06/2018', 
             '01/07/2018', '31/12/2018', '01/01/2019', '30/06/2019',
             '01/07/2019', '31/12/2019']

 
    #Separa as cotações dos ativos em semestres (lista de matrizes)
    for i in range(0,len(datas),2):
        lista_ativos_semestral.append(aux.le_arquivo_retorna_lista_ativos(datas[i], datas[i+1], False))
        lista_ibovespa_semestral.append(aux.le_arquivo_retorna_lista_ativos(datas[i], datas[i+1], True))
    

    pontos_x_por_semestre = []
    pontos_y_por_semestre = []
    solucao_final_por_semestre = []
    
    # ITERAÇÕES POR SEMESTRE
    for semestre in range(len(lista_ativos_semestral)-1):
    
        lista_ativos = copy.copy(lista_ativos_semestral[semestre])
        lista_ibovespa = copy.copy(lista_ibovespa_semestral[semestre])
        lista_ativos_proximo_semestre = copy.copy(lista_ativos_semestral[semestre+1])
        lista_ibovespa_proximo_semestre = copy.copy(lista_ibovespa_semestral[semestre+1])

        pontos_x = []
        pontos_y = []
        solucao_final = []
        
        #pontos = [cvar, var, ewma, garch, lpm

        
        for risco in range(QUANTIDADE_METRICAS):
            lista_ativos = metricas.metrica_risco(lista_ativos,risco)
            pontos_x.append([])
            pontos_y.append([])
            solucao_final.append(None)
            primeira_execucao = True  
            x_soma_execucoes = []
            y_soma_execucoes = [] 
            
            #EXECUÇÕES
            for j in range(EXECUCOES):

                #INICIALIZAÇÃO
                populacao = populacao_inicial(lista_ativos)
                pop_filtrada = filtragem(populacao, True)
                x_iteracoes = []
                y_iteracoes = []

                #ITERAÇÕES
                cont=0
                for i in range(ITERACOES):
                    print("SEMESTRE: "  + str(semestre) + " RISCO: " + str(risco) + " EXEC: " + str(j) + " ITERACOES: " + str(cont))
                    cont+=1
                    pop = otimiza(pop_filtrada, lista_ativos)
                    pop_filtrada = pop.copy()
                    solucao_parcial = melhor_carteira(pop_filtrada)
                    if solucao_final[risco] == None or solucao_parcial.fitness() > solucao_final[risco].fitness():
                        solucao_final[risco] = solucao_parcial

                #GRAFICO FINAL DA ITERAÇÃO
                x_iteracoes = []
                y_iteracoes = []
                for carteira in pop_filtrada:
                    x_iteracoes.append(carteira.getRisco())
                    y_iteracoes.append(carteira.getRetorno())   
                
                x_iteracoes.sort()
                y_iteracoes.sort()
                if primeira_execucao:
                    x_soma_execucoes = x_iteracoes
                    y_soma_execucoes = y_iteracoes
                    primeira_execucao = False
                else:
                    for i in range(len(pop_filtrada)):
                        x_soma_execucoes[i] += x_iteracoes[i]
                        y_soma_execucoes[i] += y_iteracoes[i] 

            #GRAFICO FINAL DA EXECUÇÃO
            for j in range(len(x_soma_execucoes)):
                x_soma_execucoes[j]/=EXECUCOES
                y_soma_execucoes[j]/=EXECUCOES
            
            pontos_x[risco] = x_soma_execucoes
            pontos_y[risco] = y_soma_execucoes
        
        pontos_x_por_semestre.append(pontos_x)
        pontos_y_por_semestre.append(pontos_y)
        
        solucao_final_por_semestre.append(solucao_final)
    
    index = 0
    cont = 0
    for semestre in solucao_final_por_semestre:
        index_risco = 0
        for risco in semestre:
            if(index < len(semestre)-1):
                preco_inicial = calcula_preco_inicial_carteira(risco, lista_ativos_semestral[index+1])
                preco_final = calcula_preco_final_carteira(risco, lista_ativos_semestral[index+1])
                if(preco_inicial <= preco_final):
                    # print("TROCOU")
                    cont+=1
                    solucao_final_por_semestre[index+1][index_risco] = copy.copy(risco)
                index_risco += 1
        index+=1
    print("Trocou = ", str(cont), " Vezes")
 
    grafico_tempo_barras(solucao_final_por_semestre, lista_ativos_semestral, lista_ibovespa_semestral)
    grafico_tempo(solucao_final, lista_ativos_proximo_semestre, lista_ibovespa_proximo_semestre)
    
    pareto_dos_riscos = ['paretoFinalCVaR', 'paretoFinalVaR', 'paretoFinalEWMA', 'paretoFinalGARCH', 'paretoFinalLPM']

    for i in range(len(pontos_x)):
        grafico_risco_retorno(pontos_x[i], pontos_y[i], pareto_dos_riscos[i])   

    # grafico_risco_retorno(pontos_x[0], pontos_y[0], "paretoFinalCVaR")
    
    # grafico_risco_retorno(pontos_x[1], pontos_y[1], "paretoFinalVaR")
    # grafico_risco_retorno(pontos_x[2], pontos_y[2], "paretoFinalEWMA")
    # grafico_risco_retorno(pontos_x[3], pontos_y[3], "paretoFinalGARCH")
    # grafico_risco_retorno(pontos_x[4], pontos_y[4], "paretoFinalLPM")
    
if __name__ == "__main__":
    main()


