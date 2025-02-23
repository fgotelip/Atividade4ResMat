import numpy as np
import sympy as sp

def juntaFuncoes(funcoes,tamanhos): ## Função para juntar funções em um único objeto
    funcoes = np.array(funcoes) ## Transforma a lista de funções em vetor
    tamanhos = np.array(tamanhos) ## Transforma a lista de tamanhos em vetor
    funcoesJuntas = [] ## Vetor para armazenar a função final
    tam=0 ## Posição inicial 
    for i in range(len(funcoes)):
        funcoesJuntas.append((funcoes[i],(x >= tam) & (x < tam+tamanhos[i]))) ## Adiciona a função e o intervalo dela no vetor final
        tam+=tamanhos[i] ## Atualiza a posição inicial
    return sp.Piecewise(*funcoesJuntas) ## Retorna a função final

## Como usar
x=sp.symbols('x')
f1 = 2*x
f2 = x**2 + 1
tam1=4
tam2=2
funcao_resultante = juntaFuncoes([f1, f2], [tam1, tam2])
print(funcao_resultante)

fInt=sp.integrate(funcao_resultante, x) ## Integra a função resultante

print(fInt) ## Função do teta

sp.plot(fInt, (x, 0, 6)) ## Plota a função resultante

fInt2=sp.integrate(fInt, x) ## Integra a função resultante duas vezes

print(fInt2) ## Função do v

sp.plot(fInt2, (x, 0, 6)) ## Plota a função resultante
