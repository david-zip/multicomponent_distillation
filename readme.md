# Multicomponent Distillation Column Model

## Description
Goal is to model a **multicomponent distillation column** using **FUG(K) short cut method**. The model should calculate the:
- Minimum number of ideal trays
- Number of ideal trays
- Minimum reflux ratio
- Feed stage location
- Top composition
- Bottoms composition

Once the following is complete, the model will then be modified so it may show the column height and diameter, and condenser and reboiler duties.

## Logic
**Main class**: Distillation column

Key Parameters:
- Compounds in feed
- Feed composition
- Feed flowrate
- Heavy key and light key
- Operating temperature and pressure
- Feed quality
- Top purity
- Bottom purity
- Top recovery 
- Bottom recovery

Methods:
- Show feed, distillate, bottom composition
- Find minimum stages
- Print relative volatilities
- Find minimum reflux ratio
- Find ideal number of plates
- Find feed stage location

## Current Components
- H2 (hydrogen)
- CO (carbon monoxide)
- CO2 (carbon dioxide)
- CH4 (methane)
- C2H2 (acetylene)
- C2H4 (ethylene)
- C2H6 (ethane)
- C3H4 (methyl-acetylene)
- C3H6 (propene)
- C3H8 (propane)
- C3H4 (propadiene)
- C4H6 (E-acetylene)
- C4H8 (1-butene)
- C4H10 (n-butane)
- C5+
- H2O (steam)
- N2 (Nitrogen)
