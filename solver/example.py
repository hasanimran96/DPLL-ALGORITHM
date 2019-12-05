import sys


def parse_dimacs(filename):
    clauses = []
    with open(sys.argv[1], 'r') as input_file:
        for line in input_file:
            if line[0] in ['c', 'p']:
                continue
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            literals = literals[:-1]
            clauses.append(literals)
    return clauses


clauses = parse_dimacs(sys.argv[1])
clauses = [[1, 2], [-2, -4]]
print(clauses)

print(type(clauses))

trail = []

variable_lookup = {}

distinct_variables = []
for i in range(16):
    distinct_variables.append(i+1)


def DPLL(CNF_formula):
    print("DPLL")
    trail.clear()
    if(BCP(CNF_formula) == False):
        return 'UNSAT'
    while(True):
        if(decide() == False):
            return 'SAT'
        while(BCP(CNF_formula) == False):
            if(backtrack() == False):
                return 'UNSAT'


def BCP(clauses):
    print("BCP")
    for clause in clauses:
        temp_unassigned = []
        isUnstatisfied = True
        for literal in clause:
            v = variable_lookup.get(literal, "UNASSIGNED")
            if(v == "UNASSIGNED"):
                isUnstatisfied = False
                temp_unassigned.append(literal)
                continue
            elif(v == 0):
                continue
            elif(v == 1):
                return True
        if(len(temp_unassigned) == 1):
            v = 1
            variable_lookup[temp_unassigned[0]] = v
            trail.append([temp_unassigned[0], v])
            return True
        elif(len(temp_unassigned) > 1):
            return True
        if(isUnstatisfied):
            return False


def decide():
    print("decide")
    for variable in distinct_variables:
        if(variable in variable_lookup == True):
            continue
        else:
            v = 0
            trail.append([variable, v])
            variable_lookup[variable] = v
            return True
    return False


def backtrack():
    print("backtrack")
    while(True):
        print(1)
        if not trail:
            return False
        x, v = trail.pop()
        print(x, v)
        if(v == 0):
            v = 1
            trail.append([x, v])
            variable_lookup[x] = v
            return True


output = DPLL(clauses)
print(output)
