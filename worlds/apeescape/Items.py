from typing import Optional, Dict, Set
from BaseClasses import ItemClassification, Item
from .Strings import AEItem
from .RAMAddress import RAM

base_apeescape_item_id = 128000000


class ApeEscapeItem(Item):
    game: str = "Ape Escape"

GROUPED_ITEMS: Dict[str, Set[str]] = {}

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
    AEItem.WaterNet.value: RAM.items["WaterNet"],
    AEItem.ProgWaterNet.value: RAM.items["ProgWaterNet"],
    AEItem.WaterCatch.value: RAM.items["WaterCatch"],

    # Keys
    AEItem.Key.value: RAM.items["Key"],
    AEItem.Victory.value: RAM.items["Victory"],

    # Monkey Lamps
    AEItem.CB_Lamp.value: RAM.items["CB_Lamp"],
    AEItem.DI_Lamp.value: RAM.items["DI_Lamp"],
    AEItem.CrC_Lamp.value: RAM.items["CrC_Lamp"],
    AEItem.CP_Lamp.value: RAM.items["CP_Lamp"],
    AEItem.SF_Lamp.value: RAM.items["SF_Lamp"],
    AEItem.TVT_Lobby_Lamp.value: RAM.items["TVT_Lobby_Lamp"],
    AEItem.TVT_Tank_Lamp.value: RAM.items["TVT_Tank_Lamp"],
    AEItem.MM_Lamp.value: RAM.items["MM_Lamp"],

    #Locks
    AEItem.MMLobbyDoubleDoor.value: RAM.items["MMLobbyDoubleDoor"],

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
    AEItem.ThreeRocket.value: RAM.items["ThreeRocket"]
}

# Tables to check which Item is needed for which level depending on Lamps



event_table = {
}

def createItemGroups():
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Stun Club")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Time Net")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Monkey Radar")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Slingback Shooter")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Super Hoop")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Magic Punch")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Sky Flyer")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("R.C. Car")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Water Net")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Progressive Water Net")
    GROUPED_ITEMS.setdefault("Gadgets", []).append("Water Catch")

    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.CB_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.DI_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.CrC_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.CP_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.TVT_Lobby_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.TVT_Tank_Lamp.value)
    GROUPED_ITEMS.setdefault("Lamps", []).append(AEItem.MM_Lamp.value)

createItemGroups()