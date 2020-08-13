import math
import player
import items

class Enchantment:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enchantment objects.")
    
    def __str__(self):
        return "{} --- {}".format(self.name, self.description)
    
    def enchant(enchantment, items):
        if items.ability.get("Enchantment 1") is None:
            items.ability["Enchantment 1"] = enchantment
            items.ability["Enchantment 1 Level"] = 1
            self.slot = "Enchantment 1"
        elif items.ability.get("Enchantment 2") is None:
            items.ability["Enchantment 2"] = enchantment
            items.ability["Enchantment 2 Level"] = 1
            self.slot = "Enchantment 2"
        elif items.ability.get("Enchantment 3") is None:
            items.ability["Enchantment 3"] = enchantment
            items.ability["Enchantment 3 Level"] = 1
            self.slot = "Enchantment 3"
        else:
            self.slotlvl = str(self.slot) + "Level"
            if items.ability.get(self.slot) == enchantment and items.ability.get(self.slotlvl) == 1:
                items.ability[self.slotlvl] = items.ability[self.slotlvl] + 1
            elif items.ability.get(self.slot) == enchantment and items.ability.get(self.slotlvl) == 2:
                items.ability[self.slotlvl] = items.ability[self.slotlvl] + 1
            else:
                print("No more enchantment spots!")

class Sharpness(Weapon):
    def __init__(self):
        self.name = "Sharpness"
        self.description = """
        Boosts weapon damage.
        Level 1: 11% | Level 2: 22% | Level 3: 33%
        """
        self.enchanted = """
        Your weapon glows, as you do a incantation to boost the sharpness of your weapon.
        The light reflects off the newly razor sharp edge of your weapon.
        """
        self.strength = 1
        self.attack = "You attack does {} more damage from Sharpness!".format(self.added_damage)
    def ability(self, player):
        if items.ability.get(self.slot) == self.Sharpness() and items.ability.get(self.slotlvl) == 1:
            self.added_damage = player.damage * 0.11
            player.damage = self.added_damage + player.damage
        elif items.ability.get(self.slot) == self.Sharpness() and items.ability.get(self.slotlvl) == 2:
            self.added_damage = player.damage * 0.22
            player.damage = self.added_damage + player.damage
        elif items.ability.get(self.slot) == self.Sharpness() and items.ability.get(self.slotlvl) == 3:
            self.added_damage = player.damage * 0.33
            player.damage = self.added_damage + player.damage
        else:
            return "This weapon does not have sharpness!"

    
