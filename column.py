"""
Multicomponent distillation column design using FUG(K) short-cut method

By David Rinaldi
10/03/2021
"""
import numpy as numpy
import math
from scipy.optimize import fsolve

class Distillation():
    """
    Class modelling a multicomponent distillation column
    """

    def __init__(self, components: list, flowrate: list, LK: str, HK: str, P: float, topPurity: float, bottomPurity: float):
        """
        Defining properties of the distillation class
        """
        # Storing the components and its flowrates into a dictionary
        self.feedComposition = {}
        for i in range(len(components)):
            self.feedComposition[components[i]] = flowrate[i]
        
        self.components = components
        self.columnPressure = P
        self.topPurity = topPurity
        self.bottomPurity = bottomPurity

        self.HK = HK
        