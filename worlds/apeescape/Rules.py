from typing import TYPE_CHECKING

from .Regions import connect_regions, ApeEscapeLevel
from .Strings import AEItem, AEDoor, AELocation

if TYPE_CHECKING:
    from . import ApeEscapeWorld


def set_rules(world: "ApeEscapeWorld"):
    world.levellist = initialize_level_list()
    # If entrances aren't shuffled, then we don't need to shuffle the entrances.
    if (world.options.entrance != 0x00):
        world.random.shuffle(world.levellist)
        # Some levels need to be kept at a specific entrance - put those back.
        world.levellist = fixed_levels(world.levellist, world.options.entrance)
    world.levellist = set_calculated_level_data(world.levellist, world.options.unlocksperkey)
    # Make a copy of the list for passing to the client for entrance shuffle purposes. We know this list has the levels sorted in the order they'd be presented in-game (so whatever is at the Fossil Field entrance first, etc.)
    world.entranceorder = list(world.levellist)
    # If entrances weren't shuffled, then this list is already sorted. We sort the list for ease of setting up access rules in the logic files.
    if (world.options.entrance != 0x00):
        world.levellist.sort()

    set_entrances(world)
    set_doors(world)
    set_transitions(world)
    set_locations(world)


# Entrances are specifically connections between the Time Station (level select) and a level.
# If we ever want to change the starting room of a level, this is where we would set that room.
def set_entrances(self):
    connect_regions(self, "Menu", AEDoor.TS.value, lambda state: True)
    connect_regions(self, "Menu", AEDoor.L11.value, lambda state: Keys(state, self, self.levellist[0].keys))
    connect_regions(self, "Menu", AEDoor.L12.value, lambda state: Keys(state, self, self.levellist[1].keys))
    connect_regions(self, "Menu", AEDoor.L13.value, lambda state: Keys(state, self, self.levellist[2].keys))
    connect_regions(self, "Menu", AEDoor.L21.value, lambda state: Keys(state, self, self.levellist[3].keys))
    connect_regions(self, "Menu", AEDoor.L22.value, lambda state: Keys(state, self, self.levellist[4].keys))
    connect_regions(self, "Menu", AEDoor.L23.value, lambda state: Keys(state, self, self.levellist[5].keys))
    connect_regions(self, "Menu", AEDoor.L31.value, lambda state: Keys(state, self, self.levellist[6].keys))
    connect_regions(self, "Menu", AEDoor.L41.value, lambda state: Keys(state, self, self.levellist[7].keys))
    connect_regions(self, "Menu", AEDoor.L42.value, lambda state: Keys(state, self, self.levellist[8].keys))
    connect_regions(self, "Menu", AEDoor.L43.value, lambda state: Keys(state, self, self.levellist[9].keys))
    connect_regions(self, "Menu", AEDoor.L51.value, lambda state: Keys(state, self, self.levellist[10].keys))
    connect_regions(self, "Menu", AEDoor.L52.value, lambda state: Keys(state, self, self.levellist[11].keys))
    connect_regions(self, "Menu", AEDoor.L53.value, lambda state: Keys(state, self, self.levellist[12].keys))
    connect_regions(self, "Menu", AEDoor.L61.value, lambda state: Keys(state, self, self.levellist[13].keys))
    connect_regions(self, "Menu", AEDoor.L71.value, lambda state: Keys(state, self, self.levellist[14].keys))
    connect_regions(self, "Menu", AEDoor.L72.value, lambda state: Keys(state, self, self.levellist[15].keys))
    connect_regions(self, "Menu", AEDoor.L73.value, lambda state: Keys(state, self, self.levellist[16].keys))
    connect_regions(self, "Menu", AEDoor.L81.value, lambda state: Keys(state, self, self.levellist[17].keys))
    connect_regions(self, "Menu", AEDoor.L82.value, lambda state: Keys(state, self, self.levellist[18].keys))
    connect_regions(self, "Menu", AEDoor.L83.value, lambda state: Keys(state, self, self.levellist[19].keys))
    connect_regions(self, "Menu", AEDoor.L91.value, lambda state: Keys(state, self, self.levellist[20].keys))
    # TODO: Make the condition for entering Peak Point Matrix reflect the YAML settings
    connect_regions(self, "Menu", AEDoor.L92.value, lambda state: Keys(state, self, self.levellist[21].keys))


