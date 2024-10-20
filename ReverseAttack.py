import Argument
import Assumption
import Literal
import Preferences
import Rule
from Attack import Attack
from NormalAttack import NormalAttack


class ReverseAttack(Attack):
    def __init__(self, attacker: Argument, attacked: Argument):
        super().__init__(attacker, attacked)

    def display(self):
        # Display all attackers
        attacker_display = ", ".join(arg.display() for arg in self.attacker)
        # Display all attacked arguments
        attacked_display = ", ".join(arg.display() for arg in self.attacked)
        return f"{attacker_display} attacks {attacked_display}"


def generate_normal_reverse_attacks(A: Assumption, P: Preferences, R: list[Rule]):
    subsets = A.generate_subsets()  # Generate all the possible subsets of A
    arguments = Argument.Argument.generate_arguments(R, A)  # Generate all possible arguments
    normal_attacks = []
    reverse_attacks = []

    # Iterate over all pairs of subsets (sub1 as set X and sub2 as set Y)
    for sub1 in subsets:  # sub1 represents set X
        for sub2 in subsets:  # sub2 represents set Y
            for arg in arguments:
                leaves = arg.premises
                conclusion = arg.conclusion
                    # Check if the leaves of the argument are in sub1 (X)
                if all(leaf in sub1 for leaf in leaves):
                    for y in sub2:
                       # print("y : ",y.display(),"conclusion :",conclusion.display())
                        if A.is_contrary(y, conclusion):  # the existance of an attack
                            #print("leaves1 :", leaves)
                            # Ensure that none of the premises in leaves are less preferred than y according to the preference relation
                            if all(not (p in P.less_pref and y in P.more_pref) for p in leaves):

                                # Create a normal attack between sub1 (X) and sub2 (Y)
                                norm = NormalAttack(sub1, sub2)

                                # Ensure the attack is unique before adding it to the list
                                if norm not in normal_attacks:
                                    normal_attacks.append(norm)

                if all(leaf in sub2 for leaf in leaves):
                    for x in sub1:

                        if A.is_contrary(x, conclusion):
                           # print("leaves2 :", leaves)
                            for p in leaves:
                                # If a premise (p) is less preferred than x, create a reverse attack
                                if p in P.less_pref and x in P.more_pref:
                                    norm = ReverseAttack(sub1, sub2)

                                    # Ensure the reverse attack is unique before adding it to the list
                                    if norm not in reverse_attacks:
                                        reverse_attacks.append(norm)

    return normal_attacks, reverse_attacks
