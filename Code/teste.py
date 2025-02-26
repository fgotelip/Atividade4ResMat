import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Definição da variável simbólica
x = sp.Symbol('x')

# Função degrau de Heaviside
Heaviside = sp.Heaviside

# 1. Carga Pontual (P)
def momento_pontual(P, a):
    return -P * Heaviside(x - a) * (x - a)

# 2. Carregamento Uniforme (q)
def momento_distribuido(q, a, b):
    return -(q / 2) * (Heaviside(x - a) * (x - a)**2 - Heaviside(x - b) * (x - b)**2)

# 3. Carregamento Triangular Crescente
def momento_triangular_crescente(q_max, a, b):
    return -(q_max / (6 * (b - a))) * (Heaviside(x - a) * (x - a)**3 - Heaviside(x - b) * (x - b)**3) + (q_max / 2) * Heaviside(x - b) * (x - b)**2

# 4. Carregamento Triangular Decrescente
def momento_triangular_decrescente(q_max, a, b):
    return -(q_max / (6 * (b - a))) * (Heaviside(x - a) * (x - a)**3 - Heaviside(x - b) * (x - b)**3) - (q_max / 2) * Heaviside(x - a) * (x - a)**2

# 5. Carregamento Trapezoidal Crescente
def momento_trapezoidal_crescente(q1, q2, a, b):
    return -((q2 - q1) / (6 * (b - a))) * (Heaviside(x - a) * (x - a)**3 - Heaviside(x - b) * (x - b)**3) - (q1 / 2) * (Heaviside(x - a) * (x - a)**2 - Heaviside(x - b) * (x - b)**2)

# 6. Carregamento Trapezoidal Decrescente
def momento_trapezoidal_decrescente(q1, q2, a, b):
    return -((q1 - q2) / (6 * (b - a))) * (Heaviside(x - a) * (x - a)**3 - Heaviside(x - b) * (x - b)**3) - (q2 / 2) * (Heaviside(x - a) * (x - a)**2 - Heaviside(x - b) * (x - b)**2)

# 7. Carga Momento (M)
def momento_momento(M0, a):
    return -M0 * Heaviside(x - a)

# Somando todas as funções de momento fletor conforme necessidade
M_total = (
    momento_pontual(-190.57, 0) +  # Agora as forças aplicadas no começo
    momento_pontual(30, 3.75) +
    momento_pontual(30, 5.75) +
    momento_distribuido(100, 0, 1.5) +
    momento_triangular_crescente(150, 3, 3.75) +
    momento_trapezoidal_decrescente(100, 10, 4, 5) +
    momento_momento(-20, 1.75) +  # Aplique os momentos, começando pelos que estão mais à esquerda
    momento_momento(40, 3) 

)

# Converter para função numérica
M_lambdified = sp.lambdify(x, M_total, 'numpy')

# Definir intervalo de x
x_vals = np.linspace(0, 6, 1000)
M_vals = M_lambdified(x_vals)

# Plotar o gráfico
plt.plot(x_vals, M_vals, label='M(x)', color='blue')
plt.xlabel("x (m)")
plt.ylabel("Momento Fletor M(x) (kN.m)")
plt.title("Diagrama de Momento Fletor")
plt.axhline(0, color='black', linewidth=0.8)
plt.gca().invert_yaxis()  # Inverter o eixo y para convenção de engenharia
plt.grid()
plt.legend()
plt.show()