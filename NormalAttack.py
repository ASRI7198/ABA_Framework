import Argument
from Attack import Attack


class NormalAttack(Attack):
    def __init__(self, attacker: Argument, attacked: Argument):
        super().__init__(attacker, attacked)

    def display(self):
        # Display all attackers
        attacker_display = ", ".join(arg.display() for arg in self.attacker)
        # Display all attacked arguments
        attacked_display = ", ".join(arg.display() for arg in self.attacked)
        return f"{attacker_display} attacks {attacked_display}"