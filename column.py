"""
Multicomponent distillation column design using FUG(K) short-cut method

By David Rinaldi
10/03/2021
"""
#pylint:disable=unused-wildcard-import
import numpy as numpy
import math
from scipy.optimize import fsolve

from vapor_pressure import constants
from properties import *

class Distillation():
    """
    Class modelling a multicomponent distillation column using FUG(K) shortcut method

    Assumptions:
    - Approximate column temperature as equal to feed temperature
    - Constant molar overflow
    - Ideal plates
    - T-dependent relative volatilities
    """

    def __init__(self, components, flowrate, LiK, HeK, P, T, q, topRecovery, bottomRecovery):
        """
        Defining properties of the distillation class
        """
        # Storing the components and its flowrates into a dictionary
        self.massFeedComposition = {}
        for i in range(len(components)):
            self.massFeedComposition[components[i]] = flowrate[i]
        
        self.feedComposition = {}
        for i in range(len(components)):
            self.feedComposition[components[i]] = flowrate[i] * mr[components[i]]
        
        self.feedMoleComposition = {}
        for i in range(len(components)):
            self.feedMoleComposition[components[i]] = self.feedComposition[components[i]]/sum(self.feedComposition.values())
        
        # Defining column parameters
        self.components = components
        self.columnPressure = P
        self.columnTemperature = T
        self.q = q
        self.topRecovery = topRecovery
        self.bottomRecovery = bottomRecovery

        # Defining light (LiK) and heavy (HeK) keys
        self.HeK = HeK
        self.LiK = LiK
    
    def print_feed_flowrates(self):
        """
        Prints the feed flowrates and compositions
        """
        print("\nFeed flowrate and composition")
        for key, value in self.massFeedComposition.items():
            print("%s: \t %.2f kg/h\t%.2f" % (key.title(), value, value/sum(n for n in self.massFeedComposition.values())))
        print("Total:\t\t%.2f kg/h\t%.2f" % (sum(n for n in self.massFeedComposition.values()), sum(value/sum(n for n in self.massFeedComposition.values()) for value in self.massFeedComposition.values())))
    
    def print_heavy_and_light_keys(self):
        """
        Prints the user defined light and heavy keys
        """
        print("\nLight and heavy key:")
        print("Light key: %s" % LiK.title())
        print("Heavy key: %s" % HeK.title())

    def find_vapour_pressure(self):
        """
        Calculates and prints component vapour pressure

        Some values may be completely off as it is outside the temperature range
        valid of the component

        A fix for this can be implemented in the future but for it will remain as
        it is
        """

        def pvap_calc(C1, C2, C3, C4, C5):
            """
            Calculates vapour pressure of component in Pa
            
            Constants can be found in vapourPressure.py
            """
            return lambda T: math.exp(C1 + C2/T + C3*math.log(T) + C4*T**C5)
        
        def Pa_kPa(P):
            """Converts from Pa to kPa"""
            return P/1000

        self.vapourPressures = {}
        for i in self.feedComposition.keys():
            vpPa = pvap_calc(constants[i][0], constants[i][1], constants[i][2], constants[i][3], constants[i][4])(self.columnTemperature)
            vpkPa = Pa_kPa(vpPa)
            self.vapourPressures[i] = vpkPa
        
        print("\nComponent vapour pressures")
        for key, value in self.vapourPressures.items():
            if T < constants[key][5]:
                print("%s: \t%.2f kPa (Inaccurate below T-min)" % (key.title(), value))
            elif T > constants[key][6]:
                print("%s: \t%.2f kPa (Inaccurate above T-max)" % (key.title(), value))
            else:
                print("%s: \t%.2f kPa" % (key.title(), value))
        
        return self.vapourPressures

    def find_relative_volatilty(self):
        """
        Calculates and prints relative volatilies
        """
        self.rvHeK = {}
        for i in self.feedComposition.keys():
            rv = self.vapourPressures[i]/self.vapourPressures[HeK]
            self.rvHeK[i] = rv
        
        print("\nRelative volatilites")
        for key, value in self.rvHeK.items():
            print("%s: \t%.2f" % (key.title(), value))
        
        return self.rvHeK

    def print_distillate_flowrate(self):
        """
        Prints the distillate flowrate and compositions
        """
        self.massTopComposition = {}
        self.topComposition = {}
        for key, value in self.rvHeK.items():
            if key == LiK:
                self.topComposition[key] = self.feedComposition[key]*self.topRecovery
                self.massTopComposition[key] = self.topComposition[key]/mr[key]
            elif key == HeK:
                self.topComposition[key] = self.feedComposition[key]*(1 - self.bottomRecovery)
                self.massTopComposition[key] = self.topComposition[key]/mr[key]
            elif self.rvHeK[key] > self.rvHeK[HeK]:
                self.topComposition[key] = self.feedComposition[key]
                self.massTopComposition[key] = self.topComposition[key]/mr[key]
            else:
                self.topComposition[key] = 0
                self.massTopComposition[key] = 0
            
        self.topMoleFraction = {}
        for key in self.topComposition.keys():
            self.topMoleFraction[key] = self.topComposition[key]/sum(n for n in self.topComposition.values())

        print("\nDistillate flowrate and composition")
        for key, value in self.massTopComposition.items():
            print("%s: \t%.2f kg/h\t%.2f" % (key.title(), value, value/sum(n for n in self.massTopComposition.values())))
        print("Total:\t\t%.2f kg/h\t%.2f" % (sum(n for n in self.massTopComposition.values()), sum(value/sum(n for n in self.massTopComposition.values()) for value in self.massTopComposition.values())))        

        return self.topComposition, self.massTopComposition, self.topMoleFraction

    def print_bottom_flowrate(self):
        """
        Prints the bottom flowrate and compositions
        """
        self.massBottomComposition = {}
        self.bottomComposition = {}
        for key, value in self.rvHeK.items():
            if key == LiK:
                self.bottomComposition[key] = self.feedComposition[key]*(1 - self.topRecovery)
                self.massBottomComposition[key] = self.bottomComposition[key]/mr[key]
            elif key == HeK:
                self.bottomComposition[key] = self.feedComposition[key]*self.bottomRecovery
                self.massBottomComposition[key] = self.bottomComposition[key]/mr[key]
            elif self.rvHeK[key] < self.rvHeK[HeK]:
                self.bottomComposition[key] = self.feedComposition[key]
                self.massBottomComposition[key] = self.bottomComposition[key]/mr[key]
            else:
                self.bottomComposition[key] = 0
                self.massBottomComposition[key] = 0
            
        self.bottomMoleFraction = {}
        for key in self.bottomComposition.keys():
            self.bottomMoleFraction[key] = self.bottomComposition[key]/sum(n for n in self.bottomComposition.values())
        
        print("\nBottom flowrate and composition")
        for key, value in self.massBottomComposition.items():
            print("%s: \t%.2f kg/h\t%.2f" % (key.title(), value, value/sum(n for n in self.massBottomComposition.values())))
        print("Total:\t\t%.2f kg/h\t%.2f" % (sum(n for n in self.massBottomComposition.values()), sum(value/sum(n for n in self.massBottomComposition.values()) for value in self.massBottomComposition.values())))        

        return self.bottomComposition, self.massBottomComposition, self.bottomMoleFraction
    
    def find_N_min(self, partialReboiler=True):
        """
        Using Fenske equation, the minimum number of ideal stages is found
        and printed
        """
        # Makes the equation easier to follow
        top1 = self.topMoleFraction[self.LiK]/self.topMoleFraction[self.HeK]
        top2 = self.bottomMoleFraction[self.HeK]/self.bottomMoleFraction[self.LiK]
        top3 = math.log(top1*top2)
        bottom = math.log(self.rvHeK[self.LiK])
        
        self.Nmin = math.ceil(top3/bottom)

        if partialReboiler == False:
            self.Nmin -= 1
        
        print("\nMinimum stages: %i" % self.Nmin)

        return self.Nmin

    def non_key_distribution(self):
        """
        Finds non-key distributions

        Not needed for V1 so will code in later
        """
        pass

    def find_minimum_reflux(self):
        """
        Finds the minimum reflux ratio using both Underwoods equations

        This will be the biggest challenge as need to figure out how to use a solver
        """
        U1 = 1 - self.q

        # First guess of phi
        phi = 0

        # Solver to determine what phi is
        while True:
            U1_guess = 0
            U1_guess_list = []
            for key in self.feedMoleComposition.keys():
                U1a = (self.feedMoleComposition[key]*self.rvHeK[key])/(self.rvHeK[key] - phi)
                U1_guess_list.append(U1a)
            
            U1_guess = sum(U1_guess_list)

            if U1_guess > U1 - 0.01 and U1_guess < U1 + 0.01:
                break
            else:
                phi += 0.01
            
        # Second Underwood equation to find minimum reflux ratio
        U2_list = []
        for key in self.rvHeK.keys():
            U2a = (self.rvHeK[key]*self.topMoleFraction[key])/(self.rvHeK[key] - phi)
            U2_list.append(U2a)
        
        self.Rmin = sum(U2_list) - 1

        print("\nUnderwood equation: Minumum reflux ratio for q = %.2f" % self.q)
        print("phi: \t%.2f" % phi)
        print("Rmin: \t%.2f" % self.Rmin)
        print("1<phi<rvLiK,HeK?: %s" % (1 < phi and phi < self.rvHeK[self.LiK]))

        return self.Rmin
    
    def gilliland_correlation(self, Rf=None):
        """
        Using Gilliland correlation, find the number of ideal plates at
        operating reflux
        """
        if Rf == None:
            Rf = float(input("Desired factor (1.1 - 1.5): "))
            self.R = Rf*self.Rmin
        elif Rf < 1.1 or Rf > 1.5:
            print("Reflux factor is beyond the range")
            Rf = float(input("Desired factor (1.1 - 1.5): "))
            self.R = Rf*self.Rmin
        else:
            self.R = Rf*self.Rmin
        
        X = (self.R - self.Rmin)/(self.R + 1)

        # Makes equation easier to follow
        Ya = (1 + 54.4*X)/(11 + 117.2*X)
        Yb = (X - 1)/(math.pow(X, 0.5))
        Y = 1 - math.exp(float(Ya)*float(Yb))

        self.idealPlates = math.ceil((self.Nmin + Y)/(1 - Y))

        print("\nNumber of ideal plates at operating reflux ratio %.2f" % self.R)
        print("N: %i" % self.idealPlates)
        
        return self.idealPlates
        
    def feed_stage_location(self):
        """
        Uses Kirkbride equation to determine the feed stage location
        
        ratio = Nr/Ns
        """
        inside = (self.feedMoleComposition[self.HeK]/self.feedMoleComposition[self.LiK])*((self.bottomMoleFraction[self.LiK]/self.topMoleFraction[self.HeK])**2)*(sum(self.bottomComposition.values())/sum(self.topComposition.values()))
        ratio = inside**0.206

        # Number of stripping trays
        self.Ns = round(self.idealPlates/(ratio + 1))

        # Number of rectifying trays
        self.Nr = round(self.idealPlates - self.Ns)

        # Ideal feed tray location
        self.idealFeedTray = self.Ns

        print("\nFeed stage location using Kirkbride equation")
        print("Number of rectifying trays: \t%i" % self.Nr)
        print("Number of stripping trays: \t%i" % self.Ns)
        print("Feed tray location: Tray \t%i" % self.idealFeedTray)
    
    def actual_trays(self, efficiency):
        """
        Finds actual number of trays with user defined tray efficiency
        """
        if efficiency > 1:
            self.trayEfficiency = efficiency/100
        else:
            self.trayEfficiency = efficiency
        
        self.actualTrays = math.ceil(self.idealPlates/self.trayEfficiency)

        print("\nActual number of trays: %i" % self.actualTrays)

        return self.trayEfficiency, self.actualTrays
    
    def min_reflix_graph(self):
        """
        Finds the minimum reflux ratio using both Underwoods equations

        This will be the biggest challenge as need to figure out how to use a solver
        """
        U1 = 1 - self.q

        # First guess of phi
        phi = 0
        U1_guess = None

        # Solver to determine what phi is
        while True:
            U1_guess_list = []
            for key in self.feedMoleComposition.keys():
                U1a = (self.feedMoleComposition[key]*self.rvHeK[key])/(self.rvHeK[key] - phi)
                U1_guess_list.append(U1a)
            
            U1_guess = sum(U1_guess_list)

            if U1_guess > U1 - 0.01 and U1_guess < U1 + 0.01:
                break
            else:
                phi += 0.01
            
        # Second Underwood equation to find minimum reflux ratio
        U2_list = []
        for key in self.rvHeK.keys():
            U2a = (self.rvHeK[key]*self.topMoleFraction[key])/(self.rvHeK[key] - phi)
            U2_list.append(U2a)
        
        self.Rmin = sum(U2_list) - 1


