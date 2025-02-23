from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor

## Classe para executar os calculos previstos para o exercício 2
## Classe para executar os calculos previstos para o exercício 2
class Flexao():
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

    def exibe_resultados(self):
        self.__momentoInercia.exibirResultados()
        self.__momentoFletor.calcula()

    