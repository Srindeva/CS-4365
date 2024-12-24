import sys
from csp import CSP

def parse_var_file(var_file):
    variables = {}
    with open(var_file, "r") as file:
        for line in file:
            var, domain = line.split(':')
            variables[var.strip()] = list(map(int, domain.split()))
    return  variables

def parse_con_file(con_file):
    constraints = []
    with open(con_file, "r") as file:
        for line in file:
            constraints.append(line.strip().split())
    return constraints

if __name__ == '__main__':
    #Example inputs for debugging
    #sys.argv = ['main.py', 'ex3.var1.txt', 'ex3.con.txt', 'none']
    #sys.argv = ['main.py', 'ex2.var1.txt', 'ex2.con.txt', 'none']
    #sys.argv = ['main.py', 'ex1.var1.txt', 'ex1.con.txt', 'none']
    # if not len(sys.argv) >= 4:
    #     print("Please use the given format.\npython main.py <path_to_var_file> <path_to_con_file> <none|fc>")
    # else:
        var_file = sys.argv[1]
        con_file = sys.argv[2]
        consistency = sys.argv[3]

        variables = parse_var_file(var_file)
        constraints = parse_con_file(con_file)

        csp = CSP(variables, constraints)
        forward_checking = consistency == 'fc'
        csp.backtrack(forward_checking)
        csp.print_solution()

