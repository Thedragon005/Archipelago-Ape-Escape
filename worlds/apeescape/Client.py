import sys
import logging
import time
import Utils
from typing import TYPE_CHECKING, Optional, Dict, Set, ClassVar, Any, Tuple
from Options import Toggle
from NetUtils import ClientStatus
from worlds.oot.Patches import get_override_table_bytes

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
from worlds.apeescape.Options import GadgetOption, ShuffleNetOption, ShuffleWaterNetOption, CoinOption, MailboxOption, EntranceOption, KeyOption

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

    #TODO Remove when doing official PR
    client_version = "0.6.5"

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
    inWater = 0
    waternetState = 0
    watercatchState = 0

    def __init__(self) -> None:
        super().__init__()

        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}

    def initialize_client(self):
        self.currentCoinAddress = RAM.startingCoinAddress
        self.preventKickOut = True
        #self.replacePunch = True
        self.killPlayer = True
        self.inWater = 0
        self.waternetState = 0
        self.watercatchState = 0
        self.death_counter = None
        self.previous_death_link = 0
        self.pending_death_link: bool = False
        # default to true, as we don't want to send a deathlink until playing
        self.sending_death_link: bool = True
        self.ignore_next_death_link = False
        self.lowOxygenCounter = 0
        self.bool_lowOxygen = 0

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger
        ape_identifier_ram_address: int = 0xA37F0
        ape_identifier_ram_address_PAL: int = 0xA37F0
        # BASCUS-94423SYS in ASCII = Ape Escape I think??
        bytes_expected: bytes = bytes.fromhex("4241534355532D3934343233535953")
        bytes_expected_PAL:bytes = bytes.fromhex("4245534345532D3031353634535953")
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
        logger.info("================================================")
        logger.info("Archipelago Ape Escape version "  + self.client_version)
        logger.info("================================================")
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced":
            if "tags" in args:
                assert ctx.slot is not None
                if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    self.on_deathlink(ctx)


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
                (RAM.menuStateAddress, 1, "MainRAM"),
                (RAM.menuState2Address, 1, "MainRAM"),
                (RAM.newGameAddress, 1, "MainRAM"),
                (RAM.canDiveAddress, 4, "MainRAM"),
                (RAM.canWaterCatchAddress, 1, "MainRAM"),
                (RAM.tempWaterNetAddress, 1, "MainRAM"),
                (RAM.tempWaterCatchAddress, 1, "MainRAM")
            ]
            itemsWrites = []
            Menuwrites = []
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
            newGameAddress = int.from_bytes(earlyReads[11], byteorder="little")
            canDive = int.from_bytes(earlyReads[12], byteorder="little")
            canWaterCatch = int.from_bytes(earlyReads[13], byteorder="little")
            WaterNetStateFromServer = int.from_bytes(earlyReads[14], byteorder="little")
            WaterCatchStateFromServer = int.from_bytes(earlyReads[15], byteorder="little")

            #  When in Menu,change the behavior of "NewGame" to warp you to time station instead
            if gameState == RAM.gameState["Menu"] and newGameAddress == 0xAC:
                Menuwrites += [(RAM.newGameAddress, 0x98.to_bytes(1, "little"), "MainRAM")]
                Menuwrites += [(RAM.cookieAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                await bizhawk.write(ctx.bizhawk_ctx, Menuwrites)
            # Set Initial received_ID when in first level ever OR in first hub ever
            if (recv_index == 0xFFFFFFFF) or (recv_index == 0x00FF00FF):
                recv_index = 0
                # Set gadgetStateFromServer to default if you connect in first level/first time hub
                if gadgetStateFromServer == 0xFFFF or gadgetStateFromServer == 0x00FF:
                    gadgetStateFromServer = 0

            if keyCountFromServer == 0xFF:
                # Get items from server
                keyCountFromServer = 0

            # Get WaterNet state from memory
            waternetState = 0
            if WaterNetStateFromServer != 0xFF:
                waternetState = WaterNetStateFromServer

            # Get Dive state from memory
            watercatchState = 0
            if WaterCatchStateFromServer != 0x00:
                watercatchState = WaterCatchStateFromServer

            START_recv_index = recv_index

            # Prevent sending items when connecting early (Sony, Menu or Intro Cutscene)
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
                        elif (item.item - self.offset) == RAM.items["WaterNet"]:
                            waternetState = 2
                            watercatchState = 1
                        elif (item.item - self.offset) == RAM.items["ProgWaterNet"]:
                            if waternetState != 2:
                                waternetState += 1
                        elif (item.item - self.offset) == RAM.items["WaterCatch"]:
                            watercatchState  = 1
                        elif RAM.items["Shirt"] <= (item.item - self.offset) <= RAM.items["ThreeRocket"]:
                            if (item.item - self.offset) == RAM.items["Triangle"] or (item.item - self.offset) == RAM.items["BigTriangle"] or (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                if (item.item - self.offset) == RAM.items["Triangle"]:
                                    energyChips += 1
                                elif (item.item - self.offset) == RAM.items["BigTriangle"]:
                                    energyChips += 5
                                elif (item.item - self.offset) == RAM.items["BiggerTriangle"]:
                                    energyChips += 25
                                # If total gets greater than 100, subtract 100 and give a life instead
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


                # Writes to memory if there is a new item, after the loop
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
                itemsWrites += [(RAM.tempWaterNetAddress, waternetState.to_bytes(4, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempWaterCatchAddress, watercatchState.to_bytes(1, "little"), "MainRAM")]

            self.worldkeycount = keyCountFromServer

            # Read Array
            readTuples = [
                (RAM.hundoApesAddress, 1, "MainRAM"),  # Hundo monkey count, to write to required count
                (RAM.unlockedGadgetsAddress, 1, "MainRAM"),  # Gadget unlocked states
                (RAM.currentRoomIdAddress, 1, "MainRAM"),  # Current Room
                (RAM.jakeVictoryAddress, 1, "MainRAM"),  # Jake Races Victory state
                (RAM.currentLevelAddress, 1, "MainRAM"),  # Current Level
                (self.currentCoinAddress - 2, 1, "MainRAM"),  # Previous Coin State Room
                (self.currentCoinAddress, 1, "MainRAM"),  # Current New Coin State Room
                (RAM.totalCoinsAddress, 1, "MainRAM"),  # Coin Count
                (RAM.heldGadgetAddress, 1, "MainRAM"),  # Currently held gadget
                (RAM.triangleGadgetAddress, 1, "MainRAM"),  # Gadget equipped to each face button
                (RAM.squareGadgetAddress, 1, "MainRAM"),
                (RAM.circleGadgetAddress, 1, "MainRAM"),
                (RAM.crossGadgetAddress, 1, "MainRAM"),
                (RAM.gadgetUseStateAddress, 1, "MainRAM"),  # undocumented
                (RAM.requiredApesAddress, 1, "MainRAM"),
                (RAM.currentApesAddress, 1, "MainRAM"),
                (RAM.spikeStateAddress, 1, "MainRAM"),
                (RAM.spikeState2Address, 1, "MainRAM"),
                (RAM.kickoutofLevelAddress, 4, "MainRAM"),
                (RAM.roomStatus, 1, "MainRAM"),
                (RAM.gotMailAddress, 1, "MainRAM"),
                (RAM.mailboxIDAddress, 1, "MainRAM"),
                (RAM.swim_oxygenLevelAddress,2,"MainRAM"),
                (RAM.gameRunningAddress, 1, "MainRAM"),
                (RAM.S1_P2_State, 1, "MainRAM"),
                (RAM.S1_P2_Life, 1, "MainRAM"),
                (RAM.S2_isCaptured, 1, "MainRAM"),
                (RAM.selectedWorldAddress, 1, "MainRAM"),  # In level select, the current world
                (RAM.selectedLevelAddress, 1, "MainRAM"),  # In level select, the current level
                (RAM.enteredWorldAddress, 1, "MainRAM"),  # After selecting a level, the entered world
                (RAM.enteredLevelAddress, 1, "MainRAM"),  # After selecting a level, the entered level
                (RAM.isUnderwater, 1, "MainRAM"),  # Underwater variable
                (RAM.punchVisualAddress, 32, "MainRAM"),
                (RAM.transitionPhase,1,"MainRAM"),
                (RAM.Nearby_RoomID,1,"MainRAM")
            ]

            reads = await bizhawk.read(ctx.bizhawk_ctx, readTuples)

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
            spikeState2 = int.from_bytes(reads[17], byteorder="little")
            kickoutofLevel = int.from_bytes(reads[18], byteorder="little")
            roomStatus = int.from_bytes(reads[19], byteorder="little")
            gotMail = int.from_bytes(reads[20], byteorder="little")
            mailboxID = int.from_bytes(reads[21], byteorder="little")
            swim_oxygenLevel = int.from_bytes(reads[22], byteorder="little")
            gameRunning = int.from_bytes(reads[23], byteorder="little")
            S1_P2_State = int.from_bytes(reads[24], byteorder="little")
            S1_P2_Life = int.from_bytes(reads[25], byteorder="little")
            S2_isCaptured = int.from_bytes(reads[26], byteorder="little")
            LS_currentWorld = int.from_bytes(reads[27], byteorder="little")
            LS_currentLevel = int.from_bytes(reads[28], byteorder="little")
            status_currentWorld = int.from_bytes(reads[29], byteorder="little")
            status_currentLevel = int.from_bytes(reads[30], byteorder="little")
            isUnderwater = int.from_bytes(reads[31], byteorder="little")
            punchVisualAddress = int.from_bytes(reads[32], byteorder="little")
            transitionPhase = int.from_bytes(reads[33], byteorder="little")
            NearbyRoom = int.from_bytes(reads[34], byteorder="little")

            DL_Reads = [cookies,gameRunning,gameState]
            await self.handle_death_link(ctx,DL_Reads)

            CoinReadsTupples = [
                (RAM.startingCoinAddress,100,"MainRAM"),
                (RAM.temp_startingCoinAddress, 100, "MainRAM"),
                (RAM.SA_CompletedAddress, 1, "MainRAM"),
                (RAM.Temp_SA_CompletedAddress, 1, "MainRAM"),
                (RAM.GA_CompletedAddress, 1, "MainRAM"),
                (RAM.Temp_GA_CompletedAddress, 1, "MainRAM")
            ]

            CoinReads = await bizhawk.read(ctx.bizhawk_ctx, CoinReadsTupples)

            CoinTable = int.from_bytes(CoinReads[0], byteorder="little")
            TempCoinTable = int.from_bytes(CoinReads[1], byteorder="little")
            SA_Completed = int.from_bytes(CoinReads[2], byteorder="little")
            Temp_SA_Completed = int.from_bytes(CoinReads[3], byteorder="little")
            GA_Completed = int.from_bytes(CoinReads[4], byteorder="little")
            Temp_GA_Completed = int.from_bytes(CoinReads[5], byteorder="little")

            levelCountTuples = [
                (RAM.levelMonkeyCount[11], 1, "MainRAM"),
                (RAM.levelMonkeyCount[12], 1, "MainRAM"),
                (RAM.levelMonkeyCount[13], 1, "MainRAM"),
                (RAM.levelMonkeyCount[21], 1, "MainRAM"),
                (RAM.levelMonkeyCount[22], 1, "MainRAM"),
                (RAM.levelMonkeyCount[23], 1, "MainRAM"),
                (RAM.levelMonkeyCount[31], 1, "MainRAM"),
                (RAM.levelMonkeyCount[41], 1, "MainRAM"),
                (RAM.levelMonkeyCount[42], 1, "MainRAM"),
                (RAM.levelMonkeyCount[43], 1, "MainRAM"),
                (RAM.levelMonkeyCount[51], 1, "MainRAM"),
                (RAM.levelMonkeyCount[52], 1, "MainRAM"),
                (RAM.levelMonkeyCount[53], 1, "MainRAM"),
                (RAM.levelMonkeyCount[61], 1, "MainRAM"),
                (RAM.levelMonkeyCount[71], 1, "MainRAM"),
                (RAM.levelMonkeyCount[72], 1, "MainRAM"),
                (RAM.levelMonkeyCount[73], 1, "MainRAM"),
                (RAM.levelMonkeyCount[81], 1, "MainRAM"),
                (RAM.levelMonkeyCount[82], 1, "MainRAM"),
                (RAM.levelMonkeyCount[83], 1, "MainRAM"),
                (RAM.levelMonkeyCount[91], 1, "MainRAM")
            ]
            monkeylevelcounts = await bizhawk.read(ctx.bizhawk_ctx, levelCountTuples)

            # Local update conditions
            # Condition to not update on first pass of client (self.roomglobal is 0 on first pass)
            if self.roomglobal == 0:
                localcondition = False
            else:
                localcondition = (currentLevel == self.levelglobal)

            # Stock BossRooms in a variable (For excluding these rooms in local monkeys sending)
            bossRooms = RAM.bossListLocal.keys()
            mailboxesRooms = RAM.mailboxListLocal.keys()
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

                if monkeysToSend is not None and monkeysToSend != set():
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
                    # For TVT boss, check roomStatus if it's 3 the fight is ongoing
                    if (currentRoom == 68):
                        print(roomStatus)
                        if (roomStatus == 3 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                            bosses_to_send.add(key_list[i] + self.offset)
                    else:
                        if int.from_bytes(bossesList[i], byteorder='little') == 0x00:
                            bosses_to_send.add(key_list[i] + self.offset)

                if bosses_to_send is not None and bosses_to_send != set():
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in bosses_to_send)
                    }])

            # Check for Mailboxes
            if (localcondition) and (currentRoom in mailboxesRooms):
                mailboxesaddrs = RAM.mailboxListLocal[currentRoom]
                boolGotMail = (gotMail == 0x02)
                key_list = list(mailboxesaddrs.keys())
                val_list = list(mailboxesaddrs.values())

                mail_to_send = set()

                for i in range(len(val_list)):
                        if val_list[i] == mailboxID and boolGotMail:
                            mail_to_send.add(key_list[i] + self.offset)
                if mail_to_send is not None and mail_to_send != set():
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in mail_to_send)
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

            # Write Array

            # Training Room, set to 0xFF to mark as complete
            # Gadgets unlocked
            # Required apes (to match hundo)
            writes = [
                (RAM.trainingRoomProgressAddress, 0xFF.to_bytes(1, "little"), "MainRAM"),
                (RAM.unlockedGadgetsAddress, gadgetStateFromServer.to_bytes(1, "little"), "MainRAM"),
                (RAM.requiredApesAddress, localhundoCount.to_bytes(1, "little"), "MainRAM"),
            ]
            # For coin tracking to be ignored while in Level Select

            if RAM.gameState["LevelSelect"] == gameState:
                if CoinTable != RAM.blank_coinTable and TempCoinTable == RAM.blank_coinTable:
                    writes += [(RAM.startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]
                    writes += [(RAM.temp_startingCoinAddress, CoinTable.to_bytes(100, "little"), "MainRAM")]
                if SA_Completed != 0x00 and Temp_SA_Completed == 0xFF:
                    writes += [(RAM.SA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.Temp_SA_CompletedAddress, SA_Completed.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.Temp_GA_CompletedAddress, GA_Completed.to_bytes(1, "little"), "MainRAM")]

            else:
                if CoinTable == RAM.blank_coinTable and TempCoinTable != RAM.blank_coinTable:
                    writes += [(RAM.startingCoinAddress, TempCoinTable.to_bytes(100, "little"), "MainRAM")]
                    writes += [(RAM.temp_startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]

                if SA_Completed == 0x00 and Temp_SA_Completed != 0xFF:
                    writes += [(RAM.SA_CompletedAddress, Temp_SA_Completed.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.GA_CompletedAddress, Temp_GA_Completed.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.Temp_SA_CompletedAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                    writes += [(RAM.Temp_GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                # If the previous address is empty it means you are too far, go back once
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
            # Training Room Unlock state:
            # Due to a Bug with Gadget Training, will
            if (transitionPhase == 0x06 and NearbyRoom == 90) or currentRoom == 90:
                writes += [(RAM.GadgetTrainingsUnlockAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            else:
                writes += [(RAM.GadgetTrainingsUnlockAddress, 0x8C63FDCC.to_bytes(4, "little"), "MainRAM")]

            # Kickout Prevention
            if gameState == RAM.gameState["InLevel"]:
                if kickoutofLevel != 0:
                    writes += [(RAM.kickoutofLevelAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            else:
                if kickoutofLevel == 0:
                    writes += [(RAM.kickoutofLevelAddress, 0x84830188.to_bytes(4, "little"), "MainRAM")]
            # Water Net client handling
            # If Progressive WaterNet is 0 no Swim and no Dive, if it's 1 No Dive (Swim only)

            # 8-9 Jumping/falling, 35-36 D-Jump, 83-84 Flyer => don't reset the counter
            inAir = [0x08, 0x09, 0x35, 0x36, 0x83, 0x84]
            swimming = [0x46, 0x47]
            grounded = [0x00, 0x01, 0x02, 0x05, 0x07]#, 0x80, 0x81] Removed them since you can fling you net and give you extra air
            limited_OxygenLevel = 0x64

            # Base variables
            if waternetState == 0x00:
                writes += [(RAM.swim_surfaceDetectionAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.canDiveAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_ReplenishOxygenUWAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            elif waternetState == 0x01:
                writes += [(RAM.swim_surfaceDetectionAddress, 0x0801853A.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.canDiveAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_ReplenishOxygenUWAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            else:
                # (waternetstate > 0x01)
                writes += [(RAM.swim_surfaceDetectionAddress, 0x0801853A.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.canDiveAddress, 0x08018664.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x0C021DFE.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_ReplenishOxygenUWAddress, 0xA4500018.to_bytes(4, "little"), "MainRAM")]
                writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0xA4434DC8.to_bytes(4, "little"), "MainRAM")]

            # Oxygen Handling
            if waternetState == 0x00:
                if gameState == RAM.gameState["InLevel"]:
                    if gameRunning == 0x01:
                        # Set the air to the "Limited" value if 2 conditions:
                        # Oxygen is higher that "Limited" value AND spike is Swimming or Grounded
                        if spikeState2 in swimming:
                            if (swim_oxygenLevel > limited_OxygenLevel):
                                writes += [
                                    (RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                        else:
                            # if self.waterHeight != 0:
                            # self.waterHeight = 0
                            if spikeState2 in grounded:
                                writes += [
                                    (RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]

                    else:
                        # Game Not running
                        if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                            # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                            writes += [
                                (RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                            writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]
            if waternetState == 0x01:

                if isUnderwater == 0x00 and swim_oxygenLevel != limited_OxygenLevel:
                    writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                    # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                    writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                    writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]

            # WaterCatch unlocking stuff bellow
            if watercatchState == 0x00:
                writes += [(RAM.canWaterCatchAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
            else:
                writes += [(RAM.canWaterCatchAddress, 0x04.to_bytes(1, "little"), "MainRAM")]

            # Low Oxygen Sounds
            if spikeState2 in swimming:

                # Off
                if ctx.slot_data["lowoxygensounds"] == 0x00:
                    writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                    writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                # Half Beeps
                elif ctx.slot_data["lowoxygensounds"] == 0x01:

                    self.lowOxygenCounter += 1
                    #Should start at 1
                    print(self.lowOxygenCounter)
                    if self.lowOxygenCounter <= 2:
                        writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                        writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                    elif self.lowOxygenCounter <= 3:
                        writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                        writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C028004.to_bytes(4, "little"), "MainRAM")]
                    elif self.lowOxygenCounter > 3:
                        self.lowOxygenCounter = 0

                # On (Vanilla)
                else:
                    print("Vanilla")
                    writes += [(RAM.swim_oxygenLowLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
                    writes += [(RAM.swim_oxygenMidLevelSoundAddress, 0x3C02800F.to_bytes(4, "little"), "MainRAM")]
            else:
                if self.lowOxygenCounter != 1:
                    self.lowOxygenCounter = 1

            # Unequip the Time Net if it was shuffled. Note that just checking the Net option is not sufficient to known if the net was actually shuffled - we need to ensure there are locations in this world that don't require net to be sure.
            if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true and (ctx.slot_data["coin"] == CoinOption.option_true or ctx.slot_data["mailbox"] == MailboxOption.option_true):
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
                bytes_ToWrite: bytes = bytes.fromhex(
                    "0010000000000000E00B00000000000000100000000000000000000000000000")
                ToWrite = 0x0010000000000000E00B00000000000000100000000000000000000000000000
                # print(punchVisualAddress.to_bytes(32,"little"))
                # print(bytes_ToWrite)
                if ((gadgetStateFromServer & 32) == 32) and punchVisualAddress.to_bytes(32,"little") != bytes_ToWrite:  # and self.replacePunch == True:
                    writes += [(RAM.punchVisualAddress, bytes_ToWrite, "MainRAM")]
                    print("Replaced Punch visuals")
                    #self.replacePunch = False
            #else:
                #self.replacePunch = True

            # If the current level is Gladiator Attack, the Sky Flyer is currently equipped, and the player does not have the Sky Flyer: unequip it
            if ((currentLevel == 0x0E) and (heldGadget == 6) and (gadgetStateFromServer & 64 == 0)):
                writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]


            if gameState == RAM.gameState["LevelSelect"]:
                reqkeys = ctx.slot_data["reqkeys"]

                # Get all keys required for the next world, based on first level of ERAS
                WorldUnlocks = [reqkeys[3], reqkeys[6], reqkeys[7], reqkeys[10], reqkeys[13], reqkeys[14], reqkeys[17], reqkeys[20],reqkeys[21]]

                # Check if the selected world is the last (To stay within bound of the list)
                if 0 <= LS_currentWorld < 9:
                    # If you have less World Keys that the required keys for the next ERA, disable R1, Right Stick and Right DPAD detection
                    if self.worldkeycount < WorldUnlocks[LS_currentWorld]:
                        writes += [(RAM.worldScrollToRightDPAD, 0x0000.to_bytes(2, "little"), "MainRAM")]
                        writes += [(RAM.worldScrollToRightR1, 0x0000.to_bytes(2, "little"), "MainRAM")]
                    else:
                        writes += [(RAM.worldScrollToRightDPAD, 0x0009.to_bytes(2, "little"), "MainRAM")]
                        writes += [(RAM.worldScrollToRightR1, 0x0009.to_bytes(2, "little"), "MainRAM")]

            # ======================================

            if gameState == RAM.gameState["LevelSelect"]:
                writes += [(RAM.localApeStartAddress, 0x0.to_bytes(8, "little"), "MainRAM")]
                # Setting a race to Locked still unlocks the next level, so instead, reselect the race.
                # ** Not required anymore
                #if LS_currentWorld == 3 and self.worldkeycount < reqkeys[7] or LS_currentWorld == 6 and self.worldkeycount < reqkeys[14]:
                    #writes += [(RAM.selectedWorldAddress, (LS_currentWorld - 1).to_bytes(1, "little"), "MainRAM")]

                # Update level (and potentially era) names.
                bytestowrite = ctx.slot_data["levelnames"]
                # This is a bit of a "magic number" right now. trying to get the length didn't work.
                # Trying to write all the bytes at once also didn't work.
                for x in range(0, 308):
                    writes += [(RAM.startOfLevelNames + x, bytestowrite[x].to_bytes(1, "little"), "MainRAM")]

            # Reroute the player to the correct level. Technically only needed for entrance shuffle, vanilla entrances are just a special case of entrance shuffle so this works perfectly fine for that case, too.
            if gameState == RAM.gameState["LevelIntro"] or gameState == RAM.gameState["LevelIntroTT"]:
                print("In level intro state.")
                # Pull the order of first rooms from slot data. This is a List sorted by the order of entrances in the level select - so the first value is the room being entered from Fossil Field.
                firstroomids = ctx.slot_data["firstrooms"]
                # Match these room ids to the internal identifiers - 11, 12, 13, 21, ... 83, 91, 92
                levelidtofirstroom = dict(zip(RAM.levelAddresses.keys(), firstroomids))
                # Use Selected World (0-9) and Selected Level (0-2) to determine the selected level.
                chosenLevel = 10 * status_currentWorld + status_currentLevel + 11
                # Peak Point Matrix doesn't follow the pattern, so manually override if it's that.
                if chosenLevel > 100:
                    chosenLevel = 92
                targetRoom = levelidtofirstroom.get(chosenLevel)
                # Actually send Spike to the desired level!
                writes += [(RAM.currentRoomIdAddress, targetRoom.to_bytes(1, "little"), "MainRAM")]


            # Unlock levels
            level_info = [currentApes, requiredApes, currentLevel, localhundoCount]
            writes += self.unlockLevels(monkeylevelcounts, gadgets, gameState, gadgetUseState, level_info, hundoMonkeysCount, spikeState, ctx.slot_data["reqkeys"])

            await bizhawk.write(ctx.bizhawk_ctx, writes)
            await bizhawk.write(ctx.bizhawk_ctx, itemsWrites)

            self.levelglobal = currentLevel
            self.roomglobal = currentRoom

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_death_link(self, ctx: "BizHawkClientContext", DL_Reads) -> None:
        """
        Checks whether the player has died while connected and sends a death link if so.
        """
        cookies = DL_Reads[0]
        gameRunning = DL_Reads[1]
        gamestate = DL_Reads[2]

        DL_writes = []

        if ctx.slot_data["death_link"] == Toggle.option_true:
            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.previous_death_link = ctx.last_death_link
            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if cookies == 0x00 and not self.sending_death_link and gamestate in (
                RAM.gameState["InLevel"], RAM.gameState["TimeStation"]):
                    await self.send_deathlink(ctx)
                elif cookies != 0x00:
                    self.sending_death_link = False
            if self.pending_death_link:
                DL_writes += [(RAM.cookieAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                self.pending_death_link = False
                self.sending_death_link = True
                await bizhawk.write(ctx.bizhawk_ctx, DL_writes)

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        DeathText = ctx.player_names[ctx.slot] + " says: `Oooh noooo!`(Died)"
        await ctx.send_death(DeathText)
    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    def unlockLevels(self, monkeylevelCounts, gadgets, gameState, gadgetUseState, level_info, hundoMonkeysCount, spikeState, reqkeys):

        key = self.worldkeycount
        curApesWrite = ""
        reqApesWrite = ""
        hundoWrite = ""
        currentApes = level_info[0]
        requiredApes = level_info[1]
        currentLevel = level_info[2]
        localhundoCount = level_info[3]
        levellocked = RAM.levelStatus["Locked"].to_bytes(1, byteorder="little")
        levelopen = RAM.levelStatus["Open"].to_bytes(1, byteorder="little")
        levelhundo = RAM.levelStatus["Hundo"].to_bytes(1, byteorder="little")
        allCompleted = True

        debug = False

        levels_keys = hundoMonkeysCount.keys()
        levels_list = list(levels_keys)
        if gameState == RAM.gameState["LevelSelect"] or debug:
            for x in range(len(levels_list)):
                if int.from_bytes(monkeylevelCounts[x], byteorder="little") < hundoMonkeysCount[levels_list[x]]:
                    #print("Level " + str(x) + " not completed" + str(int.from_bytes(monkeylevelCounts[x])) + "/" + str(hundoMonkeysCount[levels_list[x]]))
                    allCompleted = False
                    break
                    # Does not need to check the rest of the levels, at least 1 is not completed

        PPMUnlock = (key == reqkeys[21] and allCompleted)

        # Set unlocked/locked state of levels
        # This does not handle assignment of Specter Coin icons.
        # TODO: Change the assignment of "Hundo" status to assign it to the ENTRANCE that's completed, not the LEVEL
        # Most of this handling is about entrance order - the Hundo check would need to be pulled out of the big if chain because it's about level order right now.
        # Make sure that Hundo doesn't get set on a level that needs to be Locked and that Open doesn't get set on a level that needs to be Hundo.
        levelstates = []
        for index in range(0, 21):
            # Do we have enough keys for this level? If no, lock. If yes, continue.
            if key >= reqkeys[index]:
                # Do we have enough keys for the next level? If no, lock. If yes, continue.
                if key >= reqkeys[index + 1]:
                    # Is this level a race level? If no, continue. If yes, open.
                    if index == 6 or index == 13:
                        levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levelopen, "MainRAM"))
                    # Is every monkey in this level caught? If no, open. If yes, hundo.
                    elif int.from_bytes(monkeylevelCounts[index], byteorder="little") >= hundoMonkeysCount[levels_list[index]]:
                        levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levelhundo, "MainRAM"))
                    else:
                        levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levelopen, "MainRAM"))
                else:
                    levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levellocked, "MainRAM"))
            else:
                levelstates.append((RAM.levelAddresses[list(RAM.levelAddresses.keys())[index]], levellocked, "MainRAM"))
        # Monkey Madness must be set to locked if Peak Point Matrix should be locked
        if PPMUnlock == False:
            levelstates[20] = ((RAM.levelAddresses[list(RAM.levelAddresses.keys())[20]], levellocked, "MainRAM"))

        # If there is a change in required monkeys count, include it in the writes
        returns = list(levelstates)
        if curApesWrite != "":
            returns.append(curApesWrite)
        if reqApesWrite != "":
            returns.append(reqApesWrite)
        if hundoWrite != "":
            returns.append(hundoWrite)
        return returns