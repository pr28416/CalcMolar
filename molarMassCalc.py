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

numbers = {str(i) for i in range(10)}
lowercase = {i for i in 'qwertyuiopasdfghjklzxcvbnm'}
uppercase = {i.upper() for i in lowercase}

debug = False

def calcMolarMass(string):
    global numbers, lowercase, uppercase, table, debug
    mass = 0
    parts = [""]
    i = 0
    while i < len(string):
        if string[i] in numbers:
            j = i+1
            while j < len(string):
                if string[j] not in numbers: break
                j += 1
            parts.append(int(string[i:j]))
            parts.append("")
            i = j-1
        elif string[i] == "(":
            j = i+1
            lvl = 1
            while j < len(string):
                if string[j] == "(": lvl += 1
                elif string[j] == ")":
                    if lvl == 1: break
                    else: lvl -= 1
                j += 1
            else: return None
            parts.append(string[i:j+1])
            parts.append("")
            i = j
        else:
            parts[-1] += (string[i])
        i += 1
    parts = list(reversed([i for i in parts if len(str(i)) != 0]))
    if debug: print(parts)
    stack = []
    while len(parts) > 0:
        if type(parts[-1]) == int:
            if len(stack) == 0:
                if debug: print("integer given but nothing in stack")
                return None
            try:
                e = stack.pop()
                if type(e) == int or type(e) == float:
                    print("adding result from subexpression (multiple)")
                    if len(parts) == 0: mass += e
                    else: mass += e * parts.pop()
                else:
                    if debug: print("finding mass of", e, "with freq:", parts[-1])
                    mass += parts.pop() * list(filter(lambda x: x.symbol == e, table))[0].atomicMass
            except Exception as e:
                if debug: print("couldn't add to mass (int):", e, len(parts))
                return None
        elif type(parts[-1]) == str:
            if len(stack) > 0 and type(stack[-1]) == int:
                if debug: print("adding result from subexpression (1)")
                mass += stack.pop()
                continue
            if parts[-1][0] == "(":
                if debug: print("found subexpression:", parts[-1][1:len(parts[-1])-1])
                e = calcMolarMass(parts[-1][1:len(parts[-1])-1])
                parts.pop()
                if e is None:
                    if debug: print(f"e was none")
                    return None
                stack.append(e)
            else:
                while len(stack) > 0:
                    e = stack.pop()
                    if debug: print("attempting to add mass (1):", e, "with:", parts[-1])
                    try:
                        if type(parts[-1]) == str:
                            mass += list(filter(lambda x: x.symbol == e, table))[0].atomicMass
                        else:
                            mass += parts.pop() * list(filter(lambda x: x.symbol == e, table))[0].atomicMass
                    except Exception as err:
                        if debug: print("couldn't add to mass (1):", e, err)
                        return None
                i, j = 0, 1
                while i < len(parts[-1]):
                    while j < len(parts[-1]) and parts[-1][j] in lowercase: j += 1
                    if debug: print("Split", parts[-1], "into", parts[-1][i:j])
                    stack.append(parts[-1][i:j])
                    i, j = j, j+1
                parts.pop()
        else:
            if debug: print("Type was incorrect")
            return None
    while len(stack) > 0:
        if debug: print("unloading remaining:", stack)
        e = stack.pop()
        if type(e) == int or type(e) == float:
            mass += e
            continue
        mass += list(filter(lambda x: x.symbol == e, table))[0].atomicMass
        if debug: print("stack is now:", stack)
    return mass


if __name__ == "__main__":
    print("Welcome to the molecular formula calculator. Please enter valid formulas. \n\tExamples: H2O, NaCl, Ba(OH)2, K2CO3\nType STOP to exit")
    res = input("DEBUG ON? (y/n): ")
    debug = res.lower() == "y"
    if res.lower() == "y":
        print("Debug mode is ON")
    else:
        print("Debug mode is OFF")

    while True:
        res = input("Enter molecular formula: ")
        if not res or res == "STOP": break 
        try: print("Molar mass: %.6f (round to discretion)" % calcMolarMass(res))
        except Exception as e: print("invalid:", e)

    print("Program terminated")