class State:
    def __init__(self, x, y, m):
        self.x
        self.y
        self.m

    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            return self.name == other.name