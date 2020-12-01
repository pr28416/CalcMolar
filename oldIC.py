class Element:
    def __init__(self, *args):
        self.atomicNumber = int(args[0].strip(" "))
        self.element = args[1].strip(" ")
        self.symbol = args[2].strip(" ")
        self.atomicMass = float(args[3].strip(" "))
    def __str__(self): return f"{self.atomicNumber} {self.element} {self.symbol} ({self.atomicMass})"

table = []
with open("periodicTableElements.csv", "r") as f:
    tmp = True
    for line in f:
        if tmp: tmp = False; continue
        table.append(Element(*line.split(",")))

compound = []
while True:
    res = input("Enter symbol and occurrence: ")
    if not res: break
    compound.append(res.split(" "))

from decimal import *
mass = Decimal(0)

for item in compound:
    atomicMass = list(filter(lambda x: x.symbol == item[0], table))[0].atomicMass
    mass += Decimal(item[1]) * Decimal(atomicMass)

print("Molar mass: %.6f (round to discretion)" % mass)