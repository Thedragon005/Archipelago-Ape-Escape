"""
Traps tab for TrapSenderContext (AP-SlowRelease / Universal Tracker based).

kvui.py in this fork is kivymd-based -- tabs are MDNavigationBar / MDScreen,
added via GameManager.add_client_tab(). This widget is plain tab content,
not a TabbedPanelItem.
"""

from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
import asyncio


def get_trap_names(world, exclude=("Palm Punch Trap",)):
    """
    Same logic your autoplayer() already uses: substring match against
    world.item_names (the static, per-game name list -- works even when
    the seed has traps disabled, since it isn't limited to placed items).

    Consider replacing the inline TrapNames computation in autoplayer()
    with a call to this function too, so there's one source of truth for
    the exclusion list instead of two copies that can drift apart.
    """
    return sorted(x for x in world.item_names if "Trap" in x and x not in exclude)


class TrapPanel(MDBoxLayout):
    """
    Usage -- inside TrapSenderContext.make_gui(), subclassing the ui class
    super().make_gui() returns (this is the same pattern Universal Tracker
    itself uses to add its own tab):

        def make_gui(self):
            ui = super().make_gui()
            ui.base_title = "Trap Sender Client"

            class TrapSenderManager(ui):
                def build(self):
                    container = super().build()
                    self.trap_panel = TrapPanel(trap_list=[])
                    self.add_client_tab("Traps", self.trap_panel)
                    return container

            return TrapSenderManager

    Starts empty -- call trap_panel.populate(get_trap_names(world)) once
    the tracker's world is actually loaded (see populate_trap_tab() in the
    integration snippet), since it isn't ready yet when build() runs.
    """

    def __init__(self, trap_list=None, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.trap_list = trap_list or []

        header = MDBoxLayout(size_hint_y=None, height=dp(40), padding=dp(4), spacing=dp(4))
        self.count_label = MDLabel(text=f"{len(self.trap_list)} traps")
        send_all_btn = MDButton(MDButtonText(text="Send All"), style="filled",
                                 size_hint_x=None, width=dp(120))
        send_all_btn.bind(on_release=lambda *_: self.send_all())
        header.add_widget(self.count_label)
        header.add_widget(send_all_btn)
        self.add_widget(header)

        self.grid = MDGridLayout(cols=1, size_hint_y=None, spacing=dp(4), padding=dp(4))
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = MDScrollView(size_hint=(1, 1))
        scroll.add_widget(self.grid)
        self.add_widget(scroll)

        self.populate(self.trap_list)

    @property
    def ctx(self):
        """Same pattern kvui.py's own ServerLabel uses to reach ctx."""
        return MDApp.get_running_app().ctx

    def populate(self, trap_list):
        """(Re)build the buttons -- called once the world/trap list is known."""
        self.grid.clear_widgets()
        self.trap_list = list(trap_list)
        self.count_label.text = f"{len(self.trap_list)} traps"

        for trap_name in self.trap_list:
            btn = MDButton(MDButtonText(text=trap_name), style="outlined",
                            size_hint_y=None, height=dp(36))
            btn.bind(on_release=lambda inst, name=trap_name: self.send(name))
            self.grid.add_widget(btn)

    def send(self, trap_name):
        """Reuses your existing cheat_item() coroutine -- the real send path."""
        asyncio.create_task(self.ctx.cheat_item(trap_name))

    def send_all(self):
        for trap_name in self.trap_list:
            self.send(trap_name)
