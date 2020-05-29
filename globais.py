TAM_POP = 100
CARDINALIDADE = 9
ITERACOES = 50
PROBABILIDADE_MUTACAO = 0.1
EXECUCOES = 10
QUANTIDADE_ATIVOS = 62
listaAtivos = []
populacao = []
lista_ibovespa = []

### EWMA
λ = 0.94

### GARCH
ω = 0.0001
α = 0.75
β = 0.1

###LPM
τ = 0 # retorno-alvo: média do ativo, taxa livre de risco, um benchmarking (como o Ibovespa) ou mesmo o zero.
k = 0.000001 # nível de aversão ao risco do investidor
#k = 0 (safety first) maior nível de aversão ao risco do investidor
#k = 1 (regret)
#k = 2 (second order)
#k = 3 (semi-skewness)
#k = 4 (semi-kurtosis)  menor nível de aversão ao risco do investidor
