from worlds.apeescape.Strings import AEDoor
DOUBLE_EXIT = AEDoor.SF_CONVEYOR1_EXIT.value
SAME_ROOM_EXCEPTION = frozenset([AEDoor.SF_CONVEYOR1_EXIT.value,
                                 AEDoor.SF_CONVEYOR2_EXIT.value,
                                 AEDoor.SF_CONVEYOR3_EXIT.value,
                                 AEDoor.SF_CONVEYOR4_EXIT.value,
                                 AEDoor.SF_CONVEYOR5_EXIT.value,
                                 AEDoor.SF_CONVEYOR6_EXIT.value])

EXITS_ONLY_DOOR = frozenset([AEDoor.SF_CONVEYOR1_EXIT.value,
                                 AEDoor.SF_CONVEYOR2_EXIT.value,
                                 AEDoor.SF_CONVEYOR3_EXIT.value,
                                 AEDoor.SF_CONVEYOR4_EXIT.value,
                                 AEDoor.SF_CONVEYOR5_EXIT.value,
                                 AEDoor.SF_CONVEYOR6_EXIT.value,
                                 AEDoor.MM_COASTER_ENTRY_DISEMBARK.value,
                                 AEDoor.MM_HAUNTED_HOUSE_DISEMBARK.value])

ONEWAY_SHUFFLE_DOOR = frozenset([AEDoor.SF_CONVEYOR1_ENTRY.value,
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

BOSSES_SHUFFLE_DOOR = frozenset([AEDoor.CC_ENTRY_BOSS.value,
                                 AEDoor.CC_BOSS_ROOM.value,
                                 AEDoor.MM_CASTLE_MAIN_SPECTER1.value,
                                 AEDoor.MM_SPECTER1_ROOM.value,
                                 AEDoor.TVT_TANK_BOSS.value,
                                 AEDoor.TVT_BOSS_TANK.value])

APEESCAPE_MAX_ATTEMPTS: int = 10
APEESCAPE_DEBUG: bool = True