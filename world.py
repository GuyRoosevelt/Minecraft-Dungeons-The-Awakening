import random
import enemies
import npc
import math
import game
import time
from pygame import mixer
import os
import items
import colorama
from colorama import Fore, Style, Back
import player
import sys
import ctypes
import msvcrt
import subprocess
from ctypes import wintypes

def set_font(fonttype, fontsizex, fontsizey):
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11
    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = fontsizex
    font.dwFontSize.Y = fontsizey
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = fonttype
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass

class EmptyCampTile(MapTile):
    def intro_text(self):
      r = random.randint(1,4)
      if r == 1:
          return "An unremarkable part of the camp. You decide to look around more."
      elif r == 2:
          return "You step onto a patch of flat grass. Nothing seems to be remarkable about it."
      elif r == 3:
          return "You look around and see Training Dummies and Blacksmiths, and also a missions map. Maybe you should look around more."
      else:
          return "You decide to look around. Many things await! But for now, you are still at the camp."

class TrainingDummy(MapTile):
    def __init__(self, x, y):
        self.enemy = enemies.TrainingDummy()
        self.alive_text = "A Training Dummy stands in front of you, tied to a stick. You can attack it to test your weapon!"
        self.dead_text = "You destroyed the Training Dummy"
        self.enemy_attack = "stares at you"
        super().__init__(x, y)
        
    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text
        else:
            text = self.dead_text
        return text

class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch
        on the wall.
        You can make out four paths, each equally as dark
        and foreboding.
        """

class CampStartTile(MapTile):
    def intro_text(self):
        return """
        You look around your camp. Many things lay there. A Blacksmith and a Wandering Trader sit behind their stalls.
        You decide to explore the camp, before choosing a mission from the map in the center of the camp. 
        """

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the dungeon. You must forge onwards.
        """

