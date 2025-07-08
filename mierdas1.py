from sympy import sympify

mi_lista={"a": ("vz1+vz2","Vx2+Vs3"), "b": "Mz1+Mz2"}
print(mi_lista["a"])
a=sympify(mi_lista["a"])
b=sympify(mi_lista["b"])
expr=[]
expr.extend([a,b])
print(expr)
mi_lista["a"]="seriga"
print(mi_lista["a"])