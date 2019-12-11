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

trail = []

variable_lookup = {}

for clause in clauses:
    for literal in clause:
        if(literal < 0):
            literal = literal * -1
        if(literal not in variable_lookup):
            variable_lookup[literal] = -1


def DPLL():
    global clauses
    global trail
    global variable_lookup
    print("DPLL")
    trail.clear()
    if(BCP() == False):
        return 'UNSAT'
    while(True):
        if(decide() == False):
            return 'SAT'
        while(BCP() == False):
            if(backtrack() == False):
                return 'UNSAT'


def check_unit_clause(clause):
    zeroes = 0
    ones = 0
    unassigned = 0
    for literal in clause:
        if(literal < 0):
            literal = literal * -1
            v = variable_lookup.get(literal)
            if(v != -1):
                if(v == 0):
                    v = 1
                else:
                    v = 0
            if(v == 0):
                zeroes += 1
            if(v == -1):
                unassigned += 1
                if(unassigned > 1):
                    break
                key = literal * -1
            if(v == 1):
                break
                # ones += 1
        else:
            v = variable_lookup.get(literal)
            if(v == 0):
                zeroes += 1
            if(v == -1):
                unassigned += 1
                if(unassigned > 1):
                    break
                key = literal
            if(v == 1):
                break
                # ones += 1
    if(ones > 0):
        return None
    if(unassigned == 1 and zeroes == (len(clause)-1)):
        return key


def check_unsatisfied_clause():
    global clauses
    for clause in clauses:
        zeroes = 0
        # ones = 0
        # unassigned = 0
        for literal in clause:
            if(literal < 0):
                literal = literal * -1
                v = variable_lookup.get(literal)
                if(v != -1):
                    if(v == 0):
                        v = 1
                    else:
                        v = 0
                if(v == 0):
                    zeroes += 1
                if(v == -1):
                    break
                    # unassigned += 1
                if(v == 1):
                    break
                    # ones += 1
            else:
                v = variable_lookup.get(literal)
                if(v == 0):
                    zeroes += 1
                if(v == -1):
                    break
                    # unassigned += 1
                if(v == 1):
                    break
                    # ones += 1
        if(zeroes == len(clause)):
            return True
    return False


def BCP():
    global clauses
    global trail
    global variable_lookup
    print("BCP")
    i = 0
    while(i < len(clauses)):
        if(check_unit_clause(clauses[i]) != None):
            literal = check_unit_clause(clauses[i])
            if(literal < 0):
                literal = literal * -1
                trail.append([literal, 0, 'true'])
                variable_lookup[literal] = 0
            else:
                trail.append([literal, 1, 'true'])
                variable_lookup[literal] = 1
        i += 1
    if(check_unsatisfied_clause()):
        return False
    return True


def decide():
    global trail
    global variable_lookup
    print("decide")
    if(all(x != -1 for x in variable_lookup.values())):
        return False

    unassigned = -1
    for key, value in variable_lookup.items():
        if (value == -1):
            unassigned = key
            break
    v = 0
    trail.append([unassigned, v, 'false'])
    variable_lookup[unassigned] = v
    return True


def backtrack():
    global trail
    global variable_lookup
    print("backtrack")
    while(True):
        if not trail:
            return False

        x, v, b = trail.pop()
        if(b == 'true'):
            variable_lookup[x] = -1
        else:
            if(v == 0):
                trail.append([x, 1, 'true'])
                variable_lookup[x] = 1
            else:
                trail.append([x, 0, 'true'])
                variable_lookup[x] = 0
            return True


def print_assignments():
    global clauses
    clauses_assigned = []
    for clause in clauses:
        clause_assigned = []
        for literal in clause:
            if(literal < 0):
                literal = literal * -1
                v = variable_lookup.get(literal)
                if(v != -1):
                    v = 1-v
            else:
                v = variable_lookup.get(literal)
            clause_assigned.append(v)
        clauses_assigned.append(clause_assigned)
    print(clauses_assigned)


output = DPLL()
print(output)
# print_assignments()
print(variable_lookup)

if(output == "SAT"):
    print('sat')
    exit(10)
elif(output == "UNSAT"):
    print('unsat')
    exit(20)
