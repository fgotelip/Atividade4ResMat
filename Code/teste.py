import sympy as sp

x = sp.symbols('x')
f1 = x**2 + 2*x + 1

parte1 = f1.as_ordered_terms()[1]
f1 = f1 - parte1
integral = sp.integrate(parte1, x)

f1 = f1 + integral
print(f1)