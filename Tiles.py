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
    def __init__(self, name, cost, rent_lst, color):
        super().__init__(name, cost)
        self.num_houses = 0
        self.rent_lst = rent_lst
        self.color = color

class Railroad(TileWithCost):
    def __init__(self, name, cost):
        super().__init__(name, cost)

class Utility(TileWithCost):
    def __init__(self, name, cost):
        super().__init__(name, cost)




        
