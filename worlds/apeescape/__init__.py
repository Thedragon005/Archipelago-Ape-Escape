import math
import os
import json
from typing import ClassVar, Dict, List, Tuple, Optional, TextIO

from BaseClasses import ItemClassification, MultiWorld, Tutorial, CollectionState
from logging import warning
from Options import OptionError
from worlds.AutoWorld import WebWorld, World

from .Items import item_table, ApeEscapeItem, GROUPED_ITEMS
from .Locations import location_table, base_location_id, GROUPED_LOCATIONS
from .Regions import create_regions, ApeEscapeLevel
from .Rules import set_rules, get_required_keys
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

    tutorials = [setup_en, setup_fr]


class ApeEscapeWorld(World):
    """
    Ape Escape is a platform game published and developed by Sony for the PlayStation, released in 1999.
    The story revolves around the main protagonist, Spike, who has to prevent history from being changed
    by an army of monkeys led by Specter, the main antagonist.
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
        self.goal: Optional[int] = 0
        self.logic: Optional[int] = 0
        self.entrance: Optional[int] = 0
        self.unlocksperkey: Optional[int] = 0
        self.coin: Optional[int] = 0
        self.gadget: Optional[int] = 0
        self.superflyer: Optional[int] = 0
        self.shufflenet: Optional[int] = 0
        self.shufflewaternet: Optional[int] = 0
        self.itempool: List[ApeEscapeItem] = []

        self.levellist: List[ApeEscapeLevel] = []
        self.entranceorder: List[ApeEscapeLevel] = []

        super(ApeEscapeWorld, self).__init__(multiworld, player)

    def generate_early(self) -> None:
        self.goal = self.options.goal.value
        self.logic = self.options.logic.value
        self.entrance = self.options.entrance.value
        self.unlocksperkey = self.options.unlocksperkey.value
        self.coin = self.options.coin.value
        self.gadget = self.options.gadget.value
        self.superflyer = self.options.superflyer.value
        self.shufflenet = self.options.shufflenet.value
        self.shufflewaternet = self.options.shufflewaternet.value
        self.itempool = []

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
        # progwaternet = self.create_item(AEItem.ProgWaterNet.value)
        watercatch = self.create_item(AEItem.WaterCatch.value)

        CB_Lamp = self.create_item(AEItem.CB_Lamp.value)
        DI_Lamp = self.create_item(AEItem.DI_Lamp.value)
        CrC_Lamp = self.create_item(AEItem.CrC_Lamp.value)
        CP_Lamp = self.create_item(AEItem.CP_Lamp.value)
        SF_Lamp = self.create_item(AEItem.SF_Lamp.value)
        TVT_Lobby_Lamp = self.create_item(AEItem.TVT_Lobby_Lamp.value)
        TVT_Tank_Lamp = self.create_item(AEItem.TVT_Tank_Lamp.value)
        MM_Lamp = self.create_item(AEItem.MM_Lamp.value)
        MMLobbyDoubleDoor = self.create_item(AEItem.MMLobbyDoubleDoor.value)

        self.itempool += [MMLobbyDoubleDoor]

        # Create enough keys to access every level, depending on the key option
        if self.options.unlocksperkey == 0x00:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 6)]
        elif self.options.unlocksperkey == 0x01:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 8)]
        elif self.options.unlocksperkey == 0x02:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 16)]
        elif self.options.unlocksperkey == 0x03:
            self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 18)]

        # Monkey Lamps shuffle
        if self.options.lamp == "false":
            self.multiworld.push_precollected(CB_Lamp)
            self.multiworld.push_precollected(DI_Lamp)
            self.multiworld.push_precollected(CrC_Lamp)
            self.multiworld.push_precollected(CP_Lamp)
            self.multiworld.push_precollected(SF_Lamp)
            self.multiworld.push_precollected(TVT_Lobby_Lamp)
            self.multiworld.push_precollected(TVT_Tank_Lamp)
            self.multiworld.push_precollected(MM_Lamp)
        else:
            self.itempool += [CB_Lamp]
            self.itempool += [DI_Lamp]
            self.itempool += [CrC_Lamp]
            self.itempool += [CP_Lamp]
            self.itempool += [SF_Lamp]
            self.itempool += [TVT_Lobby_Lamp]
            self.itempool += [TVT_Tank_Lamp]
            self.itempool += [MM_Lamp]

        # Water Net shuffle handling
        if self.options.shufflewaternet == "false":
            self.multiworld.push_precollected(waternet)
        else:
            self.itempool += [watercatch]
            self.itempool += [self.create_item(AEItem.ProgWaterNet.value)]
            self.itempool += [self.create_item(AEItem.ProgWaterNet.value)]

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
                warning(
                    f"Warning: selected options for {self.player_name} have no sphere 1 locations. Giving Time Net.")
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

        for _ in range(
                len(self.multiworld.get_unfilled_locations(self.player)) - len(self.itempool) - reservedlocations):
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
        firstroomids = [0x01, 0x02, 0x03, 0x06, 0x0B, 0x0F, 0x13, 0x14, 0x16, 0x18, 0x1D, 0x1E, 0x21, 0x24, 0x25, 0x28,
                        0x2D, 0x35, 0x38, 0x3F, 0x45, 0x57]
        orderedfirstroomids = []
        for x in range(0, 22):
            entranceids.append(self.entranceorder[x].entrance)
            orderedfirstroomids.append(firstroomids[self.entranceorder[x].vanillapos])
            bytestowrite += self.entranceorder[x].bytes
            bytestowrite.append(0)  # We need a separator byte after each level name.

        return {
            "goal": self.options.goal.value,
            "logic": self.options.logic.value,
            "entrance": self.options.entrance.value,
            "unlocksperkey": self.options.unlocksperkey.value,
            "coin": self.options.coin.value,
            "mailbox": self.options.mailbox.value,
            "gadget": self.options.gadget.value,
            "lamp": self.options.lamp.value,
            "superflyer": self.options.superflyer.value,
            "shufflenet": self.options.shufflenet.value,
            "shufflewaternet": self.options.shufflewaternet.value,
            "levelnames": bytestowrite,  # List of level names in entrance order. FF leads to the first.
            "entranceids": entranceids,  # Not used by the client. List of level ids in entrance order.
            "firstrooms": orderedfirstroomids,  # List of first rooms in entrance order.
            "reqkeys": get_required_keys(self.options.unlocksperkey.value),
        }

    def write_spoiler(self, spoiler_handle: TextIO):
        if self.options.entrance.value != 0x00:
            spoiler_handle.write(
                f"\n\nApe Escape entrance connections for {self.multiworld.get_player_name(self.player)}:")
            for x in range(0, 22):
                spoiler_handle.write(f"\n  {self.levellist[x].name} ==> {self.entranceorder[x].name}")
            spoiler_handle.write(f"\n")

    def generate_output(self, output_directory: str):
        data = {
            "slot_data": self.fill_slot_data()
        }
        # Remove .apae output because it does nothing, we do everything in RAM
        # filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apae"
        # with open(os.path.join(output_directory, filename), 'w') as f:
        #     json.dump(data, f)
