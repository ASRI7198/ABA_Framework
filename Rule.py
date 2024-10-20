import Literal
class Rule():
    def __init__(self, name, body, conclusion):
        self.name = name
        self.body = body
        self.conclusion = conclusion

    def display(self):
        if self.body is None:
            return  f"{self.name}: {self.conclusion.name} <-"
        else:
            body_elements = ', '.join(
                [el.name if not isinstance(el, list) else ', '.join(i.name for i in el) for el in [self.body]]
            )
            return  f"{self.name}: {self.conclusion.name} <- {body_elements}"
    def display_2(self):
        if self.body is None:
            return  f"{self.name}: {self.conclusion.name} <-"
        else:
            body_elements = ', '.join(
                [el.name if not isinstance(el, list) else ', '.join(i.name for i in el) for el in [self.body]]
            )
            return  f"{self.name}: {self.conclusion.name} <- {body_elements}"