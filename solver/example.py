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
# clauses = [[-1], [1]]
# print(clauses)

# print(type(clauses))

trail = []

variable_lookup = {}

for clause in clauses:
    for literal in clause:
        if(literal < 0):
            literal = literal * -1
        if(literal not in variable_lookup):
            variable_lookup[literal] = -1


# print(variable_lookup)


def DPLL():
    global clauses
    global trail
    global variable_lookup
    print("DPLL")
    trail.clear()
    print(BCP() == False)
    if(BCP() == False):
        return 'UNSAT'
    while(True):
        if(decide() == False):
            return 'SAT'
        while(BCP() == False):
            if(backtrack() == False):
                return 'UNSAT'


def check_unit_clause(clause):
    sum = 0
    onlyUnassigned = -1
    for literal in clause:
        if(literal < 0):
            literal = literal * -1
        v = variable_lookup.get(literal)
        if(v == -1):
            onlyUnassigned = literal
        sum = sum + v
    if(sum == -1):
        return onlyUnassigned
    return None


def check_unsatisfied_clause():
    global clauses
    for clause in clauses:
        temp_list = []
        for literal in clause:
            if(literal < 0):
                literal = literal * -1
            v = variable_lookup.get(literal)
            temp_list.append(v)
        if(all(i == 0 for i in temp_list)):
            return False
    return True


def BCP():
    global clauses
    global trail
    global variable_lookup
    print("BCP")
    i = 0
    while(i < len(clauses)):
        if(check_unit_clause(clauses[i]) != None):
            key = check_unit_clause(clauses[i])
            trail.append([key, 1, 'true'])
            variable_lookup[key] = 1
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
    print(trail)
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
        if(b == 'false'):
            v = 1
            trail.append([x, v, 'true'])
            print(trail)
            variable_lookup[x] = v
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
            clause_assigned.append(v)
        clauses_assigned.append(clause_assigned)
    print(clauses_assigned)


output = DPLL()
print(output)
print_assignments()
print(variable_lookup)
