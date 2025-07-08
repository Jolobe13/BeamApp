import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from sympy import symbols, Symbol, simplify, integrate, diff, sin
from sympy.parsing.sympy_parser import parse_expr
import os
EI, x, EA, q, L = symbols('EI x EA q L')

class BeamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BeamApp")

        # Layout principal
        self.frame_izq = tk.Frame(root, width=600, bg="lightgray", padx=10)
        self.frame_der = tk.Frame(root, width=800, bg="white", padx=10)

        self.frame_izq.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Número de tramos (solo una vez al principio)
        tk.Label(self.frame_izq, text="Número de tramos:", bg="lightgray").pack(anchor="w")
        self.tramos_entry = tk.Entry(self.frame_izq)
        self.tramos_entry.pack(anchor="w")

        self.btn_iniciar = tk.Button(self.frame_izq, text="Iniciar", command=self.iniciar)
        self.btn_iniciar.pack(pady=10)

        self.texto_pregunta = ScrolledText(self.frame_izq, width=61, height=20)
        self.texto_pregunta.pack(fill=tk.BOTH, expand=True)

        self.boton_calcular = tk.Button(self.frame_izq, text="Siguiente", state=tk.DISABLED, command=self.comprobar_respuestas)
        self.boton_calcular.pack(pady=10)

        self.texto_resultado = ScrolledText(self.frame_der, wrap="word")
        self.texto_resultado.pack(fill=tk.BOTH, expand=True)

        # Control del flujo
        self.tramo_actual = 1
        self.etapa = 'angulos'  # qz → qx
        self.respuestas = {}
        self.datosproblema = []
        self.incognitas = {}
        self.n = 0

    def iniciar(self):
        try:
            self.n = int(self.tramos_entry.get())
        except ValueError:
            self.texto_resultado.insert(tk.END, "⚠️ Número de tramos inválido\n")
            return
        #hago la primera pregunta
        self.ruta_carpeta = "/Users/jolob/PycharmProjects/pythonProject3"
        self.ruta_archivo = os.path.join(self.ruta_carpeta, 'Datosinterfaz.txt')

        with open(self.ruta_archivo, 'w') as archivo:
            archivo.write(f"Ingrese valor del ángulo en grados (ej: 0,45,90) de...\n")
            for i in range(1, self.n + 1):
                archivo.write(f"    alfa{i} ==\n")
        with open(self.ruta_archivo, 'r') as archivo:
            self.preguntas = archivo.read()
        self.texto_pregunta.delete("1.0", tk.END)
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_pregunta.insert(tk.END, self.preguntas)  # inserto el contenido del txt

        self.finpreguntas = 'no ok'

        self.boton_calcular.config(state=tk.NORMAL)
        self.tramos_entry.config(state=tk.DISABLED)
        self.btn_iniciar.config(state=tk.DISABLED)

        #self.preguntar()

    def preguntar(self):
        # self.texto_pregunta.delete("1.0", tk.END)
        # Escribir en el archivo definido usando 'with open'. Si el archivo no existe, esta función lo crea
        if self.etapa=='apoyos':
            with open(self.ruta_archivo, 'w') as archivo:
                archivo.write("\nIngrese tipo de apoyo (ej: 1,2,3,4) de...\n1:apoyo empotrado(theta=0,w=U=0)    2:apoyo movil(M=0)\n3:apoyo fijo(M=0,w=U=0)    4:sin apoyo(M=0)\n\n")
                for i in range(1, self.n + 2):
                    archivo.write(f"    apoyo{i} ==\n")
        elif self.etapa=="cargas":
            with open(self.ruta_archivo, 'w') as archivo:
                archivo.write("Ingrese tipo de carga qz (ej: 0,q,ql,sin(alfa1) de...\n")
                for i in range(1, self.n + 1):
                    archivo.write(f"    qz{i}==\n")
                archivo.write("Ingrese tipo de carga qx (ej: 0,q,ql,cos(alfa1) de...\n")
                for i in range(1, self.n + 1):
                    archivo.write(f"    qx{i}==\n")
        elif self.etapa=="cargaspuntuales":
            with open(self.ruta_archivo, 'w') as archivo:
                archivo.write("¿hay alguna carga puntual?(s/n) ==\n")
        elif self.etapa=="cargaspuntuales2.0":
            with open(self.ruta_archivo, 'w') as archivo:
                archivo.write(f"Indique valor de la carga puntual (ej: Q,-Q,0) en cada apoyo de la estructura...\n")
                for i in range(1, self.n + 2):
                    archivo.write(f"    En el apoyo{i} ==\n")

        with open(self.ruta_archivo, 'r') as archivo:
            self.preguntas = archivo.read()

            print(self.preguntas)#variable que contiene las nuevas preguntas que le hago al usuario
            self.texto_pregunta.insert(tk.END, self.preguntas)

    def comprobar_respuestas(self):
        texto = self.texto_pregunta.get("1.0", tk.END)  # extraemos el comentario de texto desde la segunda linea
        with open("Datosinterfaz.txt", "w") as archivo:
            archivo.write(f"{texto}")
        #compruebo si se ha escrito algo en la ultima linea. En caso afirmativo, se guarda la ultima palabra
        if self.etapa=="angulos":
            with open("Datosinterfaz.txt", "r") as archivo:
                for linea in archivo:
                    if "==" in linea:
                        respuesta = linea.split("==", 1)[1].strip()
                        #self.datosproblema.append(respuesta)
                        continue
            self.etapa="apoyos"
            self.preguntar()
        elif self.etapa=="apoyos":
            with open("Datosinterfaz.txt", "r") as archivo:
                for linea in archivo:
                    if "==" in linea:
                        respuesta = linea.split("==", 1)[1].strip()
                        #self.datosproblema.append(respuesta)
                        continue
            self.etapa="cargas"
            self.preguntar()
        elif self.etapa=="cargas":
            with open("Datosinterfaz.txt", "r") as archivo:
                for linea in archivo:
                    if "==" in linea:
                        respuesta = linea.split("==", 1)[1].strip()
                        #self.datosproblema.append(respuesta)
                        continue
            self.etapa="cargaspuntuales"
            self.preguntar()
        elif self.etapa=="cargaspuntuales":
            with open("Datosinterfaz.txt", "r") as archivo:
                for linea in archivo:
                    if "==" in linea:
                        respuesta = linea.split("==", 1)[1].strip()
            if respuesta=="s":
                self.etapa="cargaspuntuales2.0"
                self.preguntar()
            elif respuesta=="n":
                self.boton_calcular.config(state=tk.DISABLED)
                with open("Datosinterfaz.txt", "r") as archivo:
                    for linea in archivo:
                        if "==" in linea:
                            respuesta = linea.split("==", 1)[1].strip()
                            self.datosproblema.append(respuesta)
                self.mostrar_haz_de_ecuaciones()
            # Obtener el último elemento
        elif self.etapa=="cargaspuntuales2.0":
            self.boton_calcular.config(state=tk.DISABLED)
            with open("Datosinterfaz.txt", "r") as archivo:
                for linea in archivo:
                    if "==" in linea:
                        respuesta = linea.split("==", 1)[1].strip()
                        self.datosproblema.append(respuesta)
            self.mostrar_haz_de_ecuaciones()
        print(self.datosproblema)

    def mostrar_haz_de_ecuaciones(self):
        for i in range(1, self.n + 1):
            Vz, Vz0 = Symbol(f'Vz{i}'), Symbol(f'Vz0{i}')
            My, My0 = Symbol(f'My{i}'), Symbol(f'My0{i}')
            theta, theta0 = Symbol(f'theta{i}'), Symbol(f'theta0{i}')
            w, w0 = Symbol(f'w{i}'), Symbol(f'w0{i}')
            N, N0 = Symbol(f'N{i}'), Symbol(f'N0{i}')
            U, U0 = Symbol(f'U{i}'), Symbol(f'U0{i}')
            L = Symbol(f'L{i}')

            qz_expr = self.datosproblema[self.n+self.n+i]
            qx_expr = self.datosproblema[self.n+self.n+self.n+i]

            qz_expr = parse_expr(qz_expr, evaluate=False)
            qx_expr = parse_expr(qx_expr, evaluate=False)
            print(f"hola{qz_expr}")

            try:
                ec1 = simplify(-integrate(diff(Vz, x) + qz_expr, x) + Vz0)
                ec2 = simplify(-integrate(diff(My, x) - ec1, x) + My0)
                ec3 = simplify(-integrate(diff(theta, x) - ec2 / EI, x) + theta0)
                ec4 = simplify(-integrate(diff(w, x) + ec3, x) + w0)
                ec5 = simplify(-integrate(diff(N, x) + qx_expr, x) + N0)
                ec6 = simplify(-integrate(diff(U, x) - ec5 / EA, x) + U0)

                self.texto_resultado.insert(tk.END, f"\n🔹 Tramo {i}:\n")
                self.texto_resultado.insert(tk.END, f"Vz{i}(x) = {ec1}\n")
                self.texto_resultado.insert(tk.END, f"My{i}(x) = {ec2}\n")
                self.texto_resultado.insert(tk.END, f"theta{i}(x) = {ec3}\n")
                self.texto_resultado.insert(tk.END, f"w{i}(x) = {ec4}\n")
                self.texto_resultado.insert(tk.END, f"N{i}(x) = {ec5}\n")
                self.texto_resultado.insert(tk.END, f"U{i}(x) = {ec6}\n")

            except Exception as e:
                self.texto_resultado.insert(tk.END, f"❌ Error en tramo {i}: {e}\n")
        self.sustituir_condiciones_sustentacion()
    def sustituir_condiciones_sustentacion(self):
        #extraer la informacion de los apoyos y sustituir las variables en el haz
        self.datosapoyos=[]
        for i in range(0,self.n+1):
            self.datosapoyos.append(self.datosproblema[i+self.n])
        if self.datosapoyos.append[0]=="4":
            My01="0"
            Vz01="0"
        elif self.datosapoyos.append[self.n]=="4":
            My01="0"
        ecuaciones=self.texto_resultado.get("1.0", tk.END)
        



# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = BeamApp(root)
    root.geometry("1000x600")
    root.mainloop()

