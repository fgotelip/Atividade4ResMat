import sympy as sp

## Classe para definir carregamentos e calcular suas informações
class Carregamento():
    def __init__(self,x1=0,x2=0,carga=0,tipo=0,carga2=0,pos=0): ## Construtor da classe
        self.__x1 =x1
        self.__x2 = x2
        self.__carga = carga
        self.__tipo = tipo
        self.__carga2 = carga2
        self.__x = sp.symbols('x')
        self.__posicao = 0
        self.__posicao2 = 0
        self.__resultante = 0
        self.__resultante2 = 0
        self.__momento = 0
        self.__teta = 0
        self.__v = 0
        self.__inclinacao = 0
        self.__h = 0
        self.__tam =self.__x2-self.__x1
      
        
        if self.__tipo == 1: ## Carregamento distribuído
            if self.__carga == self.__carga2: ## Retângulo
                self.__posicao = (self.__x1 +x2)/2 ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga ## Valor da força resultante

                self.__teta = -self.__carga/2*(self.__x-self.__x1)**3/3 ## Angulo de deflexão
                self.__v = -self.__carga/2*(self.__x-self.__x1)**4/12 ## Deflexão
                
            elif self.__carga == 0: ## Triângulo Retângulo crescente
                self.__posicao =x1+(self.__tam*2/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga2/2 ## Valor da força resultante

                self.__inclinacao = self.__carga2/self.__tam ## Inclinação da reta
                self.__teta = -self.__inclinacao/6*(self.__x-self.__x1)**4/4 ## Angulo de deflexão
                self.__v = -self.__inclinacao/6*(self.__x-self.__x1)**5/20

            elif self.__carga2 == 0: ## Triângulo Retângulo decrescente
                self.__posicao =x1+(self.__tam*1/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga/2 ## Valor da força resultante

                self.__inclinacao = -self.__carga/self.__tam ## Inclinação da reta
                self.__teta = -self.__inclinacao/6*(self.__x-self.__x1)**4/4 ## Angulo de deflexão
                self.__v = -self.__inclinacao/6*(self.__x-self.__x1)**5/20

            elif self.__carga > self.__carga2: ## Trapézio decrescente
                self.__posicao = (self.__x1 +x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga2 ## Valor resultante retângulo
                self.__posicao2 =x1+(self.__tam*1/3) ## Posição resultante triângulo
                self.__resultante2 = -self.__tam*(self.__carga-self.__carga2)/2 ## Valor resultante triângulo

                ## triângulo
                self.__h = self.__carga-self.__carga2 ## Altura do triângulo
                self.__inclinacao = -self.__h/self.__tam ## Inclinação da reta
                self.__teta = -self.__inclinacao/6*(self.__x-self.__x1)**4/4 ## Angulo de deflexão
                self.__v = -self.__inclinacao/6*(self.__x-self.__x1)**5/20 
                ## retângulo
                self.__teta += -self.__carga2/2*(self.__x-self.__posicao)**3/3 ## Angulo de deflexão
                self.__v += -self.__carga2/2*(self.__x-self.__posicao)**4/12 ## Deflexão

            elif self.__carga < self.__carga2: ## Trapézio crescente
                self.__posicao = (self.__x1 +x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga ## valor resultante retângulo
                self.__posicao2 =x1+(self.__tam*2/3) ## Posição resultante triângulo 
                self.__resultante2 = -self.__tam*(self.__carga2-self.__carga)/2 ## Valor resultante triângulo

                ## triângulo
                self.__h = self.__carga2-self.__carga  
                self.__inclinacao = self.__h/self.__tam
                self.__teta = -self.__inclinacao/6*(self.__x-self.__x1)**4/4 ## Angulo de deflexão
                self.__v = -self.__inclinacao/6*(self.__x-self.__x1)**5/20
                ## retângulo
                self.__teta += -self.__carga/2*(self.__x-self.__x1)**3/3 ## Angulo de deflexão
                self.__v += -self.__carga/2*(self.__x-self.__x1)**4/12 ## Deflexão

        elif self.__tipo == 2: ## Carga pontual
            self.__posicao =x1+pos ## Posição da força resultante
            self.__resultante = -self.__carga ## Valor da força resultante

            self.__teta = -self.__carga*(self.__x-self.__x1)**2/2 ## Angulo de deflexão
            self.__v = -self.__carga*(self.__x-self.__x1)**3/6 ## Deflexão

        elif self.__tipo == 3: ## Carga momento
            self.__posicao =x1+pos ## Posição do momento
            self.__momento = self.__carga ## Valor do momento

            self.__teta = -self.__momento*(self.__x-self.__x1) ## Angulo de deflexão
            self.__v = -self.__momento*(self.__x-self.__x1)**2/2 ## Deflexão
    
    def __calcula_deflexao_carregamento_deslocado(self): ## Calcula a deflexão para carregamento deslocado
        if self.__tipo == 1: ## Carregamento distribuído
            if self.__carga == self.__carga2: ## Retângulo
                self.__teta += self.__carga/2*(self.__x-self.__x2)**3/3 ## Angulo de deflexão
                self.__v += self.__carga/2*(self.__x-self.__x2)**4/12 ## Deflexão

            elif self.__carga == 0 or self.__carga2 ==0: ## Triângulo Retângulo
                self.__teta += self.__inclinacao/6*(self.__x-self.__x2)**4/4 ## Angulo de deflexão
                self.__v += self.__inclinacao/6*(self.__x-self.__x2)**5/20 ## Deflexão

            else: ## Trapézio decrescente
                ## triângulo
                self.__teta += self.__inclinacao/6*(self.__x-self.__x2)**4/4
                self.__v += self.__inclinacao/6*(self.__x-self.__x2)**5/20
                ## retângulo
                self.__teta += self.__carga2/2*(self.__x-self.__x2)**3/3
                self.__v += self.__carga2/2*(self.__x-self.__x2)**4/12

    def get_deflexao(self,xfinal): ## Retornar o angulo de deflexão e a deflexão
        if xfinal != self.__x2: ## Se o carregamento for deslocado
            self.__calcula_deflexao_carregamento_deslocado(self.__x2) ## Calcula a deflexão para carregamento deslocado
        
        if self.__tipo == 2 or self.__tipo == 3: ## Se for carga pontual ou momento
            if xfinal == self.__x2: ## Se estiver no final da viga
                self.__teta = 0
                self.__v = 0

        return self.__teta,self.__v
    
    def get_tipo(self): ## Retornar o tipo de carregamento
        return self.__tipo

    def get_posicao(self): ## Retornar posição da resultante
        return self.__posicao
    
    def get_posicao2(self): ## Retornar posição da segunda resultante(Trapézios)
        return self.__posicao2
 
    def get_resultante(self): ## Retornar a resultante
        return self.__resultante

    def get_resultante2(self): ## Retornar a segunda resultante (Trapézios)
        return self.__resultante2
    
    def get_momento(self):
        return self.__momento

    def get_x1(self): ## Retorna o início do carregamento
        return self.__x1

    def get_x2(self): ## Retorna o fim do carregamento
        return self.__x2
    
  

 
              
            













