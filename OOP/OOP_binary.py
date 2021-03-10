"""
OOP for a distillation model

By David Rinaldi
20/02/2021
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from math import exp as exp
from math import pow as pow

os.chdir("/Users/davidrinaldi/Documents/github/python/chemeng/Distillation/mccable-thiele/OOP")

from properties import compounds

class Feed():
    """Class representing the feed stream for a binary distialltion column"""

    def __init__(self, composition: list, flowrate: list,  P=None, T=None):
        """Defines feed properties"""
        self.feedComposition = {}
        for i in range(len(composition)):
            self.feedComposition[composition[i]] = flowrate[i]
        self.feedPressure = P
        self.feedTemperature = T

    def __len__(self):
        return len(self.feedComposition)

    def print_flowrates(self):
        """Prints the name, flowrate and composition of each component in feed stream"""
        print("\nFeed flowrate and composition")
        for key, value in self.feedComposition.items():
            print("%s:    %.2f kg/h   %.2f" % (key.title(), value, value/sum(n for n in self.feedComposition.values())))
        print("Total:     %.2f kg/h   %.2f" % (sum(n for n in self.feedComposition.values()), 1.00))
    
    def operating_conditions(self):
        if self.feedPressure is not None or self.feedTemperature is not None:
            print("\nFeed operating conditions")
        else:
            print("\nNo operating conditions specified")
        if self.feedPressure is not None:
            print("Pressure: %.2f bar" % self.feedPressure)
        if self.feedTemperature is not None:
            print("Temperature: %.2f K" % self.feedTemperature)

class Distillation(Feed):
    """Class representing a ideal binary distillation column, current use is to find
    feed stage and ideal number of stages"""
    
    def __init__(self, composition, flowrate, P, topPurity=None, bottomPurity=None, R=0):
        """Defining the properties of the distiallation class"""
        super().__init__(self, composition, flowrate)
    
        self.feedComposition = {}
        for i in range(len(composition)):
            self.feedComposition[composition[i]] = flowrate[i]

        self.components = []
        for key in self.feedComposition.keys():
            self.components.append(key)
        
        self.columnPressure = P
        self.topPurity = topPurity
        self.bottomPurity = bottomPurity
        self.R = R # Reflux ratio

        self.xF = self.feedComposition[self.components[0]]/compounds[self.components[0]]['mw'] / (self.feedComposition[self.components[0]]/compounds[self.components[0]]['mw'] + self.feedComposition[self.components[1]]/compounds[self.components[0]]['mw'])
        
        if topPurity is not None:
            self.xD = self.topPurity/compounds[self.components[0]]['mw'] / (self.topPurity/compounds[self.components[0]]['mw'] + (1-self.topPurity)/compounds[self.components[1]]["mw"])
        else:
            self.xD = None
        
        if bottomPurity is not None:
            self.xB = ((1-self.bottomPurity)/compounds[self.components[0]]['mw']) / ((1-self.bottomPurity)/compounds[self.components[0]]['mw'] + self.bottomPurity/compounds[self.components[1]]["mw"])
        else:
            self.xB = None

        TsatList = []
        for key in self.feedComposition.keys():
            TsatList.append(compounds[key]['Tsat'](self.columnPressure))
        self.T = np.linspace(min(n for n in TsatList), max(n for n in TsatList))

    def print_mole_fraction(self):
        """Prints the mole fraction of the top product/light-key"""
        keyslist = list(self.feedComposition.keys())
        
        print("\nMole fraction of %s" % keyslist[0])
        print("xF: %.2f" % self.xF)

        if topPurity is not None:
            print("xD: %.2f" % self.xD)

        if bottomPurity is not None:
            print("xB: %.2f" % self.xB)

    def show_eq_diagram(self):
        """Displays the equilibrium diagram for the composition"""
        x = lambda T: ((self.columnPressure - compounds[self.components[1]]["Psat"](T)) / (compounds[self.components[0]]["Psat"](T) - compounds[self.components[1]]['Psat'](T)))
        y = lambda T: x(T)*compounds[self.components[0]]['Psat'](T)/self.columnPressure

        plt.figure(figsize=(7, 7))
        plt.plot([x(T) for T in self.T], [y(T) for T in self.T])

        plt.plot([0,1], [0,1], "b--")
        plt.axis("equal")
        plt.xticks(np.linspace(0, 1.0, 11))
        plt.yticks(np.linspace(0.05, 1.0, 20))

        plt.title("Equilibrium Diagram for %s/%s at P = %f bar" % (self.components[0], self.components[1], self.columnPressure))
        plt.xlabel("Liquid Mole Fraction %s" % self.components[0])
        plt.ylabel("Vapour Mole Fraction %s" % self.components[1])

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.grid()
        plt.show()

    def operating_conditions(self):
        """Prints operating coniditions of the column"""
        print("\nColumn operating conditions")
        print("Pressure: %.2f bar" % self.columnPressure)
        print("Mean temperature: %.2f K" % np.mean(self.T))
        print("Top temperautre: %.2f K" % self.T[0])
        print("Bottom temperature %.2f K" % self.T[-1])

    def operating_lines(self):
        if self.R == 0:
            self.R = float(input("Reflux ratio: ")) # Reflux ratio
        R_slope = self.R/(self.R + 1)
        R_intercept = self.xD/(self.R + 1)
        zF = R_slope * self.xF + R_intercept
        S_slope = (zF - self.xB)/(self.xF - self.xB)
        S = 1/(S_slope - 1)

        print("\nOperating Line Calculations")
        print("Rectifying line intercept: %.2f" % R_intercept)
        print("Rectifying and stripping line intercept: %.2f" % zF)
        print("Stripping factor: %.2f" % S)

        return self.R

    def ideal_trays_calculation(self):
        """States the number of ideal trays"""
        if self.R == 0:
            self.R = float(input("Reflux ratio: ")) # Reflux ratio
        R_slope = self.R/(self.R + 1)
        R_intercept = self.xD/(self.R + 1)
        zF = R_slope * self.xF + R_intercept
        S_slope = (zF - self.xB)/(self.xF - self.xB)
        S = 1/(S_slope - 1)

        # Plotting the ideal stages
        xP = self.xD
        yP = self.xD

        # Displays the equilibrium diagram for the composition
        x = lambda T: ((self.columnPressure - compounds[self.components[1]]["Psat"](T)) / (compounds[self.components[0]]["Psat"](T) - compounds[self.components[1]]['Psat'](T)))
        y = lambda T: x(T)*compounds[self.components[0]]['Psat'](T)/self.columnPressure

        # Getting Feed Line
        Tbub = fsolve(lambda T: x(T) - self.xF, np.mean(self.T))
        yF = y(Tbub[0])

        # Plotting equilibrium diagram
        plt.figure(figsize=(7, 7))
        plt.plot([x(T) for T in self.T], [y(T) for T in self.T])

        plt.plot([0,1], [0,1], "b--")
        plt.axis("equal")
        plt.xticks(np.linspace(0, 1.0, 11))
        plt.yticks(np.linspace(0.05, 1.0, 20))

        plt.title("Equilibrium Diagram for %s/%s at P = %f bar" % (self.components[0], self.components[1], self.columnPressure))
        plt.xlabel("Liquid Mole Fraction %s" % self.components[0])
        plt.ylabel("Vapour Mole Fraction %s" % self.components[1])

        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.grid()

        # Plotting operating lines
        plt.plot([self.xD, self.xD], [0, self.xD], "r--")
        plt.plot(self.xD, self.xD, "ro", ms=10)
        plt.text(self.xD-0.11, 0.02, "xD = %.2f" % self.xD)

        plt.plot([self.xF, self.xF, self.xF], [0, self.xF, yF], "r--")
        plt.plot([self.xF, self.xF], [self.xF, yF], "ro", ms=10)
        plt.text(self.xF+0.01, 0.02, "xF = %.2f" % self.xF)
        plt.text(self.xF-0.1, yF+0.02, "yF= %.2f" % yF)

        plt.plot([self.xB, self.xB], [0, self.xB], "r--")
        plt.plot(self.xB, self.xB, "ro", ms=10)
        plt.text(self.xB+0.01, 0.02, "xB = %.2f" % self.xB)

        plt.plot([self.xD, self.xF], [self.xD, zF], 'r-')
        plt.plot([self.xB, self.xF], [self.xB, zF], 'r-')

        # Finding ideal number of plats and plotting on a graph
        nTray = 0
        located_feed = False
        fTray = None

        while xP > self.xB:
            nTray += 1.0

            # Store (xP, yP) in (xQ, yQ)
            xQ = xP
            yQ = yP

            # Solve for new xP and plot horizonal line
            Tdew = fsolve(lambda T: y(T) - yP, 400)
            xP = x(Tdew)
            plt.plot([xQ,xP], [yQ, yP], 'r')

            # Plot a numbered circle indicating the ideal trays
            if xP > self.xB:
                plt.plot(xP, yP, 'ro', ms=5)
                plt.text(xP - 0.03, yP, nTray)

                if located_feed is False and xP < self.xF:
                    located_feed = True
                    fTray = nTray
                    plt.text(0.05, 0.80, "Feed tray location: %i" % fTray)

                # Store xP in xQ
                xQ = xP
            
                # Compute new yP and plot vertical line
                yP = min([self.xD - R_slope * (self.xD - xP), self.xB + ((S + 1)/S)*(xP-self.xB)])
                plt.plot([xQ, xP], [yQ, yP], "r")

        nTray -= 1 # Accounts for reboiler
        
        return nTray, fTray

    def number_of_ideal_trays(self):
        """Prints the ideal number of plates and feed plate"""
        nTray, fTray = self.ideal_trays_calculation()
        print("\nIdeal number of trays: %i" % int(nTray))
        print("Feed tray location: %i" % int(fTray))

    def show_ideal_tray_diagram(self):
        """Shows the diagram used to calculate ideal trays"""
        #pylint: disable=unused-variable
        self.ideal_trays_calculation()
        plt.show()

if __name__=="__main__":
    # Define initial conditions
    stream = ["benzene", "toulene"]
    streamComposition = [40, 60]
    topPurity = 0.97
    bottomPurity = 0.98
    Patm = 1.01325
    R = 3.5

    # Define classes
    testFeed = Feed(stream, streamComposition)
    testColumn = Distillation(stream, streamComposition, Patm, topPurity, bottomPurity, R)

    # Test class methods
    testColumn.print_flowrates()
    testColumn.print_mole_fraction()
    testColumn.operating_conditions()
    testColumn.operating_lines()
    testColumn.show_ideal_tray_diagram()
    
    "testColumn.show_eq_diagram()"