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
print(clauses)

print(type(clauses))

trail = []


def DPLL(CNF_formula):
    trail.clear
    if(BCP() == False):
        return 'UNSAT'
    while(True):
        if(decide() == False):
            return 'SAT'
        while(BCP() == False):
            if(backtrack() == False):
                return


def BCP(clauses):
    for i in range(len(clauses)):
        if(len(clauses[i]) == 1):
            v = 1
            trail.append(clauses[i], v)
        for literal in range(len(clauses[i])):
            while(literal.value != 1):
                continue
            if(literal.value == 0):
                return False
    return True

# def BCP():
#     # while(there is a unit clause implying that a variable x must be set to a value v):
#     # 	trail.append(x, v, True)
#         # if(there is an unsatisfied clause):
#         # 	return False
#     return True


def decide():
    for clause in range(len(clauses)):
        for literal in clause:
            if(literal.value != None):
                return False
            # assigning false as default
            v = 0
            trail.append(literal, v)
            return True


def backtrack():
    while(True):
        if(len(trail) == 0):
            return False
        x, v = trail.pop()
        if(v == 0):
            v = 1
            trail.append(x, v)
            return True


output = DPLL(clauses)
print(output)
