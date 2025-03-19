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
    connect_regions(self, "Menu", AEDoor.TIME_ENTRY.value, lambda state: True)
    connect_regions(self, "Menu", AEDoor.FF_ENTRY.value, lambda state: Keys(state, self, self.levellist[0].keys))
    connect_regions(self, "Menu", AEDoor.PO_ENTRY.value, lambda state: Keys(state, self, self.levellist[1].keys))
    connect_regions(self, "Menu", AEDoor.ML_ENTRY.value, lambda state: Keys(state, self, self.levellist[2].keys))
    connect_regions(self, "Menu", AEDoor.TJ_ENTRY.value, lambda state: Keys(state, self, self.levellist[3].keys))
    connect_regions(self, "Menu", AEDoor.DR_ENTRY.value, lambda state: Keys(state, self, self.levellist[4].keys))
    connect_regions(self, "Menu", AEDoor.CR_ENTRY.value, lambda state: Keys(state, self, self.levellist[5].keys))
    connect_regions(self, "Menu", AEDoor.SA_ENTRY.value, lambda state: Keys(state, self, self.levellist[6].keys))
    connect_regions(self, "Menu", AEDoor.CB_ENTRY.value, lambda state: Keys(state, self, self.levellist[7].keys))
    connect_regions(self, "Menu", AEDoor.CCAVE_ENTRY.value, lambda state: Keys(state, self, self.levellist[8].keys))
    connect_regions(self, "Menu", AEDoor.DI_ENTRY.value, lambda state: Keys(state, self, self.levellist[9].keys))
    connect_regions(self, "Menu", AEDoor.SM_ENTRY.value, lambda state: Keys(state, self, self.levellist[10].keys))
    connect_regions(self, "Menu", AEDoor.FR_ENTRY.value, lambda state: Keys(state, self, self.levellist[11].keys))
    connect_regions(self, "Menu", AEDoor.HS_ENTRY.value, lambda state: Keys(state, self, self.levellist[12].keys))
    connect_regions(self, "Menu", AEDoor.GA_ENTRY.value, lambda state: Keys(state, self, self.levellist[13].keys))
    connect_regions(self, "Menu", AEDoor.ST_ENTRY.value, lambda state: Keys(state, self, self.levellist[14].keys))
    connect_regions(self, "Menu", AEDoor.WSW_ENTRY.value, lambda state: Keys(state, self, self.levellist[15].keys))
    connect_regions(self, "Menu", AEDoor.CC_ENTRY.value, lambda state: Keys(state, self, self.levellist[16].keys))
    connect_regions(self, "Menu", AEDoor.CP_ENTRY.value, lambda state: Keys(state, self, self.levellist[17].keys))
    connect_regions(self, "Menu", AEDoor.SF_ENTRY.value, lambda state: Keys(state, self, self.levellist[18].keys))
    connect_regions(self, "Menu", AEDoor.TVT_ENTRY.value, lambda state: Keys(state, self, self.levellist[19].keys))
    connect_regions(self, "Menu", AEDoor.MM_SL_HUB.value, lambda state: Keys(state, self, self.levellist[20].keys))
    # TODO: Make the condition for entering Peak Point Matrix reflect the YAML settings
    connect_regions(self, "Menu", AEDoor.PPM_ENTRY.value, lambda state: Keys(state, self, self.levellist[21].keys))


