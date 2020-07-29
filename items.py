import math
import player

class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")
    
    def __str__(self):
        if len(self.ability) == 3:
            return "{} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds ".format(self.name, self.description, self.damage, self.ability[0], self.ability_level[0], self.ability[1], self.ability_level[1], self.ability[2], self.ability_level[2], self.value)
        elif len(self.ability) == 2:
            return "{} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | Value: {} emeralds ".format(self.name, self.description, self.damage, self.ability[0], self.ability_level[0], self.ability[1], self.ability_level[1], self.value)
        elif len(self.ability) == 1:
            return "{} --- {} | Damage: {} | Enchantments: {}, Level {} | Value: {} emeralds ".format(self.name, self.description, self.damage, self.ability[0], self.ability_level[0], self.value)
        else:
            raise NotImplementedError("No more than 3 Enchantments!")

class Sword(Weapon):
    def __init__(self):
        self.name = "Sword"
        self.description = "A sturdy and reliable blade."
        self.damage = 12
        self.value = 15
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = [None]
        self.ability_level = [0]

class Daggers(Weapon):
    def __init__(self):
        self.name = "Daggers"
        self.description = "Daggers are the weapon of cravens - or so folk say."
        self.damage = 17
        self.value = 20
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = ["Fast Attack"]
        self.ability_level = [3]

class SoulKnife(Weapon):
    def __init__(self):
        self.name = "Soul Knife"
        self.description = "A ceremonial knife that uses magical energy to hold the wrath of souls inside its blade."
        self.damage = 30
        self.value = 50
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = ["Soul Gathering", "Thrust Attack"]
        self.ability_level = [2, 1] 

class Cutlass(Weapon):
    def __init__(self):
        self.name = "Cutlass"
        self.description = "This curved blade, wielded by the warriors of the Squid Coast, requires a steady hand in battle."
        self.damage = 20
        self.value = 100
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = ["Reliable Combo"]
        self.ability_level = [2]

class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")
    
    def __str__(self):
        return "{} (+{} HP) | Value: {} emeralds".format(self.name, self.healing_value, self.value)
        
class Apple(Consumable):
    def __init__(self):
        self.name = "Apple"
        self.healing_value = 10
        self.value = 12
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)

class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)

class Porkchop(Consumable):
    def __init__(self):
        self.name = "Porkchop"
        self.healing_value = 20
        self.value = 22
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)