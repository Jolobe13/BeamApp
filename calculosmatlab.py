from sympy import symbols, Symbol, simplify, integrate, diff, sin,solve,sympify, tan, cos, pretty,lambdify
import numpy as np
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr

class Calculadora():
    def __init__(self):
        self.n=input("Indique el número de tramos:")
        # Inicializar listas
        self.Vz, self.Vz0 = [], []
        self.My,self.My0 = [],[]
        self.theta, self.theta0= [], []
        self.w, self.w0= [],[]
        self.N, self.N0 = [],[]
        self.U, self.U0= [], []
        self.L, self.Qz, self.Qx= [],[], []
        #self.q=[Symbol("q")]
        #self.Q=[Symbol("Q")]
        self.qz=[]
        self.qx=[]
        self.dVz_dx = []
        self.dMy_dx = []
        self.dtheta_dx = []
        self.dw_dx = []
        self.dN_dx = []
        self.dU_dx = []
        self.listavariables, self.listavalores=[],[]
        self.listacargas=[]
        self.listaapoyos=[]
        self.equal = input("Deseas que todos los tramos tengan la misma longitud L? (s/n):")
        if self.equal == "s":
            for i in range(1, int(self.n) + 1):
                self.L.append(Symbol("L"))
         #   self.valor_longitud = input("Ingrese valor de L: ")
          #  for i in range(1, int(self.n) + 1):
           #     self.listavalores.append(self.valor_longitud)
        elif self.equal == "n":
            for i in range(1, int(self.n) + 1):
                self.L.append(Symbol(f"L{i}"))
          #      self.listavalores.append(input(f"Ingrese valor de L{i}: "))

        self.crear_variables()
        self.preguntar_apoyos()
        self.preguntar_cargas()


        print(self.listaapoyos)
        print(self.listacargas)
        print(self.listavalores)

        self.calcular()
        self.graficas()

    def crear_variables(self):
        for i in range(1, int(self.n) + 1):
            self.Vz.append(Symbol(f'Vz{i}'))
            self.Vz0.append(Symbol(f'Vz0{i}'))
            self.My.append(Symbol(f'My{i}'))
            self.My0.append(Symbol(f'My0{i}'))
            self.theta.append(Symbol(f'theta{i}'))
            self.theta0.append(Symbol(f'theta0{i}'))
            self.w.append(Symbol(f'w{i}'))
            self.w0.append(Symbol(f'w0{i}'))
            self.N.append(Symbol(f'N{i}'))
            self.N0.append(Symbol(f'N0{i}'))
            self.U.append(Symbol(f'U{i}'))
            self.U0.append(Symbol(f'U0{i}'))
            self.EI, self.EA, self.x, self.alpha = symbols('EI EA x alpha')
            self.dVz_dx.append(diff(self.Vz[-1], self.x))
            self.dMy_dx.append(diff(self.My[-1], self.x))
            self.dtheta_dx.append(diff(self.theta[-1], self.x))
            self.dw_dx.append(diff(self.w[-1], self.x))
            self.dN_dx.append(diff(self.N[-1], self.x))
            self.dU_dx.append(diff(self.U[-1], self.x))
        self.listavariables.extend(
            [self.Vz, self.Vz0, self.My, self.My0, self.theta, self.theta0, self.w,
             self.w0, self.N, self.N0, self.U, self.U0])
        # Convertimos lista de listas a lista plana
        self.listavariables = [var for sublist in self.listavariables for var in sublist]
        for i in range(len(self.listavariables)):
            self.listavalores.append("0")
        print(self.listavariables)
        #print(self.listavalores)
    def preguntar_cargas(self):
        self.simbolos_conocidos = {
            "Q": Symbol("Q"),
            "q": Symbol("q"),
            "x": Symbol("x"),
            "alpha": Symbol("alpha"),
            "EI": Symbol("EI"),
            "EA":Symbol("EA")
        }
        for i in range(1, int(self.n) + 1):
            self.simbolos_conocidos[f"q{i}"] = Symbol(f"q{i}")
            self.simbolos_conocidos[f"Q{i}"] = Symbol(f"Q{i}")
            self.simbolos_conocidos[f"L{i}"] = Symbol(f"L{i}")
        for i in range(1, int(self.n) + 1):
            self.qz.append(parse_expr(input(f"Ingrese expresion de la componente vertical del tramo{i}: "),local_dict=self.simbolos_conocidos))#sympify para convertir a valor simbolico
            self.qx.append(parse_expr(input(f"Ingrese expresion de la componente horizontal del tramo{i}: "),local_dict=self.simbolos_conocidos))
        self.preguntar_cargas_puntuales=input("¿hay alguna carga puntual?(s/n): ")
        if self.preguntar_cargas_puntuales=="s":
            print("Ingrese expresion de la carga puntual (ej: Q,-Q,0) en cada apoyo")
            for i in range(1, int(self.n) + 2):
                self.Qz.append(parse_expr(input(
                    f"Ingrese expresion de la componente vertical para el apoyo {i}: "),local_dict=self.simbolos_conocidos))  # sympify para convertir a valor simbolico
                self.Qx.append(parse_expr(input(f"Ingrese expresion de la componente horizontal para el apoyo{i}: "),local_dict=self.simbolos_conocidos))
        print(self.qz)
        print(self.Qz)
        print(self.Qx)

    def preguntar_apoyos(self):
        print("Ingrese tipo de apoyo (ej: 1,2,3,4) del...\n1:apoyo empotrado(theta=0,w=U=0)    2:apoyo movil(M=0)\n3:apoyo fijo(M=0,w=U=0)    4:sin apoyo(M=0)")
        for i in range(1,int(self.n)+2):
            self.listaapoyos.append(input(f"apoyo {i}: "))
    def calcular(self):
        self.ecuaciones = []
        self.haz_de_soluciones = []

        for i in range(0,int(self.n)):
            eq1 = simplify(-integrate(self.dVz_dx[i] + self.qz[i], self.x) + self.Vz0[i])
            eq2 = simplify(-integrate(self.dMy_dx[i] - eq1, self.x) + self.My0[i])
            eq3 = simplify(-integrate(self.dtheta_dx[i] - eq2 / self.EI, self.x) + self.theta0[i])
            eq4 = simplify(-integrate(self.dw_dx[i] + eq3, self.x) + self.w0[i])
            eq5 = simplify(-integrate(self.dN_dx[i] + self.qx[i], self.x) + self.N0[i])
            eq6 = simplify(-integrate(self.dU_dx[i] - eq5 / self.EA, self.x) + self.U0[i])

            print(f"\nHaz de soluciones para tramo {i + 1}:")
            print(f"Vz{i + 1}(x) = {(str(eq1)).replace('**','^')}")
            print(f"My{i + 1}(x) = {(str(eq2)).replace('**','^')}")
            print(f"theta{i + 1}(x) = {(str(eq3)).replace('**','^')}")
            print(f"w{i + 1}(x) = {(str(eq4)).replace('**','^')}")
            print(f"N{i + 1}(x) = {(str(eq5)).replace('**','^')}")
            print(f"U{i + 1}(x) = {(str(eq6)).replace('**','^')}")

            self.haz_de_soluciones.extend([eq1,eq2,eq3,eq4,eq5,eq6])

            self.ecuaciones.extend([
                eq1.subs(self.x, self.L[i]) - self.Vz[i],
                eq2.subs(self.x, self.L[i]) - self.My[i],
                eq3.subs(self.x, self.L[i]) - self.theta[i],
                eq4.subs(self.x, self.L[i]) - self.w[i],
                eq5.subs(self.x, self.L[i]) - self.N[i],
                eq6.subs(self.x, self.L[i]) - self.U[i],
            ])
        print(self.haz_de_soluciones)
        if self.listaapoyos[0]=="1":
            #print("el apoyo inicial es empotrado") #giros y desplazamientos nulos
            self.ecuaciones.extend([self.theta0[0],self.w0[0],self.U0[0]])
        elif self.listaapoyos[0]=="2":
            self.ecuaciones.extend([self.My0[0], self.w0[0]])
        elif self.listaapoyos[0]=="3":
            self.ecuaciones.extend([self.My0[0], self.w0[0],self.U0[0]])
        elif self.listaapoyos[0]=="4":
            #print("el apoyo inicial es libre")
            self.ecuaciones.extend([self.My0[0]])
            if self.preguntar_cargas_puntuales == "s":
                self.ecuaciones.extend([self.Vz0[0] + self.Qz[0]])
                self.ecuaciones.extend([self.N0[0] + self.Qx[0]])
            elif self.preguntar_cargas_puntuales == "n":
                self.ecuaciones.extend([self.Vz0[0]])
                self.ecuaciones.extend([self.N0[0]])
        if self.listaapoyos[int(self.n)]=="4":
            #print("el apoyo final es libre")
            self.ecuaciones.extend([self.My[int(self.n)-1]])
            if self.preguntar_cargas_puntuales == "s":
                self.ecuaciones.extend([self.Vz[int(self.n) - 1] - self.Qz[int(self.n)]])
                self.ecuaciones.extend([self.N[int(self.n) - 1] - self.Qx[int(self.n)]])
            elif self.preguntar_cargas_puntuales == "n":
                self.ecuaciones.extend([self.Vz[int(self.n) - 1]])
                self.ecuaciones.extend([self.N[int(self.n) - 1]])
        elif self.listaapoyos[int(self.n)] == "1":
            # print("el apoyo final es empotrado") #giros y desplazamientos nulos
            self.ecuaciones.extend([self.theta[int(self.n)-1], self.w[int(self.n)-1], self.U[int(self.n)-1]])
        elif self.listaapoyos[int(self.n)] == "2":
            self.ecuaciones.extend([self.My[int(self.n)-1], self.w[int(self.n)-1]])
        elif self.listaapoyos[int(self.n)] == "3":
            self.ecuaciones.extend([self.My[int(self.n)-1], self.w[int(self.n)-1], self.U[int(self.n)-1]])
        for i in range(0,int(self.n)-1):
            if self.listaapoyos[i+1] == "4":
                #print(f"el apoyo{i+2} es una union de tramos")
                self.ecuaciones.extend(
                    [self.theta[i] - self.theta0[i + 1], self.My[i] - self.My0[i + 1], self.w[i] - self.w0[i + 1],self.U[i] - self.U0[i + 1]])
                if self.preguntar_cargas_puntuales=="s":
                    self.ecuaciones.extend([self.Vz[i]-self.Vz0[i+1]-self.Qz[i+1]])
                    self.ecuaciones.extend([self.N[i] - self.N0[i + 1] - self.Qx[i + 1]])
                elif self.preguntar_cargas_puntuales=="n":
                    self.ecuaciones.extend([self.Vz[i]-self.Vz0[i+1]])
                    self.ecuaciones.extend([self.N[i] - self.N0[i + 1]])
            elif self.listaapoyos[i+1]=="3":
                #print(f"el apoyo{i+2} es un apoyo fijo")
                self.ecuaciones.extend([self.theta[i]-self.theta0[i+1],self.My[i]-self.My0[i+1],self.w[i],self.w0[i+1],self.U[i],self.U0[i+1]])

            elif self.listaapoyos[i+1]=="2":
                #print(f"el apoyo{i+2} es un apoyo movil")
                self.ecuaciones.extend([self.theta[i]-self.theta0[i+1],self.My[i]-self.My0[i+1],self.w[i],self.w0[i+1]])

            elif self.listaapoyos[i+1]=="1":
                self.ecuaciones.extend(
                    [self.theta[i],self.theta0[i + 1], self.My[i] - self.My0[i + 1], self.w[i], self.w0[i + 1],self.U[i],self.U0[i+1]])

        for i in range(0, int(self.n)):
            if all(simplify(qzi) == 0 for qzi in self.qx) and all(simplify(qzi) == 0 for qzi in self.Qx):

                self.ecuaciones.extend([self.N[i],self.N0[i]])
            if all(simplify(qzi) == 0 for qzi in self.qz) and all(simplify(qzi) == 0 for qzi in self.Qz):

                self.ecuaciones.extend([self.Vz[i], self.Vz0[i]])
        sol = solve(self.ecuaciones, self.listavariables, dict=True)
        print(sol)
        print(self.ecuaciones)
        print("Soluciones:")
        for s in sol:
            for var, val in s.items():
                val = val.simplify().subs(sin(self.alpha), tan(self.alpha) * cos(self.alpha))
                print(f"{var} = {(str(val)).replace('**','^')}")
        #reemplazamos las soluciones en el haz de soluciones
        for s in sol:
            for j in range(0, int(self.n)*6):
                self.haz_de_soluciones[j]=(self.haz_de_soluciones[j].subs(s))
        print(self.haz_de_soluciones)
        print()
        print("ecuaciones finales:")
        i=0
        for j in range(0,int(self.n)):
            print(f"Para el tramo {j+1}")
            print(f"Vz{j+1}={str(self.haz_de_soluciones[i]).replace('**','^')}")
            print(f"My{j + 1}(x) = {str(self.haz_de_soluciones[i+1]).replace('**','^')}")
            print(f"theta{j + 1}(x) = {str(self.haz_de_soluciones[i+2]).replace('**','^')}")
            print(f"w{j + 1}(x) = {str(self.haz_de_soluciones[i+3]).replace('**','^')}")
            print(f"N{j + 1}(x) = {str(self.haz_de_soluciones[i+4]).replace('**','^')}")
            print(f"U{j + 1}(x) = {str(self.haz_de_soluciones[i+5]).replace('**','^')}")
            i=i+6
    def graficas(self):
        while True:
            expresiones=[]
            inicio=int(input(f"ingrese el numero de la ecuacion a graficar (0,1,2,3,4,5)"))
            for j in range(0,int(self.n)):
            #expr_input = input(f"  Expresión simbólica de M{i + 1}(x): ")
            #expr_input=str(expr_input).replace('^','**')
            #expr_input=parse_expr(expr_input,local_dict=self.simbolos_conocidos)
            # expr1=sympify(self.haz_de_soluciones["Momentos"]
            # expr2=sympify(self.haz_de_soluciones["EsfuerzosV"]
            # expr3=sympify(self.haz_de_soluciones["EsfuerzosN"]
            # expr4=sympify(self.haz_de_soluciones["G"]
            # expr5=sympify(self.haz_de_soluciones["Momentos"]
                expr = sympify(self.haz_de_soluciones[inicio::6])#inicio:fin:paso
                inicio=inicio+6
                expresiones.append(expr)

            print(expresiones)
            expresiones = [var for sublist in expresiones for var in sublist]
            todos_los_simbolos = set()
            for eq in expresiones:
                todos_los_simbolos.update(eq.free_symbols)

            if self.x not in todos_los_simbolos:
                print("Las ecuaciones no dependen de x.")
                return

            # Pedir valores numéricos
            valores = {}
            for s in todos_los_simbolos:
                if s != self.x:
                    valor = float(input(f"Ingrese el valor numérico para {s}: "))
                    valores[s] = valor

            # Dominio
            if 'L' in [str(s) for s in todos_los_simbolos]:
                L_val = float(valores[symbols('L')])
            else:
                L_val = float(input("Ingrese el valor final del intervalo de x: "))

            x_offset=0

            for i, expr in enumerate(expresiones):
                expr_num = expr.subs(valores)
                x_local = np.linspace(0, L_val, 200)
                # Revisamos si depende de x
                if self.x in expr_num.free_symbols:
                    f = lambdify(self.x, expr_num, modules='numpy')
                    try:

                        y_vals = f(x_local)
                    except Exception as e:
                        print(f"No se pudo graficar la ecuación {i + 1}: {e}")
                        continue
                else:
                    y_vals = np.full_like(x_local, float(expr_num))  # crear un array constante

                x_global=x_local+x_offset
                plt.plot(x_global, y_vals, label=f"Ecuación {i + 1}")
                x_offset=x_offset+L_val

            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Gráficas de ecuaciones")
            plt.grid(True)
            plt.legend()
            plt.show()
Calculadora()
