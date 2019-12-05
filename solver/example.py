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


# def DPLL(CNF_formula):
#     trail.clear
#     if(BCP() == False):
#         return 'UNSAT'
#     while(True):
#         if(decide() == False):
#             return 'SAT'
#         while(BCP() == False):
#             if(backtrack() == False):
#                 return

# def check_unit(clauses):

# def BCP():
#     # while(there is a unit clause implying that a variable x must be set to a value v):
#     # 	trail.append(x, v, True)
#         # if(there is an unsatisfied clause):
#         # 	return False
#     return True

# def decide():
#     # if(all variables are assigned):
#     #     return False
#     # choose unassigned variable x
#     # v = 0 or v = 1
#     # trail.push(x, v, false)
#     return True

# def backtrack():
#     while(True):
#         if(len(trail) == 0):
#             return False
#         x, v, b = trail.pop
#         if(b == False):
#             trail.append(x, v, True)
#             return True