# A door is defined as a connection between rooms, typically bi-directional.
# For the logic behind door shuffle, this is the section to change.
def set_doors(self):
    # I'm not sure if these have to be manually connected in both directions? There are a few one-ways in here, so probably better to be explicit?
    # Time Station
    connect_regions(self, AEDoor.TSR1T2.value, AEDoor.TSR2T1.value, lambda state: True)
    connect_regions(self, AEDoor.TSR1T3.value, AEDoor.TSR3T1.value, lambda state: True)
    connect_regions(self, AEDoor.TSR2T1.value, AEDoor.TSR1T2.value, lambda state: True)
    connect_regions(self, AEDoor.TSR3T1.value, AEDoor.TSR1T3.value, lambda state: True)
    # Fossil Field (level contains no doors)
    # Primordial Ooze (level contains no doors)
    # Molten Lava
    connect_regions(self, AEDoor.L13R1T2.value, AEDoor.L13R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L13R1T3.value, AEDoor.L13R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L13R2T1.value, AEDoor.L13R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L13R3T1.value, AEDoor.L13R1T3.value, lambda state: True)
    # Thick Jungle
    connect_regions(self, AEDoor.L21R1T2.value, AEDoor.L21R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L21R1T3.value, AEDoor.L21R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L21R1T5.value, AEDoor.L21R5T1.value, lambda state: True)
    connect_regions(self, AEDoor.L21R2T1.value, AEDoor.L21R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L21R3T1.value, AEDoor.L21R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L21R3T4.value, AEDoor.L21R4T3.value, lambda state: True)
    connect_regions(self, AEDoor.L21R4T3.value, AEDoor.L21R3T4.value, lambda state: True)
    connect_regions(self, AEDoor.L21R4T5.value, AEDoor.L21R5T4.value, lambda state: True)
    connect_regions(self, AEDoor.L21R5T1.value, AEDoor.L21R1T5.value, lambda state: True)
    connect_regions(self, AEDoor.L21R5T4.value, AEDoor.L21R4T5.value, lambda state: True)
    # Dark Ruins
    connect_regions(self, AEDoor.L22R1T21.value, AEDoor.L22R2T11.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T22.value, AEDoor.L22R2T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T31.value, AEDoor.L22R3T11.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T32.value, AEDoor.L22R3T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T41.value, AEDoor.L22R4T11.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T42.value, AEDoor.L22R4T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R2T11.value, AEDoor.L22R1T21.value, lambda state: True)
    connect_regions(self, AEDoor.L22R2T12.value, AEDoor.L22R1T22.value, lambda state: True)
    connect_regions(self, AEDoor.L22R3T11.value, AEDoor.L22R1T31.value, lambda state: True)
    connect_regions(self, AEDoor.L22R3T12.value, AEDoor.L22R1T32.value, lambda state: True)
    connect_regions(self, AEDoor.L22R4T11.value, AEDoor.L22R1T41.value, lambda state: True)
    connect_regions(self, AEDoor.L22R4T12.value, AEDoor.L22R1T42.value, lambda state: True)
    # Cryptic Relics
    connect_regions(self, AEDoor.L23R1T2.value, AEDoor.L23R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L23R1T3.value, AEDoor.L23R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L23R2T1.value, AEDoor.L23R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L23R3T1.value, AEDoor.L23R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L23R3T4.value, AEDoor.L23R4T3.value, lambda state: True)
    connect_regions(self, AEDoor.L23R4T3.value, AEDoor.L23R3T4.value, lambda state: True)
    # Stadium Attack (level contains no doors)
    # Crabby Beach
    connect_regions(self, AEDoor.L41R1T2.value, AEDoor.L41R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L41R2T1.value, AEDoor.L41R1T2.value, lambda state: True)
    # Coral Cave
    connect_regions(self, AEDoor.L42R1T2.value, AEDoor.L42R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L42R2T1.value, AEDoor.L42R1T2.value, lambda state: True)
    # Dexter's Island
    connect_regions(self, AEDoor.L43R1T2.value, AEDoor.L43R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L43R2T1.value, AEDoor.L43R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L43R2T3.value, AEDoor.L43R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L43R3T1.value, AEDoor.L43R2T3.value, lambda state: True)
    connect_regions(self, AEDoor.L43R3T41.value, AEDoor.L43R4T31.value, lambda state: True)
    connect_regions(self, AEDoor.L43R3T42.value, AEDoor.L43R4T32.value, lambda state: True)
    connect_regions(self, AEDoor.L43R4T31.value, AEDoor.L43R3T41.value, lambda state: True)
    connect_regions(self, AEDoor.L43R4T32.value, AEDoor.L43R3T42.value, lambda state: True)
    connect_regions(self, AEDoor.L43R4T5.value, AEDoor.L43R5T4.value, lambda state: True)
    connect_regions(self, AEDoor.L43R5T4.value, AEDoor.L43R4T5.value, lambda state: True)
    # Snowy Mammoth (level contains no doors)
    # Frosty Retreat
    connect_regions(self, AEDoor.L52R1T2.value, AEDoor.L52R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L52R2T1.value, AEDoor.L52R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L52R2T3.value, AEDoor.L52R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L52R3T2.value, AEDoor.L52R2T3.value, lambda state: True)
    # Hot Springs
    connect_regions(self, AEDoor.L53R1T2.value, AEDoor.L53R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L53R1T3.value, AEDoor.L53R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L53R2T1.value, AEDoor.L53R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L53R3T1.value, AEDoor.L53R1T3.value, lambda state: True)
    # Gladiator Attack (level contains no doors)
    # Sushi Temple
    connect_regions(self, AEDoor.L71R1T2.value, AEDoor.L71R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L71R1T3.value, AEDoor.L71R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L71R2T1.value, AEDoor.L71R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L71R3T1.value, AEDoor.L71R1T3.value, lambda state: True)
    # Wabi Sabi Wall
    connect_regions(self, AEDoor.L72R1T2.value, AEDoor.L72R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L72R2T1.value, AEDoor.L72R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L72R2T3.value, AEDoor.L72R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L72R3T2.value, AEDoor.L72R2T3.value, lambda state: True)
    connect_regions(self, AEDoor.L72R3T4.value, AEDoor.L72R4T3.value, lambda state: True)
    connect_regions(self, AEDoor.L72R4T3.value, AEDoor.L72R3T4.value, lambda state: True)
    connect_regions(self, AEDoor.L72R4T5.value, AEDoor.L72R5T4.value, lambda state: True)
    connect_regions(self, AEDoor.L72R5T4.value, AEDoor.L72R4T5.value, lambda state: True)
    # Crumbling Castle
    connect_regions(self, AEDoor.L73R1T2.value, AEDoor.L73R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L73R1T3.value, AEDoor.L73R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L73R1T5.value, AEDoor.L73R5T1.value, lambda state: True)
    connect_regions(self, AEDoor.L73R1T7.value, AEDoor.L73R7T1.value, lambda state: True)
    connect_regions(self, AEDoor.L73R2T1.value, AEDoor.L73R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L73R2T3.value, AEDoor.L73R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L73R2T4.value, AEDoor.L73R4T2.value, lambda state: True)
    connect_regions(self, AEDoor.L73R3T1.value, AEDoor.L73R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L73R3T2.value, AEDoor.L73R2T3.value, lambda state: True)
    connect_regions(self, AEDoor.L73R4T2.value, AEDoor.L73R2T4.value, lambda state: True)
    connect_regions(self, AEDoor.L73R4T5.value, AEDoor.L73R5T4.value, lambda state: True)
    connect_regions(self, AEDoor.L73R5T1.value, AEDoor.L73R1T5.value, lambda state: True)
    connect_regions(self, AEDoor.L73R5T4.value, AEDoor.L73R4T5.value, lambda state: True)
    connect_regions(self, AEDoor.L73R5T61.value, AEDoor.L73R6T51.value, lambda state: True)
    connect_regions(self, AEDoor.L73R5T62.value, AEDoor.L73R6T52.value, lambda state: True)
    connect_regions(self, AEDoor.L73R6T51.value, AEDoor.L73R5T61.value, lambda state: True)
    connect_regions(self, AEDoor.L73R6T52.value, AEDoor.L73R5T62.value, lambda state: True)
    connect_regions(self, AEDoor.L73R7T1.value, AEDoor.L73R1T7.value, lambda state: True)
    # City Park
    connect_regions(self, AEDoor.L81R1T2.value, AEDoor.L81R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L81R1T3.value, AEDoor.L81R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L81R2T1.value, AEDoor.L81R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L81R2T3.value, AEDoor.L81R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L81R3T1.value, AEDoor.L81R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L81R3T2.value, AEDoor.L81R2T3.value, lambda state: True)
    # Specter's Factory
    connect_regions(self, AEDoor.L82R1T2.value, AEDoor.L82R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L82R2T1.value, AEDoor.L82R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L82R2T3.value, AEDoor.L82R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L82R2T41.value, AEDoor.L82R4T21.value, lambda state: True)
    connect_regions(self, AEDoor.L82R2T42.value, AEDoor.L82R4T22.value, lambda state: True)
    connect_regions(self, AEDoor.L82R2T5.value, AEDoor.L82R5T2.value, lambda state: True)
    connect_regions(self, AEDoor.L82R3T2.value, AEDoor.L82R2T3.value, lambda state: True)
    connect_regions(self, AEDoor.L82R4T21.value, AEDoor.L82R2T41.value, lambda state: True)
    connect_regions(self, AEDoor.L82R4T22.value, AEDoor.L82R2T42.value, lambda state: True)
    connect_regions(self, AEDoor.L82R5T2.value, AEDoor.L82R2T5.value, lambda state: True)
    connect_regions(self, AEDoor.L82R5T6.value, AEDoor.L82R6T5.value, lambda state: True)
    connect_regions(self, AEDoor.L82R6T5.value, AEDoor.L82R5T6.value, lambda state: True)
    connect_regions(self, AEDoor.L82R6T7.value, AEDoor.L82R7T6.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T6.value, AEDoor.L82R6T7.value, lambda state: True)
    # Specter's Factory Conveyor Room
    connect_regions(self, AEDoor.L82R7T71E.value, AEDoor.L82R7T71X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T72E.value, AEDoor.L82R7T71X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T73E.value, AEDoor.L82R7T72X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T74E.value, AEDoor.L82R7T73X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T75E.value, AEDoor.L82R7T74X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T76E.value, AEDoor.L82R7T75X.value, lambda state: True)
    connect_regions(self, AEDoor.L82R7T77E.value, AEDoor.L82R7T76X.value, lambda state: True)
    # TV Tower
    connect_regions(self, AEDoor.L83R1T2.value, AEDoor.L83R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L83R2T1.value, AEDoor.L83R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L83R2T3.value, AEDoor.L83R3T2.value, lambda state: True)
    connect_regions(self, AEDoor.L83R2T4.value, AEDoor.L83R4T2.value, lambda state: True)
    connect_regions(self, AEDoor.L83R3T2.value, AEDoor.L83R2T3.value, lambda state: True)
    connect_regions(self, AEDoor.L83R4T2.value, AEDoor.L83R2T4.value, lambda state: True)
    connect_regions(self, AEDoor.L83R4T5.value, AEDoor.L83R5T4.value, lambda state: True)
    connect_regions(self, AEDoor.L83R4T6.value, AEDoor.L83R6T4.value, lambda state: True)
    connect_regions(self, AEDoor.L83R5T4.value, AEDoor.L83R4T5.value, lambda state: True)
    connect_regions(self, AEDoor.L83R6T4.value, AEDoor.L83R4T6.value, lambda state: True)
    # Monkey Madness
    connect_regions(self, AEDoor.L91R1T2.value, AEDoor.L91R2T1.value, lambda state: True)
    connect_regions(self, AEDoor.L91R1T3.value, AEDoor.L91R3T1.value, lambda state: True)
    connect_regions(self, AEDoor.L91R1T4.value, AEDoor.L91R4T1.value, lambda state: True)
    connect_regions(self, AEDoor.L91R1T5.value, AEDoor.L91R5T1.value, lambda state: True)
    connect_regions(self, AEDoor.L91R1T10.value, AEDoor.L91R10T1.value, lambda state: True)
    connect_regions(self, AEDoor.L91R2T1.value, AEDoor.L91R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L91R3T1.value, AEDoor.L91R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L91R3T6E.value, AEDoor.L91R6T3X.value, lambda state: True)
    connect_regions(self, AEDoor.L91R4T1.value, AEDoor.L91R1T4.value, lambda state: True)
    connect_regions(self, AEDoor.L91R5T1.value, AEDoor.L91R1T5.value, lambda state: True)
    connect_regions(self, AEDoor.L91R6T7E.value, AEDoor.L91R7T6X.value, lambda state: True)
    connect_regions(self, AEDoor.L91R7T8E.value, AEDoor.L91R8T7X.value, lambda state: True)
    connect_regions(self, AEDoor.L91R8T9.value, AEDoor.L91R9T8.value, lambda state: True)
    connect_regions(self, AEDoor.L91R9T3E.value, AEDoor.L91R3T9X.value, lambda state: True)
    connect_regions(self, AEDoor.L91R9T8.value, AEDoor.L91R8T9.value, lambda state: True)
    connect_regions(self, AEDoor.L91R10T1.value, AEDoor.L91R1T10.value, lambda state: True)
    connect_regions(self, AEDoor.L91R10T11.value, AEDoor.L91R11T10.value, lambda state: True)
    connect_regions(self, AEDoor.L91R11T10.value, AEDoor.L91R10T11.value, lambda state: True)
    connect_regions(self, AEDoor.L91R11T12.value, AEDoor.L91R12T11.value, lambda state: True)
    connect_regions(self, AEDoor.L91R11T13.value, AEDoor.L91R13T11.value, lambda state: True)
    connect_regions(self, AEDoor.L91R12T11.value, AEDoor.L91R11T12.value, lambda state: True)
    connect_regions(self, AEDoor.L91R13T11.value, AEDoor.L91R11T13.value, lambda state: True)
    connect_regions(self, AEDoor.L91R13T14.value, AEDoor.L91R14T13.value, lambda state: True)
    connect_regions(self, AEDoor.L91R13T15.value, AEDoor.L91R15T13.value, lambda state: True)
    connect_regions(self, AEDoor.L91R13T17E.value, AEDoor.L91R17T13X.value, lambda state: True)
    connect_regions(self, AEDoor.L91R14T13.value, AEDoor.L91R13T14.value, lambda state: True)
    connect_regions(self, AEDoor.L91R15T13.value, AEDoor.L91R13T15.value, lambda state: True)
    connect_regions(self, AEDoor.L91R15T16.value, AEDoor.L91R16T15.value, lambda state: True)
    connect_regions(self, AEDoor.L91R16T15.value, AEDoor.L91R15T16.value, lambda state: True)
    connect_regions(self, AEDoor.L91R16T13E.value, AEDoor.L91R13T16X.value, lambda state: True)
    # Peak Point Matrix (level contains no doors)


