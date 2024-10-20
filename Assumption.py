import Literal
import itertools

class Assumption():
    def __init__(self, name, list_literals, contatries=None):
        self.name = name
        self.list_literals = list_literals
        self.contatries = contatries
        if contatries is not None:
            self.dict_contraries = self.contraries()
        else:
            self.dict_contraries = None

    def display(self):
        return f"{self.name} = {{" + ', '.join([f"{l.name}" for l in self.list_literals]) + '}'

    def contraries(self):
        dict_contraries = {Literal.Literal(li.name, True): r for li, r in zip(self.list_literals, self.contatries)}
        return dict_contraries

    def display_contraries(self):
        if self.contatries is None:
            return None
        else:
            dict_contraries = {Literal.Literal(li.name, True): Literal.Literal(r.name, False) for li, r in
                               zip(self.list_literals, self.contatries)}
            # Format the dictionary elements into a string for display
            display_str = "{" + ' , '.join(
                [f"{str(l.display())} = {r.display()}" for l, r in dict_contraries.items()]) + "}"
            return display_str

    def is_contrary(self, x, y):
        """ Check if x is the contrary of y """
        if self.dict_contraries is None:
            return False
        contrary_of_x = self.dict_contraries.get(x.flip_negation_state())
        keys = list(self.dict_contraries.keys())  # Liste des clés
        value = list(self.dict_contraries.values())

        for i, j in zip(keys, value):
            if i.display()==x.flip_negation_state().display():
               # print('i ; ',i.display(),'x ; ',x.flip_negation_state().display())
                contrary_of_x = j
                break


        #contrary_of_x = self.dict_contraries.get(x.flip_negation_state())
        # print("contrary_of_x :",contrary_of_x.display())
        # print("y:",y.display())
        # print("contrary_of_x == y : ",contrary_of_x.display() == y.display())
        # If contrary exists, check if it matches y
        return contrary_of_x.display() == y.display()

    def generate_subsets(self):
        """ Generate all possible subsets of the assumption """
        all_combinations = []
        # Generate combinations for lengths from 1 to len(list_literals)
        for r in range(1, len(self.list_literals) + 1):
            combinations = itertools.combinations(self.list_literals, r)
            all_combinations.extend(combinations)

        return all_combinations
