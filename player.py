import items
import world
import random
import math
import sys
import dill as pickle
import pyAesCrypt
import maps
import colorama
from colorama import Fore, Style, Back
import string
import os
import game
from os import path

class Player:
    def __init__(self):
        self.inventory = [items.Sword(),
                          items.Apple()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.enchantment_points = 1
        self.player_level = 1
        self.maxhp = 100
        self.hp = self.maxhp
        self.emerald = 25
        self.victory = False
        self.bufferSize = 64 * 1024
        self.passwordtxt = ''.join((random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()') for i in range(20)))

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
            print("Choose an item to equip:")
            print("")
            print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds".format(i, item.name, item.description, item.damage, item.ability["Enchantment 1"], item.ability["Enchantment 1 Level"], item.ability["Enchantment 2"], item.ability["Enchantment 2 Level"], item.ability["Enchantment 3"], item.ability["Enchantment 3 Level"], item.value))

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
                    print("{}. {} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds".format(i, item.name, item.description, item.damage, item.ability["Enchantment 1"], item.ability["Enchantment 1 Level"], item.ability["Enchantment 2"], item.ability["Enchantment 2 Level"], item.ability["Enchantment 3"], item.ability["Enchantment 3 Level"], item.value))
                print("")
        return

    def print_inventory(self):
        #max hp increases for each level by * 2.5
        os.system("cls")
        while True:
            try:
                best_weapon = self.to_equip
            except:
                best_weapon = self.most_powerful_weapon()
            print("Player Level {}".format(self.player_level))
            print("")
            print("Health Points: {}/{}".format(self.hp, self.maxhp))
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
                os.system("cls")
                return
            elif user_input in ['E', 'e']:
                print("")
                print("Items to equip: ")
                print("")
                self.equip_weapons()
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
        print("You {} the {} with your {}!".format(best_weapon.attack, enemy.name, best_weapon.name))
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
        
    def travel(self):
        room = world.tile_at(self.x, self.y)
        room.choosemap(self)

    def coords(self):
        print("You current location is at " + str(self.x) + "," + str(self.y))

    def encrypt(self, file, outfile):
        print("Password File Loaded Successfully!")
        passwordfile = open('Save\password.bin', 'rb')
        password = pickle.load(passwordfile)
        # encrypt
        print("Game File Encrypted Successfully!")
        pyAesCrypt.encryptFile(file, outfile, password, self.bufferSize)
        os.remove(file) 
        
    def decrypt(self, file, outfile):
        print("Password File Loaded Successfully!")
        passwordfile = open('Save\password.bin', 'rb')
        password = pickle.load(passwordfile)
        # decrypt
        print("Password Correct!")
        pyAesCrypt.decryptFile(file, outfile, password, self.bufferSize)
        os.remove(file)
        print("Game File Decrypted Successfully!")
        
    def save(self):
        try:
            inventory = self.inventory
            maxhp = self.maxhp
            emerald = self.emerald
            enchantment_points = self.enchantment_points
            player_level = self.player_level
            #Create Password File
            print("Password File Created Successfully!")
            passwordfile = file = open('Save\password.bin', 'wb')
            pickle.dump(self.passwordtxt, passwordfile)
            passwordfile.close()
            #Close the file
            gamesave = {
                'inventory' : inventory,
                'maxhp' : maxhp,
                'emerald' : emerald,
                'enchantment points' : enchantment_points,
                'player level' : player_level
            }
            try:
                print("Game Save Already Exists So Overwriting...")
                os.remove('Save\savefile.sav')
            except:
                pass
            picklefile = open('Save\savefile.dat', 'wb')
            print("Save Files Created Successfully!")
            #pickle the dictionary and write it to file
            pickle.dump(gamesave, picklefile)
            print("Game Saved Successfully!")
            #close the file
            picklefile.close()
            self.encrypt('Save\savefile.dat', 'Save\savefile.sav')
        except MemoryError:
            print("File Memory Corrupted!")
        except AttributeError:
            print("File Memory Invalid!")
        except IOError:
            print("File Not Found!")
        except Exception as e:
            print("Exception error occured:")
            print(e)
        
    def load(self):
        try:
            try:
                self.decrypt('Save\savefile.sav', 'Save\savefile.dat')
                print("Save Files Decrypted Successfully!")
            except:
                pass
            #read the pickle file
            picklefile = open('Save\savefile.dat', 'rb')
            print("Save Files Read Successfully!")
            #unpickle the dataframe
            game = pickle.load(picklefile)
            self.inventory = game['inventory']
            print("Inventory Loaded Successfully!")
            self.maxhp = game['maxhp']
            print("Max HP Loaded Successfully!")
            self.emerald = game['emerald']
            print("Emeralds Loaded Successfully!")
            self.enchantment_points = game['enchantment points']
            print("Enchantment Points Loaded Successfully!")
            self.player_level = game['player level']
            print("Player Level Loaded Successfully!")
            print("Game Save Loaded Successfully!")
            #close file
            picklefile.close()
            try:
                self.encrypt('Save\savefile.dat', 'Save\savefile.sav')
            except:
                pass
        except MemoryError:
            print("File Memory Corrupted!")
        except AttributeError:
            print("File Memory Invalid!")
        except IOError:
            print("File Not Found!")
        except Exception as e:
            print("Exception error occured:")
            print(e)
            
    def menu(self):
        intro_title = open('Art\\title.txt', 'r').read()
        original_color_r = 255
        original_color_g = 119
        original_color_b = 0
        os.system('cls')
        while True:
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            print(Style.RESET_ALL)
            print("R - Resume")
            print("G - Save Game")
            print("L - Load Save")
            print("C - Controls")
            print("L - View License")
            print("Q - Quit Game")
            start_menu = input("> ")
            if start_menu in ['Q', 'q']:
                while True:
                    print("Are you sure you want to exit? (Y)es or (N)o?")
                    quit_menu = input("> ")
                    if quit_menu in ['Y', 'y']:
                        sys.exit(0)
                    elif quit_menu in ['N', 'n']:
                        break
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
            elif start_menu in ['G', 'g']:
                self.save()
                try:
                    inventory = self.inventory
                    maxhp = self.maxhp
                    emerald = self.emerald
                    enchantment_points = self.enchantment_points
                    player_level = self.player_level
                    #print the dataframe
                    print("")
                    print("----------Save Data----------")
                    print("Player Level {}".format(player_level))
                    print("")
                    print("Max Hp: {}".format(maxhp))
                    print("")
                    print("Inventory:")
                    for item in inventory:
                       print('* ' + str(item))                   
                    print("")
                    print("Emeralds: {}".format(emerald))
                    print("")
                    print("Enchantment Points: {}".format(enchantment_points))
                    print("")
                except:
                    pass
            elif start_menu in ['L', 'l']:
                self.load()
                try:
                    print("")
                    print("----------Player Data----------")
                    print("Player Level {}".format(self.player_level))
                    print("")
                    print("Max Hp: {}".format(self.maxhp))
                    print("")
                    print("Inventory:")
                    for item in self.inventory:
                       print('* ' + str(item))                   
                    print("")
                    print("Emeralds: {}".format(self.emerald))
                    print("")
                    print("Enchantment Points: {}".format(self.enchantment_points))
                    print("")
                except:
                    pass
            elif start_menu in ['V', 'v']:
                ObjRead = open("LICENSE.txt", "r")
                txtContent = ObjRead.read(); 
                print("")
                print(txtContent)
            elif start_menu in ['R', 'r']:
                os.system('cls')
                return
            else:
                print("Invalid choice!")

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

    def hax(self):
        self.inventory.append(items.DebugStick())
        self.emerald = self.emerald + 100000
        self.maxhp = 10000
        self.hp = self.maxhp
        self.player_level = 100
        self.enchantment_points = 1000
        print("----------Inventory----------")
        print("Player Level {}".format(self.player_level))
        print("")
        print("Max Hp: {}".format(self.maxhp))
        print("")
        print("Inventory:")
        for item in self.inventory:
           print('* ' + str(item))                   
        print("")
        print("Emeralds: {}".format(self.emerald))
        print("")
        print("Enchantment Points: {}".format(self.enchantment_points))
        print("")

    def all(self):
        self.inventory.append(items.DebugStick())
        self.inventory.append(items.Daggers())
        self.inventory.append(items.SoulKnife())
        self.inventory.append(items.Cutlass())
        self.inventory.append(items.Apple())
        self.inventory.append(items.HealingPotion())
        self.inventory.append(items.Porkchop())
        self.inventory.append(items.Apple())
        self.inventory.append(items.HealingPotion())
        self.inventory.append(items.Porkchop())
        self.emerald = self.emerald + 999999999
        self.maxhp = 10000000
        self.hp = self.maxhp
        self.player_level = 1000
        self.enchantment_points = 9999
        print("----------Inventory----------")
        print("Player Level {}".format(self.player_level))
        print("")
        print("Max Hp: {}".format(self.maxhp))
        print("")
        print("Inventory:")
        for item in self.inventory:
           print('* ' + str(item))                   
        print("")
        print("Emeralds: {}".format(self.emerald))
        print("")
        print("Enchantment Points: {}".format(self.enchantment_points))
        print("")