class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True
    
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
        Victory is yours!"""

class EnemyTile(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def intro_text(self):
        if self.enemy.is_alive():
            text = self.alive_text 
        else:
            text = self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            damagehigh = self.enemy.damage + math.ceil(self.enemy.damage * 0.25)
            damagelow = self.enemy.damage - math.ceil(self.enemy.damage * 0.25)
            damage = random.randint(damagelow, damagehigh + 1)
            player.hp = player.hp - damage
            print("The {} {}, and does {} damage. You have {} HP remaining.".format(self.enemy.name, self.enemy_attack, damage, player.hp))


class RandomEnemyTile(EnemyTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.Vindicator()
            self.alive_text = "A snarling Vindicator jumps down in front of you, and raises it's axe threatingly."
            self.dead_text = "The corpse of a defeated Vindicator decays on the ground."
            self.enemy_attack = "slices you with a axe"

        elif r < 0.80:
            self.enemy = enemies.ArmoredVindicator()
            self.alive_text = "An Armored Vindicator yells out a fierce battle cry and rushes at you!"
            self.dead_text = "The dead Vindicator reminds you of your triumph."
            self.enemy_attack = "brings the axe down, hard, apon you"
        elif r < 0.95:
            self.enemy = enemies.ZombieHorde()
            self.alive_text = "A horde of moaning, biting zombies stumble towards you."
            self.dead_text = "Dozens of zombies lay scattered, dead, across the ground."
            self.enemy_attack = "attack you"
        else:
            self.enemy = enemies.SkeletonWarrior()
            self.alive_text = "A Skeleton, dressed in armor, aims its spear at you."
            self.dead_text = "Bones from the dead Skeleton lay scattered across the ground."
            self.enemy_attack = "stabs you with its spear"
               
        super().__init__(x, y)

class RedstoneGolemTile(EnemyTile):
    def __init__(self, x, y):
        self.enemy = enemies.RedstoneGolem()
        self.alive_text = "A hulking, glowing Redstone Golem lumbers toward you, stone fists raised, ready to smash you into bits."
        self.dead_text = "The Redstone Golem shatters into pieces of rock and Redstone, and sinks slowly into the ground."
        self.enemy_attack = "smashes the ground"
        super().__init__(x, y)
      
class TradingNPCs(MapTile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def trade(self, buyer, seller):
        if self.buyorsell == "buy":
            print("Your emeralds: {}".format(buyer.emerald))
            print("Trader's emeralds: {}".format(seller.emerald))
        elif self.buyorsell == "sell":
            print("Your emeralds: {}".format(seller.emerald))
            print("Trader's emeralds: {}".format(buyer.emerald))
        print("")
        for i, item in enumerate(seller.inventory, 1):
            if self.buyorsell == "buy":
                 print("{}. {} - {} Emeralds".format(i, item.name, item.buy_value))
            elif self.buyorsell == "sell":
                 print("{}. {} - {} Emeralds".format(i, item.name, item.sell_value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if self.buyorsell == "buy" and item.value > buyer.emerald:
            print("That's too expensive")
            return
        elif self.buyorsell == "sell" and item.value > buyer.emerald:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        if self.buyorsell == "buy":
            buyer.emerald = buyer.emerald - item.buy_value
            seller.emerald = seller.emerald + item.buy_value
        elif self.buyorsell == "sell":
            buyer.emerald = buyer.emerald - item.sell_value
            seller.emerald = seller.emerald + item.sell_value
        print("")
        print("Trade complete!")
        print("")
        if self.buyorsell == "buy":
            print("Your emeralds: {}".format(buyer.emerald))
            print("Trader's emeralds: {}".format(seller.emerald))
        elif self.buyorsell == "sell":
            print("Your emeralds: {}".format(seller.emerald))
            print("Trader's emeralds: {}".format(buyer.emerald))
        print("")
        print("Here's whats available to {}:".format(self.buyorsell))
        for i, item in enumerate(seller.inventory, 1):
            if self.buyorsell == "buy":
                print("{}. {} - {} Emeralds".format(i, item.name, item.buy_value))
            elif self.buyorsell == "sell":
                print("{}. {} - {} Emeralds".format(i, item.name, item.sell_value))

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['B', 'b']:
                self.buyorsell = "buy"
                print("")
                print("Here's whats available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['S', 's']:
                self.buyorsell = "sell"
                print("")
                print("Here's whats available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

class TraderTile(TradingNPCs):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x, y)

    def intro_text(self):
        return """
        A tall, square looking person stands behind a stall, counting his emeralds.
        He has a very long nose. The Villager looks willing to trade.
        """

class BlacksmithTile(TradingNPCs):
    def __init__(self, x, y):
        self.trader = npc.BlackSmith()
        super().__init__(x, y)

    def intro_text(self):
        return """
        A Villager is hammering something, behind the counter, on an anvil.
        He looks willing to trade.
        """

class FindEmeraldTile(MapTile):
    def __init__(self, x, y):
        self.emerald = random.randint(1, 51)
        self.emerald_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.emerald_claimed:
            self.emerald_claimed = True
            player.emerald = player.emerald + self.emerald
            print("+{} emeralds added.".format(self.emerald))

    def intro_text(self):
        if self.emerald_claimed:
            return """
            Another unremarkable part of the cave. You
            must forge onwards.
            """
        else:
            return """
            Someone dropped a few emeralds. You pick them up.
            """

class Chest(MapTile):
    def __init__(self, x, y):
        self.loot_claimed = False 
        super().__init__(x, y)

    def check_if_open(self, player):
        if self.loot_claimed == False:
            player.emerald = player.emerald + self.emerald
            random_weapon = random.choice(self.weapon_pool)
            random_item = random.choice(self.item_pool)
            player.inventory.append(random_weapon)
            player.inventory.append(random_item)
            try:
                print("You got {}, {} and {} emeralds from the chest!".format(random_weapon.name, random_item.name, self.emerald))
            except:
                print("You got {} and {} emeralds from the chest!".format(random_item.name, self.emerald))
                player.inventory.remove(None)
            self.loot_claimed = True

class CommonChest(Chest):
    def __init__(self, x, y):
        self.emerald = random.randint(1, 20)
        self.weapon_pool = [
          items.Daggers(),
          items.Daggers(),
          items.Sword(),
          items.Sword(),
          items.Sword()
        ]

        self.item_pool = [
          items.Apple(),
          items.Apple(),
          items.Apple(),
          items.Porkchop(),
          items.Porkchop(),
        ]    
        super().__init__(x, y)

    def intro_text(self):
        if self.loot_claimed:
            return """
            Another unremarkable part of the cave. You
            must forge onwards."""
        else:
            return """
            Your notice something in the corner.
            You examine it. It is brown and made of wood, and has metal latches.
            It turns out to be a Common Chest!
            """

class FancyChest(Chest):
    def __init__(self, x, y):
        self.emerald = random.randint(1, 26)
        self.weapon_pool = [
          items.Cutlass(),
          items.SoulKnife(),
          items.Daggers(),
          items.Sword(),
          items.Sword(),
        ]

        self.item_pool = [
          items.Apple(),
          items.Porkchop(),
          items.Porkchop(),
          items.HealingPotion()
        ]    
        super().__init__(x, y)

    def intro_text(self):
        if self.loot_claimed:
            return """
            Another unremarkable part of the cave. You
            must forge onwards."""
        else:
            return """
            Your notice something in the corner.
            You examine it. It is covered with red and gold accents.
            It turns out to be a Fancy Chest!
            """

class ObsidianChest(Chest):
    def __init__(self, x, y):
        self.emerald = random.randint(1, 36)
        self.weapon_pool = [
          items.Cutlass(),
          items.SoulKnife(),
          items.Daggers(),
        ]

        self.item_pool = [
          items.Porkchop(),
          items.Porkchop(),
          items.HealingPotion()
        ]    
        super().__init__(x, y)

    def intro_text(self):
        if self.loot_claimed:
            return """
            Another unremarkable part of the cave. You
            must forge onwards."""
        else:
            return """
            Your notice something in the corner.
            You examine it. It is made of dark purple obsidian, accented with glowing, blue runes.
            It turns out to be a Obisidian Chest!
            """

class RandomChest(Chest):
    def __init__(self, x, y):
        self.r = random.random()
        if self.r < 0.50:
            self.nothing = None
            self.emerald = random.randint(1, 20)
            self.weapon_pool = [
              self.nothing,
              self.nothing,
              self.nothing,
              items.Daggers(),
              items.Daggers(),
              items.Sword(),
              items.Sword(),
              items.Sword()
            ]

            self.item_pool = [
              items.Apple(),
              items.Apple(),
              items.Apple(),
              items.Porkchop(),
              items.Porkchop(),
            ]    

        elif self.r < 0.80:
            self.emerald = random.randint(1, 26)
            self.weapon_pool = [
              items.Cutlass(),
              items.SoulKnife(),
              items.Daggers(),
              items.Sword(),
              items.Sword(),
            ]

            self.item_pool = [
              items.Apple(),
              items.Porkchop(),
              items.Porkchop(),
              items.HealingPotion()
            ]
        else:
            self.emerald = random.randint(1, 36)
            self.weapon_pool = [
              items.Cutlass(),
              items.SoulKnife(),
              items.Daggers(),
            ]

            self.item_pool = [
              items.Porkchop(),
              items.Porkchop(),
              items.HealingPotion()
            ]
 
        super().__init__(x, y)
        
    def intro_text(self):
        if self.loot_claimed:
            return """
            Another unremarkable part of the cave. You
            must forge onwards."""
        else:
            if self.r < 0.50:
              return """
                Your notice something in the corner.
                You examine it. It is brown and made of wood, and has metal latches.
                It turns out to be a Common Chest!
                """
            elif self.r < 0.80:
                return """
                Your notice something in the corner.
                You examine it. It is covered with red and gold accents.
                It turns out to be a Fancy Chest!
                """
            else:
                return """
                Your notice something in the corner.
                You examine it. It is made of dark purple obsidian, accented with glowing, blue runes.
                It turns out to be a Obisidian Chest!
                """

class ChooseMap(MapTile):
    def playsound(self, file):
        mixer.init()
        mixer.music.load(file)
        mixer.music.set_volume(1)
        mixer.music.play(-1)

    def print_file(self, path):
        print(open(path, 'r').read())
    
    def choosemap(self, world):
        self.playsound("Sounds\Wanderlust.mp3")
        while True:
            print("Would you like to (T)ravel or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                mixer.music.stop()
                return
            elif user_input in ['T', 't']:
                while True:
                    print("Where would you like to travel to? Areas unlocked: (S)quid Coast or (Q)uit?")
                    user_input = input()
                    if user_input in ['Q', 'q']:
                        break
                    elif user_input in ['S', 's']:
                        def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = Fore.GREEN + Style.BRIGHT + '█', printEnd = "\r"):
                            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
                            filledLength = int(length * iteration // total)
                            bar = fill * filledLength + '-' * (length - filledLength)
                            print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
                            # Print New Line on Complete
                            if iteration == total: 
                                print()
                        os.system('cls')
                        set_font("Courier New", 30, 30)
                        self.playsound("Sounds\Intertile.mp3")
                        self.print_file('Art\\traveling_to.txt')
                        self.print_file('Art\\squidcoast.txt')
                        items = list(range(0, 8))
                        l = len(items)
                        # Initial call to print 0% progress
                        printProgressBar(0, l, prefix = 'Loading Assets...', suffix = 'Loaded', length = 40)
                        time.sleep(.3)
                        for i, item in enumerate(items):
                            time.sleep(.7)
                            printProgressBar(i + 1, l, prefix = '                      Traveling...', suffix = 'Loaded', length = 50)
                        time.sleep(.5)
                        os.system('cls')
                        mixer.music.stop()
                        print(Style.RESET_ALL)
                        game.play()
                    else:
                        print("Invalid choice!")
            else:
                print("Invalid choice!")
                
    def intro_text(self):
            return """
            A map stands on a pedestal. It shows directions to many locations.
            It looks like you can travel with it.
            """

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

world_map = [
]

tile_type_dict = {"VT": VictoryTile,
                  "EN": RandomEnemyTile,
                  "ST": StartTile,
                  "EP": EmptyCavePath,
                  "TT": TraderTile,
                  "FE": FindEmeraldTile,
                  "CC": CommonChest,
                  "FC": FancyChest,
                  "OC": ObsidianChest,
                  "RC": RandomChest,
                  "RG": RedstoneGolemTile,
                  "BS": BlacksmithTile,
                  "CT": EmptyCampTile,
                  "TD": TrainingDummy,
                  "CM": ChooseMap,
                  "CS": CampStartTile,
                  "NO": None}

lobby_dsl = """
|RC|CT|FE|CT|CT|
|CT|FE|CM|RC|TD|
|CT|CT|CT|CT|TD|
|CT|CT|CS|CT|TD|
|CT|CT|CT|CT|CT|
"""

squidcoast_dsl = """
|NO|NO|VT|NO|NO|
|NO|NO|RG|NO|NO|
|BS|EP|RC|EN|EN|
|EP|EN|NO|TT|EN|
|EN|NO|RC|NO|EN|
|EN|FE|EN|NO|TT|
|TT|NO|ST|FE|EN|
|FE|NO|EN|NO|FE|
"""

world_dsl = """
"""

def is_dsl_valid(dsl):
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
        
    return True

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")
    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile or tile_type == CampStartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)
        world_map.append(row)