if __name__ == "__main__":
    components = ["hydrogen", "carbon monoxide", "carbon dioxide", "methane", "acetylene", "ethylene", "ethane", "methyl-acetylene", "propadiene", "propylene", "propane", "ethyl-acetylene", "1-butene", "butane", "pentane", "water", "nitrogen"]
    flowrates = [0, 0, 0, 0, 0, 0, 0, 532, 0, 0, 0, 2097, 2163, 507, 15399, 0, 0]
    LiK = "ethyl-acetylene"
    HeK = "pentane"
    P = 1810
    T = 273+140
    q = 0.5
    topRecovery = 0.95
    bottomRecovery = 0.9999

    Debutanizer = Distillation(components, flowrates, LiK, HeK, P, T, q, topRecovery, bottomRecovery)

    Debutanizer.print_feed_flowrates()
    Debutanizer.print_heavy_and_light_keys()
    Debutanizer.find_vapour_pressure()
    Debutanizer.find_relative_volatilty()
    Debutanizer.print_distillate_flowrate()
    Debutanizer.print_bottom_flowrate()
    Debutanizer.find_N_min()
    Debutanizer.find_minimum_reflux()
    Debutanizer.gilliland_correlation(1.2)
    Debutanizer.feed_stage_location()
    Debutanizer.actual_trays(0.72)
