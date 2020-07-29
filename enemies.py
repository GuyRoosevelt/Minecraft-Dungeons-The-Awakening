class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects.")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0

class Vindicator(Enemy):
    def __init__(self):
        self.name = "Vindicator"
        self.hp = 15
        self.damage = 2

class ArmoredVindicator(Enemy):
    def __init__(self):
        self.name = "Armored Vindicator"
        self.hp = 30
        self.damage = 10

class ZombieHorde(Enemy):
    def __init__(self):
        self.name = "Horde of Zombies"
        self.hp = 100
        self.damage = 4

class SkeletonWarrior(Enemy):
    def __init__(self):
        self.name = "Skeleton Warrior"
        self.hp = 80
        self.damage = 10

class RedstoneGolem(Enemy):
    def __init__(self):
        self.name = "Redstone Golem"
        self.hp = 150
        self.damage = 7