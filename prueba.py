import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class VigaSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solver de Vigas")
        self.root.geometry("1400x800")  # Aumentamos el tamaño de la ventana
        self.style = tb.Style("cosmo")

        # === FRAME PRINCIPAL ===
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=BOTH, expand=True)

        # === FRAME SUPERIOR ===
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=BOTH, expand=True)

        # Izquierda: Entradas
        self.left_top = ttk.Frame(self.top_frame, padding=20)
        self.left_top.pack(side=LEFT, fill=BOTH, expand=True)

        self.build_input_frame()

        # Derecha: Canvas dibujo
        self.right_top = ttk.Frame(self.top_frame, padding=20,style="Custom.TFrame")
        self.style.configure("Custom.TFrame", background="white")
        self.right_top.pack(side=LEFT, fill=BOTH, expand=True)

        self.canvas = tk.Canvas(self.right_top, bg='white', highlightbackground="black", highlightthickness=1)
        self.canvas.pack(fill=BOTH, expand=True)

        # === FRAME INFERIOR ===
        self.bottom_frame = ttk.Frame(self.main_frame)
        self.bottom_frame.pack(fill=BOTH, expand=True)

        # Izquierda: Gráfica matplotlib
        self.left_bottom = ttk.Frame(self.bottom_frame, padding=20)
        self.left_bottom.pack(side=LEFT, fill=BOTH, expand=True)

        self.figure, self.ax = plt.subplots(figsize=(7, 5))  # Gráfico más grande
        self.chart = FigureCanvasTkAgg(self.figure, self.left_bottom)
        self.chart.get_tk_widget().pack(fill=BOTH, expand=True)

        # Derecha: Texto scrolleable con soluciones
        self.right_bottom = ttk.Frame(self.bottom_frame, padding=20)
        self.right_bottom.pack(side=LEFT, fill=BOTH, expand=True)

        ttk.Label(self.right_bottom, text="SOLUCIONES", font=("Segoe UI", 14, "bold")).pack()
        self.solution_text = ScrolledText(self.right_bottom, wrap=tk.WORD, height=25, font=("Courier New", 12))
        self.solution_text.pack(fill=BOTH, expand=True)

    def build_input_frame(self):
        font_label = ("Segoe UI", 12)
        font_entry = ("Segoe UI", 12)

        ttk.Label(self.left_top, text="Número de tramos:", font=font_label).pack(anchor="w", pady=5)
        self.n_entry = ttk.Entry(self.left_top, font=font_entry)
        self.n_entry.pack(fill=X, pady=5)

        ttk.Label(self.left_top, text="Longitudes (separadas por coma):", font=font_label).pack(anchor="w", pady=5)
        self.L_entry = ttk.Entry(self.left_top, font=font_entry)
        self.L_entry.pack(fill=X, pady=5)

        ttk.Label(self.left_top, text="Cargas qz (una por tramo):", font=font_label).pack(anchor="w", pady=5)
        self.qz_entry = ttk.Entry(self.left_top, font=font_entry)
        self.qz_entry.pack(fill=X, pady=5)

        ttk.Button(self.left_top, text="Calcular", command=self.procesar_datos, bootstyle=SUCCESS, width=20).pack(pady=20)

    def procesar_datos(self):
        try:
            n = int(self.n_entry.get())
            L_list = [float(val.strip()) for val in self.L_entry.get().split(',')]
            qz_inputs = self.qz_entry.get().split(',')

            if len(L_list) != n or len(qz_inputs) != n:
                self.solution_text.insert(tk.END, "Error: Debe ingresar un valor por tramo.\n")
                return

            self.canvas.delete("all")
            self.ax.clear()
            self.solution_text.delete("1.0", tk.END)

            self.dibujar_viga(L_list)
            self.calculo_simbolico(n, L_list, qz_inputs)

        except Exception as e:
            self.solution_text.insert(tk.END, f"Error: {str(e)}\n")

    def dibujar_viga(self, longitudes):
        start_x = 50
        y = 150
        escala = 80  # más grande
        for L in longitudes:
            end_x = start_x + L * escala
            self.canvas.create_line(start_x, y, end_x, y, width=4)
            self.canvas.create_oval(start_x - 4, y - 4, start_x + 4, y + 4, fill="black")
            start_x = end_x
        self.canvas.create_oval(start_x - 4, y - 4, start_x + 4, y + 4, fill="black")

    def calculo_simbolico(self, n, L_list, qz_inputs):
        x, EI = sp.symbols('x EI')
        soluciones = []

        for i in range(n):
            L = L_list[i]
            qz_str = qz_inputs[i].strip()
            qz = sp.sympify(qz_str) if qz_str not in ['q', '0'] else sp.Symbol(f'q{i + 1}')
            Vz0 = sp.Symbol(f'Vz0{i + 1}')
            My0 = sp.Symbol(f'My0{i + 1}')
            theta0 = sp.Symbol(f'theta0{i + 1}')
            w0 = sp.Symbol(f'w0{i + 1}')

            Vz = -sp.integrate(qz, x) + Vz0
            My = sp.integrate(Vz, x) + My0
            theta = sp.integrate(My / EI, x) + theta0
            w = sp.integrate(theta, x) + w0

            self.solution_text.insert(tk.END, f"\nTramo {i + 1}:\n")
            self.solution_text.insert(tk.END, f"Vz(x) = {sp.simplify(Vz)}\n")
            self.solution_text.insert(tk.END, f"My(x) = {sp.simplify(My)}\n")
            self.solution_text.insert(tk.END, f"theta(x) = {sp.simplify(theta)}\n")
            self.solution_text.insert(tk.END, f"w(x) = {sp.simplify(w)}\n")

            # === GRÁFICA DE MOMENTO My(x) ===
            xx = [val / 20 for val in range(0, int(L * 20) + 1)]
            fx = [float(My.subs({x: xi, EI: 1, Vz0: 0, My0: 0, theta0: 0, w0: 0, qz: 1})) for xi in xx]
            self.ax.plot(xx, fx, label=f'Tramo {i + 1}')

        self.ax.set_title("Momento Flector My(x)")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("My(x)")
        self.ax.legend()
        self.ax.grid(True)
        self.chart.draw()


if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = VigaSolverApp(root)
    root.mainloop()
