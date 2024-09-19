from typing import Optional
from BaseClasses import ItemClassification, Item
from .Strings import AEItem
from .RAMAddress import RAM

base_apeescape_item_id = 128000000


class ApeEscapeItem(Item):
    game: str = "Ape Escape"


# base IDs are the index in the static item data table, which is
# not the same order as the items in RAM (but offset 0 is a 16-bit address of
# location of room and position data)
item_table = {
    # Gadgets
    AEItem.Club.value: RAM.items["Club"],
    AEItem.Net.value: RAM.items["Net"],
    AEItem.Radar.value: RAM.items["Radar"],
    AEItem.Sling.value: RAM.items["Sling"],
    AEItem.Hoop.value: RAM.items["Hoop"],
    AEItem.Punch.value: RAM.items["Punch"],
    AEItem.Flyer.value: RAM.items["Flyer"],
    AEItem.Car.value: RAM.items["Car"],

    AEItem.WaterNet.value: 0x400,

    # Keys
    AEItem.Key.value: RAM.items["Key"],
    AEItem.Victory.value: RAM.items["Victory"],

    # Junk
    AEItem.Nothing.value: RAM.items["Nothing"],
    AEItem.Shirt.value: RAM.items["Shirt"],
    AEItem.Triangle.value: RAM.items["Triangle"],
    AEItem.BigTriangle.value: RAM.items["BigTriangle"],
    AEItem.BiggerTriangle.value: RAM.items["BiggerTriangle"],
    AEItem.Cookie.value: RAM.items["Cookie"],
    AEItem.FiveCookies.value: RAM.items["FiveCookies"],
    AEItem.Flash.value: RAM.items["Flash"],
    AEItem.ThreeFlash.value: RAM.items["ThreeFlash"],
    AEItem.Rocket.value: RAM.items["Rocket"],
    AEItem.ThreeRocket.value: RAM.items["ThreeRocket"],
}

event_table = {
}
