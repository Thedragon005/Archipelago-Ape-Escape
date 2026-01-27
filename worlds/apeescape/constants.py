from worlds.apeescape.Strings import AEDoor

entrance_map = {

}

door_map = {
    # Time Station
    AEDoor.TIME_MAIN_TRAINING.value: [AEDoor.TIME_TRAINING_MAIN.value],
    AEDoor.TIME_MAIN_MINIGAME.value: [AEDoor.TIME_MINIGAME_MAIN.value],
    AEDoor.TIME_TRAINING_MAIN.value: [AEDoor.TIME_MAIN_TRAINING.value],
    AEDoor.TIME_MINIGAME_MAIN.value: [AEDoor.TIME_MAIN_MINIGAME.value],

    # Molten Lava
    AEDoor.ML_ENTRY_VOLCANO.value: [AEDoor.ML_VOLCANO_ENTRY.value],
    AEDoor.ML_ENTRY_TRICERATOPS.value: [AEDoor.ML_TRICERATOPS_ENTRY.value],
    AEDoor.ML_VOLCANO_ENTRY.value: [AEDoor.ML_ENTRY_VOLCANO.value],
    AEDoor.ML_TRICERATOPS_ENTRY.value: [AEDoor.ML_ENTRY_TRICERATOPS.value],

    # Thick Jungle
    AEDoor.TJ_ENTRY_MUSHROOM.value: [AEDoor.TJ_MUSHROOM_ENTRY.value],
    AEDoor.TJ_ENTRY_FISH.value: [AEDoor.TJ_FISH_ENTRY.value],
    AEDoor.TJ_ENTRY_BOULDER.value: [AEDoor.TJ_BOULDER_ENTRY.value],
    AEDoor.TJ_MUSHROOM_ENTRY.value: [AEDoor.TJ_ENTRY_MUSHROOM.value],
    AEDoor.TJ_FISH_ENTRY.value: [AEDoor.TJ_ENTRY_FISH.value],
    AEDoor.TJ_FISH_TENT.value: [AEDoor.TJ_TENT_FISH.value],
    AEDoor.TJ_TENT_FISH.value: [AEDoor.TJ_FISH_TENT.value],
    AEDoor.TJ_TENT_BOULDER.value: [AEDoor.TJ_BOULDER_TENT.value],
    AEDoor.TJ_BOULDER_ENTRY.value: [AEDoor.TJ_ENTRY_BOULDER.value],
    AEDoor.TJ_BOULDER_TENT.value: [AEDoor.TJ_TENT_BOULDER.value],

    # Dark Ruins
    AEDoor.DR_OUTSIDE_FENCE.value: [AEDoor.DR_FAN_OUTSIDE_FENCE.value],
    AEDoor.DR_OUTSIDE_HOLE.value: [AEDoor.DR_FAN_OUTSIDE_HOLE.value],
    AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value: [AEDoor.DR_OBELISK_BOTTOM.value],
    AEDoor.DR_OUTSIDE_OBELISK_TOP.value: [AEDoor.DR_OBELISK_TOP.value],
    AEDoor.DR_OUTSIDE_WATER_BUTTON.value: [AEDoor.DR_WATER_SIDE.value],
    AEDoor.DR_OUTSIDE_WATER_LEDGE.value: [AEDoor.DR_WATER_LEDGE.value],
    AEDoor.DR_FAN_OUTSIDE_FENCE.value: [AEDoor.DR_OUTSIDE_FENCE.value],
    AEDoor.DR_FAN_OUTSIDE_HOLE.value: [AEDoor.DR_OUTSIDE_HOLE.value],
    AEDoor.DR_OBELISK_BOTTOM.value: [AEDoor.DR_OUTSIDE_OBELISK_BOTTOM.value],
    AEDoor.DR_OBELISK_TOP.value: [AEDoor.DR_OUTSIDE_OBELISK_TOP.value],
    AEDoor.DR_WATER_SIDE.value: [AEDoor.DR_OUTSIDE_WATER_BUTTON.value],
    AEDoor.DR_WATER_LEDGE.value: [AEDoor.DR_OUTSIDE_WATER_LEDGE.value],

    # Cryptic Relics
    AEDoor.CR_ENTRY_SIDE_ROOM.value: [AEDoor.CR_SIDE_ROOM_ENTRY.value],
    AEDoor.CR_ENTRY_MAIN_RUINS.value: [AEDoor.CR_MAIN_RUINS_ENTRY.value],
    AEDoor.CR_SIDE_ROOM_ENTRY.value: [AEDoor.CR_ENTRY_SIDE_ROOM.value],
    AEDoor.CR_MAIN_RUINS_ENTRY.value: [AEDoor.CR_ENTRY_MAIN_RUINS.value],
    AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value: [AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value],
    AEDoor.CR_PILLAR_ROOM_MAIN_RUINS.value: [AEDoor.CR_MAIN_RUINS_PILLAR_ROOM.value],

    # Crabby Beach
    AEDoor.CB_ENTRY_SECOND_ROOM.value: [AEDoor.CB_SECOND_ROOM_ENTRY.value],
    AEDoor.CB_SECOND_ROOM_ENTRY.value: [AEDoor.CB_ENTRY_SECOND_ROOM.value],

    # Coral Cave
    AEDoor.CCAVE_ENTRY_SECOND_ROOM.value: [AEDoor.CCAVE_SECOND_ROOM_ENTRY.value],
    AEDoor.CCAVE_SECOND_ROOM_ENTRY.value: [AEDoor.CCAVE_ENTRY_SECOND_ROOM.value],

    # Dexter's Island
    AEDoor.DI_ENTRY_STOMACH.value: [AEDoor.DI_STOMACH_ENTRY.value],
    AEDoor.DI_STOMACH_ENTRY.value: [AEDoor.DI_ENTRY_STOMACH.value],
    AEDoor.DI_STOMACH_SLIDE_ROOM.value: [AEDoor.DI_SLIDE_ROOM_STOMACH.value],
    AEDoor.DI_SLIDE_ROOM_STOMACH.value: [AEDoor.DI_STOMACH_SLIDE_ROOM.value],
    AEDoor.DI_SLIDE_ROOM_GALLERY.value: [AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value],
    AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value: [AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value],
    AEDoor.DI_GALLERY_SLIDE_ROOM_TOP.value: [AEDoor.DI_SLIDE_ROOM_GALLERY.value],
    AEDoor.DI_GALLERY_SLIDE_ELEVATOR.value: [AEDoor.DI_SLIDE_ROOM_GALLERY_WATER.value],
    AEDoor.DI_GALLERY_TENTACLE.value: [AEDoor.DI_TENTACLE.value],
    AEDoor.DI_TENTACLE.value: [AEDoor.DI_GALLERY_TENTACLE.value],

    # Frosty Retreat
    AEDoor.FR_ENTRY_CAVERNS.value: [AEDoor.FR_CAVERNS_ENTRY.value],
    AEDoor.FR_CAVERNS_ENTRY.value: [AEDoor.FR_ENTRY_CAVERNS.value],
    AEDoor.FR_CAVERNS_WATER.value: [AEDoor.FR_WATER_CAVERNS.value],
    AEDoor.FR_WATER_CAVERNS.value: [AEDoor.FR_CAVERNS_WATER.value],

    # Hot Springs
    AEDoor.HS_ENTRY_HOT_SPRING.value: [AEDoor.HS_HOT_SPRING.value],
    AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value: [AEDoor.HS_POLAR_BEAR_CAVE.value],
    AEDoor.HS_HOT_SPRING.value: [AEDoor.HS_ENTRY_HOT_SPRING.value],
    AEDoor.HS_POLAR_BEAR_CAVE.value: [AEDoor.HS_ENTRY_POLAR_BEAR_CAVE.value],

    # Sushi Temple
    AEDoor.ST_ENTRY_TEMPLE.value: [AEDoor.ST_TEMPLE.value],
    AEDoor.ST_ENTRY_WELL.value: [AEDoor.ST_WELL.value],
    AEDoor.ST_TEMPLE.value: [AEDoor.ST_ENTRY_TEMPLE.value],
    AEDoor.ST_WELL.value: [AEDoor.ST_ENTRY_WELL.value],

    # Wabi Sabi Wall
    AEDoor.WSW_ENTRY_GONG.value: [AEDoor.WSW_GONG_ENTRY.value],
    AEDoor.WSW_GONG_ENTRY.value: [AEDoor.WSW_ENTRY_GONG.value],
    AEDoor.WSW_GONG_MIDDLE.value: [AEDoor.WSW_MIDDLE_GONG.value],
    AEDoor.WSW_MIDDLE_GONG.value: [AEDoor.WSW_GONG_MIDDLE.value],
    AEDoor.WSW_MIDDLE_OBSTACLE.value: [AEDoor.WSW_OBSTACLE_MIDDLE.value],
    AEDoor.WSW_OBSTACLE_MIDDLE.value: [AEDoor.WSW_MIDDLE_OBSTACLE.value],
    AEDoor.WSW_OBSTACLE_BARREL.value: [AEDoor.WSW_BARREL_OBSTACLE.value],
    AEDoor.WSW_BARREL_OBSTACLE.value: [AEDoor.WSW_OBSTACLE_BARREL.value],

    # Crumbling Castle
    AEDoor.CC_ENTRY_CASTLE.value: [AEDoor.CC_CASTLEMAIN_ENTRY.value],
    AEDoor.CC_ENTRY_BELL.value: [AEDoor.CC_BELL_ENTRY.value],
    AEDoor.CC_ENTRY_BASEMENT.value: [AEDoor.CC_BASEMENT_ENTRY.value],
    AEDoor.CC_ENTRY_BOSS.value: [AEDoor.CC_BOSS_ROOM.value],
    AEDoor.CC_CASTLEMAIN_ENTRY.value: [AEDoor.CC_ENTRY_CASTLE.value],
    AEDoor.CC_CASTLEMAIN_BELL.value: [AEDoor.CC_BELL_CASTLE.value],
    AEDoor.CC_CASTLEMAIN_ELEVATOR.value: [AEDoor.CC_ELEVATOR_CASTLEMAIN.value],
    AEDoor.CC_BELL_ENTRY.value: [AEDoor.CC_ENTRY_BELL.value],
    AEDoor.CC_BELL_CASTLE.value: [AEDoor.CC_CASTLEMAIN_BELL.value],
    AEDoor.CC_ELEVATOR_CASTLEMAIN.value: [AEDoor.CC_CASTLEMAIN_ELEVATOR.value],
    AEDoor.CC_ELEVATOR_BASEMENT.value: [AEDoor.CC_BASEMENT_ELEVATOR.value],
    AEDoor.CC_BASEMENT_ENTRY.value: [AEDoor.CC_ENTRY_BASEMENT.value],
    AEDoor.CC_BASEMENT_ELEVATOR.value: [AEDoor.CC_BASEMENT_ELEVATOR.value],
    AEDoor.CC_BASEMENT_BUTTON_DOWN.value: [AEDoor.CC_BUTTON_BASEMENT_WATER.value],
    AEDoor.CC_BASEMENT_BUTTON_UP.value: [AEDoor.CC_BUTTON_BASEMENT_LEDGE.value],
    AEDoor.CC_BUTTON_BASEMENT_WATER.value: [AEDoor.CC_BASEMENT_BUTTON_DOWN.value],
    AEDoor.CC_BUTTON_BASEMENT_LEDGE.value: [AEDoor.CC_BASEMENT_BUTTON_UP.value],
    AEDoor.CC_BOSS_ROOM.value: [AEDoor.CC_ENTRY_BOSS.value],

    # City Park
    AEDoor.CP_OUTSIDE_SEWERS_FRONT.value: [AEDoor.CP_SEWERSFRONT_OUTSIDE.value],
    AEDoor.CP_OUTSIDE_BARREL.value: [AEDoor.CP_BARREL_OUTSIDE.value],
    AEDoor.CP_SEWERSFRONT_OUTSIDE.value: [AEDoor.CP_OUTSIDE_SEWERS_FRONT.value],
    AEDoor.CP_SEWERSFRONT_BARREL.value: [AEDoor.CP_BARREL_SEWERS_FRONT.value],
    AEDoor.CP_BARREL_OUTSIDE.value: [AEDoor.CP_OUTSIDE_BARREL.value],
    AEDoor.CP_BARREL_SEWERS_FRONT.value: [AEDoor.CP_SEWERSFRONT_BARREL.value],

    # Specter's Factory
    AEDoor.SF_OUTSIDE_FACTORY.value: [AEDoor.SF_FACTORY_OUTSIDE.value],
    AEDoor.SF_FACTORY_OUTSIDE.value: [AEDoor.SF_OUTSIDE_FACTORY.value],
    AEDoor.SF_FACTORY_RC_CAR.value: [AEDoor.SF_RC_CAR_FACTORY.value],
    AEDoor.SF_FACTORY_WHEEL_BOTTOM.value: [AEDoor.SF_WHEEL_FACTORY_BOTTOM.value],
    AEDoor.SF_FACTORY_WHEEL_TOP.value: [AEDoor.SF_WHEEL_FACTORY_TOP.value],
    AEDoor.SF_FACTORY_MECH.value: [AEDoor.SF_MECH_FACTORY.value],
    AEDoor.SF_RC_CAR_FACTORY.value: [AEDoor.SF_FACTORY_RC_CAR.value],
    AEDoor.SF_WHEEL_FACTORY_BOTTOM.value: [AEDoor.SF_FACTORY_WHEEL_BOTTOM.value],
    AEDoor.SF_WHEEL_FACTORY_TOP.value: [AEDoor.SF_FACTORY_WHEEL_TOP.value],
    AEDoor.SF_MECH_FACTORY.value: [AEDoor.SF_FACTORY_MECH.value],
    AEDoor.SF_MECH_LAVA.value: [AEDoor.SF_LAVA_MECH.value],
    AEDoor.SF_LAVA_MECH.value: [AEDoor.SF_MECH_LAVA.value],
    AEDoor.SF_LAVA_CONVEYOR.value: [AEDoor.SF_CONVEYOR_LAVA.value],
    AEDoor.SF_CONVEYOR_LAVA.value: [AEDoor.SF_LAVA_CONVEYOR.value],

    # Conveyor Room
    AEDoor.SF_CONVEYOR1_ENTRY.value: [AEDoor.SF_CONVEYOR1_EXIT.value],
    AEDoor.SF_CONVEYOR2_ENTRY.value: [AEDoor.SF_CONVEYOR1_EXIT.value],
    AEDoor.SF_CONVEYOR3_ENTRY.value: [AEDoor.SF_CONVEYOR2_EXIT.value],
    AEDoor.SF_CONVEYOR4_ENTRY.value: [AEDoor.SF_CONVEYOR3_EXIT.value],
    AEDoor.SF_CONVEYOR5_ENTRY.value: [AEDoor.SF_CONVEYOR4_EXIT.value],
    AEDoor.SF_CONVEYOR6_ENTRY.value: [AEDoor.SF_CONVEYOR5_EXIT.value],
    AEDoor.SF_CONVEYOR7_ENTRY.value: [AEDoor.SF_CONVEYOR6_EXIT.value],

    # TV Tower
    AEDoor.TVT_OUTSIDE_LOBBY.value: [AEDoor.TVT_LOBBY_OUTSIDE.value],
    AEDoor.TVT_LOBBY_OUTSIDE.value: [AEDoor.TVT_OUTSIDE_LOBBY.value],
    AEDoor.TVT_LOBBY_WATER.value: [AEDoor.TVT_WATER_LOBBY.value],
    AEDoor.TVT_LOBBY_TANK.value: [AEDoor.TVT_TANK_LOBBY.value],
    AEDoor.TVT_WATER_LOBBY.value: [AEDoor.TVT_LOBBY_WATER.value],
    AEDoor.TVT_TANK_LOBBY.value: [AEDoor.TVT_LOBBY_TANK.value],
    AEDoor.TVT_TANK_FAN.value: [AEDoor.TVT_FAN_TANK.value],
    AEDoor.TVT_TANK_BOSS.value: [AEDoor.TVT_BOSS_TANK.value],
    AEDoor.TVT_FAN_TANK.value: [AEDoor.TVT_TANK_FAN.value],
    AEDoor.TVT_BOSS_TANK.value: [AEDoor.TVT_TANK_BOSS.value],

    # Monkey Madness
    AEDoor.MM_SL_HUB_WESTERN.value: [AEDoor.MM_WESTERN_SL_HUB.value],
    AEDoor.MM_SL_HUB_COASTER.value: [AEDoor.MM_COASTER_ENTRY_SL_HUB.value],
    AEDoor.MM_SL_HUB_CIRCUS.value: [AEDoor.MM_CIRCUS_SL_HUB.value],
    AEDoor.MM_SL_HUB_GO_KARZ.value: [AEDoor.MM_GO_KARZ_SL_HUB.value],
    AEDoor.MM_SL_HUB_CRATER.value: [AEDoor.MM_CRATER_SL_HUB.value],
    AEDoor.MM_WESTERN_SL_HUB.value: [AEDoor.MM_SL_HUB_WESTERN.value],
    AEDoor.MM_COASTER_ENTRY_SL_HUB.value: [AEDoor.MM_SL_HUB_COASTER.value],
    AEDoor.MM_COASTER_ENTRY_COASTER1.value: [AEDoor.MM_COASTER1_ENTRY.value],
    AEDoor.MM_CIRCUS_SL_HUB.value: [AEDoor.MM_SL_HUB_CIRCUS.value],
    AEDoor.MM_GO_KARZ_SL_HUB.value: [AEDoor.MM_SL_HUB_GO_KARZ.value],
    AEDoor.MM_COASTER1_COASTER2.value: [AEDoor.MM_COASTER2_ENTRY.value],
    AEDoor.MM_COASTER2_HAUNTED_HOUSE.value: [AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value],
    AEDoor.MM_HAUNTED_HOUSE_COFFIN.value: [AEDoor.MM_COFFIN_HAUNTED_HOUSE.value],
    AEDoor.MM_COFFIN_COASTER_ENTRY.value: [AEDoor.MM_COASTER_ENTRY_DISEMBARK.value],
    AEDoor.MM_COFFIN_HAUNTED_HOUSE.value: [AEDoor.MM_HAUNTED_HOUSE_COFFIN.value],
    AEDoor.MM_CRATER_SL_HUB.value: [AEDoor.MM_SL_HUB_CRATER.value],
    AEDoor.MM_CRATER_OUTSIDE_CASTLE.value: [AEDoor.MM_OUTSIDE_CASTLE_CRATER.value],
    AEDoor.MM_OUTSIDE_CASTLE_CRATER.value: [AEDoor.MM_CRATER_OUTSIDE_CASTLE.value],
    AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value: [AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value],
    AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value: [AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value],
    AEDoor.MM_SIDE_ENTRY_OUTSIDE_CASTLE.value: [AEDoor.MM_OUTSIDE_CASTLE_SIDE_ENTRY.value],
    AEDoor.MM_CASTLE_MAIN_OUTSIDE_CASTLE.value: [AEDoor.MM_OUTSIDE_CASTLE_CASTLE_MAIN.value],
    AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value: [AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value],
    AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value: [AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value],
    AEDoor.MM_CASTLE_MAIN_SPECTER1.value: [AEDoor.MM_SPECTER1_ROOM.value],
    AEDoor.MM_MONKEY_HEAD_CASTLE_MAIN.value: [AEDoor.MM_CASTLE_MAIN_MONKEY_HEAD.value],
    AEDoor.MM_INSIDE_CLIMB_CASTLE_MAIN.value: [AEDoor.MM_CASTLE_MAIN_INSIDE_CLIMB.value],
    AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value: [AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value],
    AEDoor.MM_OUTSIDE_CLIMB_INSIDE_CLIMB.value: [AEDoor.MM_INSIDE_CLIMB_OUTSIDE_CLIMB.value],
    AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value: [AEDoor.MM_CASTLE_MAIN_FROM_OUTSIDE.value],
}

