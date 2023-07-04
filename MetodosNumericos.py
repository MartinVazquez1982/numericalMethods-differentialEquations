import matplotlib.pyplot as plt
from numpy import arange

class MetodosNumericos:
    
    # Cuando quieres graficar un metodo con distintos pasos (h), Le tenes que pasar por parametro uno de estos 3
    EULER="Euler"
    EULERMEJORADO="Euler Mejorado"
    RUNGEKUTTA="Runge-Kutta"
    
    class Punto: # Se encarga de almacenar el 'x' y el 'y' aproximado
        
        def __init__(self,x, y, yReal=None):
            self.x = x
            self.y = y
            self.yReal = yReal
            
        def __str__(self) -> str:
            salida = "Y("+str(self.x)+")= "+str(self.y)
            if self.yReal != None:
                salida = salida + " | Real: Y("+str(self.x)+")= " + str(self.yReal) + " Error: " + str(abs(self.y - self.yReal))
            return salida
            
    class ArrayAux: # Clase especial que almacena dos arreglos con los valores calculados
        
        def __init__(self, punto):
            self.x = [punto.x]
            self.y = [punto.y]
        
        def append(self, punto):
            self.x.append(punto.x)
            self.y.append(punto.y)
    
    def __init__(self, xInicial, xFinal,yInicial, funcion, funcionDesconocida=None, hFD=None) -> None:
        self.puntoInicial=MetodosNumericos.Punto(xInicial, yInicial)
        self.xN=xFinal
        self.funcion=funcion
        self.aux = None #Es un Arrayaux que almacena los valores de la ultima aproximacion calculada, asi se puede graficar
        self.funcionDesconocida = funcionDesconocida
        if self.funcionDesconocida != None and hFD != None:
            self.xDesconocida = arange(xInicial, xFinal, hFD)
            self.yDesconocida = [funcionDesconocida(x) for x in self.xDesconocida]
        else:
            self.xDesconocida = None
            self.yDesconocida = None
    
    # Algoritmo General
    def _calculo(self, metodo, h):
        N=int((self.xN-self.puntoInicial.x)/h+1)
        calculos=[self.puntoInicial]
        t = self.puntoInicial.x
        calcularError = False
        if self.funcionDesconocida != None: calcularError = True
        self.aux = MetodosNumericos.ArrayAux(self.puntoInicial)
        for i in range(1,N):
            p = None
            if calcularError:
                p = MetodosNumericos.Punto(t+h, metodo(calculos[i-1].x, calculos[i-1].y, h), self.funcionDesconocida(t+h))
            else:
                p = MetodosNumericos.Punto(t+h, metodo(calculos[i-1].x, calculos[i-1].y, h))
            calculos.append(p)
            self.aux.append(p)
            t+=h
        return calculos
    
    # Metodo de Euler
    def euler(self, h):
        return self._calculo(self._eulerCalculo, h)
    
    # Es un metodo aparte asi lo puede usar tanto euler como eulerMejorado
    def _eulerCalculo(self,x, y, h):
        return y+h*self.funcion(x,y)
    
    # Metodo de Euler Mejorado
    def eulerMejorado(self, h):
        
        def operacion(x, y, h):
            func1=self.funcion(x,y)
            func2=self.funcion(x+h, self._eulerCalculo(x, y, h))
            return y+h*(func1+func2)/2
        
        return self._calculo(operacion, h)
    
    # Metodo de Runge-Kutta
    def rungeKutta(self, h):
        
        def operacion(x, y, h):
            k1=self.funcion(x, y)
            k2=self.funcion(x+h/2, y+h/2*k1)
            k3=self.funcion(x+h/2, y+h/2*k2)
            k4=self.funcion(x+h, y+h*k3)
            return y + h/6*(k1+2*k2+2*k3+k4)
            
        return self._calculo(operacion, h)
    
    # Hace un grafico comparando los distintos metodos, no es necesario pasar todos
    def graficoDistintosMetodos(self,hEuler=None, hEulerMejorado=None, hRungeKutta=None):
        fig, grafico = plt.subplots()
        if hEuler != None:
            self.euler(hEuler)
            grafico.plot(self.aux.x, self.aux.y, label="Euler")
        if hEulerMejorado != None:
            self.eulerMejorado(hEulerMejorado)
            grafico.plot(self.aux.x, self.aux.y, label="Euler Mejorado")
        if hRungeKutta != None:
            self.rungeKutta(hRungeKutta)
            grafico.plot(self.aux.x, self.aux.y, label="Runge-Kutta")
        if self.funcionDesconocida != None and self.yDesconocida != None:
            grafico.plot(self.xDesconocida, self.yDesconocida, label="Funcion Desconocida")
        grafico.legend()
        grafico.set_title('Comparacion de Metodos Numericos')
        grafico.set_xlabel('x')
        grafico.set_ylabel('y')
        plt.show()
    
    # Metodo auxiliar para saber que metodo elegio el usuario para comparar los pasos
    def reconocerMetodo(self,metodo):
        if metodo == "Euler":
            return self.euler
        elif metodo == "Euler Mejorado":
            return self.eulerMejorado
        elif metodo == "Runge-Kutta":
            return self.rungeKutta
        else:
            raise ValueError("Simbolo No valido")
    
    # Metodo que grafica un metodo pero con distintos pasos
    def graficoDiferentesPasos(self, metodo, pasos):
        calculo = self.reconocerMetodo(metodo)
        fig, grafico = plt.subplots()
        for paso in pasos:
            calculo(paso)
            grafico.plot(self.aux.x, self.aux.y, label="h = "+str(paso))
        if self.funcionDesconocida != None and self.yDesconocida != None:
            grafico.plot(self.xDesconocida, self.yDesconocida, label="Funcion Desconocida")
        grafico.legend()
        grafico.set_title('Comparacion Metodo de '+metodo)
        grafico.set_xlabel('x')
        grafico.set_ylabel('y')
        plt.show()