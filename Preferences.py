class Preferences:
    def __init__(self, more_pref, less_pref):
        self.more_pref = more_pref
        self.less_pref = less_pref

    def display(self):
        # Convert lists of literals to string representations
        more_pref_str = ', '.join([literal.name for literal in self.more_pref])
        less_pref_str = ', '.join([literal.name for literal in self.less_pref])

        return f"{more_pref_str} > {less_pref_str}"