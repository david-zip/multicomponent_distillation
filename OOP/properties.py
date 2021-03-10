"""
Dictionary for physical and chemical properties

By David Rinaldi
20/02/2021
"""
import numpy as np
from scipy.optimize import fsolve
from math import exp as exp
from math import pow as pow

# Dictionary containing physical and chemical properties
compounds = {
    "benzene": {
        "mw": 78,
        "x_Psat": lambda T: 1 - T/562.2,
        "Psat": lambda T: (48.9 * exp((-6.98273 * compounds["benzene"]["x_Psat"](T) + 1.33213 * pow(compounds["benzene"]["x_Psat"](T), 3/2) - 2.62863 * pow(compounds["benzene"]["x_Psat"](T), 3) - 3.33399 * pow(compounds["benzene"]["x_Psat"](T), 6)) / (1 - compounds["benzene"]["x_Psat"](T)))),
        "Tsat": lambda P: fsolve(lambda T: compounds["benzene"]["Psat"](T) - P, 400)[0],
    },
    "toulene": {
        "mw": 92,
        "x_Psat": lambda T: 1 - T/591.8,
        "Psat": lambda T: (41 * exp((-7.28607* compounds["toulene"]["x_Psat"](T) + 1.38091 * pow(compounds["toulene"]["x_Psat"](T), 3/2) - 2.83433 * pow(compounds["toulene"]["x_Psat"](T), 3) - 2.79168 * pow(compounds["toulene"]["x_Psat"](T), 6)) / (1 - compounds["toulene"]["x_Psat"](T)))),
        "Tsat": lambda P: fsolve(lambda T: compounds["toulene"]["Psat"](T) - P, 400)[0],
    }
}