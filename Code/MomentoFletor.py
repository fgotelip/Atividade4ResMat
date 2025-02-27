from Carregamento import Carregamento
from Apoio import Apoio
from Confere import eh_numero,eh_opcao,eh_funcao,esta_no_intervalo,eh_sim_nao
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

## Classe para ler os carregamentos e calcular informações básicas da viga
class MomentoFletor(): ## Construtor da classe
    def __init__(self,carregamentos=[],apoios=[]):
        self.__apoios = [0,0]
        self.__carregamentos = []
        self.__Mtotal = 0
        self.__forcasy = []
        self.__momentos = []

        if apoios != []: ## Condição para testes automatizados
            self.__apoios = apoios

        if carregamentos != []: ## Condição para testes automatizados
            self.__carregamentos.append(Carregamento())
            for carregamento in carregamentos:
                self.__aux_set_carregamentos(carregamento)
            self.__xfinal = carregamentos[-1].get_x2()


    def get_Mtotal(self): ## Retorna o momento total
        return self.__Mtotal

    def __aux_set_carregamentos(self,carregamento): ## Função auxiliar para definir carregamentos
        if carregamento.get_tipo() != 3: ## Caso não seja Carga Momento
            dist = carregamento.get_posicao() - self.__apoios[0].get_pos() ## Distância do carregamento até o apoio
            self.__carregamentos.append(carregamento)
            self.__forcasy.append(carregamento.get_resultante()) ## Soma a força gerada pelo carregamento
            self.__momentos.append(carregamento.get_resultante()*dist) ## Soma o momento gerado pelo carregamento

            if carregamento.get_resultante2() != 0: ## Caso seja trapézio
                dist2 = carregamento.get_posicao2() - self.__apoios[0].get_pos()
                self.__forcasy.append(carregamento.get_resultante2())
                self.__momentos.append(carregamento.get_resultante2()*dist2)
        else: ## Caso seja Carga Momento
            self.__carregamentos.append(carregamento)
            self.__momentos.append(carregamento.get_momento())


    def __define_apoios(self,pos,antes_depois): ## função para definir os apoios
        if self.__apoios[0] == 0 or self.__apoios[1] == 0:

            sim_nao = input("Existe um apoio "+antes_depois+" da viga? (s/n): ") ## Onde está o apoio
            while not eh_sim_nao(sim_nao): ## Permite apenas entradas corretas
                sim_nao = input("Existe um apoio"+antes_depois+" da viga? (s/n): ")
            if sim_nao.lower() == 's':

                if self.__apoios[0] == 0 and self.__apoios[1] == 0: ## Caso nenhum apoio tenha sido iniciado
                    tipo = input("Escolha o tipo de apoio:\n1-2o Gênero\n2-1o Gênero")
                    while not eh_opcao(tipo,12): ## Permite apenas entradas corretas
                        tipo = input("Escolha o tipo de apoio:\n1-2o Gênero\n2-1o Gênero")
                    tipo = int(tipo)
                    if tipo == 1: ## Inicia um apoio de segundo gênero
                        self.__apoios[0]=Apoio(pos,tipo)
                    else: ## Inicia um apoio de primeiro gênero
                        self.__apoios[1]=Apoio(pos,tipo)

                elif self.__apoios[0] == 0: ## Caso já tenha um apoio de primeiro gênero
                    print("Apoio de 2o gênero definido.")
                    self.__apoios[0]=Apoio(pos,2)

                elif self.__apoios[1] == 0: ## Caso já tenha um apoio de segundo gênero
                    print("Apoio de 1o gênero definido.")
                    self.__apoios[1]=Apoio(pos,1)

    def set_carregamentos(self): ## Função para definir os carregamentos
        print("Escolha o tipo de viga:\n1-Biapoiada Simples\n2-Biapoiada com balanço\n3-Engastada Livre")
        tipo = input("Tipo de viga: ")
        while not eh_opcao(tipo,123): ## Permite apenas entradas corretas
            tipo = input("Tipo de viga: ")
        tipo_viga = int(tipo)

        if tipo_viga == 3: ## Viga engastada livre
            self.__apoios[0] = Apoio(0,3)
        elif tipo_viga == 1: ## Viga biapoiada simples
            self.__apoios[0] = Apoio(0,2)

        num_carregamentos = input("Número de carregamentos= ") ## Número de carregamentos na viga
        while not eh_numero(num_carregamentos):
            num_carregamentos = input("Número de carregamentos= ")
        num_carregamentos = int(num_carregamentos)

        x2Ant = 0 ## Final do último carregamento

        self.__carregamentos.append(Carregamento())

        for i in range(num_carregamentos): ## Loop para instanciar carregamentos
            if tipo_viga == 2: ## Definir os apoios da viga em balanço
                self.__define_apoios(x2Ant,"antes")

            print("Vamos definir o carregamento", i, "(cargas em N/m - N - N*m; tamanho da barra em m):")
            print("tamanho da barra = 0 - define carga pontual entre carregamentos")

            x1 = x2Ant ## Inicio de uma barra começa no fim da outra

            tam = input("Tamanho da barra = ") ## Tamanho da barra
            while not eh_numero(tam,True):
                tam = input("Tamanho da barra =  ")
            tam = float(tam)

            x2=x1+tam ## Final da barra inserida
            x2Ant = x2

            opcao = input("Como é dada a distribuição de cargas?\n1-Carga Distribuída\n2-Carga Pontual\n3-Carga Momento\n: ") ## Diferentes tipos de carregamento
            while not eh_opcao(opcao,123):
                opcao = input("Como é dada a distribuição de cargas?\n1-Carga Distribuída\n2-Carga Pontual\n3-Carga Momento\n: ")
            self.__opcao = int(opcao)

            if self.__opcao == 1: ## Carregamento distribuido
                carga1 = input("Carga 1 = ") ## Valor inicial da carga
                while not eh_numero(carga1,True):
                    carga1 = input("Carga 1 =   ")
                carga1 = float(carga1)

                carga2 = input("Carga 2 =  ") ## Valor final da carga
                while not eh_numero(carga2,True):
                    carga2 = input("Carga 2 =  ")
                carga2 = float(carga2)
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga1,self.__opcao,carga2))

            elif self.__opcao == 2: ## Carregamento pontual
                carga = input("Carga = ") ## Valor da carga
                while not eh_numero(carga):
                    carga1 = input("Carga =  ")
                carga = float(carga)

                if tam != 0:
                    pos = input("Posição da carga = ")
                    while not esta_no_intervalo(pos,0,tam):
                        pos = input("Posição da carga =  ")
                    pos=float(pos)
                else: ## Carga entre carregamentos
                    pos = 0
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga,self.__opcao,0,pos))

            elif self.__opcao == 3: ## Carga Momento
                carga = input("Carga Momento = ")
                while not eh_numero(carga,False,True):
                    carga = input("Carga Momento =  ")
                carga = float(carga)

                if tam != 0:
                    pos = input("Posição do momento = ")
                    while not esta_no_intervalo(pos,0,tam):
                        pos = input("Posição do momento =  ")
                    pos=float(pos)
                else: ## Momento entre carregamentos
                    pos = 0
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga,self.__opcao,0,pos))

            if tipo_viga == 2: ## Define os apoios da viga em balanço
                self.__define_apoios(x2,"depois")

        if tipo_viga == 1: ## Define os apoios da viga biapoiada simples
            self.__apoios[1]=Apoio(x2,1)
        self.__xfinal = x2


    def __calcularReacoes(self): ## Função para calcular as reações de apoio
        if self.__apoios[1] != 0:
            dist = self.__apoios[1].get_pos() - self.__apoios[0].get_pos()
            by = -sum(self.__momentos)/dist ## Reação de apoio
            self.__apoios[1].set_reacao(-by)
            self.__forcasy.append(by)
            self.__carregamentos.append(Carregamento(self.__apoios[1].get_pos(),self.__apoios[1].get_pos(),self.__apoios[1].get_reacao(),2,0)) ## Adiciona a reação de apoio de 1o gênero aos carregamentos
        else: ## Viga engastada
            self.__apoios[0].set_momento(-sum(self.__momentos))
            self.__carregamentos.append(Carregamento(self.__apoios[0].get_pos(),self.__apoios[0].get_pos(),self.__apoios[0].get_momento(),3,0)) ## Adiciona o momento de apoio aos carregamentos

        ay = -sum(self.__forcasy)
        self.__apoios[0].set_reacao(-ay)

        self.__carregamentos.append(Carregamento(self.__apoios[0].get_pos(),self.__apoios[0].get_pos(),self.__apoios[0].get_reacao(),2,0)) ## Adiciona a reação de apoio de 2o gênero aos carregamentos

        

    def get_Deflexao(self): ## Retorna o angulo de deflexão e a deflexão
        self.__calcularReacoes() ## Calcula as reações de apoio
        teta = 0
        deflexao = 0
        for carregamento in self.__carregamentos: ## Loop para percorrer os carregamentos
            tetai,deflexaoi = carregamento.get_deflexao(self.__xfinal)
            teta += tetai
            deflexao += deflexaoi
        return teta,deflexao
    
    def get_posContorno(self): ## Retorna a posição dos apoios
        if self.__apoios[0].get_tipo() == 3: ## Se for viga engastada
            return True,self.__apoios[0].get_pos(),self.__xfinal
        ## Se não for viga engastada
        return False,self.__apoios[0].get_pos(),self.__apoios[1].get_pos()
    
    def get_xfinal(self):
        return self.__xfinal
        


