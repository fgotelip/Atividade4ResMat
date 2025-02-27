from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
x = sp.symbols('x')
class Deflexao():
    def __init__(self,retangulos=[],buracos=[],carregamentos=[],apoios=[]): ## Construtor da classe
        self.__momentoInercia = MomentoDeInercia()
        self.__momentoFletor = MomentoFletor()
        self.__C1 = 0
        self.__C2 = 0
        self.__teta = 0
        self.__deflexao = 0
        
        if retangulos != [] and carregamentos != []: ## Condição para testes automatizados
            self.__momentoInercia = MomentoDeInercia(retangulos,buracos)
            self.__momentoFletor = MomentoFletor(carregamentos,apoios)

    def set_figura(self): ## Função para ler o problema
        print("Defina a área de seção transversal.")
        self.__momentoInercia.setRetangulos_user()

        print("Defina os carregamentos.")
        self.__momentoFletor.set_carregamentos()

    def __calcula_constantes(self):
        self.__teta, self.__deflexao = self.__momentoFletor.get_Deflexao()

        ehEngastada, posContorno1,posContorno2 = self.__momentoFletor.get_posContorno() ## Posição de contorno

        ## Cálculo das constantes
        C1 = sp.symbols('C1')
        C2 = sp.symbols('C2')

        if ehEngastada:
            self.__C1 = 0
            self.__C2 = 0
        else: ## Se a viga for biapoiada
            if posContorno1 == 0 or posContorno2 == 0: ## Se o apoio de 2 ou 1 genero estiver no inicio da viga
                self.__C2 = 0
                if posContorno1 == 0: ## Se o apoio de 2 genero estiver no inicio da viga
                    self.__C1 = -self.__deflexao.subs(x,posContorno2)/posContorno2 ## Substitui a posição do apoio de 1 genero na deflexão

                else: ## Se o apoio de 1 genero estiver no inicio da viga
                    self.__C1 = -self.__deflexao.subs(x,posContorno2)/posContorno2 ## Substitui a posição do apoio de 2 genero na deflexão

            else: ## Se os apoios não estiverem no inicio da viga
                eq1 = sp.Eq(C1*posContorno1 + C2 + self.__deflexao.subs(x,posContorno1),0) ## Equação 1
                eq2 = sp.Eq(C1*posContorno2 + C2 + self.__deflexao.subs(x,posContorno2),0) ## Equação 2
                sol = sp.solve((eq1,eq2),(C1,C2)) ## Resolve o sistema de equações
                self.__C1 = sol[C1]
                self.__C2 = sol[C2]
    
    def __gera_equacao_deflexao(self):
        self.__momentoInercia.calcula() ## Calcula o momento de inércia
        I = self.__momentoInercia.get_Ixx() 

        E = 200 ## Módulo de elasticidade do material em Pa
     
        EIm = E*I*10**-6 ## Módulo de elasticidade vezes o momento de inércia em Nm^2

        self.__teta = (self.__teta+self.__C1)/(EIm) ## Equação do ângulo de deflexão
        
        self.__deflexao = (self.__deflexao + self.__C1*x + self.__C2)/(EIm) ## Equação da deflexão
        #print(self.__deflexao*E*I)


    def plot_deflexao(self):
        self.__calcula_constantes()
        self.__gera_equacao_deflexao()
        
        ## angulo de deflexao
        Teta_real = sp.lambdify(x,self.__teta,"numpy")
        x_vals_teta = np.linspace(0,self.__momentoFletor.get_xfinal(),1000)
        y_vals_teta = Teta_real(x_vals_teta)

        print("Ângulo de deflexão máximo em módulo: ",max(abs(y_vals_teta)))

        ## deflexao
        V_real = sp.lambdify(x,self.__deflexao,"numpy")
        x_vals_v = np.linspace(0,self.__momentoFletor.get_xfinal(),1000)
        y_vals_v = V_real(x_vals_v)

        print("Deslocamento vertical máximo em módulo: ",max(abs(y_vals_v)))

        ## plota angulo de deflexao
        plt.figure(figsize=(10, 5))
        plt.plot(x_vals_teta,y_vals_teta, label=r'$\theta(x)$', color='b', linewidth=2)

        plt.xlabel("x (m)")
        plt.ylabel(r"$\theta$ (rad)")
        plt.title("Gráfico da Deflexão Angular $\theta(x)$")
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        
        plt.show()

        ## plota deflexao
        plt.figure(figsize=(10, 5))
        plt.plot(x_vals_v,y_vals_v, label=r'$v(x)$', color='b', linewidth=2)
        
        plt.xlabel("x (m)")
        plt.ylabel(r"$v$ (m)")
        plt.title("Gráfico da Deflexão $v(x)$")
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()

        plt.show()
            









        
     





        

    