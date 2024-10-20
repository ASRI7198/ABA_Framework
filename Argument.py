import Rule


class Argument():
    def __init__(self, premises, conclusion):
        self.premises = premises
        self.conclusion = conclusion

    def display(self):
        support_str = ', '.join([lit.display() for lit in self.premises])
        return f"{{ {support_str} }} ⊢ {self.conclusion.display()}"

    def generate_arguments(rules: Rule, assumptions):
        arguments = []


        def construct_argument(literal):
            for i in assumptions.list_literals :
                if literal.display() == i.display():
                    return [[literal], literal]  # Base case: the literal is an assumption

            for rule in rules:
                #print("rule.conclusion == literal ==> :", rule.conclusion.display(), " , ", literal.display())
                if rule.conclusion.display() == literal.display():
                   # print("holla")
                    body_elements = rule.body
                    support = set()
                    for elem in [body_elements]:
                        if isinstance(elem, list):
                            for ss in elem:
                                arg = construct_argument(ss)
                                if arg:
                                    support.update(arg[0])
                        else:
                            arg = construct_argument(elem)
                            if arg:
                                support.update(arg[0])
                    return [support, literal]
            return None  # No rule applies, no argument possible

        for ass in assumptions.list_literals:
            arguments.append([{ass}, ass])

        for rule in rules:
            arg = construct_argument(rule.conclusion)
            # print_arg(arg)

            if arg:
                arguments.append(arg)

        arg_list = []
        # add args to  the list of arguments
        for arg in arguments:
            if arg is not None:
                support, conclusion = arg
                new_arg = Argument(support, conclusion)
                arg_list.append(new_arg)

        return arg_list

    def print_arguments(arguments):
        # for arg in arguments:
        #     print(arg.display())
        return arguments
