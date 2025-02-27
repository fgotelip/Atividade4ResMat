from Carregamento import Carregamento
from Apoio import Apoio
from Retangulo import Retangulo
from Deflexao import Deflexao

retangulos=[Retangulo(0,100,0,100)]
buracos=[]

carregamentos1 = [ Carregamento(0,5,150,1,150),Carregamento(5,5,-100,3),Carregamento(5,9,110,2,0,4)]
apoios1 = [Apoio(0,3),0]

deflexao1 = Deflexao(retangulos,buracos,carregamentos1,apoios1)
deflexao1.plot_deflexao()


'''carregamentos2 = [ Carregamento(0,3,-15,3,0,3),Carregamento(3,6,30,1,60)]
apoios2 = [Apoio(0,2),Apoio(6,1)]

deflexao2 = Deflexao(retangulos,buracos,carregamentos2,apoios2)
deflexao2.plot_deflexao()'''

'''carregamentos3 = [Carregamento(0,4,30,2),Carregamento(4,6,50,1,50)]
apoios3 = [Apoio(2,2),Apoio(6,1)]

deflexao3 = Deflexao(retangulos,buracos,carregamentos3,apoios3)
deflexao3.plot_deflexao()'''


'''deflexao4 = Deflexao()
deflexao4.set_figura()
deflexao4.plot_deflexao()'''
