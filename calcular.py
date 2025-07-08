import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import symbols, sympify, lambdify
import numpy as np

class GraficadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graficador de funciones")

        # Entrada de función
        self.label = tk.Label(root, text="Introduce una función de x (por ejemplo: sin(x), x**2 + 3, etc):")
        self.label.pack(pady=5)

        self.entrada = tk.Entry(root, width=40)
        self.entrada.pack(pady=5)

        # Botón para graficar
        self.boton = tk.Button(root, text="Graficar", command=self.graficar)
        self.boton.pack(pady=5)

        # Área para la gráfica
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ejes = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=root)
        self.canvas.get_tk_widget().pack()

    def graficar(self):
        funcion_str = self.entrada.get()
        x = symbols('x')

        try:
            # Convertir string a expresión simbólica
            expr = sympify(funcion_str)
            f = lambdify(x, expr, modules=["numpy"])

            # Crear dominio y evaluar
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            # Limpiar gráfica anterior
            self.ejes.clear()

            # Dibujar nueva gráfica
            self.ejes.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}")
            self.ejes.set_title("Gráfica de la función")
            self.ejes.set_xlabel("x")
            self.ejes.set_ylabel("f(x)")
            self.ejes.grid(True)
            self.ejes.legend()

            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo interpretar la función.\n\n{e}")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GraficadorApp(root)
    root.mainloop()

