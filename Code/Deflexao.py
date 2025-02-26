from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor
import sympy as sp

class Deflexao():
    def __init__(self,retangulos=[],buracos=[],carregamentos=[],apoios=[]): ## Construtor da classe
        self.__momentoInercia = MomentoDeInercia()
        self.__momentoFletor = MomentoFletor()
        
        if retangulos != [] and carregamentos != []: ## Condição para testes automatizados
            self.__momentoInercia = MomentoDeInercia(retangulos,buracos)
            self.__momentoFletor = MomentoFletor(carregamentos,apoios)

    def set_figura(self): ## Função para ler o problema
        print("Defina a área de seção transversal.")
        self.__momentoInercia.setRetangulos_user()

        print("Defina os carregamentos.")
        self.__momentoFletor.set_carregamentos()

    def calcula_constantes(self):
        self.__momentoInercia.calcula()
        self.__momentoFletor.calcula()
        
        E = 200 ## Módulo de elasticidade do material em MPa



        

    