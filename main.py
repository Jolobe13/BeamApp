import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap import Style
from ttkbootstrap.scrolled import ScrolledText
from calcular import calcularclass
from ttkbootstrap.constants import *
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import StringVar
diccionario=dict(sonido="SIN SONIDO ")
class VentanaPrincipal():
    def __init__(self):
        self.window = ttk.Window(themename='cosmo')
        width = 1700
        height = 800
        self.window.geometry(f"{width}x{height}")
        self.window.attributes("-fullscreen", False)
        self.window.title("Ventana Principal")
        self.window.protocol("WM_DELETE_WINDOW", self.cerrar_meter)
        self.style = Style()
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        # print(screen_height)
        #x_position = (self.screen_width - width) // 2
        #y_position = (self.screen_height - height) // 2
        #self.window.geometry(f"{width}x{height}+{x_position}+{y_position}") #SE ajusta al centro de la pantalla, inncesario si se emplea el atributo “-fullscreen”
        # Se crea el primer Frame y se configura su color
        # ============ Canvas para dibujar ============
        self.canvas = Canvas(self.window, bg="white", width=300, height=300)
        self.canvas.pack(pady=10)

        # ============ Área de preguntas y entrada ============
        self.frame_dialogo = ttk.Frame(self.window, padding=10)
        self.frame_dialogo.pack(fill=X, padx=10, pady=10)
        # Etiqueta para mostrar la pregunta
        self.pregunta_label = ttk.Label(self.frame_dialogo, text="¿Quieres dibujar un círculo?", font=("Segoe UI", 12))
        self.pregunta_label.pack(side=TOP, pady=5)

        # Entrada de texto
        self.respuesta_var = StringVar()
        self.entrada = ttk.Entry(self.frame_dialogo, textvariable=self.respuesta_var, width=30)
        self.entrada.pack(pady=5)
        self.crearbotones()  # SE CREAN LOS 2 BOTONES
        #self.espacio = ttk.Label(self.window, text=" ")  ##LÍNEA en blanco para cuadrar los widgets en la ventana
        #self.espacio.grid(row=0, column=0, columnspan=2, pady=(12, 0))

        #self.style.configure("MuestreandoLabel.TLabel", font=("Arial", 14), background="red", bordercolor="red", foreground="white")  # SE CREAN el estilo del indicador “MUESTREANDO…”
        #self.etiqueta = ttk.Label(self.window, text="", style="MuestreandoLabel.TLabel")  ### INDICADOR DE ADVERTENCIA

        #for i in range(0, 5):
        #    self.window.grid_rowconfigure(f"{i}", weight=1)
         #   self.window.grid_columnconfigure(0, weight=1)
          #  self.window.grid_columnconfigure(1, weight=1)
        self.window.mainloop()


    def crearbotones(self):
        #self.cuadrodibujo = ScrolledText(self.frame1, height=25, width=100, wrap="word")
        # con wrap=”word” configuramos el salto de página del cuadro de texto.
        #self.cuadrodibujo.grid(row=1, column=0,columnspan=4,padx=10,pady=10)
        #self.cuadro_comentarios = ScrolledText(self.frame2, height=18, width=80, wrap="word")
        # con wrap=”word” configuramos el salto de página del cuadro de texto.
       # self.cuadro_comentarios.grid(row=1, column=0,columnspan=4,padx=10,pady=10)
        # SE CREAN primero varios estilos para asociarlos a los botones.
        # Cargar imagen (PNG, GIF o PGM/PPM)
        # Asegúrate de que 'icono.png' esté en el mismo directorio
        self.style.configure("Botonesfondoblanco.TButton", foreground="white", background="white")
        self.img_apoyoemp = PhotoImage(file="apoyoempotrado.png")
        self.img_apoyofijo = PhotoImage(file="apoyofijo.png")
        self.img_apoyomovil = PhotoImage(file="apoyomovil.png")

        # Crear botón con imagen
        self.btn_imagenapoyoemp = ttk.Button(self.window, style="Botonesfondoblanco.TButton", image=self.img_apoyoemp)
        self.btn_imagenapoyofijo = ttk.Button(self.window, style="Botonesfondoblanco.TButton", image=self.img_apoyofijo)
        self.btn_imagenapoyomovil = ttk.Button(self.window, style="Botonesfondoblanco.TButton", image=self.img_apoyomovil)
        #self.btn_imagenapoyoemp.grid(row=2, column=1, padx=10, pady=10)
        #self.btn_imagenapoyofijo.grid(row=2, column=2, padx=10, pady=10)
        #self.btn_imagenapoyomovil.grid(row=2, column=3, padx=10, pady=10)

        self.style.configure('ButtonMain.TButton', width=12, font=("Arial", 24))
        self.style.configure("MuestreandoLabel.TLabel", font=("Arial", 14), background="red", bordercolor="red",foreground="white")
        # SE CREAN LOS widgets de la ventana
        #self.calculartexto = ttk.Label(self.window, text="CALCUANDO...", style="MuestreandoLabel.TLabel")
        ###INDICADOR DE MUESTREAR
        self.boton_reiniciar = ttk.Button(self.window, text="REINICIAR", style='ButtonMain.TButton')
        #self.boton_reiniciar.grid(row=2, column=1, padx=10, pady=10)
        self.boton_reiniciar.pack(side=LEFT, padx=10)
        self.boton_calcular = ttk.Button(self.window, text="CALCULAR", style='ButtonMain.TButton', command=self.calcular)
        self.boton_calcular.pack(side=LEFT, padx=10)
        #self.boton_calcular.grid(row=2, column=2, padx=10, pady=10)

        #self.boton_descargar = ttk.Button(self.window, text="DESCARGAR", style='ButtonMain.TButton')

        #self.boton_descargar.grid(row=3, column=1)
        #self.cr1 = ttk.Radiobutton(self.window, text="Ver datos calibracion",value=1) ##BOTON INVISIBLE QUE MUESTRA LOS DATOS
        #self.cr1.grid(row=4, column=0)

        #self.cr1.invoke()
        #self.cr1.grid_forget()

    def cerrar_meter(self):  # si se desea cerrar. salta un messagebox para confirmar la orden
        screen_height = self.window.winfo_screenheight()
        self.x_position = (self.window.winfo_screenwidth() - 300) // 2
        self.y_position = (screen_height - 100) // 2
        self.style = Style(theme="cosmo")
        self.style.configure('TButton', font=("Helvetica", 12))
        position = (self.x_position, self.y_position)
        if Messagebox.show_question("¿Estás seguro que deseas salir del programa?", title='',
                                    buttons=['Cancelar:secondary', 'Aceptar: danger'], alert=True, parent=self.window,
                                    position=position) == 'Aceptar':
            self.window.destroy()
    def calcular(self): #crear una ventana secundaria con los diagramas
        calcularclass(self.window)

VentanaPrincipal()