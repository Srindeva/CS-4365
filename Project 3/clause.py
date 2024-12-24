class Clause:
    def __init__(self, literals):
        self.literals = literals
    def __str__(self):
        return ' '.join(self.literals)
    def __eq__(self, other_literal):
        return self.literals == other_literal
    def __hash__(self):
        return hash(frozenset(self.literals))