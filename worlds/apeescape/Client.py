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
        self.replacePunch = True
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
        self.CrCButton = 0
        self.MM_Painting_Button = 0
        self.MM_MonkeyHead_Button = 0
        self.TVT_Lobby_Button = 0
        self.bool_MMDoubleDoor = False
        self.bool_LampGlobal = False

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
        if cmd == "Retrieved":
            if "keys" not in args:
                print(f"invalid Retrieved packet to ApeEscapeClient: {args}")
                return
            keys = dict(args["keys"])
            print(keys)
            self.CrCButton = keys.get(str(ctx.auth) + "_CrcButton", None)
            self.MM_Painting_Button = keys.get(str(ctx.auth) + "_MM_Painting_Button", None)
            self.MM_MonkeyHead_Button = keys.get(str(ctx.auth) + "_MM_MonkeyHead_Button", None)
            self.TVT_Lobby_Button = keys.get(str(ctx.auth) + "_TVT_Lobby_Button", None)

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

            # Game state,locations and items read
            readTuples = [
                #GameStates
                (RAM.lastReceivedArchipelagoID, 4, "MainRAM"),
                (RAM.gameStateAddress, 1, "MainRAM"),
                (RAM.currentRoomIdAddress, 1, "MainRAM"),  # Current Room
                (RAM.Nearby_RoomIDAddress, 1, "MainRAM"),  # Nearby Room
                (RAM.currentLevelAddress, 1, "MainRAM"),  # Current Level
                (RAM.gameRunningAddress, 1, "MainRAM"),
                (RAM.jakeVictoryAddress, 1, "MainRAM"),  # Jake Races Victory state
                #Locations (Coins,Monkeys, Mailboxes)
                (self.currentCoinAddress - 2, 1, "MainRAM"),  # Previous Coin State Room
                (self.currentCoinAddress, 1, "MainRAM"),  # Current New Coin State Room
                (RAM.totalCoinsAddress, 1, "MainRAM"),  # Coin Count
                (RAM.hundoApesAddress, 1, "MainRAM"),  # Hundo monkey count, to write to required count
                (RAM.requiredApesAddress, 1, "MainRAM"),
                (RAM.currentApesAddress, 1, "MainRAM"),
                (RAM.gotMailAddress, 1, "MainRAM"),
                (RAM.mailboxIDAddress, 1, "MainRAM"),
                #Items
                (RAM.energyChipsAddress, 1, "MainRAM"),
                (RAM.cookieAddress, 1, "MainRAM"),
                (RAM.livesAddress, 1, "MainRAM"),
                (RAM.flashAddress, 1, "MainRAM"),
                (RAM.rocketAddress, 1, "MainRAM"),
                (RAM.keyCountFromServer, 1, "MainRAM"),
                #Misc
                (RAM.spikeStateAddress, 1, "MainRAM"),
                (RAM.spikeState2Address, 1, "MainRAM"),
                (RAM.kickoutofLevelAddress, 4, "MainRAM"),
                (RAM.roomStatus, 1, "MainRAM"),
                (RAM.S1_P2_State, 1, "MainRAM"),
                (RAM.S1_P2_Life, 1, "MainRAM"),
                (RAM.S2_isCaptured, 1, "MainRAM"),
            ]

            reads = await bizhawk.read(ctx.bizhawk_ctx, readTuples)

            # GameStates
            recv_index = int.from_bytes(reads[0], byteorder="little")
            gameState = int.from_bytes(reads[1], byteorder="little")
            currentRoom = int.from_bytes(reads[2], byteorder="little")
            NearbyRoom = int.from_bytes(reads[3], byteorder="little")
            currentLevel = int.from_bytes(reads[4], byteorder="little")
            gameRunning = int.from_bytes(reads[5], byteorder="little")
            jakeVictory = int.from_bytes(reads[6], byteorder="little")
            # Locations
            previousCoinStateRoom = int.from_bytes(reads[7], byteorder="little")
            currentCoinStateRoom = int.from_bytes(reads[8], byteorder="little")
            coinCount = int.from_bytes(reads[9], byteorder="little")
            localhundoCount = int.from_bytes(reads[10], byteorder="little")
            requiredApes = int.from_bytes(reads[11], byteorder="little")
            currentApes = int.from_bytes(reads[12], byteorder="little")
            gotMail = int.from_bytes(reads[13], byteorder="little")
            mailboxID = int.from_bytes(reads[14], byteorder="little")
            # Items
            energyChips = int.from_bytes(reads[15], byteorder="little")
            cookies = int.from_bytes(reads[16], byteorder="little")
            totalLives = int.from_bytes(reads[17], byteorder="little")
            flashAmmo = int.from_bytes(reads[18], byteorder="little")
            rocketAmmo = int.from_bytes(reads[19], byteorder="little")
            keyCountFromServer = int.from_bytes(reads[20], byteorder="little")
            # Misc
            spikeState = int.from_bytes(reads[21], byteorder="little")
            spikeState2 = int.from_bytes(reads[22], byteorder="little")
            kickoutofLevel = int.from_bytes(reads[23], byteorder="little")
            roomStatus = int.from_bytes(reads[24], byteorder="little")
            S1_P2_State = int.from_bytes(reads[25], byteorder="little")
            S1_P2_Life = int.from_bytes(reads[26], byteorder="little")
            S2_isCaptured = int.from_bytes(reads[27], byteorder="little")

            #Related to Gadgets
            gadgetTuples = [
                (RAM.unlockedGadgetsAddress, 1, "MainRAM"),  # Gadget unlocked states
                (RAM.gadgetStateFromServer, 2, "MainRAM"),
                (RAM.heldGadgetAddress, 1, "MainRAM"),  # Currently held gadget
                (RAM.triangleGadgetAddress, 1, "MainRAM"),  # Gadget equipped to each face button
                (RAM.squareGadgetAddress, 1, "MainRAM"),
                (RAM.circleGadgetAddress, 1, "MainRAM"),
                (RAM.crossGadgetAddress, 1, "MainRAM"),
                (RAM.gadgetUseStateAddress, 1, "MainRAM"),  # Which gadget is used in what way. **Not used at the moment
                (RAM.punchVisualAddress, 32, "MainRAM"),  # Which gadget is used in what way. **Not used at the moment
            ]

            gadgetReads = await bizhawk.read(ctx.bizhawk_ctx, gadgetTuples)

            gadgets = int.from_bytes(gadgetReads[0], byteorder="little")
            gadgetStateFromServer = int.from_bytes(gadgetReads[1], byteorder="little")
            heldGadget = int.from_bytes(gadgetReads[2], byteorder="little")
            triangleGadget = int.from_bytes(gadgetReads[3], byteorder="little")
            squareGadget = int.from_bytes(gadgetReads[4], byteorder="little")
            circleGadget = int.from_bytes(gadgetReads[5], byteorder="little")
            crossGadget = int.from_bytes(gadgetReads[6], byteorder="little")
            gadgetUseState = int.from_bytes(gadgetReads[7], byteorder="little")
            punchVisualAddress = int.from_bytes(gadgetReads[8], byteorder="little")

            # Menu and level select reads
            menuTuples = [
                (RAM.selectedWorldAddress, 1, "MainRAM"),  # In level select, the current world
                (RAM.selectedLevelAddress, 1, "MainRAM"),  # In level select, the current level
                (RAM.enteredWorldAddress, 1, "MainRAM"),  # After selecting a level, the entered world
                (RAM.enteredLevelAddress, 1, "MainRAM"),  # After selecting a level, the entered level
                (RAM.menuStateAddress, 1, "MainRAM"),
                (RAM.menuState2Address, 1, "MainRAM"),
                (RAM.newGameAddress, 1, "MainRAM"),
                (RAM.startingCoinAddress, 100, "MainRAM"),
                (RAM.temp_startingCoinAddress, 100, "MainRAM"),
                (RAM.SA_CompletedAddress, 1, "MainRAM"),
                (RAM.Temp_SA_CompletedAddress, 1, "MainRAM"),
                (RAM.GA_CompletedAddress, 1, "MainRAM"),
                (RAM.Temp_GA_CompletedAddress, 1, "MainRAM")
            ]

            menuReads = await bizhawk.read(ctx.bizhawk_ctx, menuTuples)

            # Level Select/Menu data
            LS_currentWorld = int.from_bytes(menuReads[0], byteorder="little")
            LS_currentLevel = int.from_bytes(menuReads[1], byteorder="little")
            status_currentWorld = int.from_bytes(menuReads[2], byteorder="little")
            status_currentLevel = int.from_bytes(menuReads[3], byteorder="little")
            menuState = int.from_bytes(menuReads[4], byteorder="little")
            menuState2 = int.from_bytes(menuReads[5], byteorder="little")
            newGameAddress = int.from_bytes(menuReads[6], byteorder="little")
            # Level Select Coin hiding
            CoinTable = int.from_bytes(menuReads[7], byteorder="little")
            TempCoinTable = int.from_bytes(menuReads[8], byteorder="little")
            SA_Completed = int.from_bytes(menuReads[9], byteorder="little")
            Temp_SA_Completed = int.from_bytes(menuReads[10], byteorder="little")
            GA_Completed = int.from_bytes(menuReads[11], byteorder="little")
            Temp_GA_Completed = int.from_bytes(menuReads[12], byteorder="little")

            #Water net shuffle Reads
            swimTuples = [
                (RAM.canDiveAddress, 4, "MainRAM"),
                (RAM.canWaterCatchAddress, 1, "MainRAM"),
                (RAM.tempWaterNetAddress, 1, "MainRAM"),
                (RAM.tempWaterCatchAddress, 1, "MainRAM"),
                (RAM.isUnderwater, 1, "MainRAM"),  # Underwater variable
                (RAM.swim_oxygenLevelAddress, 2, "MainRAM"),
            ]

            swimReads = await bizhawk.read(ctx.bizhawk_ctx, swimTuples)

            canDive = int.from_bytes(swimReads[0], byteorder="little")
            canWaterCatch = int.from_bytes(swimReads[1], byteorder="little")
            WaterNetStateFromServer = int.from_bytes(swimReads[2], byteorder="little")
            WaterCatchStateFromServer = int.from_bytes(swimReads[3], byteorder="little")
            isUnderwater = int.from_bytes(swimReads[4], byteorder="little")
            swim_oxygenLevel = int.from_bytes(swimReads[5], byteorder="little")

            lampTuples = [
                (RAM.tempCB_LampAddress, 1, "MainRAM"),
                (RAM.tempDI_LampAddress, 1, "MainRAM"),
                (RAM.tempCrC_LampAddress, 1, "MainRAM"),
                (RAM.tempCP_LampAddress, 1, "MainRAM"),
                (RAM.tempSF_LampAddress, 1, "MainRAM"),
                (RAM.tempTVT_Lobby_LampAddress, 1, "MainRAM"),
                (RAM.tempTVT_Tank_LampAddress, 1, "MainRAM"),
                (RAM.tempMM_LampAddress, 1, "MainRAM"),
                (RAM.localLamp_localUpdate, 4, "MainRAM"),
                (RAM.globalLamp_localUpdate, 4, "MainRAM"),
                (RAM.globalLamp_globalUpdate, 4, "MainRAM"),
            ]

            lampReads = await bizhawk.read(ctx.bizhawk_ctx, lampTuples)

            CBLampStateFromServer = int.from_bytes(lampReads[0], byteorder="little")
            DILampStateFromServer = int.from_bytes(lampReads[1], byteorder="little")
            CrCLampStateFromServer = int.from_bytes(lampReads[2], byteorder="little")
            CPLampStateFromServer = int.from_bytes(lampReads[3], byteorder="little")
            SFLampStateFromServer = int.from_bytes(lampReads[4], byteorder="little")
            TVTLobbyLampStateFromServer = int.from_bytes(lampReads[5], byteorder="little")
            TVTTankLampStateFromServer = int.from_bytes(lampReads[6], byteorder="little")
            MMLampStateFromServer = int.from_bytes(lampReads[7], byteorder="little")
            LocalLamp_LocalUpdate = int.from_bytes(lampReads[8], byteorder="little")
            GlobalLamp_LocalUpdate = int.from_bytes(lampReads[9], byteorder="little")
            GlobalLamp_GlobalUpdate = int.from_bytes(lampReads[10], byteorder="little")

            locksTuples = [
                # Buttons
                (RAM.temp_MMLobbyDoorAddress, 1, "MainRAM"),
                (RAM.MM_Lobby_DoubleDoor_OpenAddress, 1, "MainRAM"),
                (RAM.MM_Jake_DefeatedAddress, 1, "MainRAM"),
                (RAM.MM_Professor_RescuedAddress, 1, "MainRAM"),
                (RAM.MM_Clown_State, 1, "MainRAM"),
                (RAM.MM_Nathalie_RescuedAddress, 1, "MainRAM"),
                (RAM.temp_MM_Jake_DefeatedAddress, 1, "MainRAM"),
                (RAM.temp_MM_Professor_RescuedAddress, 1, "MainRAM"),
                (RAM.temp_MM_Nathalie_RescuedAddress, 1, "MainRAM"),

                # Doors
                (RAM.MM_Lobby_DoorDetection, 4, "MainRAM"),
                (RAM.CrC_Button_Pressed, 1, "MainRAM"),
                (RAM.CrC_Door_Visual, 1, "MainRAM"),
                (RAM.TVT_Lobby_Button, 1, "MainRAM"),
                (RAM.TVT_Lobby_Water_HitBox, 1, "MainRAM"),
                (RAM.MM_MonkeyHead_Button, 1, "MainRAM"),
                (RAM.MM_MonkeyHead_Door, 1, "MainRAM"),
                (RAM.MM_Painting_Button, 1, "MainRAM"),
                (RAM.MM_Painting_Visual, 1, "MainRAM"),

            ]

            locksReads = await bizhawk.read(ctx.bizhawk_ctx, locksTuples)
            # Doors
            MM_Lobby_DoubleDoor = int.from_bytes(locksReads[0], byteorder="little")
            MM_Lobby_DoubleDoor_Open = int.from_bytes(locksReads[1], byteorder="little")
            MM_Jake_DefeatedAddress = int.from_bytes(locksReads[2], byteorder="little")
            MM_Professor_RescuedAddress = int.from_bytes(locksReads[3], byteorder="little")
            MM_Clown_State = int.from_bytes(locksReads[4], byteorder="little")
            MM_Nathalie_RescuedAddress = int.from_bytes(locksReads[5], byteorder="little")
            MM_Jake_Defeated = int.from_bytes(locksReads[6], byteorder="little")
            MM_Professor_Rescued = int.from_bytes(locksReads[7], byteorder="little")
            MM_Nathalie_Rescued = int.from_bytes(locksReads[8], byteorder="little")
            MM_Lobby_DoorDetection = int.from_bytes(locksReads[9], byteorder="little")

            # Buttons
            CrC_ButtonPressed = int.from_bytes(locksReads[10], byteorder="little")
            CrC_Door_Visual = int.from_bytes(locksReads[11], byteorder="little")
            TVT_Lobby_ButtonPressed = int.from_bytes(locksReads[12], byteorder="little")
            TVT_Lobby_Water_Hitbox = int.from_bytes(locksReads[13], byteorder="little")
            MM_MonkeyHead_ButtonPressed = int.from_bytes(locksReads[14], byteorder="little")
            MM_MonkeyHead_Door = int.from_bytes(locksReads[15], byteorder="little")
            MM_Painting_ButtonPressed = int.from_bytes(locksReads[16], byteorder="little")
            MM_Painting_Visual = int.from_bytes(locksReads[17], byteorder="little")

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

            #Write tables
            itemsWrites = []
            Menuwrites = []

            # Handle death link
            DL_Reads = [cookies,gameRunning,gameState]
            await self.handle_death_link(ctx,DL_Reads)

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

            if MM_Lobby_DoubleDoor == 0xFF:
                MM_Lobby_DoubleDoor = 0

            if MM_Jake_Defeated == 0xFF:
                MM_Jake_Defeated = 0

            if MM_Professor_Rescued == 0xFF:
                MM_Professor_Rescued = 0

            if MM_Nathalie_Rescued == 0xFF:
                MM_Nathalie_Rescued = 0

            # Get WaterNet state from memory
            waternetState = 0
            if WaterNetStateFromServer != 0xFF:
                waternetState = WaterNetStateFromServer

            # Get Dive state from memory
            watercatchState = 0
            if WaterCatchStateFromServer != 0x00:
                watercatchState = WaterCatchStateFromServer

            # Get Lamp states
            CBLampState = 0
            DILampState = 0
            CrCLampState = 0
            CPLampState = 0
            SFLampState = 0
            TVTLobbyLampState = 0
            TVTTankLampState = 0
            MMLampState = 0

            if CBLampStateFromServer != 0x00 and CBLampStateFromServer != 0xFF: CBLampState = CBLampStateFromServer
            if DILampStateFromServer != 0x00 and DILampStateFromServer != 0xFF: DILampState = DILampStateFromServer
            if CrCLampStateFromServer != 0x00 and CrCLampStateFromServer != 0xFF: CrCLampState = CrCLampStateFromServer
            if CPLampStateFromServer != 0x00 and CPLampStateFromServer != 0xFF: CPLampState = CPLampStateFromServer
            if SFLampStateFromServer != 0x00 and SFLampStateFromServer != 0xFF: SFLampState = SFLampStateFromServer
            if TVTLobbyLampStateFromServer != 0x00 and TVTLobbyLampStateFromServer != 0xFF: TVTLobbyLampState = TVTLobbyLampStateFromServer
            if TVTTankLampStateFromServer != 0x00 and TVTTankLampStateFromServer != 0xFF: TVTTankLampState = TVTTankLampStateFromServer
            if MMLampStateFromServer != 0x00 and MMLampStateFromServer != 0xFF: MMLampState = MMLampStateFromServer

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
                        elif (item.item - self.offset) == RAM.items["MMLobbyDoubleDoorKey"]:
                            MM_Lobby_DoubleDoor = 1
                        elif (item.item - self.offset) == RAM.items["WaterCatch"]:
                            watercatchState = 1
                        elif (item.item - self.offset) == RAM.items["CB_Lamp"]:
                            CBLampState  = 1
                        elif (item.item - self.offset) == RAM.items["DI_Lamp"]:
                            DILampState  = 1
                        elif (item.item - self.offset) == RAM.items["CrC_Lamp"]:
                            CrCLampState = 1
                        elif (item.item - self.offset) == RAM.items["CP_Lamp"]:
                            CPLampState = 1
                        elif (item.item - self.offset) == RAM.items["SF_Lamp"]:
                            SFLampState = 1
                        elif (item.item - self.offset) == RAM.items["TVT_Lobby_Lamp"]:
                            TVTLobbyLampState = 1
                        elif (item.item - self.offset) == RAM.items["TVT_Tank_Lamp"]:
                            TVTTankLampState = 1
                        elif (item.item - self.offset) == RAM.items["MM_Lamp"]:
                            MMLampState = 1
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
                itemsWrites += [(RAM.lastReceivedArchipelagoID, recv_index.to_bytes(4, "little"), "MainRAM"),]
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
                itemsWrites += [(RAM.tempCB_LampAddress, CBLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempDI_LampAddress, DILampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempCrC_LampAddress, CrCLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempCP_LampAddress, CPLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempSF_LampAddress, SFLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempTVT_Lobby_LampAddress, TVTLobbyLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempTVT_Tank_LampAddress, TVTTankLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.tempMM_LampAddress, MMLampState.to_bytes(1, "little"), "MainRAM")]
                itemsWrites += [(RAM.temp_MMLobbyDoorAddress, MM_Lobby_DoubleDoor.to_bytes(1, "little"), "MainRAM")]

            self.worldkeycount = keyCountFromServer

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

            # Check for Coins
            if gameState != RAM.gameState["LevelSelect"]:
                # If the previous address is empty it means you are too far, go back once
                # Happens in case of save-states or loading a previous save file that did not collect the same amount of coins
                if (previousCoinStateRoom == 0xFF or previousCoinStateRoom == 0x00) and (
                        self.currentCoinAddress > RAM.startingCoinAddress):
                    self.currentCoinAddress -= 2
                # Check for new coins from current coin address
                if currentCoinStateRoom != 0xFF and currentCoinStateRoom != 0x00:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": list(x for x in [currentCoinStateRoom + self.offset + 300])
                    }])
                    self.currentCoinAddress += 2

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
                    # For TVT boss, check roomStatus, if it's 3 the fight is ongoing
                    if (currentRoom == 68):
                        if (roomStatus == 3 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                            bosses_to_send.add(key_list[i] + self.offset)
                    elif (currentRoom == 70):
                        if (gameRunning == 1 and int.from_bytes(bossesList[i], byteorder='little') == 0x00):
                            bosses_to_send.add(key_list[i] + self.offset)
                            MM_Jake_Defeated = 1
                    elif (currentRoom == 71):
                        if int.from_bytes(bossesList[i], byteorder='little') == 0x05:
                            bosses_to_send.add(key_list[i] + self.offset)
                            MM_Professor_Rescued = 1
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
            # Training Room Unlock state checkup : Set to 0x00000000 to prevent all buttons from working
            # Gadgets unlocked
            # Required apes (to match hundo)
            writes = [
                (RAM.trainingRoomProgressAddress, 0xFF.to_bytes(1, "little"), "MainRAM"),
                (RAM.GadgetTrainingsUnlockAddress, 0x00000000.to_bytes(4, "little"), "MainRAM"),
                (RAM.unlockedGadgetsAddress, gadgetStateFromServer.to_bytes(2, "little"), "MainRAM"),
                (RAM.requiredApesAddress, localhundoCount.to_bytes(1, "little"), "MainRAM"),
            ]

            # Kickout Prevention
            if kickoutofLevel != 0:
                writes += [(RAM.kickoutofLevelAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]

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
            # ===== MM Optimizations =========
            # Execute the code segment for MM Double Door and related optimizations
            MM_Reads = [currentRoom,NearbyRoom,MM_Jake_Defeated,MM_Lobby_DoubleDoor,MM_Lobby_DoorDetection,MM_Lobby_DoubleDoor_Open,MM_Jake_DefeatedAddress]
            await self.MM_Optimizations(ctx, MM_Reads)
            # ================================

            # ===== Permanent Buttons =======
            # Execute the Buttons handling code segment
            Button_Reads = [currentRoom,CrC_ButtonPressed,TVT_Lobby_ButtonPressed,MM_MonkeyHead_ButtonPressed,MM_Painting_ButtonPressed,CrC_Door_Visual,TVT_Lobby_Water_Hitbox,MM_MonkeyHead_Door,MM_Painting_Visual]
            await self.permanent_buttons_handling(ctx,Button_Reads)
            # =======================

            # ===== Lamp Unlocks =======
            # Tables for Lamp updates
            localLampsUpdate = {21: CBLampState,53: CPLampState, 79: MMLampState}
            globalLampsUpdate = {26: DILampState,46: CrCLampState,57: SFLampState,66: TVTTankLampState}
            bothLampsUpdate = {65: TVTLobbyLampState}
            # Execute the Lamp unlocking code segment
            Lamps_Reads = [currentRoom,NearbyRoom,localLampsUpdate,globalLampsUpdate,bothLampsUpdate,LocalLamp_LocalUpdate,GlobalLamp_LocalUpdate]
            await self.lamps_unlocks_handling(ctx,Lamps_Reads)
            # =======================

            # ===== Water Net =======
            # Swim/Dive Prevention code
            WN_Reads = [gameState,waternetState,gameRunning,spikeState2,swim_oxygenLevel,cookies,isUnderwater,watercatchState]
            await self.water_net_handling(ctx,WN_Reads)
            # =======================

            # ===== Gadgets handling =======
            # For checking which gadgets should be equipped
            # Also apply Magic Punch visual correction
            Gadgets_Reads = [currentLevel,heldGadget,gadgetStateFromServer,crossGadget,menuState,menuState2,punchVisualAddress]
            await self.gadgets_handler(ctx,Gadgets_Reads)
            # ======================================

            # ===== Level Select Optimisation=======
            # Execute the Level Select optimisation code segment
            LSO_Reads = [gameState,CoinTable,TempCoinTable,SA_Completed,Temp_SA_Completed,GA_Completed,Temp_GA_Completed,LS_currentWorld]
            await self.level_select_optimization(ctx, LSO_Reads)
            # ======================================

            if gameState == RAM.gameState["LevelSelect"] or gameState == RAM.gameState["LevelIntroTT"]:
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
            if gameState == RAM.gameState["LevelIntro"]:
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
            writes += self.unlockLevels(monkeylevelcounts, gameState, hundoMonkeysCount, ctx.slot_data["reqkeys"])

            await bizhawk.write(ctx.bizhawk_ctx, writes)
            await bizhawk.write(ctx.bizhawk_ctx, itemsWrites)

            self.levelglobal = currentLevel
            self.roomglobal = currentRoom

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def gadgets_handler(self, ctx: "BizHawkClientContext", Gadgets_Reads):
        currentLevel = Gadgets_Reads[0]
        heldGadget = Gadgets_Reads[1]
        gadgetStateFromServer = Gadgets_Reads[2]
        crossGadget = Gadgets_Reads[3]
        menuState = Gadgets_Reads[4]
        menuState2 = Gadgets_Reads[5]
        punchVisualAddress = Gadgets_Reads[6]

        gadgets_Writes = []

        # If the current level is Gladiator Attack, the Sky Flyer is currently equipped, and the player does not have the Sky Flyer: unequip it
        if ((currentLevel == 0x0E) and (heldGadget == 6) and (gadgetStateFromServer & 64 == 0)):
            gadgets_Writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
            gadgets_Writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]

        # Unequip the Time Net if it was shuffled. Note that just checking the Net option is not sufficient to known if the net was actually shuffled - we need to ensure there are locations in this world that don't require net to be sure.
        if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true and (
                ctx.slot_data["coin"] == CoinOption.option_true or ctx.slot_data[
            "mailbox"] == MailboxOption.option_true):
            if (crossGadget == 1) and (gadgetStateFromServer & 2 == 0):
                gadgets_Writes += [(RAM.crossGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]

        # Equip the selected starting gadget onto the triangle button. Stun Club is the default and doesn't need changing. Additionally, in the "none" case, switch the selection to the Time Net if it wasn't shuffled.
        if ((heldGadget == 0) and (gadgetStateFromServer % 2 == 0)):
            if ctx.slot_data["gadget"] == GadgetOption.option_radar:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x02.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_sling:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_hoop:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_flyer:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x06.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_car:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x07.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_punch:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                gadgets_Writes += [(RAM.heldGadgetAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
            elif ctx.slot_data["gadget"] == GadgetOption.option_none:
                gadgets_Writes += [(RAM.triangleGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                if ctx.slot_data["shufflenet"] == ShuffleNetOption.option_true:
                    gadgets_Writes += [(RAM.heldGadgetAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                elif ctx.slot_data["shufflenet"] == ShuffleNetOption.option_false:
                    gadgets_Writes += [(RAM.heldGadgetAddress, 0x01.to_bytes(1, "little"), "MainRAM")]

        # Punch Visual glitch in menu fix
        if (menuState == 0) and (menuState2 == 1):

            # Replace all values from 0x0E78C0 to 0x0E78DF to this:
            # 0010000000000000E00B00000000000000100000000000000000000000000000
            bytes_ToWrite: bytes = bytes.fromhex(
                "0010000000000000E00B00000000000000100000000000000000000000000000")
            ToWrite = 0x0010000000000000E00B00000000000000100000000000000000000000000000
            #print(punchVisualAddress.to_bytes(32,"little"))
            #print(bytes_ToWrite)
            if ((gadgetStateFromServer & 32) == 32) and punchVisualAddress.to_bytes(32,"little") != bytes_ToWrite: #and self.replacePunch == True:
                #print(punchVisualAddress)
                #print(int.from_bytes(bytes_ToWrite))
                gadgets_Writes += [(RAM.punchVisualAddress, bytes_ToWrite, "MainRAM")]
                print("Replaced Punch visuals")
                self.replacePunch = False
                #print("Fix Punch")
                #gadgets_Writes += [(RAM.unlockedGadgetsAddress, 0x24.to_bytes(1, "little"), "MainRAM")]
        else:
            self.replacePunch = True
            # Set gadget state to "Punch" only,will get replaced automatically by the writes on next client's pass
            # Should fix the bug?

        await bizhawk.write(ctx.bizhawk_ctx, gadgets_Writes)

    async def MM_Optimizations(self, ctx: "BizHawkClientContext", MM_Reads) -> None:

        currentRoom = MM_Reads[0]
        NearbyRoom = MM_Reads[1]
        MM_Jake_Defeated = MM_Reads[2]
        MM_Lobby_DoubleDoor = MM_Reads[3]
        MM_Lobby_DoorDetection = MM_Reads[4]
        MM_Lobby_DoubleDoor_Open = MM_Reads[5]
        MM_Jake_DefeatedAddress = MM_Reads[6]


        MM_Writes = []

        if MM_Jake_Defeated > 0:
            MM_Writes += [(RAM.temp_MM_Jake_DefeatedAddress, 0x01.to_bytes(1, "little"), "MainRAM")]

        if NearbyRoom == 69 and currentRoom != 69:
            print("Next room == Lobby")
            if MM_Lobby_DoubleDoor == 0x00:
                if MM_Lobby_DoorDetection != 0x8C800000:
                    MM_Writes += [(RAM.MM_Lobby_DoorDetection, 0x8C800000.to_bytes(4, "little"), "MainRAM")]
                    print("Double Door Item not acquired,disable door detection")
        if currentRoom == 69:
            # Open the Electric Door and remove the Hitbox blocking you to go to Go Karz room (Jake fight)

            MM_Writes += [(RAM.MM_Lobby_JakeDoorFenceAddress, 0x01.to_bytes(1, "little"), "MainRAM")]
            MM_Writes += [(RAM.MM_Lobby_JakeDoor_HitboxAddress, 0x80.to_bytes(1, "little"), "MainRAM")]

            if MM_Lobby_DoubleDoor == 0:
                # Prevent the door from opening no matter what,even if you defeated Jake

                if MM_Jake_Defeated == 0x00:
                    print("Jake NOT Defeated")
                    #Should not impact if it's not yet defeated since new detection address
                    MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                    MM_Writes += [(RAM.MM_Lobby_DoubleDoor_OpenAddress, 0x03.to_bytes(1, "little"), "MainRAM")]
                else:
                    #Jake is defeated by the player
                    print("Jake Defeated")

                    if self.bool_MMDoubleDoor == False:
                        # If Jake is defeated and you ENTER the lobby,door will already be to 5,close it again
                        self.bool_MMDoubleDoor = True
                        MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                        MM_Writes += [(RAM.MM_Lobby_DoubleDoor_OpenAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                    else:
                        # self.bool_MMDoubleDoor = False
                        # Activate the door detection code
                        if MM_Lobby_DoorDetection != 0x8C820000:
                            print("[MM_Door]Close door")
                            MM_Writes += [(RAM.MM_Lobby_DoorDetection, 0x8C820000.to_bytes(4, "little"), "MainRAM")]
            else:
                # TODO Now the code for without the Item works flawlesly
                # TODO Fix the code WITH the Item
                # You have the Item,set the door to 4 + Jake defeated to 5,
                # then make Jake_defeated = 0 if not defeated

                if MM_Jake_Defeated == 0x00:
                    if self.bool_MMDoubleDoor == False:
                        self.bool_MMDoubleDoor = True
                        # Door already opened if == 5
                        if MM_Lobby_DoorDetection != 0x8C820000:
                            print("[MM_Door]Door Detection")
                            MM_Writes += [(RAM.MM_Lobby_DoorDetection, 0x8C820000.to_bytes(4, "little"), "MainRAM")]
                        if MM_Lobby_DoubleDoor_Open != 0x05:
                            print("[MM_Door]Open the Door")
                            # Set the door to 4 if it is not 5, to open it back
                            MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x05.to_bytes(1, "little"), "MainRAM")]
                            MM_Writes += [(RAM.MM_Lobby_DoubleDoor_OpenAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
                    else:
                        # self.bool_MMDoubleDoor = False
                        if MM_Jake_DefeatedAddress != 0x00:
                            print("[MM_Door]Put back Jake_DefeatedAddress")
                            MM_Writes += [(RAM.MM_Jake_DefeatedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
        else:
            # Room not MM_Lobby, reset the variable
            self.bool_MMDoubleDoor = False

        await bizhawk.write(ctx.bizhawk_ctx,MM_Writes)

    async def permanent_buttons_handling(self, ctx: "BizHawkClientContext", Button_Reads) -> None:

        currentRoom = Button_Reads[0]
        CrC_ButtonPressed = Button_Reads[1]
        TVT_Lobby_ButtonPressed = Button_Reads[2]
        MM_MonkeyHead_ButtonPressed = Button_Reads[3]
        MM_Painting_ButtonPressed = Button_Reads[4]
        CrC_Door_Visual = Button_Reads[5]
        TVT_Lobby_Water_Hitbox = Button_Reads[6]
        MM_MonkeyHead_Door = Button_Reads[7]
        MM_Painting_Visual = Button_Reads[8]

        Button_Writes = []

        # If CrC_ButtonRoom button is pressed,send the value "{Player}_CrcButton" to the server's Datastorage
        # This behavior unlocks the door permanently after you press the button once.
        if currentRoom == 49:
            if CrC_ButtonPressed == 0x01:
                if self.CrCButton != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": str(ctx.player_names[ctx.slot]) + "_CrcButton",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]

                    }])
        if currentRoom == 65:
            if TVT_Lobby_ButtonPressed == 0x01:
                if self.TVT_Lobby_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": str(ctx.player_names[ctx.slot]) + "_TVT_Lobby_Button",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]

                    }])

        # Detection of Interior Climb button press (MonkeyHead Room)
        if currentRoom == 84:
            if MM_MonkeyHead_ButtonPressed == 0x01:
                if self.MM_MonkeyHead_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": str(ctx.player_names[ctx.slot]) + "_MM_MonkeyHead_Button",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]

                    }])
        # Detection of Painting button press (Outside Climb)
        if currentRoom == 82:
            if MM_Painting_ButtonPressed == 0x01:
                if self.MM_Painting_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": str(ctx.player_names[ctx.slot]) + "_MM_Painting_Button",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": 1}]

                    }])

        # Crumbling Castle door unlock check
        if currentRoom == 45:
            if CrC_Door_Visual != 0x00:
                if self.CrCButton != 1:
                    await ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [str(ctx.player_names[ctx.slot]) + "_CrcButton"]
                    }])
                if self.CrCButton == 1:
                    Button_Writes += [(RAM.CrC_Door_Visual, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TR4_TransitionEnabled, 0x00.to_bytes(1, "little"), "MainRAM")]

        # TV Tower water draining check
        if currentRoom == 65:
            if TVT_Lobby_Water_Hitbox != 0x00:
                if self.TVT_Lobby_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [str(ctx.player_names[ctx.slot]) + "_TVT_Lobby_Button"]
                    }])
                if self.TVT_Lobby_Button == 1:
                    Button_Writes += [(RAM.TVT_Lobby_Water_HitBox, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_DoorHitbox1, 0x80.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_DoorHitbox2, 0x80.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_DoorVisualP1, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_DoorVisualP2, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_BackColor1, 0xAC78.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_BackColor2, 0xAC90.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_BackColor3, 0xAE14.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_BackColor4, 0xAC9C.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_BackColor5, 0xB1B8.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_ColorS1P1, 0xB1D0.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_ColorS1P2, 0xB2EC.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_TunnelColorS1P1, 0xB1E4.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_TunnelColorS1P2, 0xB9A0.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_TunnelColorS2P1, 0xB9B8.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_TunnelColorS2P2, 0xBB44.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_Water_TunnelColorS2P3, 0xB9C4.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_WaterVisual1, 0xF70C.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_WaterVisual2, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_WaterVisual3, 0xF70C.to_bytes(2, "little"), "MainRAM")]
                    Button_Writes += [(RAM.TVT_Lobby_WaterVisual4, 0x00.to_bytes(1, "little"), "MainRAM")]
        # Monkey Madness Monkey Head door unlock check
        if currentRoom == 80:
            if MM_MonkeyHead_Door != 0x01:
                if self.MM_MonkeyHead_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [str(ctx.player_names[ctx.slot]) + "_MM_MonkeyHead_Button"]
                    }])
                if self.MM_MonkeyHead_Button == 1:
                    Button_Writes += [(RAM.MM_MonkeyHead_Door, 0x01.to_bytes(1, "little"), "MainRAM")]

            # Monkey Madness Painting door unlock check
            if MM_Painting_Visual != 0x06:
                if self.MM_Painting_Button != 1:
                    await ctx.send_msgs([{
                        "cmd": "Get",
                        "keys": [str(ctx.player_names[ctx.slot]) + "_MM_Painting_Button"]
                    }])
                if self.MM_Painting_Button == 1:
                    Button_Writes += [(RAM.MM_Painting_Visual, 0x06.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_HitBox, 0x06.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_VisualStair1, 0x03.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_VisualStair2, 0x03.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_VisualStair3, 0x03.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_HitBoxStair1, 0x06.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_HitBoxStair2, 0x06.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_HitBoxStair3, 0x06.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_VisualFence, 0x00.to_bytes(1, "little"), "MainRAM")]
                    Button_Writes += [(RAM.MM_Painting_HitBoxFence, 0x80.to_bytes(1, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, Button_Writes)

    async def lamps_unlocks_handling(self, ctx: "BizHawkClientContext", Lamps_Reads) -> None:
        # Variables
        currentRoom = Lamps_Reads[0]
        NearbyRoom = Lamps_Reads[1]
        localLampsUpdate = Lamps_Reads[2]
        globalLampsUpdate = Lamps_Reads[3]
        bothLampsUpdate = Lamps_Reads[4]
        LocalLamp_LocalUpdate = Lamps_Reads[5]
        GlobalLamp_LocalUpdate = Lamps_Reads[6]

        Lamps_writes = []

        # Trigger Monkey Lamps depending on Lamp states

        #Lamps that are both affected by Local and Global values

        if (NearbyRoom in bothLampsUpdate and NearbyRoom != currentRoom):
            if bothLampsUpdate[NearbyRoom] == 0:
                print("Update Local")
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                print("[LAMP]N_both Global Update")
                Lamps_writes += [(RAM.globalLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            elif bothLampsUpdate[NearbyRoom] == 1:
                print("[LAMP]N_both Global Update(With ITEM)")
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x9062007A.to_bytes(4, "little"), "MainRAM")]
                #Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]

        if (NearbyRoom in globalLampsUpdate and NearbyRoom != currentRoom):
            if globalLampsUpdate[NearbyRoom] == 0 and GlobalLamp_LocalUpdate != 0x00000000:
                print("[LAMP]N_global Global Update")
                Lamps_writes += [(RAM.globalLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            elif globalLampsUpdate[NearbyRoom] == 1 and GlobalLamp_LocalUpdate != 0x9082007A:
                print("[LAMP]N_global Global Update(With ITEM)")
                #Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]

        if (currentRoom in bothLampsUpdate):
            #print(self.bool_LampGlobal)
            if bothLampsUpdate[currentRoom] == 0:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                if self.bool_LampGlobal == False:
                    self.bool_LampGlobal = True
                    print("[LAMP]C_both Global Update")
                    Lamps_writes += [(RAM.globalLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                    Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                else:
                    #Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                    Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]
            elif bothLampsUpdate[currentRoom] == 1:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x9062007A.to_bytes(4, "little"), "MainRAM")]
                print("[LAMP]C_both Global Update(With ITEM)")
                Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]

        # Lamps that detect only Global values
        if (currentRoom in globalLampsUpdate):
            print(self.bool_LampGlobal)
            if globalLampsUpdate[currentRoom] == 0:
                print("[LAMP]C_global Global Update")
                if self.bool_LampGlobal == False:
                    self.bool_LampGlobal = True
                    Lamps_writes += [(RAM.globalLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                    Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
                else:
                    #Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                    Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]
            elif globalLampsUpdate[currentRoom] == 1 and GlobalLamp_LocalUpdate != 0x9082007A:
                print("[LAMP]C_global Global Update(With ITEM)")
                Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]

        if (currentRoom in localLampsUpdate):
            if localLampsUpdate[currentRoom] == 0 and LocalLamp_LocalUpdate != 0x00000000:
                print("Update Local")
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            elif localLampsUpdate[currentRoom] == 1 and LocalLamp_LocalUpdate != 0x9062007A:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x9062007A.to_bytes(4, "little"), "MainRAM")]
        if (NearbyRoom in localLampsUpdate and NearbyRoom != currentRoom):
            if localLampsUpdate[NearbyRoom] == 0 and LocalLamp_LocalUpdate != 0x00000000:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            elif localLampsUpdate[NearbyRoom] == 1 and LocalLamp_LocalUpdate != 0x9062007A:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x9062007A.to_bytes(4, "little"), "MainRAM")]

        if ((currentRoom in localLampsUpdate) == False) and (NearbyRoom in localLampsUpdate == False) and ((currentRoom in bothLampsUpdate) == False) and ((NearbyRoom in bothLampsUpdate) == False):
            print("No lamp in room or nearby Rooms")
            if LocalLamp_LocalUpdate != 0x9062007A:
                Lamps_writes += [(RAM.localLamp_localUpdate, 0x9062007A.to_bytes(4, "little"), "MainRAM")]

        if ((currentRoom in globalLampsUpdate) == False and ((currentRoom in bothLampsUpdate) == False)):
            print("Setting Lamp to false")
            self.bool_LampGlobal = False
            if (NearbyRoom not in globalLampsUpdate) and (NearbyRoom not in bothLampsUpdate):
                if GlobalLamp_LocalUpdate != 0x9082007A:
                    Lamps_writes += [(RAM.globalLamp_localUpdate, 0x9082007A.to_bytes(4, "little"), "MainRAM")]
                    Lamps_writes += [(RAM.globalLamp_globalUpdate, 0x1444000F.to_bytes(4, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, Lamps_writes)

    async def level_select_optimization(self, ctx: "BizHawkClientContext", LSO_Reads) -> None:
        # For coin display to be ignored while in Level Select
        gameState = LSO_Reads[0]
        CoinTable = LSO_Reads[1]
        TempCoinTable = LSO_Reads[2]
        SA_Completed = LSO_Reads[3]
        Temp_SA_Completed = LSO_Reads[4]
        GA_Completed = LSO_Reads[5]
        Temp_GA_Completed = LSO_Reads[6]
        LS_currentWorld = LSO_Reads[7]

        LS_Writes = []

        if RAM.gameState["LevelSelect"] == gameState:
            if CoinTable != RAM.blank_coinTable and TempCoinTable == RAM.blank_coinTable:
                LS_Writes += [(RAM.startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]
                LS_Writes += [(RAM.temp_startingCoinAddress, CoinTable.to_bytes(100, "little"), "MainRAM")]
            if SA_Completed != 0x00 and Temp_SA_Completed == 0xFF:
                LS_Writes += [(RAM.SA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.Temp_SA_CompletedAddress, SA_Completed.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.Temp_GA_CompletedAddress, GA_Completed.to_bytes(1, "little"), "MainRAM")]

        else:
            if CoinTable == RAM.blank_coinTable and TempCoinTable != RAM.blank_coinTable:
                LS_Writes += [(RAM.startingCoinAddress, TempCoinTable.to_bytes(100, "little"), "MainRAM")]
                LS_Writes += [(RAM.temp_startingCoinAddress, RAM.blank_coinTable.to_bytes(100, "little"), "MainRAM")]

            if SA_Completed == 0x00 and Temp_SA_Completed != 0xFF:
                LS_Writes += [(RAM.SA_CompletedAddress, Temp_SA_Completed.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.GA_CompletedAddress, Temp_GA_Completed.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.Temp_SA_CompletedAddress, 0xFF.to_bytes(1, "little"), "MainRAM")]
                LS_Writes += [(RAM.Temp_GA_CompletedAddress, 0x00.to_bytes(1, "little"), "MainRAM")]

        # Prevent scrolling past the unlocked ERA/level
        if gameState == RAM.gameState["LevelSelect"]:
            reqkeys = ctx.slot_data["reqkeys"]

            # Get all keys required for the next world, based on first level of ERAS
            WorldUnlocks = [reqkeys[3], reqkeys[6], reqkeys[7], reqkeys[10], reqkeys[13], reqkeys[14], reqkeys[17],
                            reqkeys[20], reqkeys[21]]

            # Check if the selected world is the last (To stay within bound of the list)
            if 0 <= LS_currentWorld < 9:
                # If you have less World Keys that the required keys for the next ERA, disable R1, Right Stick and Right DPAD detection
                if self.worldkeycount < WorldUnlocks[LS_currentWorld]:
                    LS_Writes += [(RAM.worldScrollToRightDPAD, 0x0000.to_bytes(2, "little"), "MainRAM")]
                    LS_Writes += [(RAM.worldScrollToRightR1, 0x0000.to_bytes(2, "little"), "MainRAM")]
                else:
                    LS_Writes += [(RAM.worldScrollToRightDPAD, 0x0009.to_bytes(2, "little"), "MainRAM")]
                    LS_Writes += [(RAM.worldScrollToRightR1, 0x0009.to_bytes(2, "little"), "MainRAM")]

        await bizhawk.write(ctx.bizhawk_ctx, LS_Writes)

    async def water_net_handling(self, ctx: "BizHawkClientContext",WN_Reads) -> None:
        # Water Net client handling
        # If Progressive WaterNet is 0 no Swim and no Dive, if it's 1 No Dive (Swim only)
        # 8-9 Jumping/falling, 35-36 D-Jump, 83-84 Flyer => don't reset the counter

        inAir = [0x08, 0x09, 0x35, 0x36, 0x83, 0x84]
        swimming = [0x46, 0x47]
        grounded = [0x00, 0x01, 0x02, 0x05,0x07]  # 0x80, 0x81 Removed them since you can fling you net and give you extra air
        limited_OxygenLevel = 0x64

        gameState = WN_Reads[0]
        waternetState = WN_Reads[1]
        gameRunning = WN_Reads[2]
        spikeState2 = WN_Reads[3]
        swim_oxygenLevel = WN_Reads[4]
        cookies = WN_Reads[5]
        isUnderwater = WN_Reads[6]
        watercatchState = WN_Reads[7]

        WN_writes = []
        # Base variables
        if waternetState <= 0x01:
            WN_writes += [(RAM.canDiveAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_ReplenishOxygenUWAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0x00000000.to_bytes(4, "little"), "MainRAM")]
        else:
            # (waternetstate > 0x01)
            WN_writes += [(RAM.canDiveAddress, 0x08018664.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_oxygenReplenishSoundAddress, 0x0C021DFE.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_ReplenishOxygenUWAddress, 0xA4500018.to_bytes(4, "little"), "MainRAM")]
            WN_writes += [(RAM.swim_replenishOxygenOnEntryAddress, 0xA4434DC8.to_bytes(4, "little"), "MainRAM")]

        # Oxygen Handling
        if waternetState == 0x00:
            if gameState == RAM.gameState["InLevel"]:
                if gameRunning == 0x01:
                    # Set the air to the "Limited" value if 2 conditions:
                    # Oxygen is higher that "Limited" value AND spike is Swimming or Grounded
                    if spikeState2 in swimming:
                        if (swim_oxygenLevel > limited_OxygenLevel):
                            WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                    else:
                        # if self.waterHeight != 0:
                        # self.waterHeight = 0
                        if spikeState2 in grounded:
                            WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]

                else:
                    # Game Not running
                    if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                        # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                        WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                        WN_writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]
        if waternetState == 0x01:

            if isUnderwater == 0x00 and swim_oxygenLevel != limited_OxygenLevel:
                WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
            if swim_oxygenLevel == 0 and cookies == 0 and gameRunning == 0:
                # You died while swimming, reset Oxygen to "Limited" value prevent death loops
                WN_writes += [(RAM.swim_oxygenLevelAddress, limited_OxygenLevel.to_bytes(2, "little"), "MainRAM")]
                WN_writes += [(RAM.isUnderwater, 0x00.to_bytes(1, "little"), "MainRAM")]

        # WaterCatch unlocking stuff bellow
        if watercatchState == 0x00:
            WN_writes += [(RAM.canWaterCatchAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
        else:
            WN_writes += [(RAM.canWaterCatchAddress, 0x04.to_bytes(1, "little"), "MainRAM")]
        await bizhawk.write(ctx.bizhawk_ctx,WN_writes)

    async def handle_death_link(self, ctx: "BizHawkClientContext",DL_Reads) -> None:
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
                if cookies == 0x00 and not self.sending_death_link and gamestate in (RAM.gameState["InLevel"],RAM.gameState["TimeStation"]):
                    await self.send_deathlink(ctx)
                elif cookies != 0x00:
                    self.sending_death_link = False
            if self.pending_death_link:
                DL_writes += [(RAM.cookieAddress, 0x00.to_bytes(1, "little"), "MainRAM")]
                self.pending_death_link = False
                self.sending_death_link = True
                await bizhawk.write(ctx.bizhawk_ctx,DL_writes)

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        self.sending_death_link = True
        ctx.last_death_link = time.time()
        DeathText = ctx.player_names[ctx.slot] + " says: `Oooh noooo!`(Died)"
        await ctx.send_death(DeathText)

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    def unlockLevels(self, monkeylevelCounts, gameState, hundoMonkeysCount, reqkeys):

        key = self.worldkeycount
        curApesWrite = ""
        reqApesWrite = ""
        hundoWrite = ""
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