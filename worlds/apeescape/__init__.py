import math
import os
import json
from typing import ClassVar, List, Optional

from BaseClasses import ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import item_table, ApeEscapeItem
from .Locations import location_table, base_location_id
from .Regions import create_regions
from .Rules import set_rules
from .Client import ApeEscapeClient
from .Strings import AEItem, AELocation
from .RAMAddress import RAM
from .Options import ApeEscapeOptions


class ApeEscapeWeb(WebWorld):
    theme = "dirt"

    # Update this placeholder text to something more accurate
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Adventure for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CDRomatron"]
    )

    tutorials = [setup]


class ApeEscapeWorld(World):
    """
    Funni monke game
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

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.debug: Optional[int] = 0
        self.goal: Optional[int] = 0
        self.logic: Optional[int] = 0
        self.coin: Optional[int] = 0
        self.gadget: Optional[int] = 0
        self.superflyer: Optional[int] = 0

    def generate_early(self) -> None:
        self.debug = self.options.debug.value
        self.goal = self.options.goal.value
        self.logic = self.options.logic.value
        self.coin = self.options.coin.value
        self.gadget = self.options.gadget.value
        self.superflyer = self.options.superflyer.value

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
        numberoflocations = len(location_table)
        itempool: List[ApeEscapeItem] = []

        club = self.create_item(AEItem.Club.value)
        radar = self.create_item(AEItem.Radar.value)
        shooter = self.create_item(AEItem.Sling.value)
        hoop = self.create_item(AEItem.Hoop.value)
        flyer = self.create_item(AEItem.Flyer.value)
        car = self.create_item(AEItem.Car.value)
        punch = self.create_item(AEItem.Punch.value)
        victory = self.create_item(AEItem.Victory.value)

        waternet = self.create_item(AEItem.WaterNet.value)
        numberoflocations -= 1

        self.multiworld.push_precollected(waternet)

        if self.options.debug == "off":
            itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 6)]
            numberoflocations -= 6
        # DEBUG
        elif self.options.debug == "item":
            self.multiworld.push_precollected(club)
            self.get_location(AELocation.Noonan.value).place_locked_item(radar)
            self.get_location(AELocation.Jorjy.value).place_locked_item(shooter)
            self.get_location(AELocation.Nati.value).place_locked_item(hoop)
            self.get_location(AELocation.Shay.value).place_locked_item(flyer)
            self.get_location(AELocation.DrMonk.value).place_locked_item(car)
            self.get_location(AELocation.Ahchoo.value).place_locked_item(punch)
            itempool += [self.create_item(AEItem.Key.value) for _ in range(0, 6)]
            numberoflocations -= 12
        # DEBUG
        elif self.options.debug == "key":
            itempool += [
                self.create_item(AEItem.Club.value),
                self.create_item(AEItem.Radar.value),
                self.create_item(AEItem.Sling.value),
                self.create_item(AEItem.Hoop.value),
                self.create_item(AEItem.Flyer.value),
                self.create_item(AEItem.Car.value),
                self.create_item(AEItem.Punch.value),
            ]
            key1 = self.create_item("World Key")
            key2 = self.create_item("World Key")
            key3 = self.create_item("World Key")
            key4 = self.create_item("World Key")
            key5 = self.create_item("World Key")
            key6 = self.create_item("World Key")
            self.get_location(AELocation.Noonan.value).place_locked_item(key1)
            self.get_location(AELocation.Jorjy.value).place_locked_item(key2)
            self.get_location(AELocation.Nati.value).place_locked_item(key3)
            self.get_location(AELocation.Shay.value).place_locked_item(key4)
            self.get_location(AELocation.DrMonk.value).place_locked_item(key5)
            self.get_location(AELocation.Ahchoo.value).place_locked_item(key6)
            numberoflocations -= 13

        if self.options.gadget == "club":
            self.multiworld.push_precollected(club)
            itempool += [radar, shooter, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.options.gadget == "radar":
            self.multiworld.push_precollected(radar)
            itempool += [club, shooter, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.options.gadget == "sling":
            self.multiworld.push_precollected(shooter)
            itempool += [club, radar, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.options.gadget == "hoop":
            self.multiworld.push_precollected(hoop)
            itempool += [club, radar, shooter, flyer, car, punch]
            numberoflocations -= 6
        elif self.options.gadget == "flyer":
            self.multiworld.push_precollected(flyer)
            itempool += [club, radar, shooter, hoop, car, punch]
            numberoflocations -= 6
        elif self.options.gadget == "car":
            self.multiworld.push_precollected(car)
            itempool += [club, radar, shooter, hoop, flyer, punch]
            numberoflocations -= 6
        elif self.options.gadget == "punch":
            self.multiworld.push_precollected(punch)
            itempool += [club, radar, shooter, hoop, flyer, car]
            numberoflocations -= 6
        elif self.options.gadget == "none":
            itempool += [club, radar, shooter, hoop, flyer, car, punch]
            numberoflocations -= 7

        if self.options.coin == "false":
            numberoflocations -= 60

        if self.options.goal == "first":
            self.get_location(AELocation.Specter.value).place_locked_item(victory)
            numberoflocations -= 1
        else:
            self.get_location(AELocation.Specter2.value).place_locked_item(victory)

        sixth = math.floor(numberoflocations/6)

        itempool += [self.create_item_useful(AEItem.Shirt.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_filler(AEItem.Triangle.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_filler(AEItem.BigTriangle.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_filler(AEItem.Cookie.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_useful(AEItem.Flash.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_useful(AEItem.Rocket.value) for _ in range(0, sixth)]
        numberoflocations -= sixth

        itempool += [self.create_item_filler(AEItem.Triangle.value) for _ in range(0, numberoflocations)]

        self.multiworld.itempool += itempool

    def fill_slot_data(self):
        return {
            "debug": self.options.debug.value,
            "goal": self.options.goal.value,
            "logic": self.options.logic.value,
            "coin": self.options.coin.value,
            "gadget": self.options.gadget.value,
            "superflyer": self.options.superflyer.value,
        }

    def generate_output(self, output_directory: str):
        data = {
            "slot_data": self.fill_slot_data()
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apae"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
