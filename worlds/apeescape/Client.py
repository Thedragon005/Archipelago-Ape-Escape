import sys
import logging
from typing import TYPE_CHECKING, Optional, Dict, Set, ClassVar

from NetUtils import ClientStatus

# TODO: REMOVE ASAP - Borrowed from MM2
# This imports the bizhawk apworld if it's not already imported. This code block should be removed for a PR.
if "worlds._bizhawk" not in sys.modules:
    import importlib
    import os
    import zipimport

    bh_apworld_path = os.path.join(os.path.dirname(sys.modules["worlds"].__file__), "_bizhawk.apworld")
    if os.path.isfile(bh_apworld_path):
        importer = zipimport.zipimporter(bh_apworld_path)
        spec = importer.find_spec(os.path.basename(bh_apworld_path).rsplit(".", 1)[0])
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = f"worlds.{mod.__package__}"
        mod.__name__ = f"worlds.{mod.__name__}"
        sys.modules[mod.__name__] = mod
        importer.exec_module(mod)
    elif not os.path.isdir(os.path.splitext(bh_apworld_path)[0]):
        logging.error("Did not find _bizhawk.apworld required to play Ape Escape.")

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from worlds.apeescape.RAMAddress import RAM
from worlds.apeescape.Locations import hundoMonkeysCount
from worlds.apeescape.Options import GadgetOption, ShuffleNetOption

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

EXPECTED_ROM_NAME = "ape escape / AP 2"


# These flags are communicated to the tracker as a bitfield using this order.
# Modifying the order will cause undetectable autotracking issues.

