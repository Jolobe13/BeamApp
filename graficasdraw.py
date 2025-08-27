
import matplotlib.patches as patches
from sympy import sin,pi,sqrt,cos


class Dibujar():
    def __init__(self, fig,ax,lista_apoyos,alpha,tipo_problema):
        self.tipo_problema=tipo_problema
        self.alpha=alpha
        alpha_deg = int(self.alpha[0])  # en grados
        alpha = alpha_deg * pi / 180  # en radianes
        if alpha_deg not in (90, 270):
            self.longitud = sqrt(1 / (1 - (sin(alpha) ** 2)))
        else:
            self.longitud = 1
        print(self.longitud)
        self.lista_apoyos=lista_apoyos
        self.n_apoyos=len(lista_apoyos)
        self.posicion_x_apoyos=[0]#el apoyo 1 siempre estara en el 0,0
        self.posicion_y_apoyos=[0]
        for i in range (1,self.n_apoyos):
            #if self.alpha[0]=="0" or self.alpha[0]=="90":
              #  self.posicion_x_apoyos.append(i)
             #   self.posicion_y_apoyos.append(0)
            #else:
            alpha = int(self.alpha[i-1]) * pi / 180
            self.posicion_x_apoyos.append(self.posicion_x_apoyos[i-1]+self.longitud*cos(alpha))
            self.posicion_y_apoyos.append(self.posicion_y_apoyos[i-1]+self.longitud*sin(alpha))
        print(self.posicion_y_apoyos)
        print(self.posicion_x_apoyos)
        print(self.longitud)
        self.fig = fig
        self.ax = ax
        self.ax.plot([-0.5, 3.5], [0, 0], linestyle='--', color="black")
        self.ax.text(-0.3, 0.02, 'Tierra', fontsize=8, color='black')

    def posicion_apoyos(self):
        return self.posicion_x_apoyos, self.posicion_y_apoyos

    def barras_simples_ejemplo(self):
        self.ax.set_title("Ejemplo barras simples: 3 barras con alpha=45º",fontsize=9)
        self.ax.grid(True)
        self.posicion_y_apoyos=[0,1,2,3]
        self.posicion_x_apoyos=self.posicion_y_apoyos
        self.barras_simples()
        # Agregar arco entre el eje x y la flecha axial
        arc = patches.Arc((0, 0), 1, 1, angle=0, theta1=0, theta2=int(self.alpha[0]), color='green', lw=2)
        self.ax.add_patch(arc)

        # Etiqueta del arco
        self.ax.text(0.3, 0.05, r'$\alpha$', color='green', fontsize=14)
        self.ax.set_aspect('equal', adjustable='box')
    def portico_ejemplo(self):
        self.posicion_y_apoyos=[0,1,1,1,0]
        self.posicion_x_apoyos=[0,0,1,2,2]
        self.ax.set_title("Ejemplo portico: 4 barras con\nalpha1=90º, alpha2=alpha3=0º, alpha4=270º",fontsize=9)
        self.portico()
        # Agregar arco entre el eje x y la flecha axial
        arc = patches.Arc((0, 0), self.longitud/4, self.longitud/4, angle=0, theta1=0, theta2=int(self.alpha[0]), color='green', lw=2)
        self.ax.add_patch(arc)

        # Etiqueta del arco
        self.ax.text(0.2, 0.05, r'$\alpha_1$', color='green', fontsize=14)
        self.ax.set_aspect('equal', adjustable='box')
        arc = patches.Arc((2, 1), self.longitud / 4, self.longitud / 4, angle=0, theta1=0, theta2=270,
                          color='green', lw=2)
        self.ax.add_patch(arc)
        # Etiqueta del arco
        self.ax.text(0.05, 1.05, r'$\alpha_2$', color='green', fontsize=14)
        self.ax.text(1.05, 1.05, r'$\alpha_3$', color='green', fontsize=14)
        self.ax.text(2.15, 1.05, r'$\alpha_4$', color='green', fontsize=14)
        self.ax.set_aspect('equal', adjustable='box')
        #self.ax.set_xlim(-0.5, 2.5)
        #self.ax.set_ylim(-0.5, 2.5)


    def barras(self):
        self.ax.set_title("Está describiendo esta estructura",fontsize=9)
        if self.tipo_problema=="barras simples":
            self.barras_simples()
        else:
            self.portico()
    def barras_simples(self):
        #self.ax.set_title("Está describiendo esta estructura")
        self.ax.grid(True)
        self.ax.plot(self.posicion_x_apoyos,self.posicion_y_apoyos, marker='o')  # ejemplo
        self.ax.set_xlim(-0.5, int(max(max(self.posicion_x_apoyos)+0.5,max(self.posicion_y_apoyos))+0.5))
        self.ax.set_ylim(-0.5, int(max(max(self.posicion_x_apoyos)+0.5,max(self.posicion_y_apoyos))+0.5))
        self.ax.set_autoscale_on(False)
        ##ejes 1
        self.axial_arrow = self.ax.annotate(
            "", xy=(self.posicion_x_apoyos[1]/4, self.posicion_y_apoyos[1]/4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="blue", lw=2)
        )
        self.axial_text = self.ax.text(-0.15, 0.15, "Eje Axial", fontsize=8, color="blue", ha="center")

        self.cortante_arrow = self.ax.annotate(
            "", xy=(self.posicion_y_apoyos[1]/4, -self.posicion_x_apoyos[1]/4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", lw=2)
        )
        self.cortante_text = self.ax.text(-0.15, -0.15, "Eje Cortante", fontsize=8, color="red", ha="center")

        for i in range(0,len(self.posicion_y_apoyos)-1):
            self.ax.text(self.posicion_x_apoyos[i]+0.05+(self.posicion_x_apoyos[i+1]-self.posicion_x_apoyos[i])/2, 0.05+self.posicion_y_apoyos[i]+(self.posicion_y_apoyos[i+1]-self.posicion_y_apoyos[i])/2, f"Barra {i+1}", fontsize=8, color="purple", ha="center",va="center")
    def portico(self):
        #self.ax.set_title("Está describiendo esta estructura")
        self.ax.grid(True)
        self.ax.plot(self.posicion_x_apoyos, self.posicion_y_apoyos, marker='o')  # ejemplo
        #self.ax.set_xlim(-0.5, 3.5)
        #self.ax.set_ylim(-0.5, 3.5)

        self.ax.set_xlim(-0.5, int(max(max(self.posicion_x_apoyos)+0.5,max(self.posicion_y_apoyos))+0.5))
        self.ax.set_ylim(-0.5, int(max(max(self.posicion_x_apoyos)+0.5,max(self.posicion_y_apoyos))+0.5))
        self.ax.set_autoscale_on(False)
        self.axial_arrow = self.ax.annotate(
            "", xy=(self.posicion_x_apoyos[1] / 4, self.posicion_y_apoyos[1] / 4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="blue", lw=2)
        )
        self.axial_text = self.ax.text(-0.25, 0.15, "Eje Axial 1", fontsize=8, color="blue", va="center")

        self.cortante_arrow = self.ax.annotate(
            "", xy=(self.posicion_y_apoyos[1] / 4, -self.posicion_x_apoyos[1] / 4), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="red", lw=2)
        )
        self.cortante_text = self.ax.text(0.25, -0.10, "Eje Cortante 1", fontsize=8, color="red", ha="center")
        ##ejes 2
        self.axial_arrow = self.ax.annotate(
            "", xy=(self.longitud / 4, max(self.posicion_y_apoyos)), xytext=(0, max(self.posicion_y_apoyos)),
            arrowprops=dict(arrowstyle="->", color="blue", lw=2)
        )
        self.axial_text = self.ax.text(0.1, max(self.posicion_y_apoyos)-0.1, "Eje Axial 2", fontsize=8, color="blue", va="center")

        self.cortante_arrow = self.ax.annotate(
            "", xy=(0, max(self.posicion_y_apoyos)-self.longitud / 4), xytext=(0, max(self.posicion_y_apoyos)),
            arrowprops=dict(arrowstyle="->", color="red", lw=2)
        )
        self.cortante_text = self.ax.text(0.15, max(self.posicion_y_apoyos)-0.25, "Eje Cortante 2", fontsize=8, color="red", ha="center")
        # ejes 3, solo si hay esquina
        if self.posicion_y_apoyos[-1] != self.posicion_y_apoyos[-2]:  # en este caso, si que ponemos el ultimo eje
            self.axial_arrow = self.ax.annotate(
                "", xy=(max(self.posicion_x_apoyos),max(self.posicion_y_apoyos)-self.longitud/4), xytext=(max(self.posicion_x_apoyos), max(self.posicion_y_apoyos)),
                arrowprops=dict(arrowstyle="->", color="blue", lw=2)
            )
            self.axial_text = self.ax.text(max(self.posicion_x_apoyos)-0.2, max(self.posicion_y_apoyos)-0.25, "Eje Axial 3", fontsize=8, color="blue", va="center")

            self.cortante_arrow = self.ax.annotate(
                "", xy=(max(self.posicion_x_apoyos)-self.longitud/4, max(self.posicion_y_apoyos)), xytext=(max(self.posicion_x_apoyos), max(self.posicion_y_apoyos)),
                arrowprops=dict(arrowstyle="->", color="red", lw=2)
            )
            self.cortante_text = self.ax.text(max(self.posicion_x_apoyos)-0.15, max(self.posicion_y_apoyos)-0.1, "Eje Cortante 3", fontsize=8, color="red", ha="center")

        for i in range(0, len(self.posicion_y_apoyos) - 1):
            if self.posicion_y_apoyos[i+1]==self.posicion_y_apoyos[i]:#significa que estamos en tramo horizontal
                self.ax.text(self.posicion_x_apoyos[i] + self.longitud / 2, 0.05 + self.posicion_y_apoyos[i + 1],
                             f"Barra {i+1}", fontsize=8, color="purple", va="center")
            elif self.posicion_y_apoyos[i+1]<self.posicion_y_apoyos[i]:#significa que estamos en tramo vertical hacia abajo
                self.ax.text(self.posicion_x_apoyos[i]+0.05, self.posicion_y_apoyos[i] -self.longitud / 2,
                             f"Barra {i+1}", fontsize=8, color="purple", va="center")
            elif self.posicion_y_apoyos[i+1]>self.posicion_y_apoyos[i]:#significa que estamos en tramo vertical hacia arriba
                self.ax.text(self.posicion_x_apoyos[i] + 0.05,
                             self.posicion_y_apoyos[i] + self.longitud / 2,
                             f"Barra {i + 1}", fontsize=8, color="purple", va="center")

        self.ax.plot([-0.5, 3.5], [0, 0], linestyle='--', color="black")
        self.ax.text(-0.3, 0.02, 'Tierra', fontsize=5, color='black')

    def apoyo_movil(self,respuesta,indice_apoyo):
        i=indice_apoyo
        x=self.posicion_x_apoyos[i]
        y=self.posicion_y_apoyos[i]
        if respuesta=="vertical":
            triangle = patches.Polygon([[x, y], [x+0.25, y+0.25], [x+0.25,y-0.25]], closed=True, color='blue')
            self.ax.add_patch(triangle)

            # Dibujar dos círculos pequeños debajo del triángulo
            circle1 = patches.Circle((x+0.1+0.25, y+0.25), radius=0.05, color='red')
            circle2 = patches.Circle((x+0.1+0.25, y-0.25), radius=0.05, color='red')

            self.ax.add_patch(circle1)
            self.ax.add_patch(circle2)

            # Ajustar límites para que se vea todo bien
            #self.ax.set_xlim(self.posicion_x_apoyos[0]-0.5, self.posicion_x_apoyos[-1])
            #self.ax.set_ylim(self.posicion_y_apoyos[0]-0.5, self.posicion_y_apoyos[-1])
        elif respuesta=="horizontal":
            triangle = patches.Polygon([[x-0.25, y-0.25], [x, y], [x+0.25,y-0.25]], closed=True, color='blue')
            self.ax.add_patch(triangle)

            # Dibujar dos círculos pequeños debajo del triángulo
            circle1 = patches.Circle((x+0.1-0.25, y-0.25-0.1), radius=0.05, color='red')
            circle2 = patches.Circle((x-0.1+0.25, y-0.25-0.1), radius=0.05, color='red')

            self.ax.add_patch(circle1)
            self.ax.add_patch(circle2)

            # Ajustar límites para que se vea todo bien
            #self.ax.set_xlim(self.posicion_x_apoyos[0] - 0.5, self.posicion_x_apoyos[-1])
            #self.ax.set_ylim(self.posicion_y_apoyos[0] - 0.5, self.posicion_y_apoyos[-1])


