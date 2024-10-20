import Argument
class Attack:
    def __init__(self, attacker: Argument, attacked: Argument):
        self.attacker = attacker
        self.attacked = attacked

    def display(self):
        return f"{self.attacker.display()} attacks {self.attacked.display()}"


def generate_attacks(arguments, A):
    attacks = []

    # Check every pair of arguments to see if one attacks the other
    contatries = [i.display() for i in A.contatries ]
    for arg1 in arguments:
        if arg1.conclusion.display() in contatries:
            bar = [i for i in A.dict_contraries if A.dict_contraries[
                i].display() == arg1.conclusion.display()]  # Get the bar of the contrary, exemple if ¬a=r, having r we want to get a
            bar = bar[0].flip_negation_state()

            for arg2 in arguments:
                if bar.name in [p.name for p in list(arg2.premises)]:
                    attack = Attack(arg1, arg2)
                    attacks.append(attack)

    return attacks





