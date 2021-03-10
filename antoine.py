"""
Dictionary storing constants for equation from Perry's for vapor pressure

ln(P) = C1 + C2/T + C3*ln(T) + C4*T^C5

P in Pa, T in K

Values found in Perry latest edition (9th edition I think)

Group C3H6 together as I cannot find data for ethyl-acetylene
C3H6 will be known as propadiene

By David Rinaldi
10/03/21
"""

constants = {
    "hydrogen": [12.69, -94.896, 1.1125, 0.00032915, 2],
    "carbon monoxide": [45.698, -1076.6, -4.8814, 0.000075673, 2],
    "carbon dioxide": [47.0169, -2839, -3.86388, 2.8*10**(-16), 6],
    "methane": [39.205, -1324.4, -3.4366, 0.000031019, 2],
    "acetylene": [39.63, -2552.2, -2.78, 2.39*10**(-16), 6],
    "ethylene": [53.963, -2443, -5.5643, 0.000019079, 2],
    "ethane": [51.857, -2598.7, -5.1283, 0.000014913, 2],
    "methyl-acetylene": [50.242, -3811.9, -4.2526, 6.53*10**(-17), 6],
    "propylene": [43.905, -3097.8, -3.4425, 1*10**(-16), 6],
    "propane": [59.078, -3492.6, -6.0669, 0.000010919, 2],
    "propadiene": [57.069, -3682.7, -5.5662, 6.5133*10**(-6), 2],
    "1-butene": [51.836, -4019.2, -4.5229, 4.88*10**(-17), 6],
    "butane": [66.343, -4363.2, -7.046, 9.4509*10**(-6), 2],
    "pentane": [78.741, -5420.3, -8.8253, 9.6171*10**(-6), 2],
    "water": [73.649, -7258.2, -7.3037, 4.1653*10**(-6), 2],
    "nitrogen": [58.282, -1084.1, -8.3144, 0.044127, 1]
}

def print_constants(compound: str = None):
    if compound == None:
        compound = input("Compound: ")

    print("\nConstants for %s:" % compound)
    for i in range(len(constants[compound])):
        print("C%i: %.2f" % (i+1, constants[compound][i]))
    
if __name__ == "__main__":
    print_constants("hydrogen")
    print_constants("carbon dioxide")
    print_constants("propylene")

