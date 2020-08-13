import math
import player
import items

class Map:
    def __init__(self):
        raise NotImplementedError("Do not create raw Map objects.")
    
#    def __str__(self):
#        return "".format()

class Squidcoast(Map):
    def __init__(self):
        self.name = "Squid Coast"
        self.description = """
                            A Village Under Attack – The village is under attack by the Arch-Illager's evil minions.
                            Someone needs to save the Villagers before it is too late!
                            """
        self.wintext = """
                           You were too late to rescue the Villagers, but don't fret.
                           They're still out there somewhere, waiting for a hero to find them.
                           """
        self.dsl = """
        |NO|NO|VT|NO|NO|
        |NO|NO|RG|NO|NO|
        |BS|EP|RC|EN|EN|
        |EP|EN|NO|TT|EN|
        |EN|NO|RC|NO|EN|
        |EN|FE|EN|NO|TT|
        |TT|NO|ST|FE|EN|
        |FE|NO|EN|NO|FE|
        """
        self.music = "Sounds\SquidCoast.mp3"
        self.objective = "Save the Villagers!"
        self.gear = {"Drop 1": "Fishing Rod",
                     "Drop 2": items.Cutlass(),
                     "Drop 3": items.Sword(),
                     "Drop 4": items.Daggers(),
                     "Drop 5": items.SoulKnife(),
                     "Drop 6": None}
