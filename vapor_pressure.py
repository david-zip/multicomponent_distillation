"""
Dictionary storing constants for equation from Perry's for vapor pressure

ln(P) = C1 + C2/T + C3*ln(T) + C4*T^C5

P in Pa, T in K

Values found in Perry latest edition (9th edition I think)

By David Rinaldi
10/03/21
"""
import math

constants = {
    "hydrogen": [12.69, -94.896, 1.1125, 0.00032915, 2, 13.95, 33.19],
    "carbon monoxide": [45.698, -1076.6, -4.8814, 0.000075673, 2, 68.15, 132.92],
    "carbon dioxide": [47.0169, -2839, -3.86388, 2.8*10**(-16), 6, 216.58, 304.21],
    "methane": [39.205, -1324.4, -3.4366, 0.000031019, 2, 90.69, 190.56],
    "acetylene": [39.63, -2552.2, -2.78, 2.39*10**(-16), 6, 192.4, 308.3],
    "ethylene": [53.963, -2443, -5.5643, 0.000019079, 2, 104, 282.34],
    "ethane": [51.857, -2598.7, -5.1283, 0.000014913, 2, 90.35, 305.32],
    "methyl-acetylene": [50.242, -3811.9, -4.2526, 6.53*10**(-17), 6, 170.45, 402.4],
    "propadiene": [57.069, -3682.7, -5.5662, 6.5133*10**(-6), 2, 136.87, 394],
    "propylene": [43.905, -3097.8, -3.4425, 1*10**(-16), 6, 87.89, 364.85],
    "propane": [59.078, -3492.6, -6.0669, 0.000010919, 2, 85.47, 369.83],
    "ethyl-acetylene": [77.004, -5054.5, -8.5665, 0.000010161, 2, 147.43, 440],
    "1-butene": [51.836, -4019.2, -4.5229, 4.88*10**(-17), 6, 87.8, 419.5],
    "butane": [66.343, -4363.2, -7.046, 9.4509*10**(-6), 2, 134.86, 425.12],
    "pentane": [78.741, -5420.3, -8.8253, 9.6171*10**(-6), 2, 143.42, 469.7],
    "water": [73.649, -7258.2, -7.3037, 4.1653*10**(-6), 2, 273.16, 647.1],
    "nitrogen": [58.282, -1084.1, -8.3144, 0.044127, 1, 63.15, 126.2]
}

def print_constants(compound: str = None):
    """
    Prints compounds constants, and Tmin and Tmax
    """
    if compound == None:
        compound = input("Compound: ")

    print("\nConstants for %s:" % compound)
    for i in range(len(constants[compound])):
        if i < 5:
            print("C%i: %.2f" % (i+1, constants[compound][i]))
        elif i == 5:
            print("Tmin: %.2f" % constants[compound][i])
        else:
            print("Tmax: %.2f" % constants[compound][i])
        

def find_vapour_pressure(compound, T):
    """
    Calculates and prints vapour pressure of desired component
    """
    pvap = math.exp(constants[compound][0] + constants[compound][1]/T + constants[compound][2]*math.log(T) + constants[compound][3]*T**constants[compound][4])
    print("\nVapour pressure of %s at %i K: %.2f bar" % (compound, T, pvap*(10**-5)))
    
if __name__ == "__main__":
    print_constants("hydrogen")
    print_constants("carbon dioxide")
    print_constants("propylene")
    print_constants("ethane")

    find_vapour_pressure("hydrogen", 33)
    find_vapour_pressure("carbon monoxide", 132.92)
    find_vapour_pressure("propylene", 300)
    find_vapour_pressure("ethane", 313)