"""
Creating a binary distillation column.

By David Rinaldi
20/02/2021
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from math import exp as exp
from math import pow as pow

# Storing physical and chemical properties
mw = {
    "benzene": 78,
    "toulene": 92
}

# Simple mass balance to get mole fractions of benzene
A = 'benzene'
B = 'toulene'

xF = 40/mw[A] / (40/mw[A] + 60/mw[B])
xD = 97/mw[A] / (97/mw[A] + 3/mw[B])
xB = 2/mw[A] / (2/mw[A] + 98/mw[B])

print("""
Mole Fractions of Benezene
xF: %.2f
xD: %.2f
xB: %.2f""" %(xF, xD, xB))

# Storing saturation pressure
x_Psat = {
    "benzene": lambda T: 1 - T/562.2,
    "toulene": lambda T: 1 - T/591.8
}

Psat = {
    "benzene": lambda T: (48.9 * exp((-6.98273 * x_Psat[A](T) + 1.33213 * pow(x_Psat[A](T), 3/2) - 2.62863 * pow(x_Psat[A](T), 3) - 3.33399 * pow(x_Psat[A](T), 6)) / (1 - x_Psat[A](T)))),
    "toulene": lambda T: (41 * exp((-7.28607* x_Psat[B](T) + 1.38091 * pow(x_Psat[B](T), 3/2) - 2.83433 * pow(x_Psat[B](T), 3) - 2.79168 * pow(x_Psat[B](T), 6)) / (1 - x_Psat[B](T))))
}

# Solving the equation to find Tsat
Tsat = {
    "benzene": lambda P, s=A: fsolve(lambda T: Psat[s](T) - P, 400)[0],
    "toulene": lambda P, s=B: fsolve(lambda T: Psat[s](T) - P, 400)[0]
}

P = 1.01325 # Atmospheric pressure

T_A = Tsat[A](P)
T_B = Tsat[B](P)

print("""
Saturation Temperature
Benzene: %.1f K
Toulene: %.1f K""" % (T_A, T_B))

T = np.linspace(T_A, T_B) # Create a list of numbers

# Equilibrium Diagram
x = lambda T: ((P - Psat[B](T))/(Psat[A](T) - Psat[B](T)))
y = lambda T: x(T)*Psat[A](T)/P

# Plotting the Data
plt.figure(figsize=(7, 7))
plt.plot([x(T) for T in T], [y(T) for T in T])

plt.plot([0,1], [0,1], "b--")
plt.axis("equal")
plt.xticks(np.linspace(0, 1.0, 11))
plt.yticks(np.linspace(0.05, 1.0, 20))

plt.title("Equilibrium Diagram for %s/%s at P = %f bar" % (A, B, P))
plt.xlabel("Liquid Mole Fraction %s" % A)
plt.ylabel("Vapour Mole Fraction %s" % B)

# Getting Feed Line
Tbub = fsolve(lambda T: x(T) - xF, np.mean(T))
yF = y(Tbub[0])

# Operating Lines
print("""
Operating Line Calculations""")
R_D = 3.5 # Reflux ratio
R_slope = R_D/(R_D + 1)
R_intercept = xD/(R_D + 1)
print("Rectifying line intercept: %.2f" % R_intercept)
zF = R_slope * xF + R_intercept
print("Rectifying and stripping line intercept: %.2f" % zF)
S_slope = (zF - xB)/(xF - xB)
S = 1/(S_slope - 1)
print("Stripping factor: %.2f" % S)

# Finding Ideal Plates
plt.plot([xD, xD], [0, xD], "r--")
plt.plot(xD, xD, "ro", ms=10)
plt.text(xD-0.11, 0.02, "xD = %.2f" % xD)

plt.plot([xF, xF, xF], [0, xF, yF], "r--")
plt.plot([xF, xF], [xF, yF], "ro", ms=10)
plt.text(xF+0.01, 0.02, "xF = %.2f" % xF)
plt.text(xF-0.1, yF+0.02, "yF= %.2f" % yF)

plt.plot([xB, xB], [0, xB], "r--")
plt.plot(xB, xB, "ro", ms=10)
plt.text(xB+0.01, 0.02, "xB = %.2f" % xB)

plt.plot([xD, xF], [xD, zF], 'r-')
plt.plot([xB, xF], [xB, zF], 'r-')

# Plotting the ideal stages
xP = xD
yP = xD

nTray = 0
located_feed = False
fTray = None

while xP > xB:
    nTray += 1.0

    # Store (xP, yP) in (xQ, yQ)
    xQ = xP
    yQ = yP

    # Solve for new xP and plot horizonal line
    Tdew = fsolve(lambda T: y(T) - yP, 400)
    xP = x(Tdew)
    plt.plot([xQ,xP], [yQ, yP], 'r')

    # Plot a numbered circle indicating the ideal trays
    if xP > xB:
        plt.plot(xP, yP, 'ro', ms=5)
        plt.text(xP - 0.03, yP, nTray)

        if located_feed is False and xP < xF:
            located_feed = True
            fTray = nTray
            plt.text(0.05, 0.80, "Feed tray location: %i" % fTray)

        # Store xP in xQ
        xQ = xP

        # Compute new yP and plot vertical line
        yP = min([xD - R_slope * (xD - xP), xB + ((S + 1)/S)*(xP-xB)])
        plt.plot([xQ, xP], [yQ, yP], "r")

nTray -= 1 # Accounts for reboiler

plt.text(0.05, 0.85, "nTrays = %i" % nTray)

plt.xlim(0, 1)
plt.ylim(0, 1)
plt.grid()
plt.show()