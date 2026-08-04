from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from worlds.AutoWorld import World
from BaseClasses import Region, ItemClassification
import asyncio
import random
tracker_loaded = True
from worlds.tracker import DeferredEntranceMode
from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor
from settings import get_settings
from .trap_utils import get_trap_names, EXCLUDED_TRAPS

class TrapSenderCommandProcessor(TrackerCommandProcessor):
    def _cmd_time(self, time_min=None, time_max=None):
        """If no arguments are provided, show the time per trap sent. Else, set the time per sending. Value in seconds. If two numbers are provided, then set a range to be randomly decided per send."""
        self.ctx.set_time(time_min, time_max)
    def _cmd_manual_mode(self):
        """Toggle Manual mode, which disables automatic trap sending and let them be sent manually"""
        self.ctx.manual_mode = not self.ctx.manual_mode
        logger.info(f"Set manual mode to {self.ctx.manual_mode}")

    def _cmd_delayed_checks(self, delayedchecks=None):
        """ Delayed checks prevents sending trap while the slot had not done at least X checks (3 per default)"""
        self.ctx.set_delayedstart(delayedchecks)

class TrapSenderContext(TrackerGameContext):
    time_per_min = 10
    time_per_max = 10
    tags = ["TrapSender", "Tracker"]
    game = ""
    has_game = False
    manual_mode = False
    delayedchecks = 3
    command_processor = TrapSenderCommandProcessor
    autoplayer_task = None
    def autoplayer_log(self, message):
        logger.info(message)
    def set_time(self, time_min=None, time_max=None):
        if time_min:
            self.time_per_min = float(time_min)
            if time_max and float(time_min) < float(time_max):
                self.time_per_max = float(time_max)
            else:
                self.time_per_max = float(time_min)
            logger.info(f"Set time per check to {self.time_per_min}-{self.time_per_max}s")
        else:
            logger.info(f"Time per check is {self.time_per_min}-{self.time_per_max}s")

    def set_delayedstart(self, delayedchecks=None):
        if delayedchecks:
            self.delayedchecks = delayedchecks
        else:
            #self.delayedchecks = 1
            self.delayedchecks = 3
            logger.info(f"Set delayed checks to {self.delayedchecks}")

        logger.info(f"Set delayed checks to {self.delayedchecks}")

    async def cheat_item (self,itemname=None):

        if itemname:
            print(f"You should have sent {itemname}")
            asyncio.create_task(self.send_msgs([{"cmd": "Say", "text": f"!getitem {itemname}"}]))

    async def autoplayer(self):
        print("Autoplayer")
        inbk = False
        while not self.tracker_core.player_id:
            await asyncio.sleep(1)
        world: World = self.tracker_core.multiworld.worlds[self.tracker_core.player_id]
        while True:
            #if len(self.tracker_core.locations_available) > 0:
                #inbk = False
                #goal_location = None
                #visited_regions = []
                #regions = [*map(lambda e: e.connected_region,self.tracker_core.multiworld.get_region(world.origin_region_name, self.tracker_core.player_id).get_exits())]
                #if self.region_mode:
                #    while not goal_location:
                #        randolocs = self.tracker_core.locations_available.copy()
                #        random.shuffle(randolocs)
                #        for location in randolocs:
                #            location = world.get_location(world.location_id_to_name[location])
                #            if location.parent_region == current_region:
                #                goal_location = location.address
                #                self.autoplayer_log(f"Going for {self.location_names.lookup_in_game(goal_location)}")
                #                break
                #        if not goal_location:
                #            current_region = random.choice(regions)
                #            if current_region not in visited_regions:
                #                regions += [*filter(lambda e: e not in regions and e not in visited_regions, map(lambda e: e.connected_region, current_region.get_exits()))]
                #            visited_regions.append(current_region)
                #            regions.remove(current_region)
                #            self.autoplayer_log(f"Attempting to go to: {current_region.name}")
                #            await asyncio.sleep(0.1)
                #else:
                #    goal_location = random.choice(self.tracker_core.locations_available)
                #    self.autoplayer_log(f"Going for {self.location_names.lookup_in_game(goal_location)}")
            await asyncio.sleep(random.uniform(self.time_per_min, self.time_per_max))

            # TODO For now take Item Names containing Traps,organize later to make it take all items classified as trap
            settings = get_settings()
            CanCheat = settings.server_options.disable_item_cheat == False
            # Maybe add self.ctx.locations_checked >= 1 to quick start
            # Send conditions
            #DelayedModeSend = False if self.delayed_mode == False else len(self.locations_checked) >= 1
            if self.delayedchecks == 0:
                DelayedModeSend = True
            else:
                if len(self.checked_locations) >= self.delayedchecks:
                    DelayedModeSend = True
                else:
                    DelayedModeSend = False
            ManualMode = not self.manual_mode
            print(f"LocationsChecked:{self.checked_locations}")
            if DelayedModeSend == False:
                print(f"Delaying sending of traps until {self.delayedchecks} check{"" if self.delayedchecks == 0 else "s"}")
            if self.manual_mode:
                print("Manual mode activated, no traps are sending")
            if CanCheat and DelayedModeSend and ManualMode:
                Items = world.item_names
                TrapNames = [x for x in Items if x.__contains__("Trap") and x not in EXCLUDED_TRAPS]
                RandomTrapNum = random.randint(0,len(TrapNames) -1)
                RandomTrap = TrapNames[RandomTrapNum]
                await self.cheat_item(RandomTrap)
                await asyncio.sleep(0.1)

    async def populate_trap_tab(self):
        """Wait for the tracker's world to load, then fill in the Traps tab.
        Mirrors the same wait condition autoplayer() uses above."""
        while not self.tracker_core.player_id:
            await asyncio.sleep(1)
        world: World = self.tracker_core.multiworld.worlds[self.tracker_core.player_id]
        if self.ui and hasattr(self.ui, "trap_panel"):
            self.ui.trap_panel.populate(get_trap_names(world))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Trap Sender Client"

        # kvui.py must be the first thing to import kivy -- super().make_gui()
        # above is what triggers that import (via CommonClient's make_gui'
        # "from kvui import GameManager"). trap_tab imports kivymd/kivy at
        # module level, so it can ONLY be imported here, never at the top
        # of this file. (Relative import: this file is a package member,
        # worlds/trapsender/Client.py, so it's `.trap_tab`, not `trap_tab`.)
        from .trap_tab import TrapPanel

        class TrapSenderManager(ui):
            def build(self):
                container = super().build()
                # starts empty -- tracker_core.player_id isn't set yet here
                self.trap_panel = TrapPanel(trap_list=[])
                self.add_client_tab("Traps", self.trap_panel)
                return container

        return TrapSenderManager

    def on_package(self, cmd, args):
        super().on_package(cmd, args)
        if cmd == "Connected":
            settings = get_settings()
            CanCheat = settings.server_options.disable_item_cheat == False
            if CanCheat == False:
                asyncio.create_task(self.disconnect())
                logger.info("\n\n========================================================================")
                logger.info("[!WARNING] You cannot use this client with this seed")
                logger.info("The !getitem command has been disabled by the host")
                logger.info("**The client will now disconnect from the server**")
                logger.info("========================================================================\n\n")
            if "Tracker" in self.tags:
                self.tags.remove("Tracker")
                asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))
            if self.autoplayer_task:
                self.autoplayer_task.cancel()
            self.autoplayer_task = asyncio.create_task(self.autoplayer())
            self.autoplayer_task.add_done_callback(self.autoplayer_done)
            asyncio.create_task(self.populate_trap_tab())
    def autoplayer_done(self, autoplayer_task):
        try:
            _ = autoplayer_task.result()
        except Exception as e:
            logger.error("Autoplayer Error", exc_info=True)
    def disconnect(self, *args):
        if self.autoplayer_task:
            self.autoplayer_task.cancel()
        if "Tracker" not in self.tags:
            self.tags.append("Tracker")
        return super().disconnect(*args)
def launch(*args):

    async def main(args):
        ctx = TrapSenderContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        ctx.set_time(args.time, args.time_max)

        if tracker_loaded:
            ctx.tracker_core.enforce_deferred_connections = DeferredEntranceMode.disabled
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Trap Sender Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument('--time', type=float, default=10.0, help="Minimum time per check in seconds. If maximum is not specified, defaults to this.")
    parser.add_argument('--time_max', type=float, default=None, help="Maximum time per check.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        import urllib
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            args.connect = url.netloc
            if url.username:
                args.name = urllib.parse.unquote(url.username)
            if url.password:
                args.password = urllib.parse.unquote(url.password)
        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()