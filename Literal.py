class Literal():
    def __init__(self, name, is_negation=False):
        self.name = name
        self.is_negation = is_negation

    def flip_negation_state(self):
        return Literal(self.name, not self.is_negation)

    def display(self):
        if self.is_negation == False:
            return f"{self.name}"
        else:
            return '¬' + f"{self.name}"

    def __eq__(self, other):
        """ Literals are considered equal if they have the same name and is_negation value """
        return isinstance(other, Literal) and self.name == other.name and self.is_negation == other.is_negation

    def __hash__(self):
        return hash((self.name, self.is_negation))