ONEWAY_SHUFFLE_TYPES = frozenset([AEDoor.SF_CONVEYOR1_ENTRY.value,
                                 AEDoor.SF_CONVEYOR2_ENTRY.value,
                                 AEDoor.SF_CONVEYOR3_ENTRY.value,
                                 AEDoor.SF_CONVEYOR4_ENTRY.value,
                                 AEDoor.SF_CONVEYOR5_ENTRY.value,
                                 AEDoor.SF_CONVEYOR6_ENTRY.value,
                                 AEDoor.SF_CONVEYOR7_ENTRY.value,
                                 AEDoor.MM_COASTER_ENTRY_COASTER1.value,
                                 AEDoor.MM_COASTER1_COASTER2.value,
                                 AEDoor.MM_COASTER2_HAUNTED_HOUSE.value,
                                 AEDoor.MM_COFFIN_COASTER_ENTRY.value,
                                 AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
                                 AEDoor.MM_OUTSIDE_CLIMB_CASTLE_MAIN.value])

BOSSES_SHUFFLE_TYPES = frozenset([AEDoor.CC_ENTRY_BOSS.value,
                                 AEDoor.CC_BOSS_ROOM.value,
                                 AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
                                 AEDoor.MM_SPECTER1_ROOM.value,
                                 AEDoor.TVT_TANK_BOSS.value,
                                 AEDoor.TVT_BOSS_TANK.value])

APEESCAPE_MAX_GER_ATTEMPTS: int = 10
APEESCAPE_DEBUG: bool = True