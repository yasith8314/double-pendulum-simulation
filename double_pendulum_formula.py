from sympy import symbols, Function, sin, cos, diff, simplify, lambdify, Eq, solve
from scipy.integrate import solve_ivp
import numpy as np  
import matplotlib
matplotlib.use('TkAgg')

def get_formaula():
    #Initiate Required Symbols
    t, g = symbols("t g")
    l1, l2, m1, m2 = symbols("l1 l2 m1 m2")
    a1 = Function("theta1")(t) #a1: theta1
    a2 = Function("theta2")(t) #a2: theta2

    x1 = l1 * sin(a1)
    x2 = l2 * sin(a2) + x1
    y1 = -l1 * cos(a1)
    y2 = -l2 * cos(a2) + y1

    x1_dot = diff(x1, t)
    x2_dot = diff(x2, t)
    y1_dot = diff(y1, t)
    y2_dot = diff(y2, t)

    #Kinetic Energy
    T = simplify(((m1 / 2) * ((x1_dot ** 2) + (y1_dot ** 2))) + ((m2 / 2) * ((x2_dot ** 2) + (y2_dot ** 2))))

    #Potential Energy
    P = simplify((m1 * g * y1) + (m2 * g * y2))

    #Lagrangian
    L = simplify(T - P)

    p_a1 = simplify(diff(L, a1))
    p_a2 = simplify(diff(L, a2))

    p_a1_dot = simplify(diff(L, diff(a1, t)))
    p_a2_dot = simplify(diff(L, diff(a2, t)))

    eq1 = simplify(simplify(diff(p_a1_dot, t)) - p_a1)
    eq2 = simplify(simplify(diff(p_a2_dot, t)) - p_a2)

    #Main Formula
    ee1 = simplify(Eq(eq1 / l1, 0))
    ee2 = simplify(Eq(eq2 / (l2 * m2), 0))

    #Initiate omege
    o1 = Function("omega1")(t)
    o2 = Function("omega2")(t)

    #Replace (theta dot) with omega
    ee1 = ee1.subs(diff(a1, t), o1).subs(diff(a2, t), o2)
    ee2 = ee2.subs(diff(a2, t), o2).subs(diff(a1, t), o1)

    #Get function for omega 1 and 2 by solving main formulas
    result = solve([ee1, ee2], (diff(o1, t), diff(o2, t)))
    f_omega1 = lambdify((a1, a2, o1, o2, l1, l2, m1, m2, g), result[diff(o1, t)])
    f_omega2 = lambdify((a1, a2, o1, o2, l1, l2, m1, m2, g), result[diff(o2, t)])

    return f_omega1, f_omega2


def solve_formula(f_omega1, f_omega2, initial_values: list):
    #Get Values from the list
    a1_0, a2_0, l1_val, l2_val, o1_0, o2_0, m1_val, m2_val = initial_values

    #Convert the values to SI units
    a1_0, a2_0 = a1_0 * (np.pi /180), a2_0 * (np.pi / 180)
    o1_0, o2_0 = o1_0 * (np.pi /180), o2_0 * (np.pi / 180)
    l1_val, l2_val = l1_val / 100, l2_val / 100
    m1_val, m2_val = m1_val / 1000, m2_val / 1000

    #Initialize gravity
    g_val = 9.81

    initial = [a1_0, a2_0, o1_0, o2_0]

    def f(t, y):
        a1, a2, o1, o2 = y
        d_a1, d_a2 = o1, o2
        d_o1 = f_omega1(a1, a2, o1, o2, l1_val, l2_val, m1_val, m2_val, g_val)
        d_o2 = f_omega2(a1, a2, o1, o2, l1_val, l2_val, m1_val, m2_val, g_val)
        return [d_a1, d_a2, d_o1, d_o2]


    #Solotion
    t_eval = np.linspace(0, 60, 2400)
    sol = solve_ivp(f, (0, 60), initial, t_eval=t_eval)

    a1_sol, a2_sol, o1_sol, o2_sol = sol.y

    return a1_sol, a2_sol

def get_angles(l1_val, l2_val, a1_sol, a2_sol):
    x1_val, y1_val, x2_val, y2_val = [], [], [], []
    mul = 2 / 100
    l1_val, l2_val = l1_val * mul, l2_val * mul

    for i in range(len(a1_sol)):
        x1_val.append(l1_val * np.sin(a1_sol[i]))
        y1_val.append(-1 * l1_val * np.cos(a1_sol[i]))
        x2_val.append(x1_val[-1] + l2_val * np.sin(a2_sol[i]))
        y2_val.append(y1_val[-1] + -1 * l2_val * np.cos(a2_sol[i]))

    values = {'x1_val':x1_val, 'x2_val':x2_val, "y1_val":y1_val, 'y2_val':y2_val}
    return values
