class CSP:
    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints
        self.domains = {var: list(domain) for var, domain in variables.items()}
        self.assignments = {}
        self.solution = []
    
    def is_consistent(self, variable):
        for domain in self.domains:
            if len(domain) == 0:
                return False
        for lhs, op, rhs in self.constraints:
            if lhs == variable and rhs in self.assignments:
                if not self.check_constraint(self.assignments[lhs], op, self.assignments[rhs]):
                    return False
            elif rhs == variable and lhs in self.assignments:
                if not self.check_constraint(self.assignments[lhs], op, self.assignments[rhs]):
                    return False
        return True

    def check_constraint(self, lhs_val, op, rhs_val):
        if op == '=':
            return lhs_val == rhs_val
        elif op == '!':
            return lhs_val != rhs_val
        elif op == '>':
            return lhs_val > rhs_val
        elif op == '<':
            return lhs_val < rhs_val
        return False

    def count_constraining_vars(self, variable, unassigned_vars):
        count = 0
        for constraint in self.constraints:
            if variable in constraint:
                if constraint[0] == variable:
                    other_var = constraint[2]  
                elif constraint[2] == variable:
                    other_var = constraint[0] 
                
                if other_var in unassigned_vars:
                    count += 1
        return count

    def sort_domain(self, variable):
        domain = self.get_domain(variable)
        def constraint_count(value):
            count = 0
            for constraint in self.constraints:
                if variable in constraint:
                    if constraint[0] == variable:
                        other_var = constraint[2] 
                        if other_var not in self.assignments:
                            op = constraint[1]
                            for other_value in self.get_domain(other_var):
                                if self.check_constraint(value, op, other_value):
                                    count += 1
                    else:
                        other_var = constraint[0]
                        if other_var not in self.assignments:
                            op = constraint[1]
                            for other_value in self.get_domain(other_var):
                                if self.check_constraint(other_value, op, value):
                                    count += 1
            return count
        return sorted(domain, key=constraint_count, reverse=True)

    def select_variable(self):
        unassigned_vars = [var for var in self.variables if var not in self.assignments]
        if not unassigned_vars:
            return None

        sorted_vars = sorted(unassigned_vars, key=lambda var: (
        len(self.get_domain(var)),         
        -self.count_constraining_vars(var, unassigned_vars),           
        var                                
    ))
        return sorted_vars[0]

    def forward_check(self, variable, value):
        self.assignments[variable] = value
        for lhs, op, rhs in self.constraints:
            if lhs == variable:
                other_variable = rhs
                if other_variable not in self.assignments:
                    new_domain = [val for val in self.domains[other_variable] if self.check_constraint(value, op, val)]
                    if not new_domain:
                        return False
                    self.domains[other_variable] = new_domain
            elif rhs == variable:
                other_variable = lhs 
                if other_variable not in self.assignments:
                    new_domain = [val for val in self.domains[other_variable] if self.check_constraint(val, op, value)]
                    if not new_domain:
                        return False
                    self.domains[other_variable] = new_domain
        return True

    def backtrack(self, fc):
        if len(self.assignments) == len(self.variables):
            self.add_solution()
            return True 

        variable = self.select_variable()
        for value in self.sort_domain(variable):
            self.assignments[variable] = value
            self.domains[variable] = [value]
            if self.is_consistent(variable):
                domains_backup = self.domains.copy()
                if fc:
                    if not self.forward_check(variable, value):
                        self.domains = domains_backup
                        self.add_failure() 
                        del self.assignments[variable]
                        continue
                if self.backtrack(fc):
                    return True
                
                self.domains = domains_backup
            if not self.is_consistent(variable):
                self.add_failure()
            del self.assignments[variable]
        return False

    def add_solution(self):
        output = ", ".join("{}={}".format(var, self.assignments[var]) for var in (self.assignments))
        self.solution.append(output + "  solution")

    def add_failure(self):
        output = ", ".join("{}={}".format(var, self.assignments[var]) for var in (self.assignments))
        self.solution.append(output + "  failure")
    
    def print_solution(self):
        soln_index = 1
        for line in self.solution:
            print(str(soln_index) + ". " + line)
            soln_index += 1
    
    def get_domain(self, variable):
        return self.domains.get(variable, [])

