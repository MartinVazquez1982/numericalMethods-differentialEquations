import matplotlib.pyplot as plt

class MetodosNumericos:
    
    class Punto: # Se encarga de almacenar el 'x' y el 'y' aproximado
        
        def __init__(self,x, y, yReal=None):
            self.x = x
            self.y = y
            
        def __str__(self) -> str:
            salida = "Y("+str(self.x)+")= "+str(self.y)
            return salida
    
    def __init__(self, xInicial, xFinal, sistema, y) -> None:
        self.puntosIniciales = [MetodosNumericos.Punto(xInicial, sol) for sol in y]
        self.xN=xFinal
        self.sistema=sistema
    
    # Algoritmo General
    def _calculo(self, metodo, h):
        N=int((self.xN-self.puntosIniciales[0].x)/h+1)
        calculos=[self.puntosIniciales]
        t = self.puntosIniciales[0].x
        for i in range(1,N):
            p = metodo(calculos[i-1], h)
            calculos.append([MetodosNumericos.Punto(t+h, valor) for valor in p])
            t+=h
        return calculos
    
    # Metodo de Euler
    def euler(self, h):
        return self._calculo(self._eulerCalculo, h)
    
    # Es un metodo aparte asi lo puede usar tanto euler como eulerMejorado
    def _eulerCalculo(self, puntos, h):
        x, y = self._extraerPuntos(puntos)
        salSistema = self.sistema(x,y)
        salida = []
        for i in range(len(salSistema)):
            salida.append(y[i]+h*salSistema[i])
        return salida
        
    
    # Metodo de Euler Mejorado
    def eulerMejorado(self, h):
        
        def operacion(puntos, h):
            x, y = self._extraerPuntos(puntos)
            func1=self.sistema(x,y)
            func2=self.sistema(x+h, self._eulerCalculo(puntos, h))
            salida = []
            for i in range(len(func1)):
                salida.append(y[i]+h*(func1[i]+func2[i])/2)
            return salida
        
        return self._calculo(operacion, h)
    
    # Metodo de Runge-Kutta
    def rungeKutta(self, h):
        
        def operacion(puntos, h):
            x, y = self._extraerPuntos(puntos)
            yk = []
            k1=self.sistema(x, y)
            for i in range(len(y)):
                yk.append(y[i]+h/2*k1[i])
            k2=self.sistema(x+h/2, yk)
            for i in range(len(yk)):
                yk[i] = yk[i]+h/2*k2[i]
            k3=self.sistema(x+h/2, yk)
            for i in range(len(yk)):
                yk[i] = yk[i]+h*k3[i]
            k4=self.sistema(x+h, yk)
            salida = []
            for i in range(len(y)):
                salida.append(y[i]+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]))
            return salida
            
        return self._calculo(operacion, h)
    
    def _extraerPuntos(self, puntos):
        x = puntos[0].x
        yant = []
        for i in range(len(puntos)):
            yant.append(puntos[i].y)
        return x, yant

    def _sacarPuntos(self, soluciones):
        x=[]
        y=[]
        for i in range(len(soluciones[0])):
            y.append([])
        for i in range(len(soluciones)):
           x.append(soluciones[i][0].x)
           for k in range(len(soluciones[i])):
               y[k].append(soluciones[i][k].y)
        return x, y

    def graficar(self, puntos, nombres):
        x, y = self._sacarPuntos(puntos)
        fig, grafico = plt.subplots()
        for i in range(len(y)):
            grafico.plot(x, y[i], label=str(nombres[i]))
        grafico.legend()
        grafico.set_title('Aproximaciones Numericas')
        grafico.set_xlabel('t')
        grafico.set_ylabel('kg')
        plt.show()
        