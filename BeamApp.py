import tkinter as tk
from tkinter import ttk,simpledialog,messagebox
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb
import mplcursors

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graficasdraw import Dibujar

from sympy import symbols, Symbol, simplify, integrate, diff, sin, solve, sympify, tan, cos, pretty, N,lambdify, pi
import numpy as np
from sympy.parsing.sympy_parser import parse_expr
class VigaSolverApp:
    def __init__(self, root):

        self.crear_variables()
        self.simbolos_conocidos = {
            "Q": Symbol("Q"),
            "q": Symbol("q"),
            "x": Symbol("x"),
            "alpha": Symbol("alpha"),
            "beta": Symbol("beta"),
            "EI": Symbol("EI"),
            "EA": Symbol("EA")
        }
        self.root = root
        self.root.title("BeamApp")
        self.root.geometry("1800x800")
        self.style = tb.Style("cosmo")

        # === FRAME PRINCIPAL ===
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Izquierda: Entradas
        self.left = ttk.Frame(self.main_frame, padding=5)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        font_label = ("Segoe UI", 20)
        font_entry = ("Segoe UI", 12)
        #ttk.Label(self.left, text="BEAMApp", font=font_label).pack(side=tk.TOP, anchor="w", pady=5)

        # Derecha: Frame superior con gráfica interactiva
        self.right_top = ttk.Frame(self.main_frame)
        self.right_top.pack()

        #ttk.Label(self.right_top, text="Dibujo de la viga (Interactivo)", font=("Segoe UI", 12, "bold")).pack(pady=(0, 5))

        # Crear figura de arriba (interactiva)
        self.figure_canvas, self.ax_canvas = plt.subplots(figsize=(5, 5))

        #self.ax_canvas.set_title("Ejemplo barras simples 3 tramos con alpha=45º")
        self.ax_canvas.grid(True)
        #self.ax_canvas.plot([0, 1, 2, 3], [0, 1, 2, 3], marker='o')  # ejemplo
        self.ax_canvas.set_xlim(-0.5, 3.5)
        self.ax_canvas.set_ylim(-0.5, 3.5)
        self.ax_canvas.set_autoscale_on(False)
        self.ax_canvas.set_aspect('equal', adjustable='box')

        # Canvas de Matplotlib
        self.canvas_top = FigureCanvasTkAgg(self.figure_canvas, master=self.right_top)
        self.canvas_top.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Barra de herramientas para zoom/pan con ratón
        #self.toolbar_top = NavigationToolbar2Tk(self.canvas_top, self.right_top)
        #self.toolbar_top.update()
        # --- Eventos para zoom y pan ---
        # Zoom con la rueda
        self.figure_canvas.canvas.mpl_connect("scroll_event", self.on_scroll)
        # Pan con botón derecho
        self.dragging = False
        self.last_event = None
        self.figure_canvas.canvas.mpl_connect("button_press_event", self.on_press)
        self.figure_canvas.canvas.mpl_connect("button_release_event", self.on_release)
        self.figure_canvas.canvas.mpl_connect("motion_notify_event", self.on_motion)

        # Derecha: Gráfica de resultados (abajo)
        self.right_bottom = ttk.Frame(self.main_frame, padding=5)
        self.right_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.figure_graficas, self.ax_graficas = plt.subplots(figsize=(7, 5))
        self.ax_graficas.set_title("Gráfica de resultados\n",fontsize=9)
        self.chart = FigureCanvasTkAgg(self.figure_graficas, self.right_bottom)
        self.chart.get_tk_widget().pack(ipady=10)

        # Sección de texto
        ttk.Label(self.left, text="BeamApp", font=("Segoe UI", 14, "bold")).pack()
        self.solution_text = ScrolledText(self.left, wrap=tk.WORD, height=25, font=("Courier New", 10))
        self.solution_text.pack(fill=tk.BOTH, expand=True)

        self.solution_text.insert(tk.END, f"{self.pregunta_actual}")
        self.solution_text.config(state=tk.DISABLED)

        # Entrada + Botones
        self.left_bottom = ttk.Frame(self.left, padding=5)
        self.left_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.n_entry = ttk.Entry(self.left_bottom, font=font_entry)
        self.n_entry.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=5, expand=True)
        self.n_entry.insert(0, "Responda aquí...")

        # Eventos para manejar el placeholder
        def al_entrar(event):
            if self.n_entry.get() == "Responda aquí...":
                self.n_entry.delete(0, "end")
                self.n_entry.config(foreground="black")

        def al_salir(event):
            if not self.n_entry.get():
                self.n_entry.insert(0, "Responda aquí...")
                self.n_entry.config(foreground="grey")

        self.n_entry.bind("<FocusIn>", al_entrar)
        self.n_entry.bind("<FocusOut>", al_salir)

        # Evento para Enter
        self.n_entry.bind("<Return>", self.on_responder)

        self.boton_reiniciar = tk.Button(self.left_bottom, text="Reiniciar", command=self.reiniciar, width=20, height=5)
        self.boton_reiniciar.pack(side=tk.RIGHT, padx=5, pady=5)
        self.boton_ayuda=tk.Button(self.left_bottom, text="Ayuda", command=self.ayuda, width=20,height=5)
        self.boton_ayuda.pack(side=tk.RIGHT, padx=5, pady=5)
        self.boton_responder = tk.Button(self.left_bottom, text="Responder", command=self.on_responder, width=20,height=5)
        self.boton_responder.pack(side=tk.RIGHT, padx=5, pady=5)
        #root.after(100, lambda: messagebox.showinfo("Bienvenido", "Hola! bienvenido a la app. Responda a las preguntas del cuadro de texto presionando enter o pulsando la tecla Responder. \nEn la gráfica superior se mostrará el problema que está describiendo junto con los ejes y ángulos de referencia en los que debe apoyarse. \nPara observar las gráficas de esfuerzos, momentos, etc, se deben dar valores a las incógnitas que el programa solicite y se debe especificar la gráfica deseada entre las posibles opciones que se indican.\nEs muy importante que haga caso a las indicaciones que aparecen en las preguntas antes de responderlas (aparecen entre paréntesis). Por ejemplo, la primera pregunta solo tiene como posibles respuestas portico o barras simples, lo que quiere decir que solo puede responder una de esas dos opciones, no otra diferente.\nDicho esto,¡a calcular!"))
    def on_scroll(self, event):
        # Solo si el cursor está dentro de los ejes
        if event.inaxes != self.ax_canvas:
            return

        # Factor de zoom
        scale = 1.1 if event.button == "up" else (1 / 1.1)

        # Limites actuales
        xlim = self.ax_canvas.get_xlim()
        ylim = self.ax_canvas.get_ylim()

        # Punto del cursor
        xdata, ydata = event.xdata, event.ydata

        # Nuevos límites (zoom alrededor del cursor)
        new_xmin = xdata - (xdata - xlim[0]) * scale
        new_xmax = xdata + (xlim[1] - xdata) * scale
        new_ymin = ydata - (ydata - ylim[0]) * scale
        new_ymax = ydata + (ylim[1] - ydata) * scale

        self.ax_canvas.set_xlim(new_xmin, new_xmax)
        self.ax_canvas.set_ylim(new_ymin, new_ymax)
        self.canvas_top.draw_idle()

    def on_press(self, event):
        # botón 3 = clic derecho (pan)
        if event.inaxes == self.ax_canvas and event.button == 3:
            self.dragging = True
            self.last_event = event

    def on_release(self, event):
        if event.button == 3:
            self.dragging = False
            self.last_event = None

    def on_motion(self, event):
        if not self.dragging or event.inaxes != self.ax_canvas or self.last_event is None:
            return

        # Desplazamiento en coordenadas de datos
        dx = self.last_event.xdata - event.xdata
        dy = self.last_event.ydata - event.ydata

        xlim = self.ax_canvas.get_xlim()
        ylim = self.ax_canvas.get_ylim()
        self.ax_canvas.set_xlim(xlim[0] + dx, xlim[1] + dx)
        self.ax_canvas.set_ylim(ylim[0] + dy, ylim[1] + dy)

        self.last_event = event
        self.canvas_top.draw_idle()

    def ayuda(self):
        self.root.after(100, lambda: messagebox.showinfo("Ayuda",
                                                    "Hola! bienvenido a la BeamApp. Responda a las preguntas del cuadro de texto presionando enter o pulsando la tecla Responder. \nEn la gráfica superior se mostrará el problema que está describiendo junto con los ejes y ángulos de referencia en los que debe apoyarse. Si lo necesita, puede hacer zoom con el Mouse Wheel para visualizar mejor el dibujo. \nPara observar las gráficas de esfuerzos, momentos, etc, se deben dar valores a las incógnitas que el programa solicite y se debe especificar la gráfica deseada entre las posibles opciones que se indican. \nEs muy importante que haga caso a las indicaciones que aparecen en las preguntas antes de responderlas (aparecen entre paréntesis). Por ejemplo, la primera pregunta solo tiene como posibles respuestas portico o barras simples, lo que quiere decir que solo puede responder una de esas dos opciones, no otra diferente.\nRespecto a las variables que aparecen...\nEI:producto del módulo elástico por la inercia\nEA:producto del módulo elástico por el área de la sección\nL:longitud\nVz1:esfuerzo cortante a lo largo de la barra 1\nN1:esfuerzo axial a lo largo de la barra 1\nMy1:momento a lo largo de la barra 1\ntheta1:giro perpendicular al plano a lo largo de la barra1\nw1:desplazamiento cortante a lo largo de la barra 1\nU1:desplazamientos axiales a lo largo de la barra 1\nDicho esto ¡a calcular!"))


    def crear_variables(self):
        self.j=0#contador para posicion de apoyos moviles
        self.preguntas = ["Introduzca el tipo de problema (portico/barras simples): ", "¿Deseas que todas las barras tengan la misma longitud? (si/no): "]
        self.incognita = ""
        self.respuesta_tipo_de_problema=[]#portico o barras simples
        self.tipos_angulos=[]
        self.respuesta_angulos=[]
        self.tipos_apoyos = [] #[Apoyo1: ,Apoyo2: ,Apoyo3:....]
        self.tipos_cargas = []
        self.tipos_cargas_puntuales = []
        self.respuestas_tramos = []
        self.respuestas_apoyos = []
        self.respuestas_cargas = []
        self.respuestas_cargas_puntuales = []
        self.respuestas_posicion_apoyos_moviles=[]
        self.posicion_apoyos = []
        self.fin_preguntas = "no"
        self.hay_tramos_moviles = "no"
        self.Vz, self.Vz0 = [], []
        self.My, self.My0 = [], []
        self.theta, self.theta0 = [], []
        self.w, self.w0 = [], []
        self.N, self.N0 = [], []
        self.U, self.U0 = [], []
        self.L, self.Qz, self.Qx = [], [], []
        self.qz, self.qx = [], []
        self.dVz_dx = []
        self.dMy_dx = []
        self.dtheta_dx = []
        self.dw_dx = []
        self.dN_dx = []
        self.dU_dx = []
        self.alpha=[Symbol('alpha')]
        self.pregunta_actual = self.preguntas[0]
    def reiniciar(self):
        self.crear_variables()
        self.ax_canvas.cla()
        self.ax_graficas.clear()
        self.ax_canvas.grid(True)
        self.canvas_top.draw()
        self.solution_text.config(state=tk.NORMAL)
        self.solution_text.delete("1.0", tk.END)
        self.solution_text.insert(tk.END, f"{self.pregunta_actual}")
        self.solution_text.config(state=tk.DISABLED)

    def fmt_num(self, n: float) -> str:
        """Devuelve el número sin decimales si es entero, o con 2 decimales si no lo es"""
        return f"{int(n)}" if float(n).is_integer() else f"{n:.2f}"
    def on_responder(self, event=None):
        self.respuesta = self.n_entry.get().strip()
        if self.pregunta_actual == self.preguntas[0]:
            self.respuesta_tipo_de_problema=self.respuesta
            if self.respuesta_tipo_de_problema=="portico":
                Dibujar(self.figure_canvas, self.ax_canvas,self.respuestas_apoyos,[90],self.respuesta_tipo_de_problema).portico_ejemplo()
                self.pregunta_actual = "Introduzca el número de barras (mínimo 2):"
            elif self.respuesta == "barras simples":
                self.pregunta_actual = "Introduzca el número de barras (mínimo 1):"
                Dibujar(self.figure_canvas, self.ax_canvas,self.respuestas_apoyos,[45],self.respuesta_tipo_de_problema).barras_simples_ejemplo()
            self.canvas_top.draw()
            #self.pregunta_actual = self.tipos_angulos[self.indice_angulos]
        elif self.pregunta_actual == "Introduzca el número de barras (mínimo 2):" or self.pregunta_actual=="Introduzca el número de barras (mínimo 1):":
            self.respuestas_tramos.append(self.respuesta)
            if self.respuesta=="1":#se trata de unas barras simples
                self.indice_angulos=0
                self.respuestas_tramos.append("si")
                self.L.append(Symbol("L"))
                self.tipos_angulos.append(
                    f"Introduzca el angulo en grados (solo angulos del primer y cuarto cuadrante) de alpha: ")
                self.pregunta_actual = self.tipos_angulos[self.indice_angulos]
            else:
                self.pregunta_actual=self.preguntas[1]
            #self.canvas_label.config(text=f"Ejemplo {self.respuesta_tipo_de_problema} de {self.respuestas_tramos[0]} tramos ")
            #self.mostrar_pregunta(respuesta, self.pregunta_actual)

        elif self.pregunta_actual == self.preguntas[1]:
            self.respuestas_tramos.append(self.respuesta)
            if self.respuesta == "si":
                for i in range(1, int(self.respuestas_tramos[0]) + 1):
                    self.L.append(Symbol("L"))
            elif self.respuesta == "no":
                for i in range(1, int(self.respuestas_tramos[0]) + 1):
                    self.L.append(Symbol(f"L{i}"))
            self.indice_angulos = 0
            if self.respuesta_tipo_de_problema == "portico":
                self.respuesta_angulos.append("90")
                self.mostrar_pregunta(self.respuesta,
                                      "Introduzca el angulo en grados de la barra 1 (alpha1) respecto la linea de tierra: 90 (obligatorio)")
                self.respuesta=""
                self.tipos_angulos.append(
                    f"Introduzca el angulo en grados (0 o 90) de la barra 2 (alpha2) respecto a linea de tierra:")
                for i in range(2, int(self.respuestas_tramos[0])):
                    self.tipos_angulos.append(f"Introduzca el angulo en grados (0,90 o 270) de la barra{i + 1} (alpha{i + 1}) respecto a linea de tierra:")
            elif self.respuesta_tipo_de_problema == "barras simples":
                self.tipos_angulos.append(f"Introduzca el angulo en grados (solo angulos del primer y cuarto cuadrante) de alpha: ")
            self.pregunta_actual = self.tipos_angulos[self.indice_angulos]

        elif self.pregunta_actual in self.tipos_angulos:
            if self.respuesta_tipo_de_problema=="barras simples":
                for i in range(0,int(self.respuestas_tramos[0])):
                    self.respuesta_angulos.append(self.respuesta)#de tal forma, obtenemos una lista con el mismo valor de alpha
            else:
                self.respuesta_angulos.append(self.respuesta)
            self.indice_angulos = self.indice_angulos + 1
            if self.indice_angulos < len(self.tipos_angulos):
                self.pregunta_actual = self.tipos_angulos[self.indice_angulos]
            else:
                # Queremos encontrar la posición del primer 0 y de 3*pi/2
                # Buscar los índices
                self.esquina_1=-1
                self.esquina_2=0
                if self.respuesta_tipo_de_problema=="portico":
                    self.esquina_1 = next(i for i, val in enumerate(self.respuesta_angulos) if val == "0")
                    try:
                        self.esquina_2 = next(i for i, val in enumerate(self.respuesta_angulos) if val == "270")
                    except StopIteration:
                        pass
                self.mostrar_pregunta(self.respuesta, "Ingrese tipo de apoyo (ej: 1,2,3,4) del...\n1:apoyo empotrado(theta=0,w=U=0)    2:apoyo movil(M=0)\n3:apoyo fijo(M=0,w=U=0)    4:sin apoyo")
                self.posicion_x_apoyos,self.posicion_Y_apoyos=Dibujar(self.figure_canvas, self.ax_canvas, [1]*(int(self.respuestas_tramos[0])+1), self.respuesta_angulos,
                        self.respuesta_tipo_de_problema).posicion_apoyos()
                print(self.posicion_Y_apoyos)
                for i in range(0,int(self.respuestas_tramos[0])+1):
                    self.tipos_apoyos.append(
                        f"Apoyo {i + 1} (posición ({self.fmt_num(self.posicion_x_apoyos[i])}, "
                        f"{self.fmt_num(self.posicion_Y_apoyos[i])})):")

                self.indice_apoyos=0
                self.pregunta_actual=self.tipos_apoyos[self.indice_apoyos]
                self.respuesta=""
                self.ax_canvas.cla()
                Dibujar(self.figure_canvas, self.ax_canvas, self.tipos_apoyos, self.respuesta_angulos,
                        self.respuesta_tipo_de_problema).barras()
                self.canvas_top.draw()

        elif self.pregunta_actual in self.tipos_apoyos:
            self.respuestas_apoyos.append(self.respuesta)
            if self.respuesta=="2":
                self.hay_tramos_moviles = "si"
            self.indice_apoyos=self.indice_apoyos+1
            #print(f"esta es la L {len(self.tipos_apoyos)}")
            if self.indice_apoyos<len(self.tipos_apoyos):
                self.pregunta_actual=self.tipos_apoyos[self.indice_apoyos]
            else:
                #si ya hemos preguntado por el tipo de todos los apoyos, ahora preguntamos la posicion si hay apoyo movil o pasamos a preguntar las cargas
                if self.hay_tramos_moviles=="si":
                    self.indice_tramos_moviles=0
                    for i in range(0,self.indice_apoyos):
                        if self.respuestas_apoyos[i]=="2":
                            self.posicion_apoyos.append(f"Indique el desplazamiento que permite el apoyo movil {i+1} (vertical/horizontal):")
                    self.pregunta_actual=self.posicion_apoyos[self.indice_tramos_moviles]
                else:
                    self.ax_canvas.cla()
                    Dibujar(self.figure_canvas, self.ax_canvas,self.respuestas_apoyos,self.respuesta_angulos,self.respuesta_tipo_de_problema).barras()
                    self.canvas_top.draw()
                    self.mostrar_pregunta(self.respuesta,
                                          "Indique las componentes axiales y cortantes de las cargas repartidas a las que estan sometidas las diferentes barras. \nEjemplos:\n  q,q1,q2,q3...\n  q*sin(alpha),q*cos(alpha1),q*sin(alpha2)...\n  q*cos(beta),q*sin(beta1),q*cos(beta2)...\n  0")
                    self.respuesta = ""
                    for i in range(0, int(self.respuestas_tramos[0])):
                        if self.respuesta_tipo_de_problema=="barras simples":
                            self.tipos_cargas.append(f"Ingrese componente cortante de la carga repartida en la barra {i+1}:")
                            self.tipos_cargas.append(f"Ingrese componente axial de la carga repartida en la barra {i+1}:")
                        else:
                            if self.respuesta_angulos[i] == "90":
                                self.tipos_cargas.append(
                                    f"Ingrese componente cortante (respecto eje Cortante1) de la carga repartida en la barra {i + 1}:")
                                self.tipos_cargas.append(
                                    f"Ingrese componente axial (respecto eje axial1) de la carga repartida en la barra {i + 1}:")
                            elif self.respuesta_angulos[i] == "0":
                                self.tipos_cargas.append(
                                    f"Ingrese componente cortante (respecto eje Cortante2) de la carga repartida en la barra {i + 1}:")
                                self.tipos_cargas.append(
                                    f"Ingrese componente axial (respecto eje axial2) de la carga repartida en la barra {i + 1}:")
                            elif self.respuesta_angulos[i] == "270":
                                self.tipos_cargas.append(
                                    f"Ingrese componente cortante (respecto eje Cortante3) de la carga repartida en la barra {i + 1}:")
                                self.tipos_cargas.append(
                                    f"Ingrese componente axial (respecto eje axial3) de la carga repartida en la barra {i + 1}:")
                        self.simbolos_conocidos[f"q{i+1}"] = Symbol(f"q{i+1}")
                        self.simbolos_conocidos[f"Q{i+1}"] = Symbol(f"Q{i+1}")
                        self.simbolos_conocidos[f"L{i+1}"] = Symbol(f"L{i+1}")
                        self.simbolos_conocidos[f"alpha{i+1}"] = Symbol(f"alpha{i+1}")
                        self.simbolos_conocidos[f"beta{i+1}"] = Symbol(f"beta{i+1}")
                    for i in range(int(self.respuestas_tramos[0]) + 1,
                                   int(self.respuestas_tramos[0]) + int(self.respuestas_tramos[0]) + 1):
                        self.simbolos_conocidos[f"Q{i}"] = Symbol(f"Q{i}")
                    self.indice_cargas = 0
                    self.pregunta_actual = self.tipos_cargas[self.indice_cargas]
        elif self.pregunta_actual in self.posicion_apoyos:
            if self.j==0:
                self.ax_canvas.cla()
                Dibujar(self.figure_canvas, self.ax_canvas, self.respuestas_apoyos, self.respuesta_angulos,
                        self.respuesta_tipo_de_problema).barras()
            indices = [i for i, valor in enumerate(self.respuestas_apoyos) if valor == "2"]#extrae lista con indices
            self.respuestas_posicion_apoyos_moviles.append(self.respuesta)
            Dibujar(self.figure_canvas, self.ax_canvas, self.respuestas_apoyos, self.respuesta_angulos,
                    self.respuesta_tipo_de_problema).apoyo_movil(self.respuesta, indices[self.j])
            self.canvas_top.draw()
            self.j=self.j+1
            self.indice_tramos_moviles = self.indice_tramos_moviles + 1
            if self.indice_tramos_moviles < len(self.posicion_apoyos):
                self.pregunta_actual = self.posicion_apoyos[self.indice_tramos_moviles]
            else:
                self.mostrar_pregunta(self.respuesta,
                                      "Indique las componentes axiales y cortantes de las cargas repartidas a las que estan sometidas las diferentes barras. \nEjemplos:\n  q,q1,q2,q3...\n  q*sin(alpha),q*cos(alpha1),q*sin(alpha2)...\n  q*cos(beta),q*sin(beta1),q*cos(beta2)...\n  0")
                self.respuesta = ""
                for i in range(0, int(self.respuestas_tramos[0])):
                    if self.respuesta_tipo_de_problema == "barras simples":
                        self.tipos_cargas.append(
                            f"Ingrese componente cortante de la carga repartida en la barra {i + 1}:")
                        self.tipos_cargas.append(f"Ingrese componente axial de la carga repartida en la barra {i + 1}:")
                    else:
                        if self.respuesta_angulos[i] == "90":
                            self.tipos_cargas.append(
                                f"Ingrese componente cortante (respecto eje Cortante1) de la carga repartida en la barra {i + 1}:")
                            self.tipos_cargas.append(
                                f"Ingrese componente axial (respecto eje axial1) de la carga repartida en la barra {i + 1}:")
                        elif self.respuesta_angulos[i] == "0":
                            self.tipos_cargas.append(
                                f"Ingrese componente cortante (respecto eje Cortante2) de la carga repartida en la barra {i + 1}:")
                            self.tipos_cargas.append(
                                f"Ingrese componente axial (respecto eje axial2) de la carga repartida en la barra {i + 1}:")
                        elif self.respuesta_angulos[i] == "270":
                            self.tipos_cargas.append(
                                f"Ingrese componente cortante (respecto eje Cortante3) de la carga repartida en la barra {i + 1}:")
                            self.tipos_cargas.append(
                                f"Ingrese componente axial (respecto eje axial3) de la carga repartida en la barra {i + 1}:")
                    self.simbolos_conocidos[f"q{i + 1}"] = Symbol(f"q{i + 1}")
                    self.simbolos_conocidos[f"Q{i + 1}"] = Symbol(f"Q{i + 1}")
                    self.simbolos_conocidos[f"L{i + 1}"] = Symbol(f"L{i + 1}")
                    self.simbolos_conocidos[f"alpha{i + 1}"] = Symbol(f"alpha{i + 1}")
                    self.simbolos_conocidos[f"beta{i + 1}"] = Symbol(f"beta{i + 1}")
                for i in range(int(self.respuestas_tramos[0]) + 1,
                               int(self.respuestas_tramos[0]) + int(self.respuestas_tramos[0]) + 1):
                    self.simbolos_conocidos[f"Q{i}"] = Symbol(f"Q{i}")
                self.indice_cargas = 0
                self.pregunta_actual = self.tipos_cargas[self.indice_cargas]

        elif self.pregunta_actual in self.tipos_cargas:
            self.respuestas_cargas.append(self.respuesta)
            self.indice_cargas = self.indice_cargas + 1
            if self.indice_cargas<len(self.tipos_cargas):
                self.pregunta_actual=self.tipos_cargas[self.indice_cargas]
            else:
                #guardamos los valores de las cargas en las listas self.qz y self.qx y preguntamos si hay cargas puntuales
                self.qz.append(sympify(self.respuestas_cargas[0::2]))
                self.qx.append(sympify(self.respuestas_cargas[1::2]))
                self.qz = [var for sublist in self.qz for var in sublist]
                self.qx = [var for sublist in self.qx for var in sublist]
                print(self.qz)
                self.tipos_cargas_puntuales.append("Hay alguna carga puntual en algun apoyo? (si/no):")
                self.indice_cargas_puntuales = 0
                self.pregunta_actual=self.tipos_cargas_puntuales[self.indice_cargas_puntuales]
        elif self.pregunta_actual==self.tipos_cargas_puntuales[0]:
            self.respuestas_cargas_puntuales.append(self.respuesta)
            if self.respuestas_cargas_puntuales[0]=="si":
                self.mostrar_pregunta(self.respuesta,
                                      "Indique las componentes axiales y cortantes de las cargas puntuales a las que estan sometidas los diferentes apoyos. \nEjemplos:\n  Q,Q1,Q2,Q3...\n  Q*sin(alpha),Q*cos(alpha1),Q*sin(alpha2)...\n  Q*cos(beta),Q*sin(beta1),Q*cos(beta2)...\n  0")
                self.respuesta = ""
                if self.respuesta_tipo_de_problema=="portico":
                    for i in range(0, int(self.respuestas_tramos[0])):
                        if self.respuesta_angulos[i]=="90":
                            self.tipos_cargas_puntuales.append(f"Ingrese componente cortante (respecto eje Cortante1) de la carga puntual en el apoyo {i+1}:")
                            self.tipos_cargas_puntuales.append(f"Ingrese componente axial (respecto eje axial1) de la carga puntual en el apoyo {i+1}:")
                        elif self.respuesta_angulos[i]=="0":
                            self.tipos_cargas_puntuales.append(
                                f"Ingrese componente cortante (respecto eje Cortante2) de la carga puntual en el apoyo {i + 1}:")
                            self.tipos_cargas_puntuales.append(
                                f"Ingrese componente axial (respecto eje axial2) de la carga puntual en el apoyo {i + 1}:")
                        elif self.respuesta_angulos[i]=="270":
                            self.tipos_cargas_puntuales.append(
                                f"Ingrese componente cortante (respecto eje Cortante3) de la carga puntual en el apoyo {i + 1}:")
                            self.tipos_cargas_puntuales.append(
                                f"Ingrese componente axial (respecto eje axial3) de la carga puntual en el apoyo {i + 1}:")
                    if self.respuesta_angulos[-1] == "0":
                        self.tipos_cargas_puntuales.append(
                            f"Ingrese componente cortante (respecto eje Cortante2) de la carga puntual en el apoyo {int(self.respuestas_tramos[0] + 1)}:")
                        self.tipos_cargas_puntuales.append(
                            f"Ingrese componente axial (respecto eje axial2) de la carga puntual en el apoyo {int(self.respuestas_tramos[0] + 1)}:")
                    elif self.respuesta_angulos[-1] == "270":
                        self.tipos_cargas_puntuales.append(
                            f"Ingrese componente cortante (respecto eje Cortante3) de la carga puntual en el apoyo {int(self.respuestas_tramos[0]) + 1}:")
                        self.tipos_cargas_puntuales.append(
                            f"Ingrese componente axial (respecto eje axial3) de la carga puntual en el apoyo {int(self.respuestas_tramos[0]) + 1}:")

                    #self.tipos_cargas_puntuales.append(
                     #   f"Ingrese componente cortante (respecto ejes tramo {int(self.respuestas_tramos[0])}) de la carga puntual del apoyo {int(self.respuestas_tramos[0]) + 1}:")
                    #self.tipos_cargas_puntuales.append(
                     #   f"Ingrese componente axial (respecto ejes tramo {int(self.respuestas_tramos[0])}) de la carga puntual del apoyo {int(self.respuestas_tramos[0])+1}:")
                elif self.respuesta_tipo_de_problema=="barras simples":
                    for i in range(0, int(self.respuestas_tramos[0])+1):
                        self.tipos_cargas_puntuales.append(f"Ingrese componente cortante de la carga puntual en el apoyo {i+1}:")
                        self.tipos_cargas_puntuales.append(f"Ingrese componente axial de la carga puntual en el apoyo {i+1}:")
                self.indice_cargas_puntuales = self.indice_cargas_puntuales + 1
                self.pregunta_actual = self.tipos_cargas_puntuales[self.indice_cargas_puntuales]
            elif self.respuestas_cargas_puntuales[0]=="no":
                for i in range(1, int(self.respuestas_tramos[0]) + 2):
                    # print(self.respuestas_cargas_puntuales[indice])
                    self.Qz.append(0)  # sympify para convertir a valor simbolico
                    self.Qx.append(0)
                self.pregunta_actual = "\n      HAZ DE SOLUCIONES\n"
                self.fin_preguntas = "si"
        elif self.pregunta_actual in self.tipos_cargas_puntuales and self.pregunta_actual != self.tipos_cargas_puntuales[0]:

            self.respuestas_cargas_puntuales.append(self.respuesta)
            self.indice_cargas_puntuales = self.indice_cargas_puntuales + 1
            if self.indice_cargas_puntuales<len(self.tipos_cargas_puntuales):
                self.pregunta_actual=self.tipos_cargas_puntuales[self.indice_cargas_puntuales]
            else:
                #guardamos los valores de las cargas en las listas self.Qz y self.Qx y solucionamos
                self.pregunta_actual="SOLUCIONES"
                self.fin_preguntas = "si"
                indice=1
                print(self.simbolos_conocidos)
                for i in range(1, int(self.respuestas_tramos[0]) +2):
                    self.Qz.append(parse_expr(self.respuestas_cargas_puntuales[indice],
                        local_dict=self.simbolos_conocidos))  # sympify para convertir a valor simbolico
                    self.Qx.append(parse_expr(self.respuestas_cargas_puntuales[indice+1],
                                   local_dict=self.simbolos_conocidos))
                    indice=indice+2

                print(self.Qz)
                #self.Qx = [var for sublist in self.Qx for var in sublist]
                print(self.Qx)
        elif self.pregunta_actual == "Ingrese el nombre de la funcion a graficar (Esfuerzos Cortantes, Momentos, Desplazamientos Cortantes, Giros, Esfuerzos Axiales, Desplazamientos Axiales): ":
            if self.respuesta == "Esfuerzos Cortantes":
                self.inicio = 0
            elif self.respuesta == "Momentos":
                self.inicio = 1
            elif self.respuesta == "Desplazamientos Cortantes":
                self.inicio = 2
            elif self.respuesta == "Giros":
                self.inicio = 3
            elif self.respuesta == "Esfuerzos Axiales":
                self.inicio = 4
            elif self.respuesta == "Desplazamientos Axiales":
                self.inicio = 5
            self.graficas()
        elif self.pregunta_actual == "valores":
            self.i=self.i + 1
            if self.incognita not in self.L_val:
                self.valores[self.incognita] = self.respuesta
                print(self.valores)
                if self.incognita == list(self.valores.keys())[-1]:
                    self.i = 0
                    self.incognita = list(self.L_val)[self.i]
                    self.pregunta_actual = f"Ingrese el valores numérico para {self.incognita}:"
                else:
                    self.incognita = list(self.valores.keys())[self.i]
                    self.pregunta_actual = f"Ingrese el valores numérico para {self.incognita}:"
            else:
                self.L_val[self.incognita] = self.respuesta
                if self.incognita == list(self.L_val.keys())[-1]:
                    self.pregunta_actual = "Ingrese el nombre de la funcion a graficar (Esfuerzos Cortantes, Momentos, Desplazamientos Cortantes, Giros, Esfuerzos Axiales, Desplazamientos Axiales): "

                else:
                    self.incognita = list(self.L_val.keys())[self.i]
                    self.pregunta_actual = f"Ingrese el valores numérico para {self.incognita}:"
        self.n_entry.delete(0, tk.END)  # Borra desde el primer carácter hasta el final
        self.n_entry.focus_set()#Hace que el cursor vuelva al campo de entrada (self.entry), listo para que el usuario escriba sin tener que hacer clic.
        self.mostrar_pregunta(self.respuesta, self.pregunta_actual)
        if self.pregunta_actual==f"Ingrese el valores numérico para {self.incognita}:":
            self.pregunta_actual="valores"
    def mostrar_pregunta(self,respuesta,pregunta):
        self.solution_text.config(state=tk.NORMAL)
        self.solution_text.insert(tk.END, f"{respuesta}\n\n")
        self.solution_text.insert(tk.END, pregunta)
        self.solution_text.see(tk.END)
        self.solution_text.config(state=tk.DISABLED)
        if self.fin_preguntas=="si":
            self.calculo_simbolico()
    def calculo_simbolico(self):
        self.listavariables=[]

        #self.listavalores = []
        for i in range(1, int(self.respuestas_tramos[0]) + 1):
            if self.respuestas_tramos[-1] == "si":
                j = "L"
            else:
                j=f"L{i}"
            self.Vz.append(Symbol(f'Vz{i}({j})'))
            self.Vz0.append(Symbol(f'Vz{i}(0)'))
            self.My.append(Symbol(f'My{i}({j})'))
            self.My0.append(Symbol(f'My{i}(0)'))
            self.theta.append(Symbol(f'theta{i}({j})'))
            self.theta0.append(Symbol(f'theta{i}(0)'))
            self.w.append(Symbol(f'w{i}({j})'))
            self.w0.append(Symbol(f'w{i}(0)'))
            self.N.append(Symbol(f'N{i}({j})'))
            self.N0.append(Symbol(f'N{i}(0)'))
            self.U.append(Symbol(f'U{i}({j})'))
            self.U0.append(Symbol(f'U{i}(0)'))
            self.alpha.append(Symbol(f'alpha{i}'))
            self.EI, self.EA, self.x = symbols('EI EA x')
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
        #for i in range(len(self.listavariables)):
         #   self.listavalores.append("0")
        print(self.listavariables)
        self.ecuaciones = []
        self.ecuaciones_0=[]
        self.haz_de_soluciones = []

        for i in range(0, int(self.respuestas_tramos[0])):
            eq1 = simplify(-integrate(self.dVz_dx[i] + self.qz[i], self.x) + self.Vz0[i])
            eq2 = simplify(-integrate(self.dMy_dx[i] - eq1, self.x) + self.My0[i])
            eq3 = simplify(-integrate(self.dtheta_dx[i] - eq2 / self.EI, self.x) + self.theta0[i])
            eq4 = simplify(-integrate(self.dw_dx[i] + eq3, self.x) + self.w0[i])
            eq5 = simplify(-integrate(self.dN_dx[i] + self.qx[i], self.x) + self.N0[i])
            eq6 = simplify(-integrate(self.dU_dx[i] - eq5 / self.EA, self.x) + self.U0[i])

            self.solution_text.config(state=tk.NORMAL)
            self.solution_text.insert(tk.END, f"\nHaz de soluciones para la barra {i + 1}:\n"
                                              f"Vz{i + 1}(x) = {(str(eq1)).replace('**', '^')}\n"
                                              f"My{i + 1}(x) = {(str(eq2)).replace('**', '^')}\n"
                                              f"theta{i + 1}(x) = {(str(eq3)).replace('**', '^')}\n"
                                              f"w{i + 1}(x) = {(str(eq4)).replace('**', '^')}\n"
                                              f"N{i + 1}(x) = {(str(eq5)).replace('**', '^')}\n"
                                              f"U{i + 1}(x) = {(str(eq6)).replace('**', '^')}\n")
            self.solution_text.see(tk.END)
            self.haz_de_soluciones.extend([eq1, eq2, eq3, eq4, eq5, eq6])
            self.ecuaciones.extend([
                eq1.subs(self.x, self.L[i]) - self.Vz[i],
                eq2.subs(self.x, self.L[i]) - self.My[i],
                eq3.subs(self.x, self.L[i]) - self.theta[i],
                eq4.subs(self.x, self.L[i]) - self.w[i],
                eq5.subs(self.x, self.L[i]) - self.N[i],
                eq6.subs(self.x, self.L[i]) - self.U[i],
            ])
        #print(self.haz_de_soluciones)
        if self.respuestas_apoyos[0] == "1":
            # print("el apoyo inicial es empotrado") #giros y desplazamientos nulos
            #self.ecuaciones_0.extend([self.theta0[0], self.w0[0], self.U0[0]])
            self.ecuaciones.extend([self.theta0[0], self.w0[0], self.U0[0]])
        elif self.respuestas_apoyos[0] == "2":
            #self.ecuaciones.extend([self.My0[0],self.w0[0],self.N0[0]])
            self.ecuaciones.extend([self.My0[0]])
            if self.respuestas_posicion_apoyos_moviles[0]=="vertical":
                self.ecuaciones.extend([self.Vz0[0]*cos(self.alpha[1])-self.N0[0]*sin(self.alpha[1]),self.w0[0]*sin(self.alpha[1])+self.U0*cos(self.alpha[1])])#si esta colocado verticalmente, desplazamiento axial nulo y vertical libre
            elif self.respuestas_posicion_apoyos_moviles[0] == "horizontal":
                self.ecuaciones.extend([-self.Vz0[0] * sin(self.alpha[1]) + self.N0[0] * cos(self.alpha[1]),
                                        self.w0[0] * cos(self.alpha[1]) + self.U0[0] * sin(self.alpha[1])])
        elif self.respuestas_apoyos[0] == "3":
            #self.ecuaciones_0.extend([self.My0[0], self.w0[0], self.U0[0]])
            self.ecuaciones.extend([self.My0[0], self.w0[0], self.U0[0]])
        elif self.respuestas_apoyos[0] == "4":
            # print("el apoyo inicial es libre")
            #self.ecuaciones_0.extend([self.My0[0]])
            self.ecuaciones.extend([self.My0[0]])
            if self.respuestas_cargas_puntuales[0] == "si":
                if self.Qz[0]!="0":
                    self.ecuaciones.extend([self.Vz0[0] + self.Qz[0]])
                else:
                    self.ecuaciones.extend([self.Vz0[0] + self.Qz[0]])
                if self.Qx[0]!="0":
                    self.ecuaciones.extend([self.N0[0] + self.Qx[0]])
                else:
                    self.ecuaciones.extend([self.N0[0] + self.Qx[0]])
            elif self.respuestas_cargas_puntuales[0] == "no":
                self.ecuaciones.extend([self.Vz0[0]])
                self.ecuaciones.extend([self.N0[0]])
        if self.respuestas_apoyos[int(self.respuestas_tramos[0])] == "4":
            # print("el apoyo final es libre")
            self.ecuaciones.extend([self.My[int(self.respuestas_tramos[0]) - 1]])
            if self.respuestas_cargas_puntuales[0] == "si":
                if self.Qz[int(self.respuestas_tramos[0])] != 0:
                    self.ecuaciones.extend([self.Vz[int(self.respuestas_tramos[0]) - 1] - self.Qz[int(self.respuestas_tramos[0])]])
                elif self.Qz[int(self.respuestas_tramos[0])] == 0:
                    self.ecuaciones.extend(
                        [self.Vz[int(self.respuestas_tramos[0]) - 1] - self.Qz[int(self.respuestas_tramos[0])]])
                if self.Qx[int(self.respuestas_tramos[0])] != 0:
                    self.ecuaciones.extend(
                        [self.N[int(self.respuestas_tramos[0]) - 1] - self.Qx[int(self.respuestas_tramos[0])]])
                elif self.Qx[int(self.respuestas_tramos[0])] == 0:
                    self.ecuaciones.extend(
                        [self.N[int(self.respuestas_tramos[0]) - 1] - self.Qx[int(self.respuestas_tramos[0])]])
            elif self.respuestas_cargas_puntuales[0] == "no":
                self.ecuaciones.extend([self.Vz[int(self.respuestas_tramos[0]) - 1]])
                self.ecuaciones.extend([self.N[int(self.respuestas_tramos[0]) - 1]])
        elif self.respuestas_apoyos[int(self.respuestas_tramos[0])] == "1":
            # print("el apoyo final es empotrado") #giros y desplazamientos nulos
            self.ecuaciones.extend([self.theta[int(self.respuestas_tramos[0]) - 1], self.w[int(self.respuestas_tramos[0]) - 1], self.U[int(self.respuestas_tramos[0]) - 1]])
        elif self.respuestas_apoyos[int(self.respuestas_tramos[0])] == "2":
            n = int(self.respuestas_tramos[0]) - 1
            alpha=int(self.respuesta_angulos[n])*pi/180
            self.ecuaciones.extend([self.My[n]])
            if self.respuestas_posicion_apoyos_moviles[0] == "vertical": #desplazamiento respecto lineal de tierra
                self.ecuaciones.extend([self.Qx[n+1]*sin(alpha)-self.Qz[n+1]*cos(alpha) +self.Vz[n]*cos(alpha)-self.N[n]*sin(alpha),self.w[n]*sin(alpha)+self.U[n]*cos(alpha)])#si esta colocado verticalmente, desplazamiento axial nulo y vertical libre
            elif self.respuestas_posicion_apoyos_moviles[0] == "horizontal":
                self.ecuaciones.extend([-self.Qx[n+1]*cos(alpha)+self.Qz[n+1]*sin(alpha)-self.Vz[n] * sin(alpha) + self.N[n] * cos(alpha),self.w[n] * cos(alpha) + self.U[n] * sin(alpha)])
            #self.ecuaciones.extend([self.My[int(self.respuestas_tramos[0]) - 1], self.w[int(self.respuestas_tramos[0]) - 1],self.N[int(self.respuestas_tramos[0]) - 1]])
        elif self.respuestas_apoyos[int(self.respuestas_tramos[0])] == "3":
            self.ecuaciones.extend([self.My[int(self.respuestas_tramos[0]) - 1], self.w[int(self.respuestas_tramos[0]) - 1], self.U[int(self.respuestas_tramos[0]) - 1]])
        if self.respuesta_tipo_de_problema == "portico":
            self.ecuaciones.extend(
                [self.theta[self.esquina_1-1] - self.theta0[self.esquina_1], self.My[self.esquina_1-1] - self.My0[self.esquina_1]])
            self.ecuaciones.extend([self.Vz[self.esquina_1 - 1] - self.N0[self.esquina_1] - self.Qx[self.esquina_1]])
            self.ecuaciones.extend([self.N[self.esquina_1 - 1] + self.Vz0[self.esquina_1] + self.Qz[self.esquina_1]])
            self.ecuaciones.extend([self.U[self.esquina_1 - 1] - self.w0[self.esquina_1], self.w[self.esquina_1 - 1] + self.U0[self.esquina_1]])
            if self.esquina_2 != 0:
                self.ecuaciones.extend(
                    [self.theta[self.esquina_2 - 1] - self.theta0[self.esquina_2],
                     self.My[self.esquina_2 - 1] - self.My0[self.esquina_2]])
                self.ecuaciones.extend(
                    [self.Vz[self.esquina_2 - 1] - self.N0[self.esquina_2] - self.Qx[self.esquina_2]])
                self.ecuaciones.extend(
                    [self.N[self.esquina_2 - 1] + self.Vz0[self.esquina_2] + self.Qz[self.esquina_2]])
                self.ecuaciones.extend([self.U[self.esquina_2 - 1] - self.w0[self.esquina_2],
                                        self.w[self.esquina_2 - 1] + self.U0[self.esquina_2]])
        for i in range(0, int(self.respuestas_tramos[0]) - 1):
            if i==self.esquina_1-1 or i==self.esquina_2-1:
                pass
            else:
                print(i)
                print(self.esquina_1)
                if self.respuestas_apoyos[i + 1] == "4":
                    # print(f"el apoyo{i+2} es una union de tramos")
                    self.ecuaciones.extend(
                        [self.theta[i] - self.theta0[i + 1], self.My[i] - self.My0[i + 1]])#independientemente si es barras simples o porticos
                    #if self.respuestas_cargas_puntuales[0] == "s":

                    #if self.respuesta_tipo_de_problema=="barras simples":
                    self.ecuaciones.extend([self.Vz[i] - self.Vz0[i + 1] - self.Qz[i + 1]])
                    self.ecuaciones.extend([self.N[i] - self.N0[i + 1] - self.Qx[i + 1]])
                    self.ecuaciones.extend([self.w[i] - self.w0[i + 1],self.U[i] - self.U0[i + 1]])

                elif self.respuestas_apoyos[i + 1] == "3":
                    # print(f"el apoyo{i+2} es un apoyo fijo")
                    self.ecuaciones.extend(
                        [self.theta[i] - self.theta0[i + 1], self.My[i] - self.My0[i + 1]])
                    self.ecuaciones.extend([self.w[i], self.w0[i + 1],
                         self.U[i], self.U0[i + 1]])

                elif self.respuestas_apoyos[i + 1] == "2":
                    # print(f"el apoyo{i+2} es un apoyo movil")
                    self.ecuaciones.extend(
                        [self.theta[i] - self.theta0[i + 1], self.My[i] - self.My0[i + 1], self.w[i]-self.w0[i+1], self.U[i]-self.U0[i+1]])
    
                    if self.respuestas_posicion_apoyos_moviles[0] == "vertical":
                        self.ecuaciones.extend([self.Qx[i + 1] * sin(self.alpha[i+1]) - self.Qz[i + 1] * cos(self.alpha[i+1])+self.Vz[i] * cos(self.alpha[i+1]) - self.N[i] * sin(self.alpha[i+1]),
                                                self.w[i] * sin(self.alpha[i+1]) + self.U[i] * cos(self.alpha[i+1])])  # si esta colocado verticalmente, desplazamiento axial nulo y vertical libre
                    elif self.respuestas_posicion_apoyos_moviles[0] == "horizontal":
                        self.ecuaciones.extend([-self.Qx[i + 1] * cos(self.alpha[i+1]) + self.Qz[i + 1] * sin(self.alpha[i+1])-self.Vz[i] * sin(self.alpha[i+1]) + self.N[i] * cos(self.alpha[i+1]),
                                                self.w[i] * cos(self.alpha[i+1]) + self.U[i] * sin(self.alpha[i+1])])

                elif self.respuestas_apoyos[i + 1] == "1":
                    self.ecuaciones.extend(
                        [self.theta[i]-self.theta0[i + 1], self.My[i] - self.My0[i + 1]])
                    self.ecuaciones.extend(
                        [self.w[i], self.w0[i + 1],
                         self.U[i], self.U0[i + 1]])

        for i in range(0, int(self.respuestas_tramos[0])):
            if all(simplify(qzi) == 0 for qzi in self.qx) and all(simplify(qzi) == 0 for qzi in self.Qx) and self.respuesta_angulos[0]=="0":
                self.ecuaciones.extend([self.N0[i],self.N[i],self.U0[i],self.U[i]])
            #elif all(simplify(qzi) == 0 for qzi in self.qx) and all(simplify(qzi) == 0 for qzi in self.Qx):
             #   self.ecuaciones.extend([self.N[i], self.N0[i]])
            if all(simplify(qzi) == 0 for qzi in self.qz) and all(simplify(qzi) == 0 for qzi in self.Qz) and self.respuesta_angulos[0]=="0":
                self.ecuaciones.extend([self.Vz0[i],self.Vz[i],self.w0[i],self.w[i]])
            #elif all(simplify(qzi) == 0 for qzi in self.qz) and all(simplify(qzi) == 0 for qzi in self.Qz):
             #   self.ecuaciones.extend([self.Vz[i], self.Vz0[i]])
        print(self.ecuaciones)
        #print(self.ecuaciones_0)
        self.ecuaciones_filtradas = []
        self.ecuaciones_0_filtradas=[]
        ecuaciones_simb=[]
        if self.respuesta_tipo_de_problema=="barras simples":
            c_val,s_val=symbols("c_alpha s_alpha")
            alpha = int(self.respuesta_angulos[0]) * pi / 180
            #for i in range(0,len(self.ecuaciones)):
            ecuaciones_simb = [eq.subs({cos(alpha): c_val, sin(alpha): s_val}) for eq in self.ecuaciones]
            print(f"ecuacionessustituadsad{ecuaciones_simb}")
            sol_num = solve(ecuaciones_simb, self.listavariables, dict=True)
            sol =  [{k: v.subs({c_val: cos(alpha), s_val: sin(alpha)}) for k, v in s.items()}for s in sol_num]
        else:
            sol = solve(self.ecuaciones, self.listavariables, dict=True)
        #sol = linsolve(self.ecuaciones, self.listavariables)
        #print(sol)
        #print(f"numero de ecuaciones {len(self.ecuaciones_filtradas)}")
        #print(f"numero de incognitas {len(self.listavariables)}")
        #print(self.ecuaciones)
        # reemplazamos las soluciones en el haz de soluciones
        for s in sol:
            for j in range(0, int(self.respuestas_tramos[0]) * 6):
                self.haz_de_soluciones[j] = (self.haz_de_soluciones[j].subs(s))
        print("Soluciones:")
        print()
        print("ecuaciones finales:")
        i = 0
        self.solution_text.insert(tk.END,"\n      HAZ DE SOLUCIONES CON SOLUCIONES PARTICULARES SUSTITUIDAS:\n\n")
        for j in range(0, int(self.respuestas_tramos[0])):
            self.solution_text.insert(tk.END,f"Para la barra {j + 1}\n"
                                             f"Esfuerzos Cortantes:       Vz{j + 1}(x)={str(self.haz_de_soluciones[i]).replace('**', '^')}\n"
                                             f"Momentos:                  My{j + 1}(x) = {str(self.haz_de_soluciones[i + 1]).replace('**', '^')}\n"
                                             f"Giros:                     theta{j + 1}(x) = {str(self.haz_de_soluciones[i + 2]).replace('**', '^')}\n"
                                             f"Desplazamientos Cortantes: w{j + 1}(x) = {str(self.haz_de_soluciones[i + 3]).replace('**', '^')}\n"
                                             f"Esfuerzos Axiales:         N{j + 1}(x) = {str(self.haz_de_soluciones[i + 4]).replace('**', '^')}\n"
                                             f"Desplazamientos Axiales:   U{j + 1}(x) = {str(self.haz_de_soluciones[i + 5]).replace('**', '^')}\n")
            i = i + 6
        self.solution_text.insert(tk.END, "\n     SOLUCIONES PARTICULARES \n\n")
        for s in sol:
            for var, val in s.items():
                #val = val.simplify().subs(sin(self.alpha[0]), tan(self.alpha[0]) * cos(self.alpha[0]))#creo que esto no afecta en nada
                self.solution_text.insert(tk.END,f"{var} = {(str(val)).replace('**', '^')}\n")
                self.solution_text.see(tk.END)


        self.fin_preguntas = "no"
        self.todos_los_simbolos = set()
        for eq in self.haz_de_soluciones:
            self.todos_los_simbolos.update(eq.free_symbols)
        self.valores = {}
        self.L_val = {}
        for s in self.todos_los_simbolos:
            if s != self.x and s not in self.L:
                self.valores[s] = ""#{Q:,q:}
            elif s in self.L:
                self.L_val[s]=""         #{L2:,L1:}
        self.pregunta_actual = f"valores"
        self.items=list(self.valores.items())
        self.i=0
        self.incognita=list(self.valores.keys())[self.i]
        #self.incognita=self.items[self.i]
        #print(self.valores)
        #print(self.items)
        #print(self.incognita)
        #print(self.L_val)
        self.mostrar_pregunta("", f"Ingrese el valores numérico para {self.incognita}:")

    def graficas(self):
        todaslaslineas=[]
        if 'L' in [str(s) for s in self.todos_los_simbolos]:
            for s in range(0, int(self.respuestas_tramos[0])):
                self.L_val[self.L[s]] = list(self.L_val.values())[0]
        print(self.L_val)
        self.ax_graficas.clear()
        expresiones = []
        expr = sympify(self.haz_de_soluciones[self.inicio::6])  # inicio:fin:paso. las expresiones de las funciones que quiero graficar
        #print(expr)
        expresiones.append(expr)
        # print(expresiones)
        expresiones = [var for sublist in expresiones for var in sublist]
        x_offset=0
        #print(L_val)

        for i, expr in enumerate(expresiones):
            expr_num = expr.subs(self.valores)
            expr_num=expr_num.subs(self.L_val)
            #print(expr_num.free_symbols)
            x_local = np.linspace(0, float(self.L_val[self.L[i]]), 200)
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
            linea=self.ax_graficas.plot(x_global, y_vals, label=f"Ecuación Tramo{i + 1}")
            self.ax_graficas.plot([x_global[-1], x_global[0]], [0, 0], marker='o', color="purple")
            self.cortante_text = self.ax_graficas.text(x_global[0]+(x_global[-1] - x_offset) / 2, 0.01, f"Barra {i+1}", fontsize=8,
                                                       color="purple", ha="center")
            todaslaslineas.extend(linea)
            x_offset=x_offset+float(self.L_val[self.L[i]])

        self.ax_graficas.set_xlabel("(x)")
        if self.respuesta=="Momentos":
            self.ax_graficas.set_ylabel("(My)")
        elif self.respuesta=="Esfuerzos Cortantes":
            self.ax_graficas.set_ylabel("(Vz)")
        elif self.respuesta=="Esfuerzos Axiales":
            self.ax_graficas.set_ylabel("(N)")
        elif self.respuesta=="Desplazamientos Axiales":
            self.ax_graficas.set_ylabel("(U)")
        elif self.respuesta=="Desplazamientos Cortantes":
            self.ax_graficas.set_ylabel("(w)")
        elif self.respuesta=="Giros":
            self.ax_graficas.set_ylabel("(theta)")
        self.ax_graficas.set_title(f"Diagrama de {self.respuesta}\n",fontsize=9)
        self.ax_graficas.grid(True)
        self.ax_graficas.xaxis.set_label_coords(1.02, -0.02)

        #plt.legend()
        self.chart.draw()
        cursor = mplcursors.cursor(todaslaslineas, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(
            f"x={sel.target[0]:.2f}\ny={sel.target[1]:.2f}"))

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    root.state("zoomed")
    app = VigaSolverApp(root)
    root.mainloop()

