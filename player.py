import items
import world
import random
import math
import sys
import colorama
from colorama import Fore, Style, Back
import os

class Player:
    def __init__(self):
        self.inventory = [items.Sword(),
                          items.Apple()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.enchantment_points = 1
        self.player_level = 1
        self.hp = 100
        self.emerald = 25
        self.victory = False

    def is_alive(self):
        return self.hp > 0
                        
    def equip_weapons(self):
        weapons = [item for item in self.inventory
                       if isinstance(item, items.Weapon)]
        if not weapons:
            print("You don't have any weapons to equip!")
            print("")
            return

        for i, item in enumerate(weapons, 1):
            if len(item.ability) == 3:
                print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.ability[1], item.ability_level[1], item.ability[2], item.ability_level[2], item.value))
            elif len(item.ability) == 2:
                print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.ability[1], item.ability_level[1], item.value))
            elif len(item.ability) == 1:
                print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.value))
            else:
                raise NotImplementedError("No more than 3 Enchantments!")

        stop = False
        while not stop:
            choice = input("")
            try:
                self.to_equip = weapons[int(choice) - 1]
                print("")
                print("Equipped {} -- Does {} Damage".format(self.to_equip.name, self.to_equip.damage))
                print("")
                stop = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                print("")
                for i, item in enumerate(weapons, 1):
                    if len(item.ability) == 3:
                        print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.ability[1], item.ability_level[1], item.ability[2], item.ability_level[2], item.value))
                    elif len(item.ability) == 2:
                        print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.ability[1], item.ability_level[1], item.value))
                    elif len(item.ability) == 1:
                        print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | Value: {} emeralds ".format(i, item.name, item.description, item.damage, item.ability[0], item.ability_level[0], item.value))
                    else:
                        raise NotImplementedError("No more than 3 Enchantments!")
                print("")

    def print_inventory(self):
        os.system("clear")
        while True:
            try:
                best_weapon = self.to_equip
            except:
                best_weapon = self.most_powerful_weapon()
            print("Player Level {}".format(self.player_level))
            print("")
            print("Health Points: {}".format(self.hp))
            print("")
            print("Inventory:")
            for item in self.inventory:
                print('* ' + str(item))                   
            print("")
            print("Emeralds: {}".format(self.emerald))
            print("")
            print("Enchantment Points: {}".format(self.enchantment_points))
            print("")
            print("Your equipped weapon is your {}".format(best_weapon.name))
            print("")
            print("Would you like to (E)quip a weapon, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
                os.system("clear")
            elif user_input in ['E', 'e']:
                print("")
                print("Items to equip: ")
                print("")
                self.equip_weapons()
                return self.to_equip
            else:
                print("Invalid choice!")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage

            except AttributeError:
                pass

        return best_weapon

    def attack(self):
        try:
            best_weapon = self.to_equip
        except:
            best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        damagehi = best_weapon.damage + math.ceil(best_weapon.damage * 0.25)
        damagelo = best_weapon.damage - math.ceil(best_weapon.damage * 0.25)
        damage = random.randint(damagelo, damagehi + 1)
        print("You attack the {} with your {}!".format(enemy.name, best_weapon.name))
        print("")
        print("You do {} damage!".format(damage))
        print("")
        enemy.hp -= damage
        if not enemy.is_alive():
            print("You killed the {}!".format(enemy.name))
            print("")
        else:
            print("The {}'s HP is at {}.".format(enemy.name, enemy.hp))
            print("")

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        print("Choose an item to use to heal: ")
        print("Current HP: {}".format(self.hp))
        print("")
        
        if not consumables:
            print("You don't have any items to heal you!")
            print("")
            return

        for i, item in enumerate(consumables, 1):
            print("{}. {} (+{} HP)".format(i, item.name, item.healing_value,))
            print("")
            
        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("")
                print("Current HP: {}".format(self.hp))
                print("")
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                print("")

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)
            
    def openChest(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_open(self)

    def coords(self):
        print("You current location is at " + str(self.x) + "," + str(self.y))

    def menu(self):
        intro_title = """
        
               __  __ _                            __ _     _____                                             
              |  \/  (_)                          / _| |   |  __ \                                          _ 
              | \  / |_ _ __   ___  ___ _ __ __ _| |_| |_  | |  | |_   _ _ __   __ _  ___  ___  _ __  ___  (_)
              | |\/| | | '_ \ / _ \/ __| '__/ _` |  _| __| | |  | | | | | '_ \ / _` |/ _ \/ _ \| '_ \/ __|    
              | |  | | | | | |  __/ (__| | | (_| | | | |_  | |__| | |_| | | | | (_| |  __/ (_) | | | \__ \  _ 
              |_|__|_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_____/ \__,_|_| |_|\__, |\___|\___/|_| |_|___/ (_)
                                                                                __/ |                        
               _______                                   _              _     |____/ 
              |__   __| |               /\               | |            (_)                              
                  | |  | |__   ___     /  \__      ____ _| | _____ _ __  _ _ __   ____                       
                  | |  | '_ \ / _ \   / /\ \ \ /\ / / _` | |/ / _ \ '_ \| | '_ \ / _` |                        
                  | |  | | | |  __/  / ____ \ V  V / (_| |   <  __/ | | | | | | | (_| |                        
                  |_|  |_| |_|\___| /_/    \_\_/\_/ \__,_|_|\_\___|_| |_|_|_| |_|\__, |                        
                                                                                  __/ |                        
                                                                                |____/                         
        """
        original_color_r = 255
        original_color_g = 119
        original_color_b = 0
        print(Style.RESET_ALL)
        while True:
            os.system('clear')
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            print(Style.RESET_ALL)
            print("R - Resume")
            print("C - Controls")
            print("L - View License")
            print("Q - Quit Game")
            start_menu = input("> ")
            if start_menu in ['Q', 'q']:
                sys.exit(0)
            elif start_menu in ['C', 'c']:
                while True:
                    print("Would you like to (V)iew controls, (R)ead instructions, or (Q)uit?")
                    controls_prompt = input("> ")
                    if controls_prompt in ['R', 'r']:
                        print("")
                        print("Instructions:")
                        print("")
                        print("Enter an action on where the input prompts you. Input one of the letters listed. ")
                        print("The text to the right of the colon describes the actions.")
                        print("You can only use certain action at certain times.")
                        print("Normally, the winning tile is near the north, so try to move your character there to win!")
                        break
                    elif controls_prompt in ['V', 'v']:
                        print("")
                        print("Controls:")
                        print("")
                        print("c: Views Coordinates")
                        print("i: Opens Inventory. Inventory can be used to equip weapons. If weapon is not equipped, the strongest weapon is chosen.")
                        print("n: Moves North. Only usable if player is not impeded.")
                        print("s: Moves South. Only usable if player is not impeded.")
                        print("e: Moves East. Only usable if player is not impeded.")
                        print("w: Moves West. Only usable if player is not impeded.")
                        print("t: Trades with the NPC. Only usable if player is at a NPC Trader Tile.")
                        print("o: Opens chest. Only usable if player is at a Chest Tile.")
                        print("h: Uses items to heal player. Only usable when player is damaged.")
                        print("a: Uses equipped item to attack an enemy. Only usable if player is on a tile with an enemy that is alive.")
                        break
                    elif controls_prompt in ['Q', 'q']:
                        break
                    else:
                        print("Invalid choice!")
            elif start_menu in ['L', 'l']:
                ObjRead = open("LICENSE.txt", "r")
                txtContent = ObjRead.read(); 
                print("")
                print(txtContent)
            elif start_menu in ['R', 'r']:
                os.system('clear')
                return

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    
