from typing import TYPE_CHECKING

from .Regions import ApeEscapeLevel
from .RulesGlitchless import set_glitchless_rules
from .RulesNoIJ import set_noij_rules
from .RulesIJ import set_ij_rules
# from .Regions import connect_regions
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

    if world.options.logic == "glitchless":
        set_glitchless_rules(world)
    elif world.options.logic == "noij":
        set_noij_rules(world)
    elif world.options.logic == "ij":
        set_ij_rules(world)


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
    for x in range (0, 22): # Always reset position of Peak Point Matrix
        if levellist[x].entrance == 0x1E:
            levellist[x], levellist[21] = levellist[21], levellist[x]
    if entoption == 0x01 or entoption == 0x02: # Monkey Madness, if it's not moved
        for x in range (0, 22):
            if levellist[x].entrance == 0x18:
                levellist[x], levellist[20] = levellist[20], levellist[x]
    if entoption == 0x01 or entoption == 0x03: # Stadium Attack and Gladiator Attack, if races aren't moved
        for x in range (0, 22):
            if levellist[x].entrance == 0x07:
                levellist[x], levellist[6] = levellist[6], levellist[x]
        for x in range (0, 22):
            if levellist[x].entrance == 0x0E:
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