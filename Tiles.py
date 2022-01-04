class Tile:
    def __init__(self, name):
        self.name = name
        self.players_on_tile = []
    #TODO methods
    def add_player(self, player):
        self.players_on_tile.append(player)
    def remove_player(self, player):
        if player in self.players_on_tile:
            self.players_on_tile.remove(player)

class TileWithCost(Tile):
    def __init__(self, name, cost):
        super().__init__(name)
        self.cost = cost
        self.owner = None
        
class Property(TileWithCost):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost)
        self.num_houses = 0
        self.rent_lst = rent_lst

class Railroad(TileWithCost):
    def __init__(self, name, cost):
        super().__init__(name, cost)

class Utility(TileWithCost):
    def __init__(self, name, cost):
        super().__init__(name, cost)

class BrownProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)

class LightBlueProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)

class PinkProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)

class OrangeProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)

class RedProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)

class YellowProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)
        
class GreenProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)
        
class DarkBlueProperty(Property):
    def __init__(self, name, cost, rent_lst):
        super().__init__(name, cost, rent_lst)



        