# A transition is defined as navigating between two doors in the same room.
def set_transitions(self):
    # I'm not sure if these have to be manually connected in both directions? I think they do because connections are asymmetric.
    # Time Station
    connect_regions(self, AEDoor.TS.value, AEDoor.TSR1T2.value, lambda state: True)
    connect_regions(self, AEDoor.TS.value, AEDoor.TSR1T3.value, lambda state: True)
    connect_regions(self, AEDoor.TSR1T2.value, AEDoor.TS.value, lambda state: True)
    connect_regions(self, AEDoor.TSR1T3.value, AEDoor.TS.value, lambda state: True)

    # Fossil Field (level contains a single room)
    # Primordial Ooze (level contains a single room)
    # Molten Lava
    connect_regions(self, AEDoor.L13.value, AEDoor.L13R1T2.value, lambda state: True)
    connect_regions(self, AEDoor.L13.value, AEDoor.L13R1T3.value, lambda state: True)
    connect_regions(self, AEDoor.L13R1T2.value, AEDoor.L13.value, lambda state: True)
    connect_regions(self, AEDoor.L13R1T3.value, AEDoor.L13.value, lambda state: True)

    # Thick Jungle
    # Entry Room
    connect_regions(self, AEDoor.L21.value, AEDoor.L21R1T2.value, lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.L21.value, AEDoor.L21R1T3.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.L21.value, AEDoor.L21R1T3.value, 
                        lambda state: CanSwim(state, self) or ((IJ(state, self) or HasHoop(state, self)) and HasFlyer(state, self)))
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21.value, AEDoor.L21R1T5.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.L21.value, AEDoor.L21R1T5.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.L21R1T2.value, AEDoor.L21.value, lambda state: True)
    connect_regions(self, AEDoor.L21R1T3.value, AEDoor.L21.value, 
                        lambda state: CanDive(state, self))
    connect_regions(self, AEDoor.L21R1T5.value, AEDoor.L21.value, 
                        lambda state: CanSwim(state, self))
    # Mushroom Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21R2T1.value, AEDoor.L21R2HELP.value, 
                        lambda state: HasFlyer(state, self) and CanHitWheel(state, self))
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.L21R2T1.value, AEDoor.L21R2HELP.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or (HasFlyer(state, self) and CanHitWheel(state, self))))
    else:
        connect_regions(self, AEDoor.L21R2T1.value, AEDoor.L21R2HELP.value, 
                        lambda state: IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    # Fish Room   TODO: FILL OUT THE ACTUAL LOGIC BELOW THIS POINT (can copy/paste + find/replace)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.L21R3T1.value, AEDoor.L21R3HELP.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R3T1.value, AEDoor.L21R3HELP.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21R3T4.value, AEDoor.L21R3HELP.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R3T4.value, AEDoor.L21R3HELP.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L21R3HELP.value, AEDoor.L21R3T1.value, lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.L21R3HELP.value, AEDoor.L21R3T4.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R3HELP.value, AEDoor.L21R3T4.value, 
                        lambda state: TODO)    
    # Tent/Vine Room
    connect_regions(self, AEDoor.L21R4T3.value, AEDoor.L21R4T5.value, lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21R4T5.value, AEDoor.L21R4T3.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.L21R4T5.value, AEDoor.L21R4T3.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R4T5.value, AEDoor.L21R4T3.value, 
                        lambda state: TODO)
    # Boulder Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21R5T1.value, AEDoor.L21R5T4.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.L21R5T1.value, AEDoor.L21R5T4.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R5T1.value, AEDoor.L21R5T4.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L21R5T4.value, AEDoor.L21R5T1.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L21R5T4.value, AEDoor.L21R5T1.value, 
                        lambda state: TODO)    

    # Dark Ruins
    # Outside
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T21.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T21.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T21.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T22.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T31.value, lambda state: True)
    connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T32.value, 
                        lambda state: TODO) # CREATES EVENT ITEM (pushing the block)
    connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T41.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T42.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L22.value, AEDoor.L22R1T42.value, 
                        lambda state: TODO)        
    connect_regions(self, AEDoor.L22R1T21.value, AEDoor.L22.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T22.value, AEDoor.L22.value, 
                        lambda state: TODO) # NEEDS EVENT ITEM (pushing the block)
    connect_regions(self, AEDoor.L22R1T31.value, AEDoor.L22.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T32.value, AEDoor.L22.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T41.value, AEDoor.L22.value, lambda state: True)
    connect_regions(self, AEDoor.L22R1T42.value, AEDoor.L22.value, lambda state: True)
    # Fan Basement
    connect_regions(self, AEDoor.L22R2T11.value, AEDoor.L22R2T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R2T12.value, AEDoor.L22R2T11.value, lambda state: True)
    # Obelisk
    connect_regions(self, AEDoor.L22R3T11.value, AEDoor.L22R3T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R3T12.value, AEDoor.L22R3T11.value, lambda state: True)
    # Water Basement
    connect_regions(self, AEDoor.L22R4T11.value, AEDoor.L22R4T12.value, lambda state: True)
    connect_regions(self, AEDoor.L22R4T12.value, AEDoor.L22R4T11.value, lambda state: True)

    # Cryptic Relics
    # Entry Area
    connect_regions(self, AEDoor.L23.value, AEDoor.L23R1HELP.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L23R1T2.value, AEDoor.L23R1HELP.value, lambda state: True)
    connect_regions(self, AEDoor.L23R1T3.value, AEDoor.L23R1HELP.value, lambda state: True)
    connect_regions(self, AEDoor.L23R1HELP.value, AEDoor.L23R1T2.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L23R1HELP.value, AEDoor.L23R1T3.value, 
                        lambda state: TODO)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.L23R1HELP.value, AEDoor.L23.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.L23R1HELP.value, AEDoor.L23.value, 
                        lambda state: TODO)	
    # Relics
    connect_regions(self, AEDoor.L23R3T1.value, AEDoor.L23R3T4.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L23R3T4.value, AEDoor.L23R3T1.value, 
                        lambda state: TODO)

    # Stadium Attack (level contains a single room)
    # Crabby Beach
    connect_regions(self, AEDoor.L41.value, AEDoor.L41R1T2.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L41R1T2.value, AEDoor.L41.value, lambda state: True)

    # Coral Cave
    connect_regions(self, AEDoor.L42.value, AEDoor.L42R1T2.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.L42R1T2.value, AEDoor.L42.value, 
                        lambda state: TODO)

    # Dexter's Island
    # Snowy Mammoth (level contains a single room)
    # Frosty Retreat
    # Hot Springs
    # Gladiator Attack (level contains a single room)
    # Sushi Temple
    # Wabi Sabi Wall
    # Crumbling Castle
    # City Park
    # Specter's Factory
    # TV Tower
    # Monkey Madness
    # Peak Point Matrix (level contains a single room)



