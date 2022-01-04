from Die import *
from Player import *
from Tiles import *
from GameState import *
import random

chance_dict = {1: "Advance to Broadwalk",
               2: "Advance to Go (Collect $200)",
               3: "Advance to Illinois Avenue. If you pass Go, collect $200",
               4: "Advance to St.Charles Place. If you pass Go, collect $200",
               5: "Advance to the nearest Railroad. If unowned, you may buy it from the Bank.",
               6: "Advance to the nearest Railroad. If unowned, you may buy it from the Bank.",
               7: "Advance to the nearest Utility",
               8: "Bank pays you dividend of $50",
               9: "Get Out Of Jail Free",
               10: "Go back 3 spaces",
               11: "Go to Jail. Go directly to Jail, do not pass Go",
               12: "Make general repairs on all your property. For each house pay $25. For each hotel pay $100",
               13: "Speeding fine $15",
               14: "Take a trip to Reading Railroad. If you pass Go, collect $200",
               15: "You have been elected Chairman of the Board. Pay each player $50",
               16: "Your building loan matures. Collect $150"}

community_chest_dict = {1: "Advance to Go (Collect $200)",
                        2: "Bank error in your favor. Collect $200",
                        3: "Doctor's fee. Pay $50",
                        4: "From sale of stock, you get $50",
                        5: "Get Out of Jail Free",
                        6: "Go to Jail. Go directly to Jail, do not pass Go",
                        7: "Holiday fund matures. Receive $100",
                        8: "Income tax refund. Collect $20",
                        9: "It's your birthday. Collect $10 from every player",
                        10: "Life insurance matures. Collect $100",
                        11: "Pay hospital fees of $100",
                        12: "Pay school fees of $50",
                        13: "Receive $25 consultancy fee",
                        14: "You are assessed for street repair. $40 per house. $115 per hotel.",
                        15: "You have won second prize in a beauty contest. Collect $10.",
                        16: "You inherit $100"}


def play():
    num_players = input("Welcome to Monopoly! How many players would be playing this game? ")
    while (not num_players.isdigit()) or int(num_players) <= 1:
        if not num_players.isdigit():
            num_players = input("Please type the amount of players who would be playing the game ")
        else:
            num_players = input("The amount of players must be greater than one. Please type the amount of players ")
    num_players = int(num_players)
    player_lst = []
    for i in range(num_players):
        name = input(f"What is the name for player {i + 1}? ")
        player_lst.append(Player(name, 1500))
    game = GameState(player_lst)
    while True: 
        for player in player_lst: #Amount of turns
            if len(player_lst) == 1:
                print(f"Game has ended. {player_lst[0].name} has won with {player_lst[0].money} dollars!")
                break
            roll = []
            while ((not roll) or (roll.is_double() and player.jail_counter == 0)):
                if (roll != []):
                    print(f"{player.name} gets to roll again after this turn for rolling a double")
                if not player.bankrupt:
                    print("\n")
                    action = input(f"It's {player.name}'s turn! Press R to roll the die, V to view your current properties and B to view your current balance \n")
                    while action.upper() not in ["R", "V", "B", "M"]:
                        action = input("Please select either R, V, B or M ")
                    while action.upper() != "R":
                        if action.upper() == "V":
                            print("Properties: " + str(list(map(lambda x: x.name, player.property_list))))
                            print("Railroads: " + str(list(map(lambda x: x.name, player.railroad_list))))
                            print("Utilities: " + str(list(map(lambda x: x.name, player.utility_list))))
                        elif (action.upper() == "B"):
                            print(f"{player.name}'s current balance is {player.money} dollars")
                        action = input(f"It's {player.name}'s turn! Press R to roll the die, V to view your current properties and B to view your current balance \n")
                    roll = Die()
                    print(f"{player.name} rolled {roll.dice1} and {roll.dice2}")
                    if player.jail_counter:
                        if roll.is_double():
                            print(f"{player.name} rolled a double and escaped from jail!")
                            player.jail_counter = 0
                        else:
                            print(f"{player.name} is still jailed for {player.jail_counter} turns!")
                            player.jail_counter -= 1
                            continue
                    tile_left = game.board[player.placement]
                    tile_left.remove_player(player)
                    player.placement += roll.total()
                    if player.placement > 40:
                        print("Passed Go!")
                        player.money += 200
                        player.placement -= 40
                    tile_landed = game.board[player.placement]
                    step_on_tile(game, player, tile_landed, player_lst, roll)
                    if player.money < 0:
                        player.bankrupt = True
                        print(f"{player.name} went bankrupt!")
                    else:
                        print(f"{player.name} has {player.money} dollars remaining")