# A door is defined as a connection between rooms, typically bi-directional.
# For the logic behind door shuffle, this is the section to change.
def set_doors(self):
    # I'm not sure if these have to be manually connected in both directions? There are a few one-ways in here, so probably better to be explicit?
    # Time Station
    connect_regions(self, AEDoor.TIME_MAIN_TRAINING.value, AEDoor.TIME_TRAINING_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_MINIGAME.value, AEDoor.TIME_MINIGAME_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_TRAINING_MAIN.value, AEDoor.TIME_MAIN_TRAINING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MINIGAME_MAIN.value, AEDoor.TIME_MAIN_MINIGAME.value,
                        lambda state: True)
    # Fossil Field (level contains no doors)
    # Primordial Ooze (level contains no doors)
    # Molten Lava
    connect_regions(self, AEDoor.ML_ENTRY_VOLCANO.value, AEDoor.ML_VOLCANO_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_TRICERATOPS.value, AEDoor.ML_TRICERATOPS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AEDoor.ML_ENTRY_VOLCANO.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AEDoor.ML_ENTRY_TRICERATOPS.value,
                        lambda state: True)
    # Thick Jungle
    connect_regions(self, AEDoor.TJ_ENTRY_MUSHROOM.value, AEDoor.TJ_MUSHROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_FISH.value, AEDoor.TJ_FISH_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_BOULDER.value, AEDoor.TJ_BOULDER_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_ENTRY_MUSHROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_TENT_FISH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_TENT_FISH.value, AEDoor.TJ_FISH_TENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_BOULDER_TENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_TENT_BOULDER.value,
                        lambda state: True)
    # Dark Ruins
    connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AEDoor.DR_FAN_OUTSIDE_FENCE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_HOLE.value, AEDoor.DR_FAN_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value, AEDoor.DR_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AEDoor.DR_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, AEDoor.DR_WATER_SIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, AEDoor.DR_WATER_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_FENCE.value, AEDoor.DR_OUTSIDE_FENCE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AEDoor.DR_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_TOP.value, AEDoor.DR_OUTSIDE_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_SIDE.value, AEDoor.DR_OUTSIDE_WATER_BUTTON.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_LEDGE.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value,
                        lambda state: True)
    # Cryptic Relics
    connect_regions(self, AEDoor.CR_ENTRY_SIDE_ROOM.value, AEDoor.CR_SIDE_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_ENTRY_MAIN_RUINS.value, AEDoor.CR_MAIN_RUINS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_SIDE_ROOM_ENTRY.value, AEDoor.CR_ENTRY_SIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_MAIN_RUINS_ENTRY.value, AEDoor.CR_ENTRY_MAIN_RUINS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value,
                        lambda state: True)
    # Stadium Attack (level contains no doors)
    # Crabby Beach
    connect_regions(self, AEDoor.CB_ENTRY_SECOND_ROOM.value, AEDoor.CB_SECOND_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AEDoor.CB_ENTRY_SECOND_ROOM.value,
                        lambda state: True)
    # Coral Cave
    connect_regions(self, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value,
                        lambda state: True)
    # Dexter's Island
    connect_regions(self, AEDoor.DI_ENTRY_STOMACH.value, AEDoor.DI_STOMACH_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AEDoor.DI_ENTRY_STOMACH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_SLIDE_ROOM.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_STOMACH_SLIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERY_TENTACLE.value, AEDoor.DI_TENTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_TENTACLE.value, AEDoor.DI_GALLERY_TENTACLE.value,
                        lambda state: True)
    # Snowy Mammoth (level contains no doors)
    # Frosty Retreat
    connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AEDoor.FR_CAVERNS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AEDoor.FR_WATER_CAVERNS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AEDoor.FR_CAVERNS_WATER.value,
                        lambda state: True)
    # Hot Springs
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AEDoor.HS_HOT_SPRING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value, AEDoor.HS_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_HOT_SPRING.value, AEDoor.HS_ENTRY_HOT_SPRING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    # Gladiator Attack (level contains no doors)
    # Sushi Temple
    connect_regions(self, AEDoor.ST_ENTRY_TEMPLE.value, AEDoor.ST_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_WELL.value, AEDoor.ST_WELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_TEMPLE.value, AEDoor.ST_ENTRY_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_WELL.value, AEDoor.ST_ENTRY_WELL.value,
                        lambda state: True)
    # Wabi Sabi Wall
    connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AEDoor.WSW_GONG_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_ENTRY_GONG.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_GONG_MIDDLE.value, AEDoor.WSW_MIDDLE_GONG.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_GONG_MIDDLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AEDoor.WSW_OBSTACLE_MIDDLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_MIDDLE_OBSTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_OBSTACLE_BARREL.value, AEDoor.WSW_BARREL_OBSTACLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AEDoor.WSW_OBSTACLE_BARREL.value,
                        lambda state: True)
    # Crumbling Castle
    connect_regions(self, AEDoor.CC_ENTRY_CASTLE.value, AEDoor.CC_CASTLEMAIN_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_BELL_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BASEMENT.value, AEDoor.CC_BASEMENT_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BOSS.value, AEDoor.CC_BOSS_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_ENTRY_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_BELL.value, AEDoor.CC_BELL_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_ELEVATOR_CASTLEMAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AEDoor.CC_ENTRY_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BELL_CASTLE.value, AEDoor.CC_CASTLEMAIN_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ELEVATOR_BASEMENT.value, AEDoor.CC_BASEMENT_ELEVATOR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_ELEVATOR_BASEMENT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BUTTON_BASEMENT_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_UP.value, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value, AEDoor.CC_BASEMENT_BUTTON_UP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BOSS_ROOM.value, AEDoor.CC_ENTRY_BOSS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AEDoor.CP_BARREL_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_BARREL_SEWERS_FRONT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARREL_OUTSIDE.value, AEDoor.CP_OUTSIDE_BARREL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AEDoor.CP_SEWERSFRONT_BARREL.value,
                        lambda state: True)
    # Specter's Factory
    connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AEDoor.SF_FACTORY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_OUTSIDE.value, AEDoor.SF_OUTSIDE_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_RC_CAR_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_WHEEL_FACTORY_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_MECH.value, AEDoor.SF_MECH_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_TOP.value, AEDoor.SF_FACTORY_WHEEL_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AEDoor.SF_FACTORY_MECH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_LAVA.value, AEDoor.SF_LAVA_MECH.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_MECH_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_LAVA_CONVEYOR.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_LAVA_CONVEYOR.value,
                        lambda state: True)
    # Specter's Factory Conveyor Room
    connect_regions(self, AEDoor.SF_CONVEYOR1_ENTRY.value, AEDoor.SF_CONVEYOR1_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR2_ENTRY.value, AEDoor.SF_CONVEYOR1_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR3_ENTRY.value, AEDoor.SF_CONVEYOR2_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR4_ENTRY.value, AEDoor.SF_CONVEYOR3_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR5_ENTRY.value, AEDoor.SF_CONVEYOR4_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR6_ENTRY.value, AEDoor.SF_CONVEYOR5_EXIT.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR7_ENTRY.value, AEDoor.SF_CONVEYOR6_EXIT.value,
                        lambda state: True)
    # TV Tower
    connect_regions(self, AEDoor.TVT_OUTSIDE_LOBBY.value, AEDoor.TVT_LOBBY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_OUTSIDE_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_WATER.value, AEDoor.TVT_WATER_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_LOBBY_TANK.value, AEDoor.TVT_TANK_LOBBY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AEDoor.TVT_LOBBY_WATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_LOBBY_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_FAN_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_BOSS.value, AEDoor.TVT_BOSS_TANK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_FAN_TANK.value, AEDoor.TVT_TANK_FAN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_BOSS_TANK.value, AEDoor.TVT_TANK_BOSS.value,
                        lambda state: True)
    # Monkey Madness
    connect_regions(self, AEDoor.MM_SL_HUB_WESTERN.value, AEDoor.MM_WESTERN_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_COASTER.value, AEDoor.MM_COASTER_ENTRY_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CIRCUS.value, AEDoor.MM_CIRCUS_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_GO_KARZ.value, AEDoor.MM_GO_KARZ_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CRATER.value, AEDoor.MM_CRATER_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AEDoor.MM_SL_HUB_WESTERN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AEDoor.MM_SL_HUB_COASTER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_COASTER1.value, AEDoor.MM_COASTER1_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CIRCUS_SL_HUB.value, AEDoor.MM_SL_HUB_CIRCUS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_GO_KARZ_SL_HUB.value, AEDoor.MM_SL_HUB_GO_KARZ.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER1_COASTER2.value, AEDoor.MM_COASTER2_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER2_HAUNTED_HOUSE.value, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COFFIN_COASTER_ENTRY.value, AEDoor.MM_COASTER_ENTRY_DISEMBARK.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AEDoor.MM_SL_HUB_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, AEDoor.MM_SPECTER1_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value,
                        lambda state: True)


