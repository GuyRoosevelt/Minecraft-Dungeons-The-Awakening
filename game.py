import colorama
from colorama import Fore, Style, Back
from player import Player
from collections import OrderedDict
import world
import time
import random
import player
import os
from pygame import mixer
import sys
import ctypes
import msvcrt
import pyautogui
import subprocess
from ctypes import wintypes
import subprocess
import maps
import math

def get_available_actions(room, player):
    actions = OrderedDict()
    print("")
    print("Choose an action: ")
    action_adder(actions, 'c', player.coords, "View coordinates")
    action_adder(actions, 'm', player.menu, "Open Menu")
    action_adder(actions, 'l33thax0r', player.hax, "HAX")
    action_adder(actions, 'a11th3st0ps', player.all, "HAX")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "View inventory")
    if isinstance(room, world.TradingNPCs):
        action_adder(actions, 't', player.trade, "Trade")
    if isinstance(room, world.ChooseMap):
        action_adder(actions, 't', player.travel, "Travel")
    if isinstance(room, world.Chest) and room.loot_claimed == False:
        action_adder(actions, 'o', player.openChest, "Open Chest")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if isinstance(room, world.TrainingDummy) and room.enemy.is_alive():
            action_adder(actions, 'a', player.attack, "Attack Dummy")
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
    if not name == str('HAX'):
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

def play_sound(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.set_volume(1)
    mixer.music.play(-1)

def lobby():
    set_font("Courier New", 20, 20)
    r = random.randint(1,2)
    if r == 1:
        play_sound("Sounds\Dalarna.mp3")
    else:
        play_sound("Sounds\Halland.mp3")
    world.world_map = [
    ]
    world.world_dsl = world.lobby_dsl
    pyautogui.press('f11')
    time.sleep(0.1)
    pyautogui.press('f11')
    os.system("cls")
    print("Location: Camp")
    world.parse_world_dsl()
    player = Player()
    player.victory = False
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        print("")
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)

def travel_lobby():
    def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = Fore.GREEN + Style.BRIGHT + '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()
    os.system('cls')
    play_sound("Sounds\Intertile.mp3")
    set_font("Courier New", 25, 25)
    items = list(range(0, 8))
    l = len(items)
    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Loading Assets...', suffix = 'Loaded', length = 40)
    time.sleep(.3)
    for i, item in enumerate(items):
        time.sleep(.7)
        printProgressBar(i + 1, l, prefix = '                      Traveling to lobby...', suffix = 'Loaded', length = 50)
    time.sleep(.5)
    os.system('cls')
    mixer.music.stop()
    print(Style.RESET_ALL)
    lobby()

def play():
    tic = time.perf_counter()
    set_font("Courier New", 20, 20)
    play_sound("Sounds\SquidCoast.mp3")
    world.world_map = [
    ]
    world.world_dsl = world.squidcoast_dsl
    os.system("cls")
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
            toc = time.perf_counter()
            intro_title = open('Art\\lose.txt', 'r').read() + str("\n\nGame won in {} seconds".format(math.ceil(toc - tic)))
            original_color_r = 0
            original_color_g = 0
            original_color_b = 0
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            for i in range(30,51):
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.02)
                os.system('cls')
                original_color_r = original_color_r + 10
                original_color_g = original_color_g + 5
                original_color_b = original_color_b
            os.system('cls')
            original_color_r = 255
            original_color_g = 119
            original_color_b = 0
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            time.sleep(9)
            os.system('cls')
            for i in range(30,51):
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.02)
                os.system('cls')
                original_color_r = original_color_r - 10
                original_color_g = original_color_g - 5
                original_color_b = original_color_b
            time.sleep(.5)
            travel_lobby()
        elif player.victory:
            play_sound("Sounds\Finally.mp3")
            toc = time.perf_counter()
            intro_title = open('Art\\win.txt', 'r').read() + str("\n\nGame won in {} seconds".format(math.ceil(toc - tic)))
            original_color_r = 0
            original_color_g = 0
            original_color_b = 0
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            for i in range(30,51):
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.02)
                os.system('cls')
                original_color_r = original_color_r + 10
                original_color_g = original_color_g + 5
                original_color_b = original_color_b
            os.system('cls')
            original_color_r = 255
            original_color_g = 119
            original_color_b = 0
            print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
            time.sleep(9)
            os.system('cls')
            for i in range(30,51):
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.02)
                os.system('cls')
                original_color_r = original_color_r - 10
                original_color_g = original_color_g - 5
                original_color_b = original_color_b
            time.sleep(.5)
            travel_lobby()

def display_intro_text():
    set_font("Courier New", 25, 25)
    intro_title = open('Art\\logo.txt', 'r').read()
    original_color_r = 0
    original_color_g = 0
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    for i in range(30,51):
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.001)
        os.system('cls')
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    os.system('cls')
    original_color_r = 255
    original_color_g = 119
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    time.sleep(1)
    os.system('cls')
    for i in range(30,51):
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.02)
        os.system('cls')
        original_color_r = original_color_r - 10
        original_color_g = original_color_g - 5
        original_color_b = original_color_b
    os.system('cls')
    play_sound("Sounds\Finnbacka.mp3")
    time.sleep(1)
    intro_title = open('Art\\title.txt', 'r').read()
    for i in range(30,51):
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.001)
        os.system('cls')
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    os.system('cls')
    print('\033[38;2;255;119;0m' + intro_title)

def intro():
    set_font("Courier New", 17, 17)
    ctypes.windll.kernel32.SetConsoleTitleW("Minecraft Dungeons: The Awakening")
    intro_title = open('Art\\splash.txt', 'r').read()
    original_color_r = 0
    original_color_g = 0
    original_color_b = 0
    play_sound("Sounds\Intro.mp3")
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    for i in range(30,51):
        print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
        time.sleep(.001)
        os.system('cls')
        original_color_r = original_color_r + 10
        original_color_g = original_color_g + 5
        original_color_b = original_color_b
    original_color_r = 255
    original_color_g = 119
    original_color_b = 0
    print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
    print(Style.RESET_ALL)
    time.sleep(4.5)
    os.system('cls')
    display_intro_text()
    while True:
        print(Style.RESET_ALL)
        print("S - Start Game")
        print("C - Controls")
        print("V - View License")
        print("Q - Quit game")
        start_menu = input("> ")
        if start_menu in ['Q', 'q']:
            return
        elif start_menu in ['C', 'c']:
            while True:
                print("Would you like to (V)iew controls, (R)ead instructions, or (Q)uit?")
                controls_prompt = input("--> ")
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
        elif start_menu in ['V', 'v']:
            ObjRead = open("LICENSE.txt", "r")
            txtContent = ObjRead.read(); 
            print("")
            print(txtContent)
        elif start_menu in ['S', 's']:
            intro_title = open('Art\\title.txt', 'r').read()
            original_color_r = 255
            original_color_g = 119
            original_color_b = 0
            os.system('cls')
            for i in range(30,51):
                print('\033[38;2;%d;%d;%dm' % (original_color_r, original_color_g, original_color_b) + intro_title)
                time.sleep(.001)
                os.system('cls')
                original_color_r = original_color_r - 10
                original_color_g = original_color_g - 5
                original_color_b = original_color_b
            os.system('cls')
            print(Style.RESET_ALL)
            mixer.music.stop()
            try:
                lobby()
            except Exception as e:
                print("Exception error occured:")
                print(e)
                input("Press Enter to Exit...")
                sys.exit(0)
        else:
            print("Invalid choice!")
