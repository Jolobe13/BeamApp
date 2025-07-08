import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, StringVar
import math
from ttkbootstrap import Style
from tkinter import PhotoImage
class VentanaPrincipal():
    def __init__(self):
    # Crear ventana
        self.root = ttk.Window(themename="flatly")
        self.root.geometry("1200x800")

        self.style = Style()
        # ============ Canvas para dibujar ============

        self.marco = ttk.Frame(self.root, padding=50, borderwidth=3, relief="solid")
        self.marco.pack(pady=10)
        self.canvas = Canvas(self.marco, bg="white", width=1000, height=400)
        self.canvas.pack(pady=0)

        # ============ Área de preguntas y entrada ============
        self.frame1 = ttk.Frame(self.root, padding=0)
        self.frame1.pack(fill=X, padx=10, pady=5)
        self.frame2 = ttk.Frame(self.root,width=600)
        self.frame2.pack(side=LEFT, padx=10, pady=5)
        self.frame5 = ttk.Frame(self.root,width=600)
        self.frame5.pack(side=LEFT, padx=10, pady=5)
        self.frame3=ttk.Frame(self.frame5,width=600)
        self.frame3.pack(side=TOP, padx=10, pady=5)
        self.frame4=ttk.Frame(self.frame5,width=600)
        self.frame4.pack(side=BOTTOM, padx=10, pady=5)

        # Etiqueta para mostrar la pregunta

        self.pregunta_label1 = ttk.Label(self.frame1, text=f"", font=("Segoe UI", 12))
        self.pregunta_label1.pack(side=TOP, pady=5)
        self.pregunta="Indique el número de tramos:"
        self.pregunta_label = ttk.Label(self.frame1, text=f"{self.pregunta}", font=("Segoe UI", 12))
        self.pregunta_label.pack(side=LEFT, pady=5)


        # Entrada de texto
        self.respuesta_var = StringVar()
        self.entrada = ttk.Entry(self.frame1, textvariable=self.respuesta_var, width=30)
        self.entrada.pack(side=LEFT, pady=5)

        # Frame para botones de Sí / No
        # Estado de flujo
        self.estado_pregunta = {"paso": 1}
        #boton para enviar respuesta
        self.boton_responder = ttk.Button(self.frame1, text="Responder", command=self.procesar_respuesta)
        self.boton_responder.pack(side=LEFT, padx=10)
        self.boton_reiniciar = ttk.Button(self.frame4, text="Reiniciar", command=self.reiniciar)
        self.boton_reiniciar.pack(side=LEFT, padx=10)
        self.boton_reiniciar.config(state="disabled")
        self.boton_calcular = ttk.Button(self.frame4, text="Calcular", command=self.calcular)
        self.boton_calcular.pack(side=LEFT, padx=10)
        self.boton_calcular.config(state="disabled")

        self.paso=1
        self.listaangulos= {}
        self.numeroangulo = 1
        self.listaapoyos={}
        self.cuentaapoyos=1
        self.listacargas={}
        self.cuentacargas=1
        # Ejecutar app
        self.root.mainloop()
    def procesar_respuesta(self):
        self.respuesta = self.respuesta_var.get().strip().lower()  # Normalizamos

        if self.paso == 1:
            self.numerotramos=int(self.respuesta_var.get())
            try:
                self.numerotramos = int(self.respuesta)
                if self.numerotramos < 1:
                    self.pregunta_label.config(text="El número debe ser mayor que 0.")
                    return
            except ValueError:
                self.pregunta_label.config(text="Por favor, introduce un número válido.")
                return
            # Coordenadas del centro
            x0, y0 = 25, 200
            self.longitud = 600/self.numerotramos

            for i in range(self.numerotramos):
                #angulo = 2 * math.pi * i / n_lineas  # Radianes
                x1 = x0 + self.longitud
                y1 = y0  # Eje y invertido en tkinter
                self.canvas.create_line(x0, y0, x1, y1, fill="blue", width=2)
                self.canvas.create_line(x0,y0-10,x0,y0+10, fill="blue", width=2)
                self.canvas.create_line(x1, y1 - 10, x1, y1 + 10, fill="blue", width=2)
                x0=x1
                y0=y1
            #self.canvas.pack(expand=True)

            self.pregunta_label1.config(text=f"Se dibujaron {self.numerotramos} tramos.")
            self.pregunta_label.config(text=f"Indique ángulo en grados de alfa1")

            # Limpiar campo de entrada
            self.respuesta_var.set("")
            self.paso = self.paso + 1
            for i in range(1, self.numerotramos + 1):
                nombre = f"angulo{i}"
                self.listaangulos[nombre] = 0

        elif self.paso == 2:
            self.canvas.delete("all")
            self.respuesta = int(self.respuesta_var.get())
            self.listaangulos[f"angulo{self.numeroangulo}"]=math.radians(int(self.respuesta))
            self.numeroangulo=self.numeroangulo+1
            print(self.listaangulos)
            x0, y0 = 25, 200
            for i in range(1,self.numerotramos+1):
                #angulo = 2 * math.pi * i / n_lineas  # Radianes
                x1 = x0 + self.longitud*math.cos(self.listaangulos[f"angulo{i}"])
                y1 = y0 - self.longitud*math.sin(self.listaangulos[f"angulo{i}"]) # Eje y invertido en tkinter
                self.canvas.create_line(x0, y0, x1, y1, fill="blue", width=2)
                self.canvas.create_line(x0,y0-10,x0,y0+10, fill="blue", width=2)
                self.canvas.create_line(x1, y1 - 10, x1, y1 + 10, fill="blue", width=2)
                x0=x1
                y0=y1

            self.respuesta_var.set("")
            if self.numeroangulo<self.numerotramos:
                self.pregunta_label.config(text=f"Indique ángulo en grados de alfa{self.numeroangulo}")
            elif self.numeroangulo==self.numerotramos:
                self.pregunta_label.config(text=f"Indique ángulo en grados de alfa{self.numeroangulo}")
            else:
                self.paso = self.paso + 1
                self.pregunta_label.config(text="Indique tipo de apoyo 1")
                self.entrada.config(state="disabled")
                self.boton_responder.config(state="disabled")
                self.procesar_respuesta()
        elif self.paso == 3:

            self.style.configure("Botonesfondoblanco.TButton", foreground="white", background="white")
            self.img_apoyoemp = PhotoImage(file="apoyoempotrado.png")
            self.img_apoyofijo = PhotoImage(file="apoyofijo.png")
            self.img_apoyomovil = PhotoImage(file="apoyomovil.png")
            self.img_sinapoyo = PhotoImage(file="sinapoyo.png")

            # Crear botón con imagen
            self.btn_imagenapoyoemp = ttk.Button(self.frame2, style="Botonesfondoblanco.TButton",
                                                 image=self.img_apoyoemp,command=lambda: self.guardarapoyo("apoyo empotrado"))
            self.btn_imagenapoyofijo = ttk.Button(self.frame2, style="Botonesfondoblanco.TButton",
                                                  image=self.img_apoyofijo,command=lambda:self.guardarapoyo("apoyo fijo"))
            self.btn_imagenapoyomovil = ttk.Button(self.frame2, style="Botonesfondoblanco.TButton",
                                                   image=self.img_apoyomovil,command=lambda:self.guardarapoyo("apoyo movil"))
            self.btn_imagensinapoyo = ttk.Button(self.frame2, style="Botonesfondoblanco.TButton",
                                                   image=self.img_sinapoyo,command=lambda:self.guardarapoyo("sin apoyo"))
            self.btn_imagenapoyoemp.grid(row=0,column=0)
            self.btn_imagenapoyofijo.grid(row=0,column=1)
            self.btn_imagenapoyomovil.grid(row=1,column=0)
            self.btn_imagensinapoyo.grid(row=1,column=1)
        elif self.paso == 4:
            self.listacargas[f"qz{self.cuentacargas}"]=str(self.respuesta_var.get())
            self.cuentacargas=self.cuentacargas+1
            self.pregunta_label.config(text=f"Indique tipo de carga cortante tramo {self.cuentacargas}")
            self.respuesta_var.set("")
            print(self.listacargas)
    def guardarapoyo(self,tipo):
        self.tipo = tipo
        self.pregunta_label1.config(text=f"El apoyo {self.cuentaapoyos} es {self.tipo}")
        self.listaapoyos[f"apoyo{self.cuentaapoyos}"]=self.tipo
        print(self.listaapoyos)
        self.cuentaapoyos=self.cuentaapoyos+1
        self.pregunta_label.config(text=f"Indique tipo de apoyo {self.cuentaapoyos}")
        if self.cuentaapoyos > self.numerotramos + 1:
            self.paso = self.paso + 1
            self.pregunta_label.config(text=f"Indique tipo de carga cortante tramo 1")
            self.btn_imagenapoyoemp.grid_forget()
            self.btn_imagenapoyofijo.grid_forget()
            self.btn_imagenapoyomovil.grid_forget()
            self.btn_imagensinapoyo.grid_forget()
            self.entrada.config(state="able")
            self.boton_responder.config(state="able")
            for i in range(1,self.numerotramos+1):
                nombre= f"qz{i}"
                self.listacargas[nombre]=0
            for i in range(1,self.numerotramos+1):
                nombre= f"qx{i}"
                self.listacargas[nombre]=0
            for i in range(1,self.numerotramos+1):
                nombre= f"Q{i}"
                self.listacargas[nombre]=0
    def calcular(self):
        print("calculando")
    def reiniciar(self):
        self.canvas.delete("all")  # Borrar dibujos anteriores
        self.paso=1
VentanaPrincipal()