# A transition is defined as navigating between two doors in the same room.
def set_transitions(self):
    # I'm not sure if these have to be manually connected in both directions? I think they do because connections are asymmetric.
    # Time Station
    connect_regions(self, AEDoor.TIME_ENTRY.value, AEDoor.TIME_MAIN_TRAINING.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_ENTRY.value, AEDoor.TIME_MAIN_MINIGAME.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_TRAINING.value, AEDoor.TIME_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TIME_MAIN_MINIGAME.value, AEDoor.TIME_ENTRY.value,
                        lambda state: True)

    # Fossil Field (level contains a single room)
    # Primordial Ooze (level contains a single room)
    # Molten Lava
    connect_regions(self, AEDoor.ML_ENTRY.value, AEDoor.ML_ENTRY_VOLCANO.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY.value, AEDoor.ML_ENTRY_TRICERATOPS.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_VOLCANO.value, AEDoor.ML_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ML_ENTRY_TRICERATOPS.value, AEDoor.ML_ENTRY.value,
                        lambda state: True)

    # Thick Jungle
    # Entry Room
    connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_MUSHROOM.value,
                        lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_FISH.value, 
                        lambda state: CanSwim(state, self) or ((IJ(state, self) or HasHoop(state, self)) and HasFlyer(state, self)))
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value, 
                        lambda state: CanSwim(state, self))
    else:
        connect_regions(self, AEDoor.TJ_ENTRY.value, AEDoor.TJ_ENTRY_BOULDER.value, 
                        lambda state: CanSwim(state, self) or HasFlyer(state, self))
    connect_regions(self, AEDoor.TJ_ENTRY_MUSHROOM.value, AEDoor.TJ_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TJ_ENTRY_FISH.value, AEDoor.TJ_ENTRY.value, 
                        lambda state: CanDive(state, self))
    connect_regions(self, AEDoor.TJ_ENTRY_BOULDER.value, AEDoor.TJ_ENTRY.value, 
                        lambda state: CanSwim(state, self))
    # Mushroom Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: HasFlyer(state, self) and CanHitWheel(state, self))
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: (IJ(state, self) or HasHoop(state, self) or (HasFlyer(state, self) and CanHitWheel(state, self))))
    else:
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AEDoor.TJ_MUSHROOMMAIN.value, 
                        lambda state: IJ(state, self) or HasHoop(state, self) or HasFlyer(state, self))
    # Fish Room
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_FISH_ENTRY.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_FISH_TENT.value, AEDoor.TJ_FISHBOAT.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_ENTRY.value,
                        lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_TENT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AEDoor.TJ_FISH_TENT.value, 
                        lambda state: TODO)
    # Tent/Vine Room
    connect_regions(self, AEDoor.TJ_TENT_FISH.value, AEDoor.TJ_TENT_BOULDER.value,
                        lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AEDoor.TJ_TENT_FISH.value, 
                        lambda state: TODO)
    # Boulder Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_BOULDER_TENT.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_BOULDER_TENT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_ENTRY.value, AEDoor.TJ_BOULDER_TENT.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_BOULDER_ENTRY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AEDoor.TJ_BOULDER_ENTRY.value, 
                        lambda state: TODO)

    # Dark Ruins
    # Outside
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_FENCE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_HOLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, 
                        lambda state: TODO)
    self.__add_event_location(self.L22R1T32, "Dark Ruins - Floor Broken", "DR-Block") # Event Item
    connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.DR_ENTRY.value, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_HOLE.value, AEDoor.DR_ENTRY.value, 
                        lambda state: state.has("DR-Block", self.player, 1))
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_OBELISK_TOP.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_BUTTON.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OUTSIDE_WATER_LEDGE.value, AEDoor.DR_ENTRY.value,
                        lambda state: True)
    # Fan Basement
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_FENCE.value, AEDoor.DR_FAN_OUTSIDE_HOLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AEDoor.DR_FAN_OUTSIDE_FENCE.value,
                        lambda state: True)
    # Obelisk
    connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AEDoor.DR_OBELISK_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_OBELISK_TOP.value, AEDoor.DR_OBELISK_BOTTOM.value,
                        lambda state: True)
    # Water Basement
    connect_regions(self, AEDoor.DR_WATER_SIDE.value, AEDoor.DR_WATER_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DR_WATER_LEDGE.value, AEDoor.DR_WATER_SIDE.value,
                        lambda state: True)

    # Cryptic Relics
    # Entry Area
    connect_regions(self, AEDoor.CR_ENTRY.value, AEDoor.CR_CR_ENTRYOBA.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CR_ENTRY_SIDE_ROOM.value, AEDoor.CR_CR_ENTRYOBA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_ENTRY_MAIN_RUINS.value, AEDoor.CR_CR_ENTRYOBA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CR_CR_ENTRYOBA.value, AEDoor.CR_ENTRY_SIDE_ROOM.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CR_CR_ENTRYOBA.value, AEDoor.CR_ENTRY_MAIN_RUINS.value, 
                        lambda state: TODO)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.CR_CR_ENTRYOBA.value, AEDoor.CR_ENTRY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CR_CR_ENTRYOBA.value, AEDoor.CR_ENTRY.value, 
                        lambda state: TODO)
    # Relics
    connect_regions(self, AEDoor.CR_MAIN_RUINS_ENTRY.value, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AEDoor.CR_MAIN_RUINS_ENTRY.value, 
                        lambda state: TODO)

    # Stadium Attack (level contains a single room)
    # Crabby Beach
    connect_regions(self, AEDoor.CB_ENTRY.value, AEDoor.CB_ENTRY_SECOND_ROOM.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CB_ENTRY_SECOND_ROOM.value, AEDoor.CB_ENTRY.value,
                        lambda state: True)

    # Coral Cave
    connect_regions(self, AEDoor.CCAVE_ENTRY.value, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CCAVE_ENTRY_SECOND_ROOM.value, AEDoor.CCAVE_ENTRY.value, 
                        lambda state: TODO)

    # Dexter's Island
    # Outside
    connect_regions(self, AEDoor.DI_ENTRY.value, AEDoor.DI_ENTRY_STOMACH.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DI_ENTRY_STOMACH.value, AEDoor.DI_ENTRY.value,
                        lambda state: True)
    # Stomach
    connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AEDoor.DI_STOMACH_SLIDE_ROOM.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_STOMACH_SLIDE_ROOM.value, AEDoor.DI_STOMACH_ENTRY.value,
                        lambda state: True)
    # Slide
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, 
                        lambda state: TODO)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AEDoor.DI_SLIDE_ROOM_GALLERY.value, 
                        lambda state: TODO)
    if self.options.logic == "expert":
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value, 
                        lambda state: IJ(state, self))
    connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY.value, AEDoor.DI_SLIDE_ROOM_STOMACH.value, 
                        lambda state: TODO)
    self.__add_event_location(self.L43R3T41, "Dexter's Island - Button Reached", "DI-Button") # Event Item
    # Gallery
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value,
                        lambda state: True)
    connect_regions(self, AEDoor.DI_GALLERYBOULDER.value, AEDoor.DI_GALLERY_TENTACLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.DI_GALLERY_TENTACLE.value, AEDoor.DI_GALLERYBOULDER.value, 
                        lambda state: TODO)

    # Snowy Mammoth (level contains a single room)
    # Frosty Retreat
    # Outside
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.FR_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.FR_ENTRY.value, AEDoor.FR_ENTRY_CAVERNS.value, 
                        lambda state: TODO)
    # Caverns
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_CAVERNS_WATER.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AEDoor.FR_CAVERNS_WATER.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.FR_CAVERNS_WATER.value, AEDoor.FR_CAVERNS_ENTRY.value,
                        lambda state: True)

    # Hot Springs
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_HOT_SPRING.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_HOT_SPRING.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.HS_ENTRY.value, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_HOT_SPRING.value, AEDoor.HS_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value, AEDoor.HS_ENTRY.value,
                        lambda state: True)

    # Gladiator Attack (level contains a single room)
    # Sushi Temple
    connect_regions(self, AEDoor.ST_ENTRY.value, AEDoor.ST_ENTRY_TEMPLE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY.value, AEDoor.ST_ENTRY_WELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_TEMPLE.value, AEDoor.ST_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.ST_ENTRY_WELL.value, AEDoor.ST_ENTRY.value,
                        lambda state: True)

    # Wabi Sabi Wall
    # Entry
    connect_regions(self, AEDoor.WSW_ENTRY.value, AEDoor.WSW_ENTRY_GONG.value,
                        lambda state: True)
    # Gong Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_GONG_MIDDLE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AEDoor.WSW_GONG_MIDDLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.WSW_GONG_MIDDLE.value, AEDoor.WSW_GONG_ENTRY.value,
                        lambda state: True)
    # Middle
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_MIDDLE_OBSTACLE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AEDoor.WSW_MIDDLE_OBSTACLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AEDoor.WSW_MIDDLE_GONG.value,
                        lambda state: True)
    # Obstacle Course
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AEDoor.WSW_OBSTACLE_BARREL.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.WSW_OBSTACLE_BARREL.value, AEDoor.WSW_OBSTACLE_MIDDLE.value,
                        lambda state: True)

    # Crumbling Castle
    # Outside
    connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_CASTLE.value,
                        lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BASEMENT.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_ENTRY.value, AEDoor.CC_ENTRY_BELL.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_ENTRY_CASTLE.value, AEDoor.CC_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_ENTRY_BASEMENT.value, AEDoor.CC_ENTRY.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_ENTRY.value,
                        lambda state: True)
    # Boss Door - must be able to reach and hit the button in another room.
    connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AEDoor.CC_ENTRY_BOSS.value, 
                        lambda state: state.has("CC-Button", self.player, 1) and CanHitOnce(state, self)) 
    # Castle
    connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_BELL.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_CASTLEMAIN_BELL.value, AEDoor.CC_CASTLEMAIN_ENTRY.value,
                        lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAIN_ENTRY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAIN_ENTRY.value, 
                        lambda state: TODO)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ENTRY.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_CASTLEMAIN_ELEVATOR.value, AEDoor.CC_CASTLEMAINTHRONEROOM.value, 
                        lambda state: TODO)
    # Bell Tower
    connect_regions(self, AEDoor.CC_BELL_CASTLE.value, AEDoor.CC_BELL_ENTRY.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_BELL_ENTRY.value, AEDoor.CC_BELL_CASTLE.value,
                        lambda state: True)
    # Elevator Room
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_ELEVATOR_BASEMENT.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AEDoor.CC_ELEVATOR_BASEMENT.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_ELEVATOR_BASEMENT.value, AEDoor.CC_ELEVATOR_CASTLEMAIN.value,
                        lambda state: True)
    # Waterway
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ENTRY.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, AEDoor.CC_BASEMENT_ELEVATOR.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CC_BASEMENT_BUTTON_UP.value, AEDoor.CC_BASEMENT_ELEVATOR.value,
                        lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_ENTRY.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_DOWN.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_UP.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CC_BASEMENT_ELEVATOR.value, AEDoor.CC_BASEMENT_BUTTON_UP.value, 
                        lambda state: TODO)
    # Button Room
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_LEDGE.value, AEDoor.CC_BUTTON_BASEMENT_WATER.value,
                        lambda state: True)
    self.__add_event_location(self.L73R6T51, "Crumbling Castle - Button Reached", "CC-Button") # Event Item
    
    # City Park
    # Outside
    connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_BARREL.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CP_ENTRY.value, AEDoor.CP_OUTSIDE_BARREL.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CP_OUTSIDE_SEWERS_FRONT.value, AEDoor.CP_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AEDoor.CP_ENTRY.value, 
                        lambda state: TODO)
    # Front Sewer
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AEDoor.CP_SEWERSFRONT_BARREL.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, 
                        lambda state: TODO)
    # Back Sewer
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.CP_BARREL_OUTSIDE.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.CP_BARREL_OUTSIDE.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CP_BARREL_SEWERS_FRONT.value, AEDoor.CP_BARRELSEWERMIDDLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AEDoor.CP_BARREL_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AEDoor.CP_BARREL_SEWERS_FRONT.value, 
                        lambda state: TODO)

    # Specter's Factory
    # Outside
    connect_regions(self, AEDoor.SF_ENTRY.value, AEDoor.SF_OUTSIDE_FACTORY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_OUTSIDE_FACTORY.value, AEDoor.SF_ENTRY.value, 
                        lambda state: TODO)
    # Main Factory
    connect_regions(self, AEDoor.SF_FACTORY_OUTSIDE.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_OUTSIDE.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_BOTTOM.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.SF_FACTORY_RC_CAR.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_RC_CAR.value,
                        lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_MECH.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_MECH.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.SF_FACTORY_WHEEL_TOP.value, AEDoor.SF_FACTORY_MECH.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.SF_FACTORY_MECH.value, AEDoor.SF_FACTORY_WHEEL_TOP.value, 
                        lambda state: TODO)
    # Triple Wheel
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value, AEDoor.SF_WHEEL_FACTORY_TOP.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.SF_WHEEL_FACTORY_TOP.value, AEDoor.SF_WHEEL_FACTORY_BOTTOM.value,
                        lambda state: True)
    # Mech Room
    connect_regions(self, AEDoor.SF_MECH_FACTORY.value, AEDoor.SF_MECH_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_MECH_LAVA.value, AEDoor.SF_MECH_FACTORY.value,
                        lambda state: True)
    # Lava Room
    if self.options.logic == "normal" or self.options.logic == "expert":
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_LAVA_CONVEYOR.value, 
                        lambda state: TODO)
    else: # This is correct as CanHitWheel includes Flyer only on expert, making hard the unique.
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AEDoor.SF_LAVA_CONVEYOR.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.SF_LAVA_CONVEYOR.value, AEDoor.SF_LAVA_MECH.value,
                        lambda state: True)
    # Conveyor Room (at least it's all True...)
    connect_regions(self, AEDoor.SF_CONVEYOR1_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True))
    connect_regions(self, AEDoor.SF_CONVEYOR2_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR3_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR4_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR5_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR6_EXIT.value, AEDoor.SF_CONVEYOR_LAVA.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR1_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR2_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR3_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR4_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR5_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR6_ENTRY.value,
                        lambda state: True)
    connect_regions(self, AEDoor.SF_CONVEYOR_LAVA.value, AEDoor.SF_CONVEYOR7_ENTRY.value,
                        lambda state: True)

    # TV Tower
    # Outside
    connect_regions(self, AEDoor.TVT_ENTRY.value, AEDoor.TVT_OUTSIDE_LOBBY.value,
                        lambda state: True)
    # Lobby
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_WATER.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_WATER.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.TVT_LOBBY_OUTSIDE.value, AEDoor.TVT_LOBBY_TANK.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.TVT_LOBBY_WATER.value, AEDoor.TVT_LOBBY_OUTSIDE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.TVT_LOBBY_TANK.value, AEDoor.TVT_LOBBY_OUTSIDE.value,
                        lambda state: True)
    # Tank Room
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_TANK_FAN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AEDoor.TVT_TANK_BOSS.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_TANK_LOBBY.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.TVT_TANK_FAN.value, AEDoor.TVT_TANK_LOBBY.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.TVT_TANK_BOSS.value, AEDoor.TVT_TANK_LOBBY.value,
                        lambda state: True)

    # Monkey Madness
    # Specter Land
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_WESTERN.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_COASTER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_CIRCUS.value,
                        lambda state: True)
    # This is not a mistake because the apworld pre-opens the Jake arena as part of handling the Lobby door.
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_GO_KARZ.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB.value, AEDoor.MM_SL_HUB_CRATER.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.MM_SL_HUB_WESTERN.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_COASTER.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CIRCUS.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_GO_KARZ.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_SL_HUB_CRATER.value, AEDoor.MM_SL_HUB.value,
                        lambda state: True)
    # Coaster (several one-way connections here)
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AEDoor.MM_COASTER_ENTRY_COASTER1.value, lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER1_ENTRY.value, AEDoor.MM_COASTER1_COASTER2.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_COASTER2_ENTRY.value, AEDoor.MM_COASTER2_HAUNTED_HOUSE.value,
                        lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AEDoor.MM_HAUNTED_HOUSE_COFFIN.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.MM_COFFIN_HAUNTED_HOUSE.value, AEDoor.MM_COFFIN_COASTER_ENTRY.value, 
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.MM_COASTER_ENTRY_DISEMBARK.value, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, lambda state: True)
    # Crater
    connect_regions(self, AEDoor.MM_CRATER_SL_HUB.value, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value,
                        lambda state: True)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_CRATER_SL_HUB.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AEDoor.MM_CRATER_SL_HUB.value, 
                        lambda state: TODO)
    # Castle Outside
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value,
                        lambda state: MM_Lamp(state, self))
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value,
                        lambda state: True)
    self.__add_event_location(self.L91R12T11, "Monkey Madness - Spawn UFOs", "MM-UFOs") # Event Item
    # Castle Foyer
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, 
                        lambda state: TODO)
    if self.options.logic == "normal": # This will reference MM-Painting
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AEDoor.MM_CASTLE_MAIN_SPECTER1.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, # This will reference MM-Button
                        lambda state: TODO)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value, AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value,
                        lambda state: True)
    # Monkey Head + Inside Climb + Outside Climb
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value,
                        lambda state: True)
    connect_regions(self, AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value, AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value,
                        lambda state: True)
    if self.options.logic == "normal" or self.options.logic == "hard":
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value, 
                        lambda state: TODO)
    self.__add_event_location(self.L91R14T13, "Monkey Madness - Monkey Head Room", "MM-Button") # Event Item
    self.__add_event_location(self.L91R16T13E, "Monkey Madness - Specter 1 Open", "MM-Painting") # Event Item


