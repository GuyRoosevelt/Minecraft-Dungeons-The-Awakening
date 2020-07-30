import colorama
from colorama import Fore, Style, Back
from player import Player
from collections import OrderedDict
import world
import time
import random
import os
import sys

def get_available_actions(room, player):
    actions = OrderedDict()
    print("")
    print("Choose an action: ")    action_adder(actions, 'c', player.coords, "View coordinates")
    action_adder(actions, 'm', menu(), "Open Menu")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "View inventory")
    if isinstance(room, world.TradingNPCs):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, world.Chest) and room.loot_claimed == False:
        action_adder(actions, 'o', player.openChest, "Open Chest")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Go north")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Go south")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Go east")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Go west")
            
    if player.hp < 100:
        action_adder(actions, 'h', player.heal, "Heal")
        
    return actions

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))

def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        print("")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")
            print("")

def play():
    os.system("clear")
    print("Objective: Escape from The Dungeons!")
    world.parse_world_dsl()
    player = Player()
 
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        print("")
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("Your journey has come to an early end!")
            print("""
                     _____                         ____                 
                    / ____|                       / __ \                
                   | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
                   | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
                   | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
                    \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
            """)
            time.sleep(5)
        elif player.victory:
            print("""
                  __     __          __          ___       _ 
                  \ \   / /          \ \        / (_)     | |
                   \ \_/ /__  _   _   \ \  /\  / / _ _ __ | |
                    \   / _ \| | | |   \ \/  \/ / | | '_ \| |
                     | | (_) | |_| |    \  /\  /  | | | | |_|
                     |_|\___/ \__,_|     \/  \/   |_|_| |_(_)
            """)
            time.sleep(5)

def display_intro_text():
    intro_title = """
                          OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
                          OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
                          OOOOOOOkkkkkkkkkOOOOOOOOkkkkkkkkkOOOOOOO
                          kkkkkkkkkkkkkkko:      :okkkkkkkkkkkkkkk
                          kkkkkkxdooooodxc        cxdooooodxkkkkkk
                          kkkkkkl       oc.      .co'     'lkkkkkk
                          kkkkkkl      .ll'      'll.    .'lkkkkkk
                          kkkkkkl      .lkxxxxxxxxkl.    ..lkkkkkk
                          kkkkkkdl     cdkkkkkkkkkkdc     ldkkkkkk
                          kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
                          kkkkkkd:  okkxc          cxkko  :dkkkkkk
                          kkkkkkl.  :kOo            oOk:   lkkkkkk
                          OOkkOkl.  ;dxl  lxxxxxxl  lxd;   lkOkkOO
                          OOOOOOl.       'dOOOOOOd'        lOOOOOO
                          OOOOOOd;      ':xOOOOOOx:'      ;dOOOOOO
                          OOOOOOOkkkkkkkkkOOOOOOOOkkkkkkkkkOOOOOOO
                          OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
                          OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    """
    print_text = intro_title
    original_color_r = 0
    original_color_g = 0
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    for i in range(30,51):
        print("\n" * 80)
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.1)
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    os.system('clear')
    original_color_r = 255
    original_color_g = 119
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    time.sleep(3)
    for i in range(30,51):
        print("\n" * 80)
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.1)
        original_color_r = original_color_r - 10
        original_color_g = original_color_g - 5
        original_color_b = original_color_b
    os.system('clear')
    time.sleep(1)
    intro_title = """
    
           __  __ _                            __ _     _____                                             
          |  \/  (_)                          / _| |   |  __ \                                          _ 
          | \  / |_ _ __   ___  ___ _ __ __ _| |_| |_  | |  | |_   _ _ __   __ _  ___  ___  _ __  ___  (_)
          | |\/| | | '_ \ / _ \/ __| '__/ _` |  _| __| | |  | | | | | '_ \ / _` |/ _ \/ _ \| '_ \/ __|    
          | |  | | | | | |  __/ (__| | | (_| | | | |_  | |__| | |_| | | | | (_| |  __/ (_) | | | \__ \  _ 
          |_|__|_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_____/ \__,_|_| |_|\__, |\___|\___/|_| |_|___/ (_)
                                                                            __/ |                        
            _______                                   _              _     |____/ 
           |__   __| |              /\               | |            (_)                              
              | |  | |__   ___     /  \__      ____ _| | _____ _ __  _ _ __   ____                       
              | |  | '_ \ / _ \   / /\ \ \ /\ / / _` | |/ / _ \ '_ \| | '_ \ / _` |                        
              | |  | | | |  __/  / ____ \ V  V / (_| |   <  __/ | | | | | | | (_| |                        
              |_|  |_| |_|\___| /_/    \_\_/\_/ \__,_|_|\_\___|_| |_|_|_| |_|\__, |                        
                                                                              __/ |                        
                                                                             |____/                         
    """
    for i in range(30,51):
        print("\n" * 80)
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.1)
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    os.system('clear')
    print('\033[38;2;255;119;0m' + intro_title)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = Fore.GREEN + Style.BRIGHT + '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def loadProgressBar():
    items = list(range(0, 8))
    l = len(items)
    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Loading Assets...', suffix = 'Loaded', length = 40)
    time.sleep(.3)
    for i, item in enumerate(items):
        time.sleep(random.random())
        printProgressBar(i + 1, l, prefix = '                      Loading...', suffix = 'Loaded', length = 50)
    time.sleep(.5)

