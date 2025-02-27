from Carregamento import Carregamento
from Apoio import Apoio
from Retangulo import Retangulo
from Deflexao import Deflexao

## Execução principal do exercício 3

#T3
#carregamentos = [ Carregamento(0,1.5,100,1,100),Carregamento(1.5,2,-20,3,0,0.25),Carregamento(2,3,40,3,0,1),Carregamento(3,3.75,0,1,150),Carregamento(3.75,4,30,2,0,0),Carregamento(4,5,100,1,10),Carregamento(5,6,30,2,0,0.75)]
carregamentos = [ Carregamento(0,3,-15,3,0,3),Carregamento(3,6,30,1,60)]
apoios = [Apoio(0,2),Apoio(6,1)]
retangulos=[Retangulo(0,100,0,100)]
buracos=[]

deflexao = Deflexao(retangulos,buracos,carregamentos,apoios)
deflexao.plot_deflexao()

'''
flexao2 = Flexao()
flexao2.set_figura()
flexao2.exibe_resultados()
'''