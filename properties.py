"""
Dictionary storing the the properties of all molecules

Mr (kg/kmol)
Density (kg/m3)

By David Rinaldi
10/03
"""

mr = {
    "hydrogen": 2.016,
    "carbon monoxide": 28.01,
    "carbon dioxide": 44.01,
    "methane": 16.04,
    "acetylene": 26.04,
    "ethylene": 28.05,
    "ethane": 30.07,
    "methyl-acetylene": 40.06,
    "propadiene": 40.06,
    "propylene": 42.08,
    "propane": 44.1,
    "ethyl-acetylene": 54.09,
    "1-butene": 56.11,
    "butane": 58.12,
    "pentane": 72.15,
    "water": 18.02,
    "nitrogen": 28.01
}

mr = {
    "hydrogen": 2.016,
    "carbon monoxide": 28.01,
    "carbon dioxide": 44.01,
    "methane": 16.04,
    "acetylene": 26.04,
    "ethylene": 28.05,
    "ethane": 30.07,
    "methyl-acetylene": 40.06,
    "propadiene": 40.06,
    "propylene": 42.08,
    "propane": 44.1,
    "ethyl-acetylene": 54.09,
    "1-butene": 56.11,
    "butane": 58.12,
    "pentane": 72.15,
    "water": 18.02,
    "nitrogen": 28.01
}

density = {
    "hydrogen": 3.026,
    "carbon monoxide": 43.58,
    "carbon dioxide": 954.6,
    "methane": 27.1,
    "acetylene": 323.9,
    "ethylene": 323.9,
    "ethane": 69.27,
    "methyl-acetylene": 40.06,
    "propadiene": 40.06,
    "propylene": 42.08,
    "propane": 44.1,
    "ethyl-acetylene": 54.09,
    "1-butene": 56.11,
    "butane": 58.12,
    "pentane": 72.15,
    "water": 18.02,
    "nitrogen": 28.01
}

def print_mr(compound):
    print("%s: \t%.2f kg/kmol" % (compound, mr[compound]))

if __name__ == "__main__":
    print_mr("hydrogen")