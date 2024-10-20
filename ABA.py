import Literal
import Rule


class ABA():
    def __init__(self, L, R, A):  # ici je pense on doit faire A : assumption
        self.L = L
        self.R = R
        self.A = A
        self.cont = A.dict_contraries

    def isAtomic(self, rule):
        if all(elem in self.A.list_literals for elem in [rule.body]):
            return True
        else:
            return False

    """  ABA (L,R,A;-)  """

    def circularToNonCircular(self):
        """ Converts a circular ABA framework to a non-circular one """
        k = len(self.L) - len(self.A.list_literals)  # Number of non-assumption literals
        temp_R = []
        temp_L = []
        for r in self.R:

            # Handle atomic rules (conclusion is an assumption)
            if self.isAtomic(r):

                for i in range(1, k + 1):
                    if i != k:  # Skip the final rule as s^k = s (no need to rename)
                        # Create new literals with modified names for non-assumptions
                        new_lit = Literal.Literal(f"{r.conclusion.name}_{i}", r.conclusion.is_negation)
                        temp_L.append(new_lit)

                        # Create the new rule with updated literals
                        r_new = Rule.Rule(f"{r.name}_{i}", r.body, new_lit)

                        temp_R.append(r_new)

            # Handle non-atomic rules (conclusion is NOT an assumption)
            else:
                for i in range(2, k + 1):  # Start at 2, since we don't modify r_1

                    new_literals = []  # store the body elements of the current rule
                    for b in [r.body]:
                        if b in self.A.list_literals:  # If b is an assumption, keep it
                            new_literals.append(b)
                        else:  # If b is not an assumption, modify its name
                            if isinstance(b,list):
                                for nb in b:
                                    new_lit = Literal.Literal(f"{nb.name}_{i - 1}", nb.is_negation)
                                    new_literals.append(new_lit)
                                    temp_L.append(new_lit)  # add the new litteral to L
                            else:
                                new_lit = Literal.Literal(f"{b.name}_{i - 1}", b.is_negation)
                                new_literals.append(new_lit)
                                temp_L.append(new_lit)  # add the new litteral to L

                    if i != k:
                        # Create the new rule with updated literals and conclusion
                        r_temp = Rule.Rule(f"{r.name}_{i}", new_literals,
                                      Literal.Literal(f"{r.conclusion.name}_{i}", r.conclusion.is_negation))

                    else:
                        r_temp = Rule.Rule(f"{r.name}_{i}", new_literals,
                                      Literal.Literal(f"{r.conclusion.name}", r.conclusion.is_negation))

                    temp_R.append(r_temp)

        # extend  L with the new literals created in the loop
        existing = [l.name for l in self.L]  # Keep track of the elements already in self.L

        for i in range(len(temp_L)):
            if temp_L[i].name not in existing:
                self.L.append(temp_L[i])
                existing.append(temp_L[i].name)

        # extend R with the new rules
        self.R.extend(temp_R)

    def toAtomic(self):
        # self.cont = A.list_contraries

        # self.CircularToNonCircular()
        temp_R = []
        temp_A = []
        tmp_contraries = {}

        new_assumptions = []

        L_A = [literal for literal in [self.L] if literal not in [self.A.list_literals]]
        for s in L_A:
            if isinstance(s, list):
                for k in s:
                    s_d = Literal.Literal(f"{k.name}_d", k.is_negation)
                    s_nd = Literal.Literal(f"{k.name}_nd", k.is_negation)

                    temp_A.append(s_d)
                    temp_A.append(s_nd)

                    tmp_contraries[Literal.Literal(s_d.name, True)] = Literal.Literal(s_nd.name, False)
                    tmp_contraries[Literal.Literal(s_nd.name, True)] = Literal.Literal(k.name, False)
            else:

                s_d = Literal.Literal(f"{s.name}_d", s.is_negation)
                s_nd = Literal.Literal(f"{s.name}_nd", s.is_negation)

                temp_A.append(s_d)
                temp_A.append(s_nd)

                tmp_contraries[Literal.Literal(s_d.name, True)] = Literal.Literal(s_nd.name, False)
                tmp_contraries[Literal.Literal(s_nd.name, True)] = Literal.Literal(s.name, False)

        existing_L = [l.name for l in self.L]
        existing_A = [l.name for l in self.A.list_literals]
        existing_contraries = {Literal.Literal(li.name, True): Literal.Literal(r.name, False) for li, r in
                               self.A.contraries().items()}

        for i in range(len(temp_A)):
            if temp_A[i].name not in existing_A:
                self.L.append(temp_A[i])
                self.A.list_literals.append(temp_A[i])
                existing_L.append(temp_A[i].name)
                existing_A.append(temp_A[i].name)

        existing_contraries.update(tmp_contraries)

        self.cont = existing_contraries
        # Jusqu'ici, j'ai fait A', L' et -' . Il me reste R'.
        for rule in self.R:
            if all(el in self.A.list_literals for el in [rule.body]):
                temp_R.append(rule)
            else:
                new_body = []
                for el in [rule.body]:
                    if isinstance(el, list):
                        for k in el:
                            if k not in self.A.list_literals:
                                k = Literal.Literal(f"{k.name}_d", False)
                                new_body.append(k)
                    else:
                        new_body.append(el)
                new_rule = Rule.Rule(rule.name, new_body, rule.conclusion)
                temp_R.append(new_rule)
        self.R = temp_R
        # print("Updated contraries:", new_contraries)
        liste1=[]
        print("New A':", existing_A)
        print("New L'':", existing_L)
        liste1.append(existing_A)
        liste1.append(existing_L)
        liste2=[]
        for key, value in self.cont.items():
            liste2.append(f"{key.display()} : {value.display()}")
        liste3=[]
        for rule in self.R:
            liste3.append(rule.display())

        # result_data = {
        #     "new_A": existing_A,  # Liste de données pour New A'
        #     "new_L": existing_L,  # Liste de données pour New L''
        #     "contraries": self.cont,  # Dictionnaire de contraires
        #     "rules": self.R  # Liste des règles
        # }
        return liste1,liste2,liste3
