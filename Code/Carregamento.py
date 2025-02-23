import sympy as sp

## Classe para definir carregamentos e calcular suas informações
class Carregamento():
    def __init__(self, x1=0, x2=0,carga=0,tipo=0,carga2=0,pos=-1): ## Construtor da classe
        self.__x1 = x1
        self.__x2 = x2
        self.__carga = carga
        self.__tipo = tipo
        self.__carga2 = carga2
        self.__pos = pos
        self.__tam = x2-x1
        self.__x = sp.symbols('x')
        self.__posicao = 0
        self.__posicao2 = 0
        self.__resultante = 0
        self.__resultante2 = 0
        self.__momento = 0
        self.__w = 0
        self.__v = 0
        self.__v2 = None
        self.__m = 0
        self.__m2 = None
        
        if self.__tipo == 1: ## Carregamento distribuído
            if self.__carga == self.__carga2: ## Retângulo
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga ## Valor da força resultante

                self.__w = self.__carga ## Valor da carga

            elif self.__carga == 0: ## Triângulo Retângulo crescente
                self.__posicao = self.__x1+(self.__tam*2/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga2/2 ## Valor da força resultante

                self.__w = (self.__carga2/self.__tam)*self.__x ## Valor da carga

            elif self.__carga2 == 0: ## Triângulo Retângulo decrescente
                self.__posicao = self.__x1+(self.__tam*1/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga/2 ## Valor da força resultante

                self.__w = self.__carga - (self.__carga/self.__tam)*self.__x

            elif self.__carga > self.__carga2: ## Trapézio decrescente
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga2 ## Valor resultante retângulo
                self.__posicao2 = self.__x1+(self.__tam*1/3) ## Posição resultante triângulo
                self.__resultante2 = -self.__tam*(self.__carga-self.__carga2)/2 ## Valor resultante triângulo

                self.__w = -((self.__carga-self.__carga2)/self.__tam)*self.__x + self.__carga ## Valor da carga

            elif self.__carga < self.__carga2: ## Trapézio crescente
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga ## valor resultante retângulo
                self.__posicao2 = self.__x1+(self.__tam*2/3) ## Posição resultante triângulo 
                self.__resultante2 = -self.__tam*(self.__carga2-self.__carga)/2 ## Valor resultante triângulo

                self.__w = ((self.__carga2-self.__carga)/self.__tam)*self.__x + self.__carga ## Valor da carga

        elif self.__tipo == 2: ## Carga pontual
            self.__posicao = self.__x1+pos ## Posição da força resultante
            self.__resultante = -self.__carga ## Valor da força resultante

        elif self.__tipo == 3: ## Carregamento por f(X)
            self.__w = sp.sympify(self.__carga)
            forca = sp.integrate(self.__w,(self.__x,0,self.__tam)) ## Valor força resultante
            self.__resultante = -float(forca)
            momento = sp.integrate(self.__w * self.__x,(self.__x, 0, self.__tam)) ## Momento resultante
            posicao = float(momento / forca) ## Posição força resultante
            self.__posicao = self.__x1 + posicao ## Posição resultante em relação a viga toda
        
        elif self.__tipo == 4: ## Carga momento
            self.__posicao = self.__x1+pos ## Posição do momento
            self.__momento = -self.__carga ## Valor do momento

    def geraEsforcos(self,vant,mant,xant=0): ## Função para gerar os esforços na barra
        tamAnt = self.__x1 - xant 
        self.__gera_vx(vant,tamAnt) ## Chama para o calculo do cortante 
        self.__gera_mx(mant,tamAnt) ## Chama para o calculo do fletor
        print("M1",self.__m)
        if self.__tipo == 2 or self.__tipo == 4:
            if self.__m2 != None:
                print("M2",self.__m2)
    
    def __gera_vx(self,vant,tamAnt): ## Função para calcular o cortante
        
        if isinstance(vant,sp.Basic): ## Confere se é função
            vant = vant.subs(self.__x,tamAnt) ## Cortante anterior

        if self.__tipo == 2 or self.__tipo == 4: ## Carregamento pontual ou momento
            v = vant
            if self.__tipo == 2: ## Carregamento pontual
                v2 = vant + self.__resultante ## Segunda cortante 
                if self.__pos == 0: ## Se a força está no início da barra
                    self.__v = v2
                elif self.__pos == self.__tam: ## Se a força está no final da barra
                    self.__v = v
                else: 
                    self.__v = v
                    self.__v2 = v2
            elif self.__tipo == 4: ## Carga Momento
                self.__v = v


        else: ## Carregamento distribuído e f(X)
            self.__v = sp.integrate(-self.__w,self.__x) + vant

    def __gera_mx(self,mant,tamAnt): ## Função para calcular o fletor
        if isinstance(mant,sp.Basic): ## Confere se é função
            mant = mant.subs(self.__x,tamAnt)
    

        m = sp.integrate(self.__v,self.__x) + mant

        if self.__tipo == 2 or self.__tipo == 4: ## Carregamento pontual ou momento
            if self.__tipo == 2 and self.__v2 != None: ## Carregamento pontual
                mant2 = m.subs(self.__x,self.__pos)
                m2 = sp.integrate(self.__v2,self.__x) + mant2
            elif self.__tipo == 4: ## Carga Momento
                mant2 = m.subs(self.__x,self.__pos)
                termo_independente = m.subs(self.__x,0) ## Termo independente da função
                m2 = m.subs(termo_independente,mant2+self.__momento) ## Calcula o segundo fletor subtraindo o termo independente

            if self.__pos == 0: ## Se a força(ou o momento) está no início da barra
                self.__m = m
            elif self.__pos == self.__tam: ## Se a força(ou o momento) está no final da barra
                self.__m = m
            else:
                self.__m = m
                self.__m2 = m2

        else: ## Carregamento distribuído e f(X)
            self.__m = m
        
        

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
        return -self.__momento

    def get_x1(self): ## Retorna o início do carregamento
        return self.__x1

    def get_x2(self): ## Retorna o fim do carregamento
        return self.__x2
    
    def get_v(self): ## Retorna o cortante
        return self.__v
    
    def get_v2(self): ## Retorna o segundo cortante
        return self.__v2
    
    def get_m(self): ## Retorna o fletor 
        return self.__m
    
    def get_m2(self): ## Retorna o segundo fletor
        return self.__m2