# A location is always accessed from a transition. The level entrance is a special case of a transition.
def set_locations(self):
    # Time Station
    if self.options.mailbox == "true" or (self.options.shufflenet == "true" and self.options.coin == "true"):
        connect_regions(self, AEDoor.TS.value, AELocation.Mailbox60.value, lambda state: True)
        connect_regions(self, AEDoor.TS.value, AELocation.Mailbox61.value, lambda state: True)
        connect_regions(self, AEDoor.TSR3T1.value, AELocation.Mailbox62.value, lambda state: True)
        connect_regions(self, AEDoor.TSR2T1.value, AELocation.Mailbox63.value, lambda state: True)

    # Fossil Field
    connect_regions(self, AEDoor.L11.value, AELocation.W1L1Noonan.value, lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.L11.value, AELocation.W1L1Jorjy.value, lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.L11.value, AELocation.W1L1Nati.value, lambda state: HasNet(state, self))
    if self.options.logic == "normal":
       connect_regions(self, AEDoor.L11.value, AELocation.W1L1TrayC.value,
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
       connect_regions(self, AEDoor.L11.value, AELocation.W1L1TrayC.value,
                        lambda state: HasNet(state, self))

    if self.options.coin == "true":
        connect_regions(self, AEDoor.L11.value, AELocation.Coin1.value,
                        lambda state: True)
    
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.L11.value, AELocation.Mailbox1.value,
                        lambda state: True)
        connect_regions(self, AEDoor.L11.value, AELocation.Mailbox2.value,
                        lambda state: True)
        connect_regions(self, AEDoor.L11.value, AELocation.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))
    
    # Primordial Ooze
    # Molten Lava
    # Thick Jungle
    # Dark Ruins
    # Cryptic Relics
    # Stadium Attack
    # Crabby Beach
    # Coral Cave
    # Dexter's Island
    # Snowy Mammoth
    # Frosty Retreat
    # Hot Springs
    # Gladiator Attack
    # Sushi Temple
    # Wabi Sabi Wall
    # Crumbling Castle
    # City Park
    # Specter's Factory
    # TV Tower
    # Monkey Madness
    # Peak Point Matrix


