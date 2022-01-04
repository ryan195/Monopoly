from Tiles import *

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.property_list = []
        self.jail_counter = 0
        self.railroad_list = []
        self.utility_list = []
        self.bankrupt = False
        self.placement = 1
        self.nus_cap5 = 0
        self.brown = []
        self.lightblue = []
        self.pink = []
        self.orange = []
        self.red = []
        self.yellow = []
        self.green = []
        self.darkblue = []
        self.houses = 0
        self.hotels = 0
    def option_to_buy_tile(self, tile):
        if self.money >= tile.cost:
            purchase = input(f"Press T to purchase {tile.name} for {tile.cost} dollars ")
            if purchase.upper() == "T":
                self.money -= tile.cost
                if isinstance(tile, Property):
                    self.property_list.append(tile)
                    if type(tile) == BrownProperty:
                        self.brown.append(tile)
                    elif type(tile) == LightBlueProperty:
                        self.lightblue.append(tile)
                    elif type(tile) == PinkProperty:
                        self.pink.append(tile)
                    elif type(tile) == OrangeProperty:
                        self.orange.append(tile)
                    elif type(tile) == RedProperty:
                        self.red.append(tile)
                    elif type(tile) == YellowProperty:
                        self.yellow.append(tile)
                    elif type(tile) == GreenProperty:
                        self.green.append(tile)
                    else:
                        self.darkblue.append(tile)
                elif type(tile) == Railroad:
                    self.railroad_list.append(tile)
                else:
                    self.utility_list.append(tile)
                tile.owner = self
                print(f"{self.name} purchased {tile.name} for {tile.cost} dollars")
            else:
                print(f"{self.name} decided not to purchase {tile.name}")
    def pay_rent(self, rent, tile):
        print(f"{self.name} pays {rent} in rent to {tile.owner.name}")
        tile.owner.money += rent
        self.money -= rent
    def buy_houses(self, tile):
        num_houses = tile.num_houses
        if num_houses == 5:
            print(f"{self.name} already have a hotel")
        else:
            if type(tile) == BrownProperty or type(tile) == LightBlueProperty:
                house_cost = 50
            elif type(tile) == PinkProperty or type(tile) == OrangeProperty:
                house_cost = 100
            elif type(tile) == OrangeProperty or type(tile) == RedProperty:
                house_cost = 150
            else:
                house_cost = 200
            max_houses_to_purchase = min(player.money // house_cost, 5 - num_houses)
            print(f"{self.name} can purchase {max_houses_to_purchase} houses")
            #TODO sanity check
            num_houses_bought = int(input(f"How many houses does {player.name} want to purchase?"))
            money_spent = (num_houses_bought * house_cost)
            self.money -= money_spent
            tile.num_houses += num_houses_bought
            self.houses += num_houses_bought
            print(f"{self.name} has purchased {num_houses_bought} houses for {money_spent}.")
            
        
        
    
