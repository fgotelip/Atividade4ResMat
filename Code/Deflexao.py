from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor
import sympy as sp
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
        self.__momentoInercia.calcula() ## Calcula o momento de inércia
        I = self.__momentoInercia.get_Ixx() 

        self.__teta, self.__deflexao = self.__momentoFletor.get_Deflexao()

        ehEngastada, posContorno1,posContorno2 = self.__momentoFletor.get_posContorno() ## Posição de contorno

        E = 200 ## Módulo de elasticidade do material em MPa

        ## Cálculo das constantes
        C1 = sp.symbols('C1')
        C2 = sp.symbols('C2')

        if ehEngastada:
            self.__C1 = 0
            self.__C2 = -self.__deflexao.subs(x,posContorno2) ## Substitui o tamanho da viga na deflexão
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
        self.__teta += self.__C1
        self.__deflexao += self.__C1*x + self.__C2


    def plot_deflexao(self):
        self.__calcula_constantes()
        self.__gera_equacao_deflexao()

        









        
     





        

    