# Item Checking Helper Functions
def Keys(state, world, count):
    return state.has(AEItem.Key.value, world.player, count)


def HasClub(state, world):
    return state.has(AEItem.Club.value, world.player, 1)


def HasNet(state, world):
    return state.has(AEItem.Net.value, world.player, 1)


def HasRadar(state, world):
    return state.has(AEItem.Radar.value, world.player, 1)


def HasSling(state, world):
    return state.has(AEItem.Sling.value, world.player, 1)


def HasHoop(state, world):
    return state.has(AEItem.Hoop.value, world.player, 1)


def HasFlyer(state, world):
    return state.has(AEItem.Flyer.value, world.player, 1)


def HasRC(state, world):
    return state.has(AEItem.Car.value, world.player, 1)


def HasPunch(state, world):
    return state.has(AEItem.Punch.value, world.player, 1)


def HasWaterNet(state, world):
    return CanWaterCatch(state, world)


def CanSwim(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 1))


def CanDive(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 2))


# Logic Helper Functions
def CanWaterCatch(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or (state.has(AEItem.WaterCatch.value, world.player, 1) and state.has(AEItem.ProgWaterNet.value, world.player, 1)))


def CanHitOnce(state, world):
    return HasClub(state, world) or HasRadar(state, world) or HasSling(state, world) or HasHoop(state, world) or HasFlyer(state, world) or HasRC(state, world) or HasPunch(state, world)


