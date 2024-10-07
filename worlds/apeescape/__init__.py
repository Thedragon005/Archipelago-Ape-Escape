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
from .Regions import create_regions
from .Rules import set_rules
from .Client import ApeEscapeClient
from .Strings import AEItem, AELocation
from .RAMAddress import RAM
from .Options import ApeEscapeOptions


class ApeEscapeWeb(WebWorld):
    theme = "stone"

    # Verify this placeholder text is accurate
    setup = Tutorial(
        "Ape Escape Multiworld Setup Guide",
        "A guide to setting up Ape Escape in Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CDRomatron, Thedragon005, IHNN"]
    )

    tutorials = [setup]


class ApeEscapeWorld(World):
    """
    Go ape and catch Specter!
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
        self.coin: Optional[int] = 0
        self.gadget: Optional[int] = 0
        self.superflyer: Optional[int] = 0
        self.shufflenet: Optional[int] = 0
        self.itempool: List[ApeEscapeItem] = []

    def generate_early(self) -> None:
        self.goal = self.options.goal.value
        self.logic = self.options.logic.value
        self.coin = self.options.coin.value
        self.gadget = self.options.gadget.value
        self.superflyer = self.options.superflyer.value
        self.shufflenet = self.options.shufflenet.value
        self.itempool = []

    def generate_basic(self) -> None:
        club = self.create_item(AEItem.Club.value)
        net = self.create_item(AEItem.Net.value)
        radar = self.create_item(AEItem.Radar.value)
        shooter = self.create_item(AEItem.Sling.value)
        hoop = self.create_item(AEItem.Hoop.value)
        flyer = self.create_item(AEItem.Flyer.value)
        car = self.create_item(AEItem.Car.value)
        punch = self.create_item(AEItem.Punch.value)
        waternet = self.create_item(AEItem.WaterNet.value)

        if self.options.shufflenet == "true":
            # Condition to check if this is a 1 world multiworld
            if self.multiworld.players == 1:
                if self.options.coin == "true":
                    # If the net and coins are shuffled, manually place the net in one of the possible locations for it.
                    # Create a new collection state to test with.
                    netless_state = CollectionState(self.multiworld)
                    # Add the world keys (via item pool) to the testing state.
                    for item in [self.create_item(AEItem.Key.value) for _ in range(0, 6)]:
                        netless_state.collect(item)
                    # Add the other gadgets to the testing state.
                    for item in [waternet, club, radar, shooter, hoop, flyer, car, punch]:
                        netless_state.collect(item)
                    netless_state.update_reachable_regions(self.player)
                    # Determine what locations are reachable without the net.
                    net_locations = self.multiworld.get_reachable_locations(netless_state, self.player)
                    print(net_locations)
                    # Place the net in a random one of these locations. Could also use forbid_item instead - iterating through all locations to see if they're in reachable, and forbidding the ones that aren't. This should work for testing, though.
                    self.get_location(self.random.choice(net_locations).name).place_locked_item(net)
                    # Test code to force place the net in Gladiator Attack.
                    # self.get_location(AELocation.Coin36D.value).place_locked_item(net)

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

        self.itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 6)]

        if self.options.shufflenet == "false":
            self.multiworld.push_precollected(net)
        elif self.options.shufflenet == "true":
            # Condition to check if this is a 1 world multiworld
            if self.multiworld.players == 1:
                if self.options.coin == "true":
                    reservedlocations += 1
                elif self.options.coin == "false":
                    # if it is and coins are NOT shuffled: Throw a warning about incompatible options and just give the net anyway.
                    # If instead we want to error out and prevent generation, uncomment this line:
                    # raise OptionError(f"{self.player_name} has no sphere 1 locations!")
                    # TODO: error out or add mailboxes as locations in the future
                    warning(f"Warning: selected options for {self.player_name} have no sphere 1 locations. Giving Time Net.")
                    self.multiworld.push_precollected(net)
            else:
                # Throw a warning about potentially incompatible options (if generation fails, make sure at least world has net shuffle turned off.)
                warning(f"{self.player_name} has Net Shuffle on. If all players have Net Shuffle on, multiworlds will likely fail to generate.")

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
        return {
            "goal": self.options.goal.value,
            "logic": self.options.logic.value,
            "coin": self.options.coin.value,
            "gadget": self.options.gadget.value,
            "superflyer": self.options.superflyer.value,
            "shufflenet": self.options.shufflenet.value,
        }

    def generate_output(self, output_directory: str):
        data = {
            "slot_data": self.fill_slot_data()
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apae"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
