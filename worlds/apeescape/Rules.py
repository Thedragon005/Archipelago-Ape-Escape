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
def set_entrances(self):
    connect_regions(self, "Menu", AEDoor.TS.value, lambda state: True)
    connect_regions(self, "Menu", AEDoor.L11.value, lambda state: Keys(state, self, self.levellist[0].keys))
    connect_regions(self, "Menu", AEDoor.L12.value, lambda state: Keys(state, self, self.levellist[1].keys))
    # Add the rest of the Menu -> Level Entry connections (copy from other Rules).


# A door is defined as a connection between rooms, typically bi-directional.
def set_doors(self):
    # I'm not sure if these have to be manually connected in both directions?
    # Time Station
    connect_regions(self, AEDoor.TSR1T2.value, AEDoor.TSR2T1.value, lambda state: True)
    connect_regions(self, AEDoor.TSR2T1.value, AEDoor.TSR1T2.value, lambda state: True)
    connect_regions(self, AEDoor.TSR1T3.value, AEDoor.TSR3T1.value, lambda state: True)
    connect_regions(self, AEDoor.TSR3T1.value, AEDoor.TSR1T3.value, lambda state: True)
    # Fossil Field
    # Primordial Ooze


# A transition is defined as navigating between two doors in the same room.
def set_transitions(self):
    # Time Station
    connect_regions(self, AEDoor.TS.value, AEDoor.TSR1T2.value, lambda state: True)
    connect_regions(self, AEDoor.TS.value, AEDoor.TSR1T3.value, lambda state: True)
    # Fossil Field
    # Primordial Ooze


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
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Coin1.value,
                        lambda state: True)
    
	if self.options.mailbox == "true":
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox1.value,
                        lambda state: True)
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox2.value,
                        lambda state: True)
        connect_regions(self, AERoom.W1L1Main.value, AELocation.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))


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
    for x in range (0, 22):
        if levellist[x].entrance == 0x1E: # Always reset position of Peak Point Matrix
            levellist[x], levellist[21] = levellist[21], levellist[x]
        if levellist[x].entrance == 0x18 and (entoption == 0x01 or entoption == 0x02): # Monkey Madness
            levellist[x], levellist[20] = levellist[20], levellist[x]
        if levellist[x].entrance == 0x07 and (entoption == 0x01 or entoption == 0x03): # Stadium Attack
            levellist[x], levellist[6] = levellist[6], levellist[x]
        if levellist[x].entrance == 0x0E and (entoption == 0x01 or entoption == 0x03): # Gladiator Attack
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