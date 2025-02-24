from Carregamento import Carregamento
from Apoio import Apoio
from Retangulo import Retangulo
from Flexao import Flexao

## Execução principal do exercício 3

#T3
#carregamentos = [ Carregamento(0,1.5,100,1,100),Carregamento(1.5,2,-20,4,0,0.25),Carregamento(2,3,40,4,0,1),Carregamento(3,3.75,"133.3333*x",3),Carregamento(3.75,4,30,2,0,0),Carregamento(4,5,100,1,10),Carregamento(5,6,30,2,0,0.75)]
carregamentos = [ Carregamento(0,2,100,1,100),Carregamento(2,4,-20,4,0,1),Carregamento(4,6,20,1,0)]
apoios = [Apoio(0,2),Apoio(6,1)]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

flexao = Flexao(retangulos,buracos,carregamentos,apoios)
flexao.exibe_resultados()

'''
flexao2 = Flexao()
flexao2.set_figura()
flexao2.exibe_resultados()
'''