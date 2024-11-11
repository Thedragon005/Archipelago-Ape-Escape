from typing import TYPE_CHECKING

from .Entrances import initialize_level_list, fixed_levels, set_calculated_level_data
from .RulesGlitchless import set_glitchless_rules
from .RulesNoIJ import set_noij_rules
from .RulesIJ import set_ij_rules
from .Regions import connect_regions, ApeEscapeLevel
if TYPE_CHECKING:
    from . import ApeEscapeWorld


def set_rules(world: "ApeEscapeWorld"):
    world.levellist = initialize_level_list()
    # self.levellist = initialize_level_list()
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