# A location is always accessed from a transition. The level entrance is a special case of a transition.
def set_locations(self):
    # Time Station
    if self.options.mailbox == "true" or (self.options.shufflenet == "true" and self.options.coin == "true"):
        connect_regions(self, AEDoor.TIME_ENTRY.value, AELocation.Mailbox60.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_ENTRY.value, AELocation.Mailbox61.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_MINIGAME_MAIN.value, AELocation.Mailbox62.value,
                        lambda state: True)
        connect_regions(self, AEDoor.TIME_TRAINING_MAIN.value, AELocation.Mailbox63.value,
                        lambda state: True)

    # Fossil Field
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Noonan.value,
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Jorjy.value,
                        lambda state: HasNet(state, self))
    connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1Nati.value,
                        lambda state: HasNet(state, self))
    if self.options.logic == "normal":
       connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1TrayC.value,
                        lambda state: (HasFlyer(state, self) or IJ(state, self)) and HasNet(state, self))
    else:
       connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.W1L1TrayC.value,
                        lambda state: HasNet(state, self))

    if self.options.coin == "true":
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Coin1.value,
                        lambda state: True)
    
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox1.value,
                        lambda state: True)
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox2.value,
                        lambda state: True)
        connect_regions(self, AEDoor.FF_ENTRY.value, AELocation.Mailbox3.value,
                        lambda state: CanHitOnce(state, self))
    
    # Primordial Ooze
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Shay.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2DrMonk.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Ahchoo.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: TODO)
    elif self.options.logic == "hard":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Grunt.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Tyrone.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Gornif.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.W1L2Gornif.value, 
                        lambda state: TODO)

    if self.options.coin == "true":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Coin2.value,
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox4.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox5.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox6.value,
                        lambda state: True)
        connect_regions(self, AEDoor.PO_ENTRY.value, AELocation.Mailbox7.value,
                        lambda state: True)
    
    # Molten Lava
    # Outside
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Scotty.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Coco.value, 
                        lambda state: TODO)
    if self.options.logic == "normal":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3JThomas.value, 
                        lambda state: TODO)
    else:
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3JThomas.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.W1L3Moggan.value, 
                        lambda state: TODO)
    # Volcano
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.W1L3Barney.value, 
                        lambda state: TODO)
    connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.W1L3Mattie.value, 
                        lambda state: TODO)
    # Triceratops
    connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.W1L3Rocky.value, 
                        lambda state: TODO)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Coin3.value,
                        lambda state: True)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Mailbox8.value,
                        lambda state: True)
        connect_regions(self, AEDoor.ML_ENTRY.value, AELocation.Mailbox9.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ML_VOLCANO_ENTRY.value, AELocation.Mailbox10.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.Mailbox11.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ML_TRICERATOPS_ENTRY.value, AELocation.Mailbox12.value, 
                        lambda state: TODO)

    # Thick Jungle
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Coin6.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_MUSHROOMMAIN.value, AELocation.Coin7.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Coin8.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.Coin9.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Mailbox13.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_ENTRY.value, AELocation.Mailbox14.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.Mailbox15.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_MUSHROOM_ENTRY.value, AELocation.Mailbox16.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox17.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox18.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_FISHBOAT.value, AELocation.Mailbox19.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_TENT_BOULDER.value, AELocation.Mailbox20.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TJ_BOULDER_TENT.value, AELocation.Mailbox21.value, 
                        lambda state: TODO)

    # Dark Ruins
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Coin11.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_OUTSIDE_FENCE.value, AELocation.Coin11.value, 
                        lambda state: True)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Coin12.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.Coin13.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_WATER_SIDE.value, AELocation.Coin14.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox22.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox23.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox24.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_ENTRY.value, AELocation.Mailbox25.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Mailbox26.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_FAN_OUTSIDE_HOLE.value, AELocation.Mailbox27.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DR_OBELISK_BOTTOM.value, AELocation.Mailbox28.value, 
                        lambda state: TODO)

    # Cryptic Relics
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Coin17.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.Mailbox29.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CR_ENTRY.value, AELocation.Mailbox30.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Mailbox31.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value, AELocation.Mailbox32.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value, AELocation.Mailbox33.value, 
                        lambda state: TODO)

    # Stadium Attack
    if self.options.coin == "true":
        connect_regions(self, AEDoor.SA_ENTRY.value, AEDoor.SA_COMPLETE.value, 
                        lambda state: CanSwim(state, self))

    # Crabby Beach (Needs events on monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.Coin21.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.Mailbox34.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CB_ENTRY.value, AELocation.Mailbox35.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CB_SECOND_ROOM_ENTRY.value, AELocation.Mailbox36.value, 
                        lambda state: TODO)

    # Coral Cave
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Coin23.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Mailbox37.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CCAVE_SECOND_ROOM_ENTRY.value, AELocation.Mailbox38.value, 
                        lambda state: TODO)

    # Dexter's Island (Needs events on monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Coin24.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_STOMACH_ENTRY.value, AELocation.Coin25.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AELocation.Coin28.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value, AELocation.Coin28.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Mailbox39.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_ENTRY.value, AELocation.Mailbox40.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_SLIDE_ROOM_STOMACH.value, AELocation.Mailbox41.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value, AELocation.Mailbox42.value, 
                        lambda state: TODO)

    # Snowy Mammoth
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Coin29.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox43.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox44.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.SM_ENTRY.value, AELocation.Mailbox45.value, 
                        lambda state: TODO)

    # Frosty Retreat
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.FR_ENTRY_CAVERNS.value, AELocation.Coin30.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.FR_WATER_CAVERNS.value, AELocation.Coin31.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.Coin32.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.FR_CAVERNS_ENTRY.value, AELocation.Mailbox46.value, 
                        lambda state: TODO)

    # Hot Springs
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.Coin34.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.Coin35.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.HS_ENTRY.value, AELocation.Mailbox47.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.HS_HOT_SPRING.value, AELocation.Mailbox48.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.HS_POLAR_BEAR_CAVE.value, AELocation.Mailbox49.value, 
                        lambda state: TODO)

    # Gladiator Attack
    if self.options.coin == "true":
        connect_regions(self, AEDoor.GA_ENTRY.value, AEDoor.GA_COMPLETE.value, 
                        lambda state: TODO)

    # Sushi Temple
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.ST_ENTRY.value, AELocation.Coin37.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Coin38.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ST_WELL.value, AELocation.Coin39.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Mailbox50.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ST_TEMPLE.value, AELocation.Mailbox51.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.ST_WELL.value, AELocation.Mailbox52.value, 
                        lambda state: TODO)

    # Wabi Sabi Wall
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.WSW_ENTRY_GONG.value, AELocation.Coin40.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.Coin41.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.WSW_BARREL_OBSTACLE.value, AELocation.Coin44.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.WSW_GONG_ENTRY.value, AELocation.Mailbox53.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.WSW_MIDDLE_GONG.value, AELocation.Mailbox54.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.WSW_MIDDLE_OBSTACLE.value, AELocation.Mailbox55.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.WSW_OBSTACLE_MIDDLE.value, AELocation.Mailbox56.value, 
                        lambda state: TODO)

    # Crumbling Castle
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CC_ENTRY_BELL.value, AELocation.Coin45.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CC_CASTLEMAINTHRONEROOM.value, AELocation.Coin46.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CC_BUTTON_BASEMENT_WATER.value, AELocation.Coin49.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CC_ELEVATOR_CASTLEMAIN.value, AELocation.Coin50.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.CC_ENTRY.value, AELocation.Mailbox57.value, 
                        lambda state: TODO)

    # City Park (Needs events on monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.CP_ENTRY.value, AELocation.Coin53.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CP_OUTSIDE_BARREL.value, AELocation.Coin53.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CP_SEWERSFRONT_OUTSIDE.value, AELocation.Coin54.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CP_SEWERSFRONT_BARREL.value, AELocation.Coin54.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.CP_BARRELSEWERMIDDLE.value, AELocation.Coin55.value, 
                        lambda state: TODO)

    # Specter's Factory (Needs events on monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.SF_RC_CAR_FACTORY.value, AELocation.Coin58.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.SF_LAVA_MECH.value, AELocation.Coin59.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.SF_ENTRY.value, AELocation.Mailbox58.value, 
                        lambda state: TODO)

    # TV Tower (Needs events on monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.TVT_WATER_LOBBY.value, AELocation.Coin64.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.TVT_TANK_LOBBY.value, AELocation.Coin66.value, 
                        lambda state: TODO)

    # Monkey Madness (Needs events on specific? monkeys)
    
    if self.options.coin == "true":
        connect_regions(self, AEDoor.MM_COASTER1_ENTRY.value, AELocation.Coin73.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_COASTER2_ENTRY.value, AELocation.Coin74.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value, AELocation.Coin75.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_WESTERN_SL_HUB.value, AELocation.Coin77.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_CRATER_OUTSIDE_CASTLE.value, AELocation.Coin78.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_OUTSIDE_CASTLE_CRATER.value, AELocation.Coin79.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value, AELocation.Coin80.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value, AELocation.Coin84.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value, AELocation.Coin85.value, 
                        lambda state: TODO)
        connect_regions(self, AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value, AELocation.Coin82.value, 
                        lambda state: TODO)
    if self.options.mailbox == "true":
        connect_regions(self, AEDoor.MM_COASTER_ENTRY_SL_HUB.value, AELocation.Mailbox59.value, 
                        lambda state: TODO)

    # Peak Point Matrix
    if options.goal == "second":
        connect_regions(self, AEDoor.PPM_ENTRY.value, AELocation.PPM_SPECTER2.value, 
                        lambda state: TODO)


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


def CanSwim(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 1))


def CanDive(state, world):
    return (state.has(AEItem.WaterNet.value, world.player, 1) or state.has(AEItem.ProgWaterNet.value, world.player, 2))


# Logic Helper Functions
def HasWaterNet(state, world): # CanSwim + CanWaterCatch together
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
    # return state.has("CB Monkey", world.player, 3)
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