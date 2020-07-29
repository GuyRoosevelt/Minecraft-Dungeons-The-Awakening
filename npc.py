import items

class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")

    def __str__(self):
        return self.name

class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
        self.emerald = 100
        self.inventory = [items.Apple(),
                          items.Apple(),
                          items.Apple(),
                          items.HealingPotion(),
                          items.HealingPotion()]

class BlackSmith(NonPlayableCharacter):
    def __init__(self):
        self.name = "Black Smith"
        self.emerald = 250
        self.inventory = [items.Sword(),
                          items.Daggers(),
                          items.SoulKnife(),
                          items.Cutlass(),
                          items.HealingPotion()]
