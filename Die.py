import random

class Die:
    def __init__(self):
        self.dice1 = random.randint(1,6)
        self.dice2 = random.randint(1,6)
    def is_double(self):
        return self.dice1 == self.dice2
    def total(self):
        return self.dice1 + self.dice2