def CanHitMultiple(state, world):
    if world.options.logic == "normal":
        return HasClub(state, world) or HasSling(state, world) or HasPunch(state, world)
    else:
        return HasClub(state, world) or HasSling(state, world) or HasHoop(state, world) or HasPunch(state, world)


def CanHitWheel(state, world):
    if world.options.logic == "normal" or world.options.logic == "hard":
        return CanHitMultiple(state, world)
    else:
        return CanHitMultiple(state, world) or HasFlyer(state, world) or HasRC(state, world)


# TODO: Pass in a specific region here
def SuperFlyer(state, world):
    # If the option is off, Super Flyer is not in logic.
    if world.options.superflyer == "false":
        return False

    # If the difficulty is normal, Super Flyer is never in logic.
    if world.options.logic == "normal":
        return False

    # If the player does not have the required gadgets, Super Flyer is unavailable.
    if (HasFlyer(state, world) and (HasNet(state, world) or HasClub(state, world) or HasSling(state, world) or HasPunch(state,world))) == False:
        return False

    # If the player can reach this location without activating the Flyer, Super Flyer is available. To check for this, we check for the ability to access this region on a modified CollectionState. The Radar conveniently has the same ground pound properties as the Flyer while introducing no new access, and so replacing the Flyer with the Radar in this state serves as a valid check.
    # TODO: actually implement the above description LOL (right now placement could expect two Super Flyers)
    return True


