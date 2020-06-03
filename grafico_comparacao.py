import numpy as np
import matplotlib.pyplot as plt

retornos_acumulados_semestral = []
retornos_acumulados_direto = []
desvio_semestral = []
desvio_direto = []

with open("semestral/retorno_acumulado.txt", "r+") as f:
    linha = f.readline().split(",")
    
    for i in range(len(linha)):
        if(i%2 == 0):
            retornos_acumulados_semestral.append(float(linha[i]))
        else:
            desvio_semestral.append(float(linha[i]))


with open("direto/retorno_acumulado.txt", "r+") as f:
    linha = f.readline().split(",")
    for i in range (0,len(linha) - 1,2):
        print(i)
        retornos_acumulados_direto.append(float(linha[i]))
        desvio_direto.append(float(linha[i+1]))


print(retornos_acumulados_semestral)
print(retornos_acumulados_direto)

print(desvio_semestral)
print(desvio_direto)


# create plot
n_groups = len(retornos_acumulados_semestral)
fig, ax = plt.subplots()
X = np.arange(n_groups)
bar_width = 0.3
opacity = 0.5


rects1 = plt.bar(X , retornos_acumulados_semestral, yerr = desvio_semestral, width = bar_width, capsize=5,
alpha=opacity,color='#999999',label='Semestral', hatch="..")

rects2 = plt.bar(X+ bar_width, retornos_acumulados_direto, yerr=desvio_direto, width = bar_width, capsize=5,
alpha=opacity,color='#333333',label='Direto', hatch="///")

plt.xlabel('Métricas de risco')
plt.ylabel('Retorno acumulado (%)')
plt.title('Retorno acumulado entre 2017 e 2019')
plt.xticks(X + bar_width-0.15, ('CVaR', 'VaR', 'EWMA', 'GARCH', 'LPM'))
plt.legend()
plt.tight_layout()
plt.savefig('graficoComparacao.png')
plt.show()