def step_on_tile(game, player, tile, player_lst, roll):
    tile.add_player(player)
    print(f"{player.name} landed on {tile.name}")
    if isinstance(tile, Property): #Player lands on a property
        if tile.owner != None and tile.owner != player: #Need pay
            player.pay_rent(tile.rent_lst[tile.num_houses], tile)
        elif tile.owner == player:
            if has_monopoly(player, tile):
                player.buy_houses(tile)
            else:
                print(f"{player.name} is unable to buy houses for {tile.name}")
        else: #Option to buy
            player.option_to_buy_tile(tile)
    elif type(tile) == Railroad: #Player lands on a railroad
        if tile.owner != None and tile.owner != player:
            num_railroad = len(tile.owner.railroad_list)
            if num_railroad <= 2:
                rent = 25 * num_railroad
            elif num_railroad == 3:
                rent = 100
            else:
                rent = 200
            player.pay_rent(rent, tile)
        elif tile.owner == None:
            player.option_to_buy_tile(tile)
    elif type(tile) == Utility: #Player lands on a utility
        if tile.owner != None and tile.owner != player:
            num_utilities = len(tile.owner.utility_list)
            if num_utilities == 1:
                rent = 4 * roll.total()
            else:
                rent = 10 * roll.total()
            player.pay_rent(rent, tile)
        elif tile.owner == None:
            player.option_to_buy_tile(tile)
    else:
        if tile.name == "Chance":
            card_drawn = random.randint(1, 16)
            print(chance_dict[card_drawn])
            if card_drawn in [1, 2, 3, 4, 5, 6, 7, 10, 11, 14]:
                tile.remove_player(player)
            if card_drawn == 1:
                player.placement = 40
                step_on_tile(game, player, game.board[40], player_lst, roll)
            elif card_drawn == 2:
                player.money += 200
                print("Passed Go!")
                player.placement = 1
                step_on_tile(game, player, game.board[1], player_lst, roll)
            elif card_drawn == 3:
                if player.placement > 25:
                    player.money += 200
                    print("Passed Go!")
                player.placement = 25
                step_on_tile(game, player, game.board[25], player_lst, roll)
            elif card_drawn == 4:
                if player.placement > 12:
                    player.money += 200
                    print("Passed Go!")
                player.placement = 12
                step_on_tile(game, player, game.board[12], player_lst, roll)
            elif card_drawn in [5,6]:
                if player.placement <= 6:
                    player.placement = 6
                    step_on_tile(game, player, game.board[6], player_lst, roll)
                elif player.placement <= 16:
                    player.placement = 16
                    step_on_tile(game, player, game.board[16], player_lst, roll)
                elif player.placement <= 26:
                    player.placement = 26
                    step_on_tile(game, player, game.board[26], player_lst, roll)
                elif player.placement <= 36:
                    player.placement = 36
                    step_on_tile(game, player, game.board[36], player_lst, roll)
                else:
                    player.money += 200
                    print("Passed Go!")
                    player.placement = 6
                    step_on_tile(game, player, game.board[6], player_lst, roll)
            elif card_drawn == 7:
                if player.placement <= 13:
                    player.placement = 13
                    step_on_tile(game, player, game.board[13], player_lst, roll)
                elif player.placement <= 29:
                    player.placement = 29
                    step_on_tile(game, player, game.board[29], player_lst, roll)
                else:
                    player.money += 200
                    print("Passed Go!")
                    player.placement = 13
                    step_on_tile(game, player, game.board[13], player_lst, roll)
            elif card_drawn == 8:
                player.money += 50
            elif card_drawn == 9:
                player.jail_free += 1
            elif card_drawn == 10:
                if tile is game.board[8]:
                    current = 8
                elif tile is game.board[23]:
                    current = 23
                else:
                    current = 37
                player.placement = (current - 3)
                step_on_tile(game, player, game.board[current - 3], player_lst, roll)
            elif card_drawn == 11:
                if player.jail_free:
                    player.jail_free -= 1
                    print(f"{player.name} used get out of jail free card")
                else:
                    player.jail_counter = 3
                    player.placement = 11
                    game.board[11].add_player(player)
            elif card_drawn == 12:
                player.money -= ((25 * player.houses) + (100 * player.hotels))
            elif card_drawn == 13:
                player.money -= 15
            elif card_drawn == 14:
                if player.placement > 6:
                    player.money += 200
                    print("Passed Go!")
                player.placement = 6
                step_on_tile(game, player, game.board[6], player_lst, roll)
            elif card_drawn == 15:
                for players in player_lst:
                    if player != players:
                        player.money -= 50
                        players.money += 50
            else:
                player.money += 150
        elif tile.name == "Community Chest":
            card_drawn = random.randint(1, 16)
            print(community_chest_dict[card_drawn])
            if card_drawn == 1:
                player.money += 200
                print("Passed Go!")
                player.placement = 1
                tile.remove_player(player)
                step_on_tile(game, player, game.board[1], player_lst, roll)
            elif card_drawn == 2:
                player.money += 200
            elif card_drawn == 3:
                player.money -= 50
            elif card_drawn == 4:
                player.money += 50
            elif card_drawn == 5:
                player.jail_free += 1
            elif card_drawn == 6:
                if player.jail_free:
                    player.jail_free -= 1
                    print(f"{player.name} used get out of jail free card")
                else:
                    player.jail_counter = 3
                    player.placement = 11
                    tile.remove_player(player)
                    game.board[11].add_player(player)
            elif card_drawn == 7:
                player.money += 100
            elif card_drawn == 8:
                player.money += 20
            elif card_drawn == 9:
                for players in player_lst:
                    if players != player:
                        players.money -= 10
                        player.money += 10
                        if players.money < 0:
                            print(f"{players.name} went bankrupt!")
                            players.bankrupt = True
            elif card_drawn == 10:
                player.money += 100
            elif card_drawn == 11:
                player.money -= 100
            elif card_drawn == 12:
                player.money -= 50
            elif card_drawn == 13:
                player.money += 25
            elif card_drawn == 14:
                player.money -= ((40 * player.houses) + (115 * player.hotels))
            elif card_drawn == 15:
                player.money += 10
            else:
                player.money += 100
        elif tile.name == "Go To Jail":
            if player.jail_free:
                player.jail_free -= 1
                print(f"{player.name} used get out of jail free card")
            else:
                player.jail_counter = 3
                player.placement = 11
                tile.remove_player(player)
                game.board[11].add_player(player)
        elif tile.name == "Income Tax":
            player.money -= 200
        elif tile.name == "Luxury Tax":
            player.money -= 100
        
def has_monopoly(player, tile):
    if tile.color == "brown":
        if tile.owner.brown == 2:
            return True
    elif tile.color == "lightblue":
        if tile.owner.lightblue == 3:
            return True
    elif tile.color == "pink":
        if tile.owner.pink == 3:
            return True
    elif tile.color == "orange":
        if tile.owner.orange == 3:
            return True
    elif tile.color == "red":
        if tile.owner.red == 3:
            return True
    elif tile.color == "yellow":
        if tile.owner.yellow == 3:
            return True
    elif tile.color == "green":
        if tile.owner.green == 3:
            return True
    else:
        if tile.owner.darkblue == 2:
            return True
    return False
                
                    
                
    
        