def IJ(state, world):
    return HasSling(state, world) and world.options.infinitejump == "true"


# Lamp and Door Functions
def MM_DoubleDoor(state, world):
    return state.has(AEItem.MMDoubleDoorKey.value, world.player, 1)


# TODO: All logic around lamps with event items.
def CB_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.CB_Lamp.value, world.player, 1)


def DI_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.DI_Lamp.value, world.player, 1)


def CRC_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.CrC_Lamp.value, world.player, 1)


def CP_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.CP_Lamp.value, world.player, 1)


def SF_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.SF_Lamp.value, world.player, 1)


def TVT_Lobby_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.TVT_Lobby_Lamp.value, world.player, 1)


def TVT_Tank_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.TVT_Tank_Lamp.value, world.player, 1)


def MM_Lamp(state, world):
    # Check for the state of the option. If lamps are shuffled, return what's written. Else, check for X monkey events in the level.
    return state.has(AEItem.MM_Lamp.value, world.player, 1)


# Entrance Shuffle Helper Functions
def initialize_level_list():
    levelnames = ["Fossil Field", "Primordial Ooze", "Molten Lava", "Thick Jungle", "Dark Ruins", "Cryptic Relics", "Stadium Attack", "Crabby Beach", "Coral Cave", "Dexter's Island", "Snowy Mammoth", "Frosty Retreat", "Hot Springs", "Gladiator Attack", "Sushi Temple", "Wabi Sabi Wall", "Crumbling Castle", "City Park", "Specter's Factory", "TV Tower", "Monkey Madness", "Peak Point Matrix"]
    levelids = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x14, 0x15, 0x16, 0x18, 0x1E]
    levellist = []
    for x in range (0, 22):
        levellist.append(ApeEscapeLevel(levelnames[x], levelids[x], x))
    return levellist


