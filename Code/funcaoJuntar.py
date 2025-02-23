import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
## Ideia original.
"""def juntaFuncoes(funcoes,tamanhos): ## Função para juntar funções em um único objeto
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

sp.plot(fInt2, (x, 0, 6)) ## Plota a função resultante"""


## Ideia do gpteto. Me parece errada. Possivel de ser arrumada.
def juntaFuncoes(funcoes, tamanhos):
    x = sp.Symbol('x')
    limites = np.cumsum([0] + tamanhos)
    funcoesJuntas = []

    for i in range(len(funcoes)):
        intervalo = (x >= limites[i]) & (x < limites[i+1])
        funcoesJuntas.append((funcoes[i], intervalo))

    return sp.Piecewise(*funcoesJuntas)

# Definição da variável simbólica
x = sp.Symbol('x')

# Definição do momento fletor M(x)
f1 = 2*x
f2 = x**2 + 1
tamanhos = [4, 2]

# Criar função do momento fletor
M = juntaFuncoes([f1, f2], tamanhos)
print("Momento fletor M(x):")
sp.pprint(M)

# Definição das constantes de integração
C1, C2 = sp.symbols('C1 C2')

# Primeira integração (Teta)
teta1 = sp.integrate(f1, x) + C1  # Integração no primeiro intervalo
teta2 = sp.integrate(f2, x) + C1  # Integração no segundo intervalo
teta = juntaFuncoes([teta1, teta2], tamanhos)
print("Teta(x):")
sp.pprint(teta)

# Segunda integração (V)
v1 = sp.integrate(teta1, x) + C2  # Integração no primeiro intervalo
v2 = sp.integrate(teta2, x) + C2  # Integração no segundo intervalo
v = juntaFuncoes([v1, v2], tamanhos)
print("V(x):")
sp.pprint(v)

# Definição dos pontos de transição
limites = np.cumsum([0] + tamanhos)
L = sum(tamanhos)  # Comprimento total da viga

# Condições de contorno
eq1 = sp.Eq(v.subs(x, 0), 0)  # Condição de v(0) = 0
eq2 = sp.Eq(v.subs(x, L), 0)  # Condição de v(L) = 0

# Avaliar a segunda condição de contorno corretamente
# Substituir x = L na expressão de v(x) manualmente
v_L = v2.subs(x, L)  # Usar a expressão do segundo intervalo (x >= 4 ∧ x < 6)
eq2 = sp.Eq(v_L, 0)

print("Equação 1 (v(0) = 0):", eq1)
print("Equação 2 (v(L) = 0):", eq2)

# Resolver as constantes
sol = sp.solve([eq1, eq2], [C1, C2], dict=True)
print("Solução para C1 e C2:", sol)

# Verificar se as constantes foram resolvidas
if not sol:
    raise ValueError("As constantes C1 e C2 não puderam ser resolvidas. Verifique as condições de contorno.")

# Substituir as constantes nas expressões
teta = teta.subs(sol[0])
v = v.subs(sol[0])

# **Conversão para funções numéricas**
teta_func = sp.lambdify(x, teta, modules=['numpy', {'Piecewise': np.piecewise}])
v_func = sp.lambdify(x, v, modules=['numpy', {'Piecewise': np.piecewise}])

# **Gerando os valores para o gráfico**
x_vals = np.linspace(0, L, 1000)

# Avaliar as funções numericamente
teta_vals = teta_func(x_vals)
v_vals = v_func(x_vals)

# **Plotagem corrigida**
plt.figure(figsize=(8, 4))
plt.plot(x_vals, teta_vals, label="Teta(x)")
plt.xlabel("x")
plt.ylabel("Teta(x)")
plt.legend()
plt.grid()
plt.title("Curva de Teta(x)")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(x_vals, v_vals, label="V(x)", color="r")
plt.xlabel("x")
plt.ylabel("V(x)")
plt.legend()
plt.grid()
plt.title("Curva de V(x)")
plt.show()