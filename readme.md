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

## Personal Goals
As I am still learning how to code in an object-orientated style, the following program will be made use OOP.

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


