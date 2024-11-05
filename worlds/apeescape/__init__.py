import math
import os
import json
from typing import ClassVar, Dict, List, Tuple, Optional

from BaseClasses import ItemClassification, MultiWorld, Tutorial, CollectionState
from logging import warning
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from .Items import item_table, ApeEscapeItem, GROUPED_ITEMS
from .Locations import location_table, base_location_id, GROUPED_LOCATIONS
from .Regions import create_regions, ApeEscapeLevel
from .Rules import set_rules
from .Client import ApeEscapeClient
from .Strings import AEItem, AELocation
from .RAMAddress import RAM
from .Options import ApeEscapeOptions


class ApeEscapeWeb(WebWorld):
    theme = "stone"

    # Verify this placeholder text is accurate
    setup_en = Tutorial(
        "Ape Escape Multiworld Setup Guide",
        "A guide to setting up Ape Escape in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CDRomatron, Thedragon005, IHNN"]
    )
    setup_fr = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Français",
        "setup_fr.md",
        "setup/fr",
        ["Thedragon005"]
    )

    tutorials = [setup_en,setup_fr]


class ApeEscapeWorld(World):
    """
    Ape Escape is a platform game published and developed by Sony for the PlayStation, released in 1999.
    The story revolves around the main protagonist, Spike, who has to prevent history from being changed by an army of
    Monkeys led by Specter, the main antagonist.
    """
    game = "Ape Escape"
    web: ClassVar[WebWorld] = ApeEscapeWeb()
    topology_present = True

    options_dataclass = ApeEscapeOptions
    options: ApeEscapeOptions

    item_name_to_id = item_table

    for key, value in item_name_to_id.items():
        item_name_to_id[key] = value + base_location_id

    location_name_to_id = location_table

    for key, value in location_name_to_id.items():
        location_name_to_id[key] = value + base_location_id

    item_name_groups = GROUPED_ITEMS
    location_name_groups = GROUPED_LOCATIONS

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.goal: Optional[int] = 0
        self.logic: Optional[int] = 0
        self.entrance: Optional[int] = 0
        self.unlocksperkey: Optional[int] = 0
        self.coin: Optional[int] = 0
        self.gadget: Optional[int] = 0
        self.superflyer: Optional[int] = 0
        self.shufflenet: Optional[int] = 0
        self.itempool: List[ApeEscapeItem] = []
        self.levellist: List[ApeEscapeLevel] = []
        self.entranceorder: List[ApeEscapeLevel] = []

    def generate_early(self) -> None:
        self.goal = self.options.goal.value
        self.logic = self.options.logic.value
        self.entrance: self.options.entrance.value
        self.unlocksperkey: self.options.unlocksperkey.value
        self.coin = self.options.coin.value
        self.gadget = self.options.gadget.value
        self.superflyer = self.options.superflyer.value
        self.shufflenet = self.options.shufflenet.value
        self.itempool = []

    def generate_basic(self):
        self.levellist = initialize_level_list()
        # If entrances aren't shuffled, then we don't need to shuffle the entrances.
        if (self.options.entrance != 0x00):
            self.random.shuffle(self.levellist)
            # Some levels need to be kept at a specific entrance - put those back.
            self.levellist = fixed_levels(self.levellist, self.options.entrance)
        self.levellist = set_calculated_level_data(self.levellist, self.options.unlocksperkey)
        # Make a copy of the list for passing to the client for entrance shuffle purposes. We know this list has the levels sorted in the order they'd be presented in-game (so whatever is at the Fossil Field entrance first, etc.)
        self.entranceorder = list(self.levellist)
        # If entrances weren't shuffled, then this list is already sorted. We sort the list for ease of setting up access rules in the logic files.
        if (self.options.entrance != 0x00):
            self.levellist.sort()

    def create_regions(self):
        create_regions(self)

    def set_rules(self):
        set_rules(self)

    def create_item(self, name: str) -> ApeEscapeItem:
        item_id = item_table[name]
        classification = ItemClassification.progression

        item = ApeEscapeItem(name, classification, item_id, self.player)
        return item

    def create_item_useful(self, name: str) -> ApeEscapeItem:
        item_id = item_table[name]
        classification = ItemClassification.useful

        item = ApeEscapeItem(name, classification, item_id, self.player)
        return item

    def create_item_filler(self, name: str) -> ApeEscapeItem:
        item_id = item_table[name]
        classification = ItemClassification.filler

        item = ApeEscapeItem(name, classification, item_id, self.player)
        return item

    def create_items(self):
        reservedlocations = 0

        club = self.create_item(AEItem.Club.value)
        net = self.create_item(AEItem.Net.value)
        radar = self.create_item(AEItem.Radar.value)
        shooter = self.create_item(AEItem.Sling.value)
        hoop = self.create_item(AEItem.Hoop.value)
        flyer = self.create_item(AEItem.Flyer.value)
        car = self.create_item(AEItem.Car.value)
        punch = self.create_item(AEItem.Punch.value)
        victory = self.create_item(AEItem.Victory.value)

        waternet = self.create_item(AEItem.WaterNet.value)

        self.multiworld.push_precollected(waternet)

        # Create enough keys to access every level, depending on the key option
        if self.options.unlocksperkey == 0x00:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 6)]
        elif self.options.unlocksperkey == 0x01:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 8)]
        elif self.options.unlocksperkey == 0x02:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 16)]
        elif self.options.unlocksperkey == 0x03:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 18)]

        # Net shuffle handling.
        if self.options.shufflenet == "false":
            self.multiworld.push_precollected(net)
        elif self.options.shufflenet == "true":
            # If net shuffle is on, make sure there are locations that don't require net.
            if self.options.coin == "true" or self.options.mailbox == "true":
                self.itempool += [net]
            else:
                # All locations require net with these options, so throw a warning about incompatible options and just give the net anyway.
                # if instead we want to error out and prevent generation, uncomment this line:
                # raise OptionError(f"{self.player_name} has no sphere 1 locations!")
                warning(f"Warning: selected options for {self.player_name} have no sphere 1 locations. Giving Time Net.")
                self.multiworld.push_precollected(net)

        if self.options.gadget == "club":
            self.multiworld.push_precollected(club)
            self.itempool += [radar, shooter, hoop, flyer, car, punch]
        elif self.options.gadget == "radar":
            self.multiworld.push_precollected(radar)
            self.itempool += [club, shooter, hoop, flyer, car, punch]
        elif self.options.gadget == "sling":
            self.multiworld.push_precollected(shooter)
            self.itempool += [club, radar, hoop, flyer, car, punch]
        elif self.options.gadget == "hoop":
            self.multiworld.push_precollected(hoop)
            self.itempool += [club, radar, shooter, flyer, car, punch]
        elif self.options.gadget == "flyer":
            self.multiworld.push_precollected(flyer)
            self.itempool += [club, radar, shooter, hoop, car, punch]
        elif self.options.gadget == "car":
            self.multiworld.push_precollected(car)
            self.itempool += [club, radar, shooter, hoop, flyer, punch]
        elif self.options.gadget == "punch":
            self.multiworld.push_precollected(punch)
            self.itempool += [club, radar, shooter, hoop, flyer, car]
        elif self.options.gadget == "none":
            self.itempool += [club, radar, shooter, hoop, flyer, car, punch]

        if self.options.goal == "first":
            self.get_location(AELocation.Specter.value).place_locked_item(victory)
        else:
            self.get_location(AELocation.Specter2.value).place_locked_item(victory)

        # This is where creating items for increasing special pellet maximums would go.

        # Junk item fill: randomly pick items according to a set of weights.
        # Filler item weights are for 1 Jacket, 1/5 Cookies, 1/5/25 Energy Chips, 1/3 Explosive/Guided Pellets, and Nothing, respectively.
        weights = [7, 16, 3, 31, 14, 4, 9, 3, 9, 3, 1]
        for x in range(1, len(weights)):
            weights[x] = weights[x] + weights[x - 1]

        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(self.itempool) - reservedlocations):
            randomFiller = self.random.randint(1, weights[len(weights) - 1])
            if 0 < randomFiller <= weights[0]:
                self.itempool += [self.create_item_useful(AEItem.Shirt.value)]
            elif weights[0] < randomFiller <= weights[1]:
                self.itempool += [self.create_item_filler(AEItem.Cookie.value)]
            elif weights[1] < randomFiller <= weights[2]:
                self.itempool += [self.create_item_filler(AEItem.FiveCookies.value)]
            elif weights[2] < randomFiller <= weights[3]:
                self.itempool += [self.create_item_filler(AEItem.Triangle.value)]
            elif weights[3] < randomFiller <= weights[4]:
                self.itempool += [self.create_item_filler(AEItem.BigTriangle.value)]
            elif weights[4] < randomFiller <= weights[5]:
                self.itempool += [self.create_item_filler(AEItem.BiggerTriangle.value)]
            elif weights[5] < randomFiller <= weights[6]:
                self.itempool += [self.create_item_useful(AEItem.Flash.value)]
            elif weights[6] < randomFiller <= weights[7]:
                self.itempool += [self.create_item_useful(AEItem.ThreeFlash.value)]
            elif weights[7] < randomFiller <= weights[8]:
                self.itempool += [self.create_item_useful(AEItem.Rocket.value)]
            elif weights[8] < randomFiller <= weights[9]:
                self.itempool += [self.create_item_useful(AEItem.ThreeRocket.value)]
            else:
                self.itempool += [self.create_item_filler(AEItem.Nothing.value)]

        self.multiworld.itempool += self.itempool

    def fill_slot_data(self):
        bytestowrite = []
        entranceids = []
        firstroomids = [0x01, 0x02, 0x03, 0x06, 0x0B, 0x0F, 0x13, 0x14, 0x16, 0x18, 0x1D, 0x1E, 0x21, 0x24, 0x25, 0x28, 0x2D, 0x35, 0x38, 0x3F, 0x45, 0x57]
        orderedfirstroomids = []
        for x in range(0, 22):
            entranceids.append(self.entranceorder[x].entrance)
            orderedfirstroomids.append(firstroomids[self.entranceorder[x].vanillapos])
            bytestowrite += self.entranceorder[x].bytes
            bytestowrite.append(0) # We need a separator byte after each level name.
            
        return {
            "goal": self.options.goal.value,
            "logic": self.options.logic.value,
            "entrance": self.options.entrance.value,
            "unlocksperkey": self.options.unlocksperkey.value,
            "coin": self.options.coin.value,
            "mailbox": self.options.mailbox.value,
            "gadget": self.options.gadget.value,
            "superflyer": self.options.superflyer.value,
            "shufflenet": self.options.shufflenet.value,
            "levelnames": bytestowrite,
            "entranceids": entranceids,
            "firstrooms": orderedfirstroomids,
            "reqkeys": get_required_keys(self.options.unlocksperkey.value),
        }

    def generate_output(self, output_directory: str):
        data = {
            "slot_data": self.fill_slot_data()
        }
        # Remove .apae output because it does nothing, we do everything in RAM
        # filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apae"
        # with open(os.path.join(output_directory, filename), 'w') as f:
        #     json.dump(data, f)


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
    if byte.isspace(): # Space
        return 255
    if byte.isalpha():
        return ord(byte) - 49 # Both uppercase and lowercase letters
    if byte.isdecimal():
        if int(byte) < 6:
            return ord(byte) + 56 # 0-5
        else:
            return ord(byte) + 68 # 6-9
    if ord(byte) == 39: # Single apostrophe
        return 187

def fixed_levels(levellist, entoption):
    for x in range (0, 22):
        if levellist[x].entrance == 0x1E:
            levellist[x], levellist[21] = levellist[21], levellist[x]
        if levellist[x].entrance == 0x07 and entoption == 0x01:
            levellist[x], levellist[6] = levellist[6], levellist[x]
        if levellist[x].entrance == 0x0E and entoption == 0x01:
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
    if option == 0x00: # world
        return [0,  0,  0,  1,  1,  1,  2,  2,  2,  2,  3,  3,  3,  4,  4,  4,  4,  5,  5,  5,  6,  6]
    if option == 0x01: # world and races
        return [0,  0,  0,  1,  1,  1,  2,  3,  3,  3,  4,  4,  4,  5,  6,  6,  6,  7,  7,  7,  8,  8]
    if option == 0x02: # level
        return [0,  0,  0,  1,  2,  3,  4,  4,  5,  6,  7,  8,  9,  10, 10, 11, 12, 13, 14, 15, 16, 16]
    if option == 0x03: # level and races
        return [0,  0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 17, 18, 18]