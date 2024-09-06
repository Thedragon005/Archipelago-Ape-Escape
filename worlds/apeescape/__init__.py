import math
import os
import json
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from BaseClasses import Item, ItemClassification, MultiWorld, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import item_table, ItemData, nothing_item_id, event_table, ApeEscapeItem
from .Locations import location_table, base_location_id
from .Regions import create_regions
from .Rules import set_rules
from .Client import ApeEscapeClient
from .Strings import AEItem, AELocation
from .RAMAddress import RAM
from .Options import ApeEscapeOptions, DebugOption, GoalOption, LogicOption, CoinOption
from Options import AssembleOptions


class ApeEscapeWeb(WebWorld):
    theme = "dirt"

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
        item_name_to_id[key] = value + 128000000

    location_name_to_id = location_table

    for key, value in location_name_to_id.items():
        location_name_to_id[key] = value + 128000000

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.game = "Ape Escape"
        self.debug: Optional[int] = 0
        self.goal: Optional[int] = 0
        self.logic: Optional[int] = 0
        self.coin: Optional[int] = 0
        self.gadget: Optional[int] = 0

    def generate_early(self) -> None:
        self.debug = self.options.debug
        self.goal = self.options.goal
        self.logic = self.options.logic
        self.coin = self.options.coin
        self.gadget = self.options.gadget

    def create_regions(self):
        create_regions(self.multiworld,self.options, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        item_id = item_table[name]
        classification = ItemClassification.progression

        item = ApeEscapeItem(name, classification, item_id, self.player)
        return item

    def create_item_filler(self, name: str) -> Item:
        item_id = item_table[name]
        classification = ItemClassification.filler

        item = ApeEscapeItem(name, classification, item_id, self.player)
        return item


    def create_items(self):
        numberoflocations = len(location_table)

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

        if self.multiworld.debug[self.player].value == 0x00:
            self.multiworld.itempool += [self.create_item(AEItem.Key.value) for i in range(0, 6)]
            numberoflocations -= 6
        # DEBUG
        elif self.multiworld.debug[self.player].value == 0x01:
            self.multiworld.push_precollected(club)
            self.multiworld.get_location(AELocation.Noonan.value, self.player).place_locked_item(radar)
            self.multiworld.get_location(AELocation.Jorjy.value, self.player).place_locked_item(shooter)
            self.multiworld.get_location(AELocation.Nati.value, self.player).place_locked_item(hoop)
            self.multiworld.get_location(AELocation.Shay.value, self.player).place_locked_item(flyer)
            self.multiworld.get_location(AELocation.DrMonk.value, self.player).place_locked_item(car)
            self.multiworld.get_location(AELocation.Ahchoo.value, self.player).place_locked_item(punch)
            self.multiworld.itempool += [self.create_item(AEItem.Key.value) for i in range(0, 6)]
            numberoflocations -= 12
        # DEBUG
        elif self.multiworld.debug[self.player].value == 0x02:
            self.multiworld.push_precollected(club)
            self.multiworld.itempool += [radar, shooter, hoop, flyer, car, punch]
            key1 = self.create_item("World Key")
            key2 = self.create_item("World Key")
            key3 = self.create_item("World Key")
            key4 = self.create_item("World Key")
            key5 = self.create_item("World Key")
            key6 = self.create_item("World Key")
            self.multiworld.get_location(AELocation.Noonan.value, self.player).place_locked_item(key1)
            self.multiworld.get_location(AELocation.Jorjy.value, self.player).place_locked_item(key2)
            self.multiworld.get_location(AELocation.Nati.value, self.player).place_locked_item(key3)
            self.multiworld.get_location(AELocation.Shay.value, self.player).place_locked_item(key4)
            self.multiworld.get_location(AELocation.DrMonk.value, self.player).place_locked_item(key5)
            self.multiworld.get_location(AELocation.Ahchoo.value, self.player).place_locked_item(key6)
            numberoflocations -= 12



        if self.multiworld.gadget[self.player].value == 0x00:
            self.multiworld.push_precollected(club)
            self.multiworld.itempool += [radar, shooter, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x01:
            self.multiworld.push_precollected(radar)
            self.multiworld.itempool += [club, shooter, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x02:
            self.multiworld.push_precollected(shooter)
            self.multiworld.itempool += [club, radar, hoop, flyer, car, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x03:
            self.multiworld.push_precollected(hoop)
            self.multiworld.itempool += [club, radar, shooter, flyer, car, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x04:
            self.multiworld.push_precollected(flyer)
            self.multiworld.itempool += [club, radar, shooter, hoop, car, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x05:
            self.multiworld.push_precollected(car)
            self.multiworld.itempool += [club, radar, shooter, hoop, flyer, punch]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x06:
            self.multiworld.push_precollected(punch)
            self.multiworld.itempool += [club, radar, shooter, hoop, flyer, car]
            numberoflocations -= 6
        elif self.multiworld.gadget[self.player].value == 0x08:
            self.multiworld.itempool += [club, radar, shooter, hoop, flyer, car, punch]
            numberoflocations -= 7



        if self.options.coin.value == 0x01:
            numberoflocations -= 60



        if self.options.goal.value == 0x00:
            self.multiworld.get_location(AELocation.Specter.value, self.player).place_locked_item(victory)
            numberoflocations -= 1
        else:
            self.multiworld.get_location(AELocation.Specter2.value, self.player).place_locked_item(victory)

        sixth = math.floor(numberoflocations/6)

        self.multiworld.itempool += [self.create_item_filler(AEItem.Shirt.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.Triangle.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.BigTriangle.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.Cookie.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.Flash.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.Rocket.value) for i in range(0, sixth)]
        numberoflocations -= sixth

        self.multiworld.itempool += [self.create_item_filler(AEItem.Nothing.value) for i in range(0, numberoflocations)]

    def fill_slot_data(self):
        return {
            "debug": self.options.debug.value,
            "goal": self.options.goal.value,
            "logic": self.options.logic.value,
            "coin": self.options.coin.value,
            "gadget": self.options.gadget.value,
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name]: item_table[i.item.name] for i in
                                 self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apae"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