def intro():
    intro_title = """
    
           __  __ _                            __ _     _____                                             
          |  \/  (_)                          / _| |   |  __ \                                          _ 
          | \  / |_ _ __   ___  ___ _ __ __ _| |_| |_  | |  | |_   _ _ __   __ _  ___  ___  _ __  ___  (_)
          | |\/| | | '_ \ / _ \/ __| '__/ _` |  _| __| | |  | | | | | '_ \ / _` |/ _ \/ _ \| '_ \/ __|    
          | |  | | | | | |  __/ (__| | | (_| | | | |_  | |__| | |_| | | | | (_| |  __/ (_) | | | \__ \  _ 
          |_|__|_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_____/ \__,_|_| |_|\__, |\___|\___/|_| |_|___/ (_)
                                                                            __/ |                        
            _______                                   _              _     |____/ 
           |__   __| |              /\               | |            (_)                              
              | |  | |__   ___     /  \__      ____ _| | _____ _ __  _ _ __   ____                       
              | |  | '_ \ / _ \   / /\ \ \ /\ / / _` | |/ / _ \ '_ \| | '_ \ / _` |                        
              | |  | | | |  __/  / ____ \ V  V / (_| |   <  __/ | | | | | | | (_| |                        
              |_|  |_| |_|\___| /_/    \_\_/\_/ \__,_|_|\_\___|_| |_|_|_| |_|\__, |                        
                                                                              __/ |                        
                                                                             |____/                         
    """
    os.system('clear')
    original_color_r = 0
    original_color_g = 0
    original_color_b = 0
    for i in range(30,51):
        print("\n" * 80)
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.1)
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    os.system('clear')
    original_color_r = 255
    original_color_g = 119
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    print(Style.RESET_ALL)
    loadProgressBar()
    os.system('clear')
    display_intro_text()
    while True:
        print(Style.RESET_ALL)
        print("S - Start Game")
        print("C - Controls")
        print("L - View License")
        print("Q - Quit")
        start_menu = input("> ")
        if start_menu in ['Q', 'q']:
            return
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
        elif start_menu in ['S', 's']:
            original_color_r = 255
            original_color_g = 119
            original_color_b = 0
            os.system('clear')
            for i in range(30,51):
                print("\n" * 80)
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.1)
                original_color_r = original_color_r - 10
                original_color_g = original_color_g - 5
                original_color_b = original_color_b
            os.system('clear')
            print(Style.RESET_ALL)
            play()
        else:
            print("Invalid choice!")

def menu():
    original_color_r = 255
    original_color_g = 119
    original_color_b = 0
    os.system('clear')
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    print(Style.RESET_ALL)
    while True:
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