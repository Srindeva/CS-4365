import sys
import re
from clause import Clause

class Resolution:
    def __init__(self):
        self.kb = []
        self.test_clause = Clause([])

    def load_kb(self, file_name):
        with open(file_name, 'r') as kb_file:
            lines = [re.sub(r'\s+', ' ', line.strip()) for line in kb_file if line.strip()]
            for line in lines[:-1]:
                clause = Clause(line.split())
                self.kb.append(clause)
            self.test_clause = Clause(lines[-1].split())
    
    def resolve(self, alpha, beta):
        pre_resolved = set(alpha.literals).union(beta.literals)
        resolved = pre_resolved.copy()

        for alpha_literal in alpha.literals:
            for beta_literal in beta.literals:
                if self.is_complement(alpha_literal, beta_literal):
                    resolved.discard(alpha_literal)
                    resolved.discard(beta_literal)
                    if not resolved:
                        return False
                    elif self.is_contradiction(resolved):
                        return True
                    else:
                        for clause in self.kb:
                            if set(clause.literals) == resolved:
                                return True
                        return Clause(list(resolved))
        return True
    
    def prove(self):
        clause_index = 1
        for clause in self.kb:
            print(f"{clause_index}. {clause} {{}}")
            clause_index += 1

        test_case_complement = self.get_complement(self.test_clause)
        for complement in test_case_complement:
            self.kb.append(complement)
            print(f"{clause_index}. {complement} {{}}")
            clause_index += 1

        clause = 1
        while clause < clause_index - 1:
            prev_clause = 0
            while prev_clause < clause:
                resolution = self.resolve(self.kb[clause], self.kb[prev_clause])
                if resolution is False:
                    print(f"{clause_index}. Contradiction {{{clause + 1}, {prev_clause + 1}}}")
                    clause_index += 1
                    print("Valid")
                    sys.exit(0)
                elif resolution is True:
                    prev_clause += 1
                    continue
                else:
                    print(f"{clause_index}. {resolution} {{{clause + 1}, {prev_clause + 1}}}")
                    self.kb.append(resolution)
                    clause_index += 1
                prev_clause += 1
            clause += 1
        print("Not Valid")
    
    def get_complement(self, clause):
        return [Clause([f'~{literal}' if '~' not in literal else literal[1:]]) for literal in clause.literals]
    
    def is_complement(self, alpha, beta):
        return (alpha == ('~' + beta) or beta == ('~' + alpha))
    
    def is_contradiction(self, clause):
        return any(self.is_complement(alpha, beta) for alpha in clause for beta in clause if alpha != beta)

    def print_kb(self):
        for line in self.kb:
            print(line)
    
