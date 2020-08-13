import math
import player

class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects.")
    
    def __str__(self):
        return "{} --- {} | Damage: {} | Enchantments: {}, Level {} | {}, Level {} | {}, Level {} | Value: {} emeralds".format(self.name, self.description, self.damage, self.ability["Enchantment 1"], self.ability["Enchantment 1 Level"], self.ability["Enchantment 2"], self.ability["Enchantment 2 Level"], self.ability["Enchantment 3"], self.ability["Enchantment 3 Level"], self.value)

class Sword(Weapon):
    def __init__(self):
        self.name = "Sword"
        self.description = "A sturdy and reliable blade."
        self.damage = 12
        self.attack = "slash"
        self.value = 15
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = {"Enchantment 1": None,
                        "Enchantment 1 Level": 0,
                        "Enchantment 2": None,
                        "Enchantment 2 Level": 0,
                        "Enchantment 3": None,
                        "Enchantment 3 Level": 0}
        
class Daggers(Weapon):
    def __init__(self):
        self.name = "Daggers"
        self.description = "Daggers are the weapon of cravens - or so folk say."
        self.damage = 17
        self.attack = "rapidly stab"
        self.value = 20
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = {"Enchantment 1": "Fast Attack",
                        "Enchantment 1 Level": 3,
                        "Enchantment 2": None,
                        "Enchantment 2 Level": 0,
                        "Enchantment 3": None,
                        "Enchantment 3 Level": 0}

class SoulKnife(Weapon):
    def __init__(self):
        self.name = "Soul Knife"
        self.description = "A ceremonial knife that uses magical energy to hold the wrath of souls inside its blade."
        self.damage = 30
        self.attack = "reach out and impale"
        self.value = 50
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = {"Enchantment 1": "Soul Gathering",
                        "Enchantment 1 Level": 2,
                        "Enchantment 2": "Thrust Attack",
                        "Enchantment 2 Level": 1,
                        "Enchantment 3": None,
                        "Enchantment 3 Level": 0}
        
class Cutlass(Weapon):
    def __init__(self):
        self.name = "Cutlass"
        self.description = "This curved blade, wielded by the warriors of the Squid Coast, requires a steady hand in battle."
        self.damage = 20
        self.attack = "quickly slice"
        self.value = 100
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = {"Enchantment 1": "Reliable Combo",
                        "Enchantment 1 Level": 2,
                        "Enchantment 2": None,
                        "Enchantment 2 Level": 0,
                        "Enchantment 3": None,
                        "Enchantment 3 Level": 0}

class DebugStick(Weapon):
    def __init__(self):
        self.name = "Debug Stick"
        self.description = "This Debug Stick, buit for game developers in the past, may look plain and harmless, but kills every thing with the lightest touch."
        self.damage = 9999999
        self.attack = "hack and murder"
        self.value = 999
        self.buy_value = math.ceil(self.value * 0.25) + self.value
        self.sell_value = self.value - math.ceil(self.value * 0.25)
        self.ability = {"Enchantment 1": "Instant Kill",
                        "Enchantment 1 Level": 1,
                        "Enchantment 2": None,
                        "Enchantment 2 Level": 0,
                        "Enchantment 3": None,
                        "Enchantment 3 Level": 0}
        
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