def level_to_bytes(name):
    bytelist = []
    for x in name:
        bytelist.append(character_lookup(x))
    return bytelist


def character_lookup(byte):
    if byte.isspace():  # Space
        return 255
    if byte.isalpha():
        return ord(byte) - 49  # Both uppercase and lowercase letters
    if byte.isdecimal():
        if int(byte) < 6:
            return ord(byte) + 56  # 0-5
        else:
            return ord(byte) + 68  # 6-9
    if ord(byte) == 39:  # Single apostrophe
        return 187


def fixed_levels(levellist, entoption):
    # Always reset position of Peak Point Matrix
    for x in range (0, 22):
        if levellist[x].entrance == 0x1E:
            levellist[x], levellist[21] = levellist[21], levellist[x]
    # Reset position of Monkey Madness if the option requires it
    if entoption == 0x01 or entoption == 0x02:
        for x in range (0, 22):
            if levellist[x].entrance == 0x18 
                levellist[x], levellist[20] = levellist[20], levellist[x]
    # Reset position of races if the option requires it
    if entoption == 0x01 or entoption == 0x03:
        for x in range (0, 22):
            if levellist[x].entrance == 0x07: # Stadium Attack
                levellist[x], levellist[6] = levellist[6], levellist[x]
        for x in range (0, 22):
            if levellist[x].entrance == 0x0E: # Gladiator Attack
                levellist[x], levellist[13] = levellist[13], levellist[x]
    return levellist


def set_calculated_level_data(levellist, keyoption):
    reqkeys = get_required_keys(keyoption)
    for x in range (0, 22):
        levellist[x].bytes = level_to_bytes(levellist[x].name)
        levellist[x].keys = reqkeys[x]
        levellist[x].newpos = x
    return levellist


def get_required_keys(option):
    if option == 0x00:  # world
        return [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6]
    if option == 0x01:  # world and races
        return [0, 0, 0, 1, 1, 1, 2, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8]
    if option == 0x02:  # level
        return [0, 0, 0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 16, 16]
    if option == 0x03:  # level and races
        return [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 18]