class ApeEscapeClient(BizHawkClient):
    game = "Ape Escape"
    system = "PSX"
    local_checked_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_found_key_items: Dict[str, bool]
    goal_flag: int

    offset = 128000000
    levelglobal = 0
    roomglobal = 0
    worldkeycount = 0
    boss1flag = 0
    boss2flag = 0
    boss3flag = 0
    boss4flag = 0
    preventKickOut = True
    replacePunch = True
    currentCoinAddress = RAM.startingCoinAddress
    resetClient = False

    def __init__(self) -> None:
        super().__init__()

        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}

    def initialize_client(self):
        self.currentCoinAddress = RAM.startingCoinAddress
        self.preventKickOut = True
        self.replacePunch = True

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger
        ape_identifier_ram_address: int = 0xA37F0
        # BASCUS-94423SYS in ASCII = Ape Escape I think??
        bytes_expected: bytes = bytes.fromhex("4241534355532D3934343233535953")
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                ape_identifier_ram_address, len(bytes_expected), "MainRAM"
            )]))[0]
            if bytes_actual != bytes_expected:
                return False
        except Exception:
            return False

        if not self.game == "Ape Escape":
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        x = 3

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        # Detects if the AP connection is made.
        # If not,"return" immediately to not send anything while not connected
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.auth is None:
            self.initClient = False
            return
        # Detection for triggering "initialise_client()" when Disconnecting/Reconnecting to AP (only once per connection)
        if self.initClient == False:
            self.initClient = True
            self.initialize_client()
        try:
            earlyReadTuples = [
                (RAM.energyChipsAddress, 1, "MainRAM"),
                (RAM.cookieAddress, 1, "MainRAM"),
                (RAM.livesAddress, 1, "MainRAM"),
                (RAM.flashAddress, 1, "MainRAM"),
                (RAM.rocketAddress, 1, "MainRAM"),
                (RAM.keyCountFromServer, 1, "MainRAM"),
                (RAM.lastReceivedArchipelagoID, 4, "MainRAM"),
                (RAM.gadgetStateFromServer, 2, "MainRAM"),
                (RAM.gameStateAddress, 1, "MainRAM"),
                (RAM.menuStateAddress,1, "MainRAM"),
                (RAM.menuState2Address, 1, "MainRAM")
            ]
            itemsWrites = []
            # All reads that are required BEFORE connecting/early
            earlyReads = await bizhawk.read(ctx.bizhawk_ctx, earlyReadTuples)

            energyChips = int.from_bytes(earlyReads[0], byteorder="little")
            cookies = int.from_bytes(earlyReads[1], byteorder="little")
            totalLives = int.from_bytes(earlyReads[2], byteorder="little")
            flashAmmo = int.from_bytes(earlyReads[3], byteorder="little")
            rocketAmmo = int.from_bytes(earlyReads[4], byteorder="little")
            keyCountFromServer = int.from_bytes(earlyReads[5], byteorder="little")
            recv_index = int.from_bytes(earlyReads[6], byteorder="little")
            gadgetStateFromServer = int.from_bytes(earlyReads[7], byteorder="little")
            gameState = int.from_bytes(earlyReads[8], byteorder="little")
            menuState = int.from_bytes(earlyReads[9], byteorder="little")
            menuState2 = int.from_bytes(earlyReads[10], byteorder="little")

            # Set Initial received_ID when in first level ever OR in first hub ever
            if (recv_index == 0xFFFFFFFF) or (recv_index == 0x00FF00FF):
                recv_index = 0
                # Set gadgetStateFromServer to default if you connect in first level/first time hub
                if gadgetStateFromServer == 0xFFFF or gadgetStateFromServer == 0x00FF:
                    gadgetStateFromServer = 0

            if keyCountFromServer == 0xFF:
                # Get items from server
                keyCountFromServer = 0

            START_recv_index = recv_index

            # Prevent sending items when connecting early (Sony,Menu or Intro Cutscene)
            boolIsFirstBoot = gameState == RAM.gameState["Sony"] or gameState == RAM.gameState["Menu"] or gameState == RAM.gameState["Cutscene2"]
            if recv_index < (len(ctx.items_received)) and not boolIsFirstBoot:
                increment = 0
                for item in ctx.items_received :
                    # Increment to already received address first before sending
                    if increment < START_recv_index:
                        increment += 1
                    else:
                        recv_index += 1
                        if RAM.items["Club"] <= (item.item - self.offset) <= RAM.items["Car"]:
                            if gadgetStateFromServer | (item.item - self.offset) != gadgetStateFromServer:
                                gadgetStateFromServer = gadgetStateFromServer | (item.item - self.offset)
                        elif item.item - self.offset == RAM.items["Key"]:
                            keyCountFromServer += 1
                        elif item.item - self.offset == RAM.items["Victory"]:
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])
                        elif RAM.items["Shirt"] <= (item.item - self.offset) <= RAM.items["ThreeRocket"]:
                            if (item.item - self.offset) == RAM.items["Triangle"] or (item.item - self.offset) == RAM.items["BigTriangle"] or (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                if (item.item - self.offset) == RAM.items["Triangle"]:
                                    energyChips += 1
                                elif (item.item - self.offset) == RAM.items["BigTriangle"]:
                                    energyChips += 5
                                elif (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                    energyChips += 25
                                # If total gets greater than 100,subtract 100 and give a life instead
                                if energyChips >= 100:
                                    energyChips = energyChips - 100
                                    # Don't give a life if it would exceed 99 lives
                                    if totalLives < 100:
                                        totalLives += 1
                            elif (item.item - self.offset) == RAM.items["Cookie"]:
                                if cookies < 5:
                                    cookies += 1
                            elif (item.item - self.offset) == RAM.items["FiveCookies"]:
                                cookies = 5
                            elif (item.item - self.offset) == RAM.items["Shirt"]:
                                if totalLives < 100:
                                    totalLives += 1
                            # add special pellets, ensuring they don't go over the current cap
                            elif (item.item - self.offset) == RAM.items["Flash"]:
                                if flashAmmo < 9:
                                    flashAmmo += 1
                            elif (item.item - self.offset) == RAM.items["Rocket"]:
                                if rocketAmmo < 9:
                                    rocketAmmo += 1
                            elif (item.item - self.offset) == RAM.items["ThreeFlash"]:
                                flashAmmo += 3
                                if flashAmmo > 9:
                                    flashAmmo = 9
                            elif (item.item - self.offset) == RAM.items["ThreeRocket"]:
                                rocketAmmo += 3
                                if rocketAmmo > 9:
                                    rocketAmmo = 9

                # Writes to memory if there is a new item,after the loop
                itemsWrites += [(RAM.lastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempLastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM")]
                itemsWrites += [(RAM.energyChipsAddress, energyChips.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.cookieAddress, cookies.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.livesAddress, totalLives.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.flashAddress, flashAmmo.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.rocketAddress, rocketAmmo.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.keyCountFromServer, keyCountFromServer.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempKeyCountFromServer, keyCountFromServer.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.gadgetStateFromServer, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempGadgetStateFromServer, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM")]

            self.worldkeycount = keyCountFromServer

            # Read Array
            # 0: Hundo monkey count, to write to required count
            # 1: Gadget unlocked states
            # 2: Current Room
            # 3: Current Game state
            # 4: Jake Races Victory state
            # 5: Current Level
            # 6: Previous Coin State Room
            # 7: Current New Coin State Room
            # 8: Coin Count
            # 9: Currently held gadget
            # 10-13: Gadget equipped to each face button

            readTuples = [
                (RAM.hundoApesAddress, 1, "MainRAM"),
                (RAM.unlockedGadgetsAddress, 1, "MainRAM"),
                (RAM.currentRoomIdAddress, 1, "MainRAM"),
                (RAM.jakeVictoryAddress, 1, "MainRAM"),
                (RAM.currentLevelAddress, 1, "MainRAM"),
                (self.currentCoinAddress -2, 1, "MainRAM"),
                (self.currentCoinAddress, 1, "MainRAM"),
                (RAM.totalCoinsAddress, 1, "MainRAM"),
                (RAM.heldGadgetAddress, 1, "MainRAM"),
                (RAM.triangleGadgetAddress, 1, "MainRAM"),
                (RAM.squareGadgetAddress, 1, "MainRAM"),
                (RAM.circleGadgetAddress, 1, "MainRAM"),
                (RAM.crossGadgetAddress, 1, "MainRAM"),
                (RAM.gadgetUseStateAddress, 1, "MainRAM"),
                (RAM.requiredApesAddress, 1, "MainRAM"),
                (RAM.currentApesAddress, 1, "MainRAM"),
                (RAM.spikeStateAddress, 1, "MainRAM"),
                (RAM.roomStatus, 1, "MainRAM"),
                (RAM.S1_P2_State, 1, "MainRAM"),
                (RAM.S1_P2_Life, 1, "MainRAM"),
                (RAM.S2_isCaptured, 1, "MainRAM"),

            ]

            reads = await bizhawk.read(ctx.bizhawk_ctx, readTuples)

            levelCountTuples = [
                (RAM.levelMonkeyCount[11], 1, "MainRAM"),
                (RAM.levelMonkeyCount[12], 1, "MainRAM"),
                (RAM.levelMonkeyCount[13], 1, "MainRAM"),
                (RAM.levelMonkeyCount[21], 1, "MainRAM"),
                (RAM.levelMonkeyCount[22], 1, "MainRAM"),
                (RAM.levelMonkeyCount[23], 1, "MainRAM"),
                (RAM.levelMonkeyCount[41], 1, "MainRAM"),
                (RAM.levelMonkeyCount[42], 1, "MainRAM"),
                (RAM.levelMonkeyCount[43], 1, "MainRAM"),
                (RAM.levelMonkeyCount[51], 1, "MainRAM"),
                (RAM.levelMonkeyCount[52], 1, "MainRAM"),
                (RAM.levelMonkeyCount[53], 1, "MainRAM"),
                (RAM.levelMonkeyCount[71], 1, "MainRAM"),
                (RAM.levelMonkeyCount[72], 1, "MainRAM"),
                (RAM.levelMonkeyCount[73], 1, "MainRAM"),
                (RAM.levelMonkeyCount[81], 1, "MainRAM"),
                (RAM.levelMonkeyCount[82], 1, "MainRAM"),
                (RAM.levelMonkeyCount[83], 1, "MainRAM"),
                (RAM.levelMonkeyCount[91], 1, "MainRAM")
            ]
            monkeylevelcounts = await bizhawk.read(ctx.bizhawk_ctx, levelCountTuples)

            localhundoCount = int.from_bytes(reads[0], byteorder="little")
            gadgets = int.from_bytes(reads[1], byteorder="little")
            currentRoom = int.from_bytes(reads[2], byteorder="little")
            jakeVictory = int.from_bytes(reads[3], byteorder="little")
            currentLevel = int.from_bytes(reads[4], byteorder="little")
            previousCoinStateRoom = int.from_bytes(reads[5], byteorder="little")
            currentCoinStateRoom = int.from_bytes(reads[6], byteorder="little")
            coinCount = int.from_bytes(reads[7], byteorder="little")
            heldGadget = int.from_bytes(reads[8], byteorder="little")
            triangleGadget = int.from_bytes(reads[9], byteorder="little")
            squareGadget = int.from_bytes(reads[10], byteorder="little")
            circleGadget = int.from_bytes(reads[11], byteorder="little")
            crossGadget = int.from_bytes(reads[12], byteorder="little")
            gadgetUseState = int.from_bytes(reads[13], byteorder="little")
            requiredApes = int.from_bytes(reads[14], byteorder="little")
            currentApes = int.from_bytes(reads[15], byteorder="little")
            spikeState = int.from_bytes(reads[16], byteorder="little")
            roomStatus = int.from_bytes(reads[17], byteorder="little")
            gotMail = int.from_bytes(reads[18], byteorder="little")
            mailboxID = int.from_bytes(reads[19], byteorder="little")
            S1_P2_State = int.from_bytes(reads[20], byteorder="little")
            S1_P2_Life = int.from_bytes(reads[21], byteorder="little")
            S2_isCaptured = int.from_bytes(reads[22], byteorder="little")

            # Local update conditions
            # Condition to not update on first pass of client (self.roomglobal is 0 on first pass)
            if self.roomglobal == 0:
                localcondition = False
            else:
                localcondition = (currentLevel == self.levelglobal)

            # Stock BossRooms in a variable (For excluding these rooms in local monkeys sending)
            bossRooms = RAM.bossListLocal.keys()
            # Check if in level select or in time hub, then read global monkeys
            if gameState == RAM.gameState["LevelSelect"] or currentLevel == RAM.levels["Time"]:
                keyList = list(RAM.monkeyListGlobal.keys())
                valList = list(RAM.monkeyListGlobal.values())

                addresses = []

                for val in valList:
                    tuple1 = (val, 1, "MainRAM")
                    addresses.append(tuple1)

                globalMonkeys = await bizhawk.read(ctx.bizhawk_ctx, addresses)
                monkeysToSend = set()

                for i in range(len(globalMonkeys)):
                    if int.from_bytes(globalMonkeys[i], byteorder='little') == RAM.caughtStatus["PrevCaught"]:
                        monkeysToSend.add(keyList[i] + self.offset)

                if monkeysToSend is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in monkeysToSend)
                    }])

            # elif being in a level
            # check if NOT in a boss room since there is no monkeys to send there
            elif gameState == RAM.gameState["InLevel"] and (localcondition) and not(currentRoom in bossRooms):
                monkeyaddrs = RAM.monkeyListLocal[currentRoom]
                key_list = list(monkeyaddrs.keys())
                val_list = list(monkeyaddrs.values())
                addresses = []

                for val in val_list:
                    tuple1 = (val, 1, "MainRAM")
                    addresses.append(tuple1)

                localmonkeys = await bizhawk.read(ctx.bizhawk_ctx, addresses)
                monkeys_to_send = set()

                for i in range(len(localmonkeys)):
                    if int.from_bytes(localmonkeys[i], byteorder='little') == RAM.caughtStatus["Caught"]:
                        monkeys_to_send.add(key_list[i] + self.offset)

                if monkeys_to_send is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in monkeys_to_send)
                    }])
            # Check for level bosses
            if gameState == RAM.gameState["InLevel"] and (localcondition) and (currentRoom in bossRooms):
                bossaddrs = RAM.bossListLocal[currentRoom]
                key_list = list(bossaddrs.keys())
                val_list = list(bossaddrs.values())
                addresses = []

                for val in val_list:
                    tuple1 = (val, 1, "MainRAM")
                    addresses.append(tuple1)

                bossesList = await bizhawk.read(ctx.bizhawk_ctx, addresses)
                bosses_to_send = set()

                for i in range(len(bossesList)):
                    # For TVT boss,check roomStatus if it's 3 the fight is ongoing
                    if (currentRoom == 68):
                        print(roomStatus)
                        if (roomStatus == 3 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                            bosses_to_send.add(key_list[i] + self.offset)
                    else:
                        if int.from_bytes(bossesList[i], byteorder='little') == 0x00:
                            bosses_to_send.add(key_list[i] + self.offset)

                if bosses_to_send is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in bosses_to_send)
                    }])


            # Check for victory conditions
            specter1Condition = (currentRoom == 86 and S1_P2_State == 1 and S1_P2_Life == 0)
            specter2Condition = (currentRoom == 87 and S2_isCaptured == 1)
            if RAM.gameState["InLevel"] == gameState and specter1Condition:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(x for x in [self.offset + 205])
                }])

            if RAM.gameState["InLevel"] == gameState and specter2Condition:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(x for x in [self.offset + 206])
                }])

            # If the previous address is empty it means you are too far,go back once
            # Happens in case of save-states or loading a previous save file that did not collect the same amount of coins
            if (previousCoinStateRoom == 0xFF or previousCoinStateRoom == 0x00) and (self.currentCoinAddress > RAM.startingCoinAddress):
                self.currentCoinAddress -= 2
            # Check for new coins from current coin address
            if currentCoinStateRoom != 0xFF and currentCoinStateRoom != 0x00:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(x for x in [currentCoinStateRoom + self.offset + 300])
                }])
                self.currentCoinAddress += 2

            # Check for Jake Victory
            if currentRoom == 19 and gameState == RAM.gameState["JakeCleared"] and jakeVictory == 0x2:
                coins = set()
                coins.add(295 + self.offset)
                coins.add(296 + self.offset)
                coins.add(297 + self.offset)
                coins.add(298 + self.offset)
                coins.add(299 + self.offset)
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(x for x in coins)
                }])
            elif currentRoom == 36 and gameState == RAM.gameState["JakeCleared"] and jakeVictory == 0x2:
                coins = set()
                coins.add(290 + self.offset)
                coins.add(291 + self.offset)
                coins.add(292 + self.offset)
                coins.add(293 + self.offset)
                coins.add(294 + self.offset)
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(x for x in coins)
                }])

            # Write Array
            # Training Room, set to 0xFF to mark as complete
            # Gadgets unlocked
            # Required apes (to match hundo)
            # Local apes first room (optional: for if in hub)
            # unlockLevels()

            writes = [
                (RAM.trainingRoomProgressAddress, 0xFF.to_bytes(1, "little"), "MainRAM"),
                (RAM.unlockedGadgetsAddress, gadgetStateFromServer.to_bytes(1, "little"), "MainRAM"),
                (RAM.requiredApesAddress, localhundoCount.to_bytes(1, "little"), "MainRAM"),
            ]

            # Unequip the Time Net if it was shuffled. 
            if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true:
                if (crossGadget == 1) and (gadgetStateFromServer & 2 == 0):
                    writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]

            # Equip the selected starting gadget onto the triangle button. Stun Club is the default and doesn't need changing. Additionally, in the "none" case, switch the selection to the Time Net if it wasn't shuffled.
            if ((heldGadget == 0) and (gadgetStateFromServer % 2 == 0)):
                if ctx.slot_data["gadget"] == GadgetOption.option_radar:
                    writes += [(RAM.triangleGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_sling:
                    writes += [(RAM.triangleGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_hoop:
                    writes += [(RAM.triangleGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_flyer:
                    writes += [(RAM.triangleGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_car:
                    writes += [(RAM.triangleGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_punch:
                    writes += [(RAM.triangleGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.heldGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["gadget"] == GadgetOption.option_none:
                    writes += [(RAM.triangleGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                    if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true:
                        writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                    elif ctx.slot_data["shufflenet"] == ShuffleNetOption.option_false:
                        writes += [(RAM.heldGadgetAddress, 0x01.to_bytes(1, "little"), "MainRAM")]

            # Punch Visual glitch in menu fix
            if (menuState == 0) and (menuState2 == 1):
                # Replace all values from 0x0E78C0 to 0x0E78DF to this:
                # 0010000000000000E00B00000000000000100000000000000000000000000000
                if ((gadgetStateFromServer & 32) == 32) and self.replacePunch == True:
                    bytes_ToWrite: bytes = bytes.fromhex("0010000000000000E00B00000000000000100000000000000000000000000000")
                    writes += [(RAM.punchVisualAddress, bytes_ToWrite, "MainRAM")]
                    self.replacePunch = False
            else:
                self.replacePunch = True

            # If the current level is Gladiator Attack, the Sky Flyer is currently equipped, and the player does not have the Sky Flyer: unequip it
            if ((currentLevel == 0x0E) and (heldGadget == 6) and ((gadgetStateFromServer & 64 == 0))):
                writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]

            if gameState == RAM.gameState["LevelSelect"]:
                writes += [(RAM.localApeStartAddress, 0x0.to_bytes(8, "little"), "MainRAM")]

            level_info = [currentApes,requiredApes,currentLevel,localhundoCount]
            writes += self.unlockLevels(monkeylevelcounts, gadgets,gameState,gadgetUseState,level_info,hundoMonkeysCount,spikeState)

            await bizhawk.write(ctx.bizhawk_ctx, writes)
            await bizhawk.write(ctx.bizhawk_ctx, itemsWrites)

            self.levelglobal = currentLevel
            self.roomglobal = currentRoom

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    def unlockLevels(self, monkeylevelCounts, gadgets,gameState,gadgetUseState,level_info,hundoMonkeysCount,spikeState):

        key = self.worldkeycount
        curApesWrite = ""
        reqApesWrite = ""
        hundoWrite = ""
        currentApes = level_info[0]
        requiredApes = level_info[1]
        currentLevel = level_info[2]
        localhundoCount = level_info[3]
        W2UnLock = key >= 1
        W3UnLock = key >= 2
        W4UnLock = key >= 3
        W5UnLock = key >= 3
        W6UnLock = key >= 4
        W7UnLock = key >= 5
        W8UnLock = key >= 5
        W9UnLock = key >= 6
        allCompleted = True

        debug = False

        levels_keys = hundoMonkeysCount.keys()
        levels_list = list(levels_keys)
        if gameState == RAM.gameState["LevelSelect"] or debug:
            for x in range(len(levels_list)):
                if int.from_bytes(monkeylevelCounts[x], byteorder="little") < hundoMonkeysCount[levels_list[x]]:
                    print("Level " + str(x) + " not completed" + str(int.from_bytes(monkeylevelCounts[x])) + "/" + str(hundoMonkeysCount[levels_list[x]]))
                    allCompleted = False
                    break
                    # Does not need to know the rest of the levels,at least 1 in not completed

        PPMUnlock = key >= 6 and allCompleted
        # Tried my hand at blocking ALL kick-outs
        # Put the 100% monkeys count from each level into an array for easier access

        # If in any level,prevent Kick-out
        if gameState == RAM.gameState["InLevel"] and (currentLevel in levels_keys):
            # I've been told a dupe glitch exist.
            # To keep it fair, reduce the number of current monkeys if it goes higher than max
            if currentApes > hundoMonkeysCount[currentLevel]:
                curApesWrite = (RAM.currentApesAddress, hundoMonkeysCount[currentLevel].to_bytes(1, byteorder="little"), "MainRAM")
                currentApes = hundoMonkeysCount[currentLevel]
            # If the Kick out prevention is up,detect the number of monkeys and add 1 to prevent kickout
            if self.preventKickOut:
                if spikeState == 2 or spikeState == 132 or gadgetUseState == 8:
                    if currentApes == localhundoCount:
                        reqApesWrite = (RAM.requiredApesAddress, (hundoMonkeysCount[currentLevel] + 1).to_bytes(1, byteorder="little"), "MainRAM")
                        hundoWrite = (RAM.hundoApesAddress, (hundoMonkeysCount[currentLevel] + 1).to_bytes(1, byteorder="little"), "MainRAM")
                # After catching is over set the requiredApes back to normal amount and disable Kick out Prevention
                else:
                    if (currentApes >= requiredApes) or (requiredApes >= (hundoMonkeysCount[currentLevel] + 1)):
                        reqApesWrite = (RAM.requiredApesAddress, hundoMonkeysCount[currentLevel].to_bytes(1, byteorder="little"), "MainRAM")
                        hundoWrite = (RAM.hundoApesAddress, hundoMonkeysCount[currentLevel].to_bytes(1, byteorder="little"), "MainRAM")
                        self.preventKickOut = False
            elif self.preventKickOut == False and currentApes < hundoMonkeysCount[currentLevel]:
                self.preventKickOut = True
        # Reset Kickout prevention if leaving level
        elif gameState != RAM.gameState["InLevel"] and self.preventKickOut == False:
            self.preventKickOut = True

        current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
        currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        if key > 0:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")

        w11 = (RAM.levelAddresses[11], current, "MainRAM")
        w12 = (RAM.levelAddresses[12], current, "MainRAM")
        w13 = (RAM.levelAddresses[13], currentLock, "MainRAM")

        if key == 1:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        elif key > 1:
            current = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
        else:
            current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w21 = (RAM.levelAddresses[21], current, "MainRAM")
        w22 = (RAM.levelAddresses[22], current, "MainRAM")
        w23 = (RAM.levelAddresses[23], currentLock, "MainRAM")

        if key == 2:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        elif key > 2:
            current = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
        else:
            current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w31 = (RAM.levelAddresses[31], current, "MainRAM")
        w41 = (RAM.levelAddresses[41], current, "MainRAM")
        w42 = (RAM.levelAddresses[42], current, "MainRAM")
        w43 = (RAM.levelAddresses[43], currentLock, "MainRAM")
        if key == 3:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        elif key > 3:
            current = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")

        else:
            current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w51 = (RAM.levelAddresses[51], current, "MainRAM")
        w52 = (RAM.levelAddresses[52], current, "MainRAM")
        w53 = (RAM.levelAddresses[53], currentLock, "MainRAM")

        if key == 4:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        elif key > 4:
            current = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
        else:
            current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w61 = (RAM.levelAddresses[61], current, "MainRAM")
        w71 = (RAM.levelAddresses[71], current, "MainRAM")
        w72 = (RAM.levelAddresses[72], current, "MainRAM")
        w73 = (RAM.levelAddresses[73], currentLock, "MainRAM")

        if key == 5:
            current = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        elif key > 5:
            current = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Complete"].to_bytes(1, byteorder="little")
        else:
            current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
            currentLock = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w81 = (RAM.levelAddresses[81], current, "MainRAM")
        w82 = (RAM.levelAddresses[82], current, "MainRAM")
        w83 = (RAM.levelAddresses[83], currentLock, "MainRAM")

        # if key >= 6:
        # Changed to make it locked by default,then it will change to 100% Completed if all monkeys caught and Keys >= 6
        # It will also unlock with level 8-3 being Open or 100% Complete
        current = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")

        w91 = (RAM.levelAddresses[91], current, "MainRAM")

        if int.from_bytes(monkeylevelCounts[0], byteorder="little") >= hundoMonkeysCount[levels_list[0]]:
            w11 = (RAM.levelAddresses[11], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[1], byteorder="little") >= hundoMonkeysCount[levels_list[1]]:
            w12 = (RAM.levelAddresses[12], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[2], byteorder="little") >= hundoMonkeysCount[levels_list[2]] and W2UnLock:
            w13 = (RAM.levelAddresses[13], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[3], byteorder="little") >= hundoMonkeysCount[levels_list[3]]:
            w21 = (RAM.levelAddresses[21], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[4], byteorder="little") >= hundoMonkeysCount[levels_list[4]]:
            w22 = (RAM.levelAddresses[22], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[5], byteorder="little") >= hundoMonkeysCount[levels_list[5]] and W3UnLock:
            w23 = (RAM.levelAddresses[23], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[6], byteorder="little") >= hundoMonkeysCount[levels_list[6]]:
            w41 = (RAM.levelAddresses[41], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[7], byteorder="little") >= hundoMonkeysCount[levels_list[7]]:
            w42 = (RAM.levelAddresses[42], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[8], byteorder="little") >= hundoMonkeysCount[levels_list[8]] and W5UnLock:
            w43 = (RAM.levelAddresses[43], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[9], byteorder="little") >= hundoMonkeysCount[levels_list[9]]:
            w51 = (RAM.levelAddresses[51], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[10], byteorder="little") >= hundoMonkeysCount[levels_list[10]]:
            w52 = (RAM.levelAddresses[52], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[11], byteorder="little") >= hundoMonkeysCount[levels_list[11]] and W6UnLock:
            w53 = (RAM.levelAddresses[53], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[12], byteorder="little") >= hundoMonkeysCount[levels_list[12]]:
            w71 = (RAM.levelAddresses[71], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[13], byteorder="little") >= hundoMonkeysCount[levels_list[13]]:
            w72 = (RAM.levelAddresses[72], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[14], byteorder="little") >= hundoMonkeysCount[levels_list[14]] and W8UnLock:
            w73 = (RAM.levelAddresses[73], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[15], byteorder="little") >= hundoMonkeysCount[levels_list[15]]:
            w81 = (RAM.levelAddresses[81], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[16], byteorder="little") >= hundoMonkeysCount[levels_list[16]]:
            w82 = (RAM.levelAddresses[82], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[17], byteorder="little") >= hundoMonkeysCount[levels_list[17]] and W9UnLock:
            w83 = (RAM.levelAddresses[83], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")

        if int.from_bytes(monkeylevelCounts[18], byteorder="little") >= hundoMonkeysCount[levels_list[18]] and PPMUnlock:
            w91 = (RAM.levelAddresses[91], RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little"), "MainRAM")
        # If there is a change in required monkeys count,include it in the writes
        returns = [w11, w12, w13, w21, w22, w23, w31, w41, w42, w43, w51, w52, w53, w61, w71, w72, w73, w81, w82, w83,
                    w91]
        if curApesWrite != "":
            returns.append(curApesWrite)
        if reqApesWrite != "":
            returns.append(reqApesWrite)
        if hundoWrite != "":
            returns.append(hundoWrite)
